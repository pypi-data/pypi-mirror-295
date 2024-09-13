from typing import Dict
import copy
import json
import datetime
import requests
from PIL import Image
import numpy as np
from tqdm import tqdm
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from shapely.geometry import Polygon
import cv2
import time


class Coco():
    def __init__(self, client_headers = None):
        """
            When initializing the Coco class, if you are trying to convert Mask annotations, you will need to pass in your client: lb.Client()
        Args:
            client.headers (optional): Authentication headers to download Mask annotations from exports  
        """
        self.headers = client_headers

    def layer_iterator(
        self,
        feature_map,
        node_layer,
        encoded_value=0,
        parent_featureSchemaIds=[],
        parent_featureSchemaId=False,
    ):
        """Receives a normalized ontology layer (list of dictionaries) and for each dictionary (node), pulls key information where they key=featureSchemaid
            Then if a given node has another layer, recursively call this function to loop through all the nested layers of the ontoology node dictionary
        Args:
            feature_map (dict)              :   Building dictinoary where key=featureSchemaid
            node_layer (list)               :   List of ontology node dictionaries to loop through
            encoded_value (int)             :   Each dictionary gets an encoded value, and this increases by one each ontology node dictionary read into the feature_map
            parent_featureSchemaIds (list)  :   For a given ontology node dictionary, a list of parent featureSchemaid strings
            parent_featureSchemaId (str)    :   The immediate parent ontology node dictionary featureSchemaid
        Returns:
            The same input arguments, only with updated values for feature_map and encoded_value
        """
        if parent_featureSchemaId:
            parent_featureSchemaIds.append(parent_featureSchemaId)
        parent_featureSchemaId = ""
        for node in node_layer:
            encoded_value += 1
            color = ""
            if "tool" in node.keys():
                node_type = node["tool"]
                node_kind = "tool"
                node_name = node["name"]
                next_layer = node["classifications"]
                color = node["color"]
            elif "instructions" in node.keys():
                node_name = node["instructions"]
                node_kind = "classification"
                node_type = node["type"]
                next_layer = node["options"]
            else:
                node_name = node["label"]
                node_kind = "option"
                if "options" in node.keys():
                    next_layer = node["options"]
                    node_type = "branch_option"
                else:
                    next_layer = []
                    node_type = "leaf_option"
            node_dict = {
                node["featureSchemaId"]: {
                    "name": node_name,
                    "color": color,
                    "type": node_type,
                    "kind": node_kind,
                    "parent_featureSchemaIds": parent_featureSchemaIds,
                    "encoded_value": encoded_value,
                }
            }
            feature_map.update(node_dict)
            if next_layer:
                (
                    feature_map,
                    next_layer,
                    encoded_value,
                    parent_featureSchemaIds,
                    parent_featureSchemaId,
                ) = self.layer_iterator(
                    feature_map=feature_map,
                    node_layer=next_layer,
                    encoded_value=encoded_value,
                    parent_featureSchemaIds=parent_featureSchemaIds,
                    parent_featureSchemaId=node["featureSchemaId"],
                )
            parent_featureSchemaIds = parent_featureSchemaIds[:-1]
        return (
            feature_map,
            next_layer,
            encoded_value,
            parent_featureSchemaIds,
            parent_featureSchemaId,
        )

    def index_ontology(self, ontology_normalized):
        """Given an ontology, returns a dictionary where {key=featureSchemaid : values = {"name", "color", "type", "kind", "parent_featureSchemaIds", "encoded_value"} for each feature in the ontology
        Args:
            ontology_normalized   :   Queried from a project using project.ontology().normalized
        Returns:
            Dictionary with key information on each node in an ontology, where {key=featureSchemaid : values = {"name", "color", "type", "kind", "parent_featureSchemaIds", "encoded_value"}
        """
        feature_map = {}
        tools = ontology_normalized["tools"]
        classifications = ontology_normalized["classifications"]
        if tools:
            results = self.layer_iterator(feature_map=feature_map, node_layer=tools)
            feature_map = results[0]
        if classifications:
            feature_map = self.layer_iterator(
                feature_map=feature_map,
                node_layer=classifications,
                encoded_value=results[2],
                parent_featureSchemaIds=[],
                parent_featureSchemaId=False,
            )[0]
        return feature_map

    def coco_bbox_converter(self, data_row_id: str, annotation: Dict, category_id: str) -> Dict[str, str]:
        """Given a label dictionary and a bounding box annotation from said label, will return the coco-converted bounding box annotation dictionary
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label['Label']['objects'], which comes from project.export_labels()
            category_id (str)               :     Desired category_id for the coco_annotation
        Returns:
            An annotation dictionary in the COCO format
        """
        coco_annotation = {
            "image_id": data_row_id,
            "bbox": [
                str(annotation["bounding_box"]["top"]),
                str(annotation["bounding_box"]["left"]),
                str(annotation["bounding_box"]["height"]),
                str(annotation["bounding_box"]["width"]),
            ],
            "category_id": str(category_id),
            "id": annotation["feature_id"],
        }
        return coco_annotation

    def coco_line_converter(self, data_row_id: str, annotation: Dict, category_id: str) -> Dict[str, str]:
        """Given a label dictionary and a line annotation from said label, will return the coco-converted line annotation dictionary
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label['Label']['objects'], which comes from project.export_labels()
            category_id (str)               :     Desired category_id for the coco_annotation
        Returns:
            An annotation dictionary in the COCO format
        """
        line = annotation["line"]
        coco_line = []
        num_line_keypoints = 0
        for coordinates in line:
            coco_line.append(str(coordinates["x"]))
            coco_line.append(str(coordinates["y"]))
            coco_line.append("2")
            num_line_keypoints += 1
        coco_annotation = {
            "image_id": str(data_row_id),
            "keypoints": coco_line,
            "num_keypoints": str(num_line_keypoints),
            "category_id": str(category_id),
            "id": str(annotation["feature_id"]),
        }
        return coco_annotation, num_line_keypoints

    def coco_point_converter(self, data_row_id: str, annotation: Dict, category_id: str) -> Dict[str, str]:
        """Given a label dictionary and a point annotation from said label, will return the coco-converted point annotation dictionary
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label['Label']['objects'], which comes from project.export_labels()
            category_id (str)               :     Desired category_id for the coco_annotation
        Returns:
            An annotation dictionary in the COCO format
        """
        coco_annotation = {
            "image_id": str(data_row_id),
            "keypoints": [
                str(annotation["point"]["x"]),
                str(annotation["point"]["y"]),
                "2",
            ],
            "num_keypoints": str(1),
            "category_id": str(category_id),
            "id": str(annotation["feature_id"]),
        }
        return coco_annotation

    def coco_polygon_converter(self, data_row_id: str, annotation: Dict, category_id: str) -> Dict[str, str]:
        """Given a label dictionary and a point annotation from said label, will return the coco-converted polygon annotation dictionary
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label['Label']['objects'], which comes from project.export_labels()
            category_id (str)               :     Desired category_id for the coco_annotation
        Returns:
            An annotation dictionary in the COCO format
        """
        all_points = []
        points_as_coords = []
        for coord in annotation["polygon"]:
            points_as_coords.append([coord["x"], coord["y"]])
            all_points.append(str(coord["x"]))
            all_points.append(str(coord["y"]))
        polygon = Polygon(points_as_coords)
        coco_annotation = {
            "image_id": data_row_id,
            "segmentation": all_points,
            "bbox": [
                str(polygon.bounds[0]),
                str(polygon.bounds[1]),
                str(polygon.bounds[2] - polygon.bounds[0]),
                str(polygon.bounds[3] - polygon.bounds[1]),
            ],
            "area": str(polygon.area),
            "id": str(annotation["feature_id"]),
            "iscrowd": "0",
            "category_id": str(category_id),
        }
        return coco_annotation

    def download_mask(self, url: Dict) -> np.ndarray:
        """Downloads a mask URL
        Args:
            url (dict)       :     URL of a mask
        Returns:
            A 2-D numPy array of said mask
        """
        downloaded = True
        while downloaded:
            # to ensure api limit doesn't throw an error
            requests_per_min = 1500
            interval = 60 / requests_per_min
            time.sleep(interval)
            try:
                payload = requests.get(url, headers=self.headers)
                if payload.status_code == 200:
                    pil_image = Image.open(BytesIO(payload.content))

                    # Convert the image to grayscale if it's not already
                    if pil_image.mode != "L":
                        pil_image = pil_image.convert("L")

                    # Convert the image to a NumPy array
                    np_array = np.array(pil_image)
                    downloaded = False
            except:
                downloaded = True

        return np_array

    def hex_to_rgb(self, hex_color):
        # Remove the hash (#) at the start if it's there
        hex_color = hex_color.lstrip('#')
        
        # Convert the hex color to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    
        return [r, g, b]   

    def coco_mask_converter(self, data_row_id: str, annotation: Dict, category_id: str, panoptic = False) -> Dict[str, str]:
        """Given a label dictionary and a mask annotation from said label, will return the coco-converted segmentation mask annotation dictionary
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label['Label']['objects'], which comes from project.export_labels()
            category_id (str)               :     Desired category_id for the coco_annotation
        Returns:
            An annotation dictionary in the COCO format
        """
        color = annotation["composite_mask"]["color_rgb"]
        
        contours, _ = cv2.findContours(
            self.download_mask(annotation["mask"]["url"]),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        all_points = []
        points_as_coords = []
        for contour in contours:
            contour = contour.flatten().tolist()
            if len(contour) >= 6:
                for i in range(0, len(contour), 2):
                    points_as_coords.append([contour[i], contour[i + 1]])
                    all_points.append(str(contour[i]))
                    all_points.append(str(contour[i + 1]))
        polygon = Polygon(points_as_coords)
        if panoptic:
            r, g, b = color[0], color[1], color[2]
            coco_annotation = {
                "id": r + (g*256) + (b*(256**2)),
                "category_id": str(category_id),
                "area": str(polygon.area),
                "bbox": [
                    str(polygon.bounds[0]),
                    str(polygon.bounds[1]),
                    str(polygon.bounds[2] - polygon.bounds[0]),
                    str(polygon.bounds[3] - polygon.bounds[1]),
                ],
                "iscrowd": "0",
            }
        else:
            coco_annotation = {
                "image_id": data_row_id,
                "segmentation": all_points,
                "bbox": [
                    str(polygon.bounds[0]),
                    str(polygon.bounds[1]),
                    str(polygon.bounds[2] - polygon.bounds[0]),
                    str(polygon.bounds[3] - polygon.bounds[1]),
                ],
                "area": str(polygon.area),
                "id": str(annotation["feature_id"]),
                "iscrowd": "0",
                "category_id": str(category_id),
            }
        return coco_annotation

    def coco_annotation_converter(self, data_row_id: str, annotation: Dict, ontology_index: Dict[str, str], panoptic = False):
        """Wrapper to triage and multithread the coco annotation conversion - if nested classes exist, the category_id will be the first radio/checklist classification answer available
        Args:
            data_row_id (str)               :     Labelbox Data Row ID for this label
            annotation (dict)               :     Annotation dictionary from label["projects"][project_id]['labels']['annotations']['objects'], which comes from project.export_labels()
            ontology_index (dict)           :     A dictionary where {key=featureSchemaId : value = {"encoded_value"} which corresponds to category_id
        Returns:
            A dictionary corresponding to the coco annotation syntax - the category ID used will be the top-level tool
        """

        max_line_keypoints = 0
        category_id = ontology_index[annotation["feature_schema_id"]]["encoded_value"]

        if "classifications" in annotation.keys():
            if annotation["classifications"]:
                for classification in annotation["classifications"]:
                    if "answer" in classification.keys():
                        if type(classification["answer"]) == dict:
                            category_id = ontology_index[classification["schemaId"]][
                                "encoded_value"
                            ]
                            break
                    else:
                        category_id = ontology_index[
                            classification["answers"][0]["schemaId"]
                        ]["encoded_value"]
                        break
        if "bounding_box" in annotation.keys():
            coco_annotation = self.coco_bbox_converter(
                data_row_id, annotation, category_id
            )
        elif "line" in annotation.keys():
            coco_annotation, max_line_keypoints = self.coco_line_converter(
                data_row_id, annotation, category_id
            )
        elif "point" in annotation.keys():
            coco_annotation = self.coco_point_converter(
                data_row_id, annotation, category_id
            )
        elif "polygon" in annotation.keys():
            coco_annotation = self.coco_polygon_converter(
                data_row_id, annotation, category_id
            )
        elif "mask" in annotation.keys():
            coco_annotation = self.coco_mask_converter(
                data_row_id, annotation, category_id, panoptic
            )
        return coco_annotation, max_line_keypoints

    def convert_from_lb(self, data_row_json, ontology, panoptic = False):
            """
            Convert Labelbox NDJSON file to COCO format.

            :Args:
                data_row_json (required): The JSON data representing the Labelbox NDJSON file.
                ontology (required): project.ontology().normalized to make this independent of LB
                panoptic (optional): boolean, default = False
            :return: 
                The converted COCO format.
            """

            labels_list = data_row_json
            
            # Parse out important info for the COCO format from export file
            project_id = next(iter(labels_list[0]["projects"])) 
            name = labels_list[0]["projects"][project_id]["name"]
            created_by = labels_list[0]["projects"][project_id]["labels"][0]["label_details"]["created_by"]

            # Info section generated from project information
            info = {
                "description": name,
                "url": f"https://app.labelbox.com/projects/{name}/overview",
                "version": "1.0",
                "year": datetime.datetime.now().year,
                "contributor": created_by,
                "date_created": datetime.datetime.now().strftime("%Y/%m/%d"),
            }
            # Licenses section is left empty

            licenses = [{"url": "N/A", "id": 1, "name": "N/A"}]

            data_rows = {}
            for label in labels_list:
                data_row = label["data_row"]
                data_rows.update({data_row["id"]: data_row["row_data"]})
            # Images section generated from data row export
            print(f"\nConverting Data Rows into a COCO Dataset...\n")

            images = []
            data_row_check = []  # This is a check for projects where one data row has multiple labels (consensus, benchmark)
            for id_count, label in tqdm(enumerate(labels_list)):
                data_row = label["data_row"]
                if data_row["id"] not in data_row_check:
                    data_row_check.append(data_row["id"])
                    if "global_key" in data_row.keys():
                        file_name = data_row["global_key"]
                    else:
                        file_name = data_row["external_id"]
                    images.append(
                        {
                            "license": 1,
                            "file_name": file_name,
                            "height": label["media_attributes"]["height"],
                            "width": label["media_attributes"]["width"],
                            "date_captured": label["projects"][project_id]["labels"][0][
                                "label_details"
                            ][
                                "created_at"
                            ],  # data_row.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "id": id_count + 1 if panoptic else data_row["id"],
                            "coco_url": data_row["row_data"],
                        }
                    )
            print(f"\nData Rows Converted into a COCO Dataset.")

            print(f"\nConverting Annotations into the COCO Format...\n")
            ontology_index = self.index_ontology(ontology)
            global_max_keypoints = 0

            futures = []
            annotations = []
            idx = 0
            segment_info = []

            with ThreadPoolExecutor() as exc:
                if panoptic:
                    image_count = 1
                    for label in labels_list:
                        segment_info = []
                        for annotation in label["projects"][project_id]["labels"][idx]["annotations"]["objects"]:
                            futures.append(
                                exc.submit(
                                    self.coco_annotation_converter,
                                    label["data_row"]["id"],
                                    annotation,
                                    ontology_index,
                                    panoptic
                                )
                            )
                        for f in tqdm(as_completed(futures)):
                            res = f.result()

                            if int(res[1]) > global_max_keypoints:
                                global_max_keypoints = int(copy.deepcopy(res[1]))
                            segment_info.append(res[0])
                        data_row = label["data_row"]
                        if "global_key" in data_row.keys():
                            file_name = data_row["global_key"]
                        else:
                            file_name = data_row["external_id"]
                        annotations.append(
                            {
                                "image_id": image_count,
                                "file_name": file_name,
                                "segment_info" : segment_info
                            }
                        )
                        image_count += 1
                else:
                    for label in labels_list:
                        for annotation in label["projects"][project_id]["labels"][idx]["annotations"]["objects"]:
                            futures.append(
                                exc.submit(
                                    self.coco_annotation_converter,
                                    label["data_row"]["id"],
                                    annotation,
                                    ontology_index
                                )
                            )
                    for f in tqdm(as_completed(futures)):

                        res = f.result()

                        if int(res[1]) > global_max_keypoints:
                            global_max_keypoints = int(copy.deepcopy(res[1]))
                        annotations.append(res[0])
            print(f"\nAnnotation Conversion Complete. Converted {len(annotations)} annotations into the COCO Format.")

            categories = []
            thing_class = ["person",
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair dryer"]
            print(f"\nConverting the Ontology into the COCO Dataset Format...")
            if panoptic:
                for featureSchemaId in ontology_index:
                    name = ontology_index[featureSchemaId]["name"]
                    categories.append(
                                {
                                    "id": str(ontology_index[featureSchemaId]["encoded_value"]),
                                    "name": name,
                                    "supercategory": ontology_index[featureSchemaId]["name"],
                                    "isthing" : 1 if name in thing_class else 0,
                                    "color": self.hex_to_rgb(ontology_index[featureSchemaId]["color"])
                                }
                            )
            else:
                for featureSchemaId in ontology_index:
                    if ontology_index[featureSchemaId]["type"] == "line":
                        keypoints = []
                        skeleton = []
                        for i in range(0, global_max_keypoints):
                            keypoints.append(str("line_") + str(i + 1))
                            skeleton.append([str(i), str(i + 1)])
                        categories.append(
                            {
                                "supercategory": ontology_index[featureSchemaId]["name"],
                                "id": str(ontology_index[featureSchemaId]["encoded_value"]),
                                "name": ontology_index[featureSchemaId]["name"],
                                "keypoints": keypoints,
                                "skeleton": skeleton,
                            }
                        )
                    elif ontology_index[featureSchemaId]["type"] == "point":
                        categories.append(
                            {
                                "supercategory": ontology_index[featureSchemaId]["name"],
                                "id": str(ontology_index[featureSchemaId]["encoded_value"]),
                                "name": ontology_index[featureSchemaId]["name"],
                                "keypoints": ["point"],
                                "skeleton": ["0", "0"],
                            }
                        )
                    elif ontology_index[featureSchemaId]["kind"] == "tool":
                        categories.append(
                            {
                                "supercategory": ontology_index[featureSchemaId]["name"],
                                "id": str(ontology_index[featureSchemaId]["encoded_value"]),
                                "name": ontology_index[featureSchemaId]["name"],
                            }
                        )
                    elif len(ontology_index[featureSchemaId]["parent_featureSchemaIds"]) == 2:
                        supercategory = ontology_index[
                            ontology_index[featureSchemaId]["parent_featureSchemaIds"][0]
                        ]["name"]
                        categories.append(
                            {
                                "supercategory": supercategory,
                                "id": str(ontology_index[featureSchemaId]["encoded_value"]),
                                "name": ontology_index[featureSchemaId]["name"],
                            }
                        )
            print(f"\nOntology Conversion Complete")

            coco_dataset = {
                "info": info,
                "licenses": licenses,
                "images": images,
                "annotations": annotations,
                "categories": categories,
            }

            print(f"\nCOCO Conversion Complete")

            with open(f"coco_{project_id}.json", "w") as f:
                json.dump(coco_dataset, f, indent=4)

    def convert_to_lb(self, coco_annotation) -> None:

        """Convert a coco annotation to a Labelbox bbox payload
        Args:
            coco_annotation: standardized coco_annotation file name
        Returns:
            data_rows_list: to be used with dataset.create_data_rows(data_rows_list) for uploading
            label_ndjson[List]: where {"dataRow": {"globalKey": global_key}} is added to ndjson payload
        """
        with open(coco_annotation, 'r') as f:
            coco_data = json.load(f)

        categories_dict = {}
        for category in coco_data['categories']:
            categories_dict[category['id']] = category['name']
        
        annotations_list = []
        
        # Process each annotation entry
        for annotation in coco_data['annotations']:
            global_key = annotation['image_id']
            if 'segmentation' in annotation.keys():
                ndjson_payload = []
                tool_name = "polygon"
                segmentation = annotation['segmentation']
                for i in range(0, len(segmentation), 2):
                    if i >= len(segmentation):
                        break
                    x = segmentation[i]
                    y = segmentation[i+1]
                    ndjson_payload.append({"x": x, "y": y})
                category_id = annotation['category_id']
                category_name = categories_dict[category_id]
                
                annotation_entry = {
                    "name" : category_name,
                    tool_name : ndjson_payload
                }
            elif 'keypoints' in annotation.keys():
                tool_name = "point"
                segmentation = annotation['keypoints']
                x = segmentation[0]
                y = segmentation[1]
                ndjson_payload = {"x" : x, "y" : y}
                category_id = annotation['category_id']
                category_name = categories_dict[category_id]
                
                annotation_entry = {
                    "name" : category_name,
                }
                annotation_entry.update({tool_name : ndjson_payload})
            else:
                ndjson_payload = {}
                tool_name = "bbox"
                segmentation = annotation['bbox']
                positions = ["top", "left", "width", "height"]
                for idx,position in enumerate(positions):
                    ndjson_payload.update({position : segmentation[idx]})

                # Get category name using category ID
                category_id = annotation['category_id']
                category_name = categories_dict[category_id]
                
                annotation_entry = {
                        "name" : category_name,
                }
                annotation_entry.update({tool_name : ndjson_payload})

            annotation_entry.update({"dataRow": {"id": global_key}})
            
            annotations_list.append(annotation_entry)
        
        return annotations_list 