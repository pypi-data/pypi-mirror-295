from typing import Optional


class DatasetFile:
    """
    Class to store the metadata for a dataset file.

    Parameters
    ----------
    id : str
        The identifier of the dataset file.

    name: str
        The file name of the dataset file.

    num_rows : long
        The number of rows in the dataset file.

    num_columns: int
        The number of columns in the dataset file.

    processing_status: string
        The status of the dataset file in the processing pipeline. Possible values are
        'Completed', 'Failed', 'Cancelled', 'Running', and 'Queued'.

    processing_error: string
        If the dataset file processing failed, a description of the issue that caused
        the failure.

    uploaded_timestamp: str
        Timestamp in UTC when dataset file was uploaded to the dataset.
    """

    def __init__(
        self,
        id: str,
        name: str,
        num_rows: Optional[int],
        num_columns: int,
        processing_status: str,
        processing_error: Optional[str],
    ):
        self.id = id
        self.name = name
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.processing_status = processing_status
        self.processing_error = processing_error

    def describe(self) -> str:
        """Returns the dataset file metadata as string. Includes the identifier, file
        name, number of rows, and number of columns."""
        description = f"File: {self.name} [{self.id}]\n"
        description += f"Number of rows: {self.num_rows}\n"
        description += f"Number of columns: {self.num_columns}\n"
        description += f"Status: {self.processing_status}\n"
        if self.processing_status != "" and self.processing_error is not None:
            description += f"Error: {self.processing_error}\n"
        return description
