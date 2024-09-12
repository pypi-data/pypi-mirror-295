import labelbox as lb
from uuid import uuid4
from typing import List, Dict

import labelbox.types as lb_types


class _LbConverter:
    def __init__(
        self, project_id: str, client: lb.Client, ontology_mapping: Dict[str, str] = None
    ) -> None:
        """
        Initializes the _LbConverter class.

        Args:
            project_id (str): The ID of the project.
            client (lb.Client): The Labelbox client.
            ontology_mapping (Dict[str, str]): The mapping of ontology labels.

        Returns:
            None
        """
        self.client: lb.Client = client
        self.project: str = project_id
        self.ontology_mapping: Dict[str, str] = ontology_mapping
        self.labels: List[lb_types.Label] = []

    def export_data_row(self) -> List[Dict[str, str]]:
        """
        Exports the data rows from the project.

        Returns:
            List[Dict[str, str]]: The exported data rows.
        """
        project = self.client.get_project(self.project)

        self.client.enable_experimental = True

        export_params = {
            "attachments": False,
            "metadata_fields": False,
            "data_row_details": True,
            "project_details": True,
            "label_details": True,
            "performance_details": False,
            "interpolated_frames": True,
        }

        export_task = project.export(params=export_params)
        export_task.wait_till_done()

        data_rows = []

        if export_task.has_errors():
            export_task.get_stream(
                converter=lb.JsonConverter(), stream_type=lb.StreamType.ERRORS
            ).start(stream_handler=lambda error: print(error))

        if export_task.has_result():
            stream = export_task.get_stream(
                converter=lb.JsonConverter(), stream_type=lb.StreamType.RESULT
            )
            for output in stream:
                data_rows.append(output.json_str)

        return data_rows

    def import_ground_truths(
        self, mal_job_name: str = f"mal-{str(uuid4())}"
    ) -> lb.LabelImport:
        """
        Imports ground truths to the project.

        Args:
            mal_job_name (str, optional): The name of the import job. Defaults to f"mal-{str(uuid4())}".

        Returns:
            lb.LabelImport: The import job.
        """
        if len(self.labels) == 0:
            raise Exception("No labels to import")
        upload_job = lb.LabelImport.create_from_objects(
            client=self.client,
            project_id=self.project,
            name=mal_job_name,
            labels=self.labels,
        )
        upload_job.wait_until_done()

        return upload_job

    def import_predictions(
        self, mal_job_name: str = f"mal-{str(uuid4())}"
    ) -> lb.MALPredictionImport:
        """
        Imports predictions to the project.

        Args:
            mal_job_name (str, optional): The name of the import job. Defaults to f"mal-{str(uuid4())}".

        Returns:
            lb.MALPredictionImport: The import job.
        """
        if len(self.labels) == 0:
            raise Exception("No labels to import")
        upload_job = lb.MALPredictionImport.create_from_objects(
            client=self.client,
            project_id=self.project,
            name=mal_job_name,
            predictions=self.labels,
        )
        upload_job.wait_until_done()

        return upload_job

    def create_bbox_labels(self, results: List[Dict[str, str]]) -> None:
        """
        Creates bounding box labels that can be imported.

        Args:
            results (List[Dict[str, str]]): The results containing the global key and predictions.

        Returns:
            None
        """
        for result in results:
            annotations = []
            if "predictions" in result:
                for prediction in result["predictions"]:
                    lb_name = self.ontology_mapping[prediction["answer"]]
                    bbox_source = lb_types.ObjectAnnotation(
                        name=lb_name,
                        value=lb_types.Rectangle(
                            start=lb_types.Point(
                                x=prediction["start_x"], y=prediction["start_y"]
                            ),
                            end=lb_types.Point(
                                x=prediction["end_x"], y=prediction["end_y"]
                            ),
                        ),
                    )
                    annotations.append(bbox_source)
                self.labels.append(
                    lb_types.Label(
                        data=lb_types.ImageData(global_key=result["global_key"]),
                        annotations=annotations,
                    )
                )

    def create_segment_labels(self, results: List[Dict[str, str]]) -> None:
        """
        Creates segment labels that can be imported.

        Args:
            results (List[Dict[str, str]]): The results containing the global key and predictions.

        Returns:
            None
        """
        for result in results:
            annotations = []
            if "predictions" in result:
                for prediction in result["predictions"]:
                    color = (255, 255, 255)
                    if "color" in prediction:
                        color = prediction["color"]
                    lb_name = self.ontology_mapping[prediction["answer"]]
                    mask_data = lb_types.MaskData(im_bytes=prediction["mask"])
                    mask_annotation = lb_types.ObjectAnnotation(
                        name=lb_name, value=lb_types.Mask(mask=mask_data, color=color)
                    )
                    annotations.append(mask_annotation)
                self.labels.append(
                    lb_types.Label(
                        data=lb_types.ImageData(global_key=result["global_key"]),
                        annotations=annotations,
                    )
                )

    def create_polygon_labels(self, results: List[Dict[str, str]]) -> None:
        """
        Creates polygon labels that can be imported.

        Args:
            results (List[Dict[str, str]]): The results containing the global key and predictions.

        Returns:
            None
        """
        for result in results:
            annotations = []
            if "predictions" in result:
                for prediction in result["predictions"]:
                    lb_name = self.ontology_mapping[prediction["answer"]]
                    polygon_annotation = lb_types.ObjectAnnotation(
                        name=lb_name,
                        value=lb_types.Polygon(
                            points=[
                                lb_types.Point(x=coordinates[0], y=coordinates[1])
                                for coordinates in prediction["points"]
                            ]
                        ),
                    )
                    annotations.append(polygon_annotation)
                self.labels.append(
                    lb_types.Label(
                        data=lb_types.ImageData(global_key=result["global_key"]),
                        annotations=annotations,
                    )
                )
