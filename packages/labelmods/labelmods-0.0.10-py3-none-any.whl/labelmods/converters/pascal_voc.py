import os
import xml.etree.ElementTree as ET
from typing import List, Dict


class PascalVoc:
    def __init__(self):
        pass

    def convert_to_lb(
        self,
        input_files: List[str],
        ontology_mapping: Dict[str, str],
        image_mapping: Dict[str, str],
    ) -> List[Dict]:
        """
        Convert Pascal VOC XML files to Labelbox NDJSON format.

        :param input_files: List of XML file paths to be converted.
        :param ontology_mapping: Dictionary mapping Pascal VOC class names to Labelbox class names.
        :param image_mapping: Dictionary mapping Pascal VOC filenames to Labelbox globalKeys.
        :return: List of dictionaries in NDJSON format.
        """
        ndjson_data = []

        for xml_file in input_files:
            if not os.path.exists(xml_file):
                print(f"File not found: {xml_file}")
                continue

            tree = ET.parse(xml_file)
            root = tree.getroot()

            filename = root.find("filename").text
            global_key = image_mapping.get(filename)

            if not global_key:
                print(f"No global key found for {filename}, skipping this file.")
                continue

            for obj in root.findall("object"):
                name = obj.find("name").text
                mapped_name = ontology_mapping.get(name, "")
                if not mapped_name:
                    print(f"No mapping found for {name}, skipping this file.")
                    continue

                bndbox = obj.find("bndbox")
                xmin = int(bndbox.find("xmin").text)
                ymin = int(bndbox.find("ymin").text)
                xmax = int(bndbox.find("xmax").text)
                ymax = int(bndbox.find("ymax").text)

                annotation = {
                    "name": mapped_name,
                    "bbox": {
                        "top": ymin,
                        "left": xmin,
                        "height": ymax - ymin,
                        "width": xmax - xmin,
                    },
                    "dataRow": {"globalKey": global_key},
                }

                ndjson_data.append(annotation)

        return ndjson_data

    def convert_from_lb(self, data_row_json) -> str:
        """
        Convert Labelbox NDJSON file to Pascal VOC XML format.

        :param data_row_json: The JSON data representing the Labelbox NDJSON file.
        :return: The converted XML string in Pascal VOC format.
        """

        project_id = next(iter(data_row_json["projects"]))

        annotationElem = ET.Element("annotation")
        ET.SubElement(annotationElem, "folder").text = ""
        ET.SubElement(annotationElem, "filename").text = os.path.basename(
            data_row_json["data_row"]["row_data"]
        )
        ET.SubElement(annotationElem, "path").text = data_row_json["data_row"][
            "row_data"
        ]

        sizeElem = ET.SubElement(annotationElem, "size")
        ET.SubElement(sizeElem, "width").text = str(
            data_row_json["media_attributes"]["width"]
        )
        ET.SubElement(sizeElem, "height").text = str(
            data_row_json["media_attributes"]["height"]
        )
        ET.SubElement(sizeElem, "depth").text = "3"  # 3 for RGB

        ET.SubElement(annotationElem, "segmented").text = "0"  # default value

        # Create nbboxes
        # Stop to one label per data row
        obj_list = data_row_json["projects"][project_id]["labels"][0]["annotations"][
            "objects"
        ]

        for obj in obj_list:

            if obj["annotation_kind"] == "ImageBoundingBox":
                objElem = ET.SubElement(annotationElem, "object")
                ET.SubElement(objElem, "name").text = obj["name"]
                ET.SubElement(objElem, "pose").text = "Unspecified"
                ET.SubElement(objElem, "truncated").text = "0"
                ET.SubElement(objElem, "difficult").text = "0"
                ET.SubElement(objElem, "occluded").text = "0"

                bboxElem = ET.SubElement(objElem, "bndbox")
                ET.SubElement(bboxElem, "xmin").text = str(obj["bounding_box"]["left"])
                ET.SubElement(bboxElem, "ymin").text = str(obj["bounding_box"]["top"])
                ET.SubElement(bboxElem, "xmax").text = str(
                    obj["bounding_box"]["left"] + obj["bounding_box"]["width"]
                )
                ET.SubElement(bboxElem, "ymax").text = str(
                    obj["bounding_box"]["top"] + obj["bounding_box"]["height"]
                )

        return ET.dump(annotationElem)