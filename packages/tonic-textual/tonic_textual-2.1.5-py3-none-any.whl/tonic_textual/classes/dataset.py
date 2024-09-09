from __future__ import annotations
from typing import List, Dict, Optional, Any
import os
import json
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import requests.exceptions
import requests
from tonic_textual.classes.tonic_exception import DatasetFileMatchesExistingFile
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.datasetfile import DatasetFile
from tonic_textual.services.datasetfile import DatasetFileService


class Dataset:
    """Class to represent and provide access to a Tonic Textual dataset.

    Parameters
    ----------
    id: str
        Dataset identifier.

    name: str
        Dataset name.

    files: Dict
        Serialized DatasetFile objects representing the files in a dataset.

    client: HttpClient
        The HTTP client to use.
    """

    def __init__(
        self, id: str, name: str, files: List[Dict[str, Any]], client: HttpClient
    ):
        self.id = id
        self.name = name
        self.client = client
        self.datasetfile_service = DatasetFileService(self.client)
        self.files = [
            DatasetFile(
                f["fileId"],
                f["fileName"],
                f.get("numRows"),
                f["numColumns"],
                f["processingStatus"],
                f.get("processingError"),
            )
            for f in files
        ]

        if len(self.files) > 0:
            self.num_columns = max([f.num_columns for f in self.files])
        else:
            self.num_columns = None

        self.num_rows_per_request = 1000
        self.total_rows_fetched = 0

        self._total_rows_fetched_in_current_file = 0
        self._cur_file_idx = 0

    def reset(self):
        self.total_rows_fetched = 0
        self._cur_file_idx = 0
        self._total_rows_fetched_in_current_file = 0

    def upload_then_add_file(self, file_path: str, file_name: Optional[str] = None):
        """
        Uploads a file to the dataset.

        Parameters
        --------
        file_path: str
            The absolute path of the file to upload.
        file_name: str
            The name of the file to save to Tonic Textual.

        Raises
        ------

        DatasetFileMatchesExistingFile
            Returned if the file content matches an existing file.

        """
        if file_name is None:
            file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            with tqdm(
                desc="[INFO] Uploading",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as t:
                reader_wrapper = CallbackIOWrapper(t.update, f, "read")

                files = {
                    "document": (
                        None,
                        json.dumps(
                            {
                                "fileName": file_name,
                                "csvConfig": {},
                                "datasetId": self.id,
                            }
                        ),
                        "application/json",
                    ),
                    "file": reader_wrapper,
                }
                try:
                    updated_dataset = self.client.http_post(
                        f"/api/dataset/{self.id}/files/upload", files=files
                    )
                    # numRows is null when a file is first uploaded
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 409:
                        raise DatasetFileMatchesExistingFile(e)
                    else:
                        raise e
        self.files = [
            DatasetFile(
                f["fileId"],
                f["fileName"],
                f.get("numRows"),
                f["numColumns"],
                f["processingStatus"],
                f.get("processingError"),
            )
            for f in updated_dataset["files"]
        ]
        self.num_columns = max([f.num_columns for f in self.files])

    def fetch_all_df(self):
        """
        Fetches all of the data in the dataset as a pandas dataframe.

        Returns
        -------
        pd.DataFrame
            Dataset data in a pandas dataframe.
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "Pandas is required to fetch the dataset data as a pandas dataframe. Please install pandas before using this method."
            ) from e
        data = self._fetch_all()

        if self.num_columns is None:
            return pd.DataFrame()

        # RAW file, not CSV
        if self.num_columns == 0:
            if len(data) == 0:
                return pd.DataFrame(columns=["text"])
            return pd.DataFrame(data, columns=["text"])

        columns = ["col" + str(x) for x in range(self.num_columns)]
        if len(data) == 0:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame(data, columns=columns)

    def fetch_all_json(self) -> str:
        """
        Fetches all of the data in the dataset as JSON.

        Returns
        -------
        str
            Dataset data in JSON format.
        """
        return json.dumps(self._fetch_all())

    def _fetch_all(self) -> List[List[str]]:
        """
        Fetches all data from the dataset.

        Returns
        -------
        List[List[str]]
            The datset data.
        """
        response = []
        with requests.Session() as session:
            for file in self.files:
                try:
                    if file.num_columns == 0:
                        more_data = self.client.http_get_file(
                            f"/api/dataset/{self.id}/files/{file.id}/get_data",
                            session=session,
                        )
                        response += [[more_data]]
                    else:
                        more_data = self.client.http_get(
                            f"/api/dataset/{self.id}/files/{file.id}/get_data",
                            session=session,
                        )
                        response += more_data
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 409:
                        continue
                    else:
                        raise e
            return response

    def get_processed_files(self) -> List[DatasetFile]:
        """
        Gets all of the files in the dataset for which processing is complete. The data
        in these files is returned when data is requested.

        Returns
        ------
        List[DatasetFile]:
            The list of processed dataset files.
        """
        return list(filter(lambda x: x.processing_status == "Completed", self.files))

    def get_queued_files(self) -> List[DatasetFile]:
        """
        Gets all of the files in the dataset that are waiting to be processed.

        Returns
        ------
        List[DatasetFile]:
            The list of dataset files that await processing.
        """
        return list(filter(lambda x: x.processing_status == "Queued", self.files))

    def get_running_files(self) -> List[DatasetFile]:
        """
        Gets all of the files in the dataset that are currently being processed.

        Returns
        ------
        List[DatasetFile]:
            The list of files that are being processed.
        """
        return list(filter(lambda x: x.processing_status == "Running", self.files))

    def get_failed_files(self) -> List[DatasetFile]:
        """
        Gets all of the files in dataset that encountered an error when they were
        processed. These files are effectively ignored.

        Returns
        ------
        List[DatasetFile]:
            The list of files that had processing errors.
        """
        return list(filter(lambda x: x.processing_status == "Failed", self.files))

    def _check_processing_and_update(self):
        """
        Checks the processing status of the files in the dataset and updates the files
        list.
        """
        if len(self.get_queued_files() + self.get_running_files()) > 0:
            self.files = self.datasetfile_service.get_files(self.id)

    def describe(self) -> str:
        """
        Returns a string of the dataset name, identifier, and the list of files.

        Examples
        --------
        >>> workspace.describe()
        Dataset: your_dataset_name [dataset_id]
        Number of Files: 2
        Number of Rows: 1000
        """
        self._check_processing_and_update()

        files_waiting_for_proc = self.get_queued_files() + self.get_running_files()
        files_with_error = self.get_failed_files()
        number_rows = sum(
            [x.num_rows if x.num_rows is not None else 0 for x in self.files]
        )
        result = f"Dataset: {self.name} [{self.id}]\n"
        result += f"Number of Files: {len(self.get_processed_files())}\n"
        result += "Files that are waiting for processing: "
        result += f"{', '.join([str((f.id,f.name)) for f in files_waiting_for_proc])}\n"
        result += "Files that encountered errors while processing: "
        result += f"{', '.join([str((f.id,f.name)) for f in files_with_error])}\n"
        result += f"Number of Rows: {number_rows}\n"
        result += f"Number of rows fetched: {self.total_rows_fetched}"
        return result
