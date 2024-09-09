import io
import json
import os
from typing import List, Optional, Union

import requests
from requests import RequestException

from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.parse_api_responses.file_parse_result import FileParseResult
from tonic_textual.classes.pipeline import Pipeline
from tonic_textual.classes.tonic_exception import PipelineDeleteError, PipelineCreateError

from tonic_textual.classes.textual_telemetry import TextualTelemetry


class TonicTextualParse:
    """Wrapper class for invoking Tonic Textual API

    Parameters
    ----------
    base_url : str
        The URL to your Tonic Textual instance. Do not include trailing backslashes.
    api_key : str
        Your API token. This argument is optional. Instead of providing the API token
        here, it is recommended that you set the API key in your environment as the
        value of TEXTUAL_API_KEY.
    verify: bool
        Whether SSL Certification verification is performed.  This is enabled by
        default.
    Examples
    --------
    >>> from tonic_textual.parse_api import TonicTextualParse
    >>> textual = TonicTextualParse("https://textual.tonic.ai")
    """

    def __init__(
        self, base_url: str, api_key: Optional[str] = None, verify: bool = True
    ):
        if api_key is None:
            api_key = os.environ.get("TONIC_TEXTUAL_API_KEY")
            if api_key is None:
                raise Exception(
                    "No API key provided. Either provide an API key, or set the API "
                    "key as the value of the TEXTUAL_API_KEY environment "
                    "variable."
                )
        self.api_key = api_key
        self.client = HttpClient(base_url, self.api_key, verify)
        self.verify = verify
        self.telemetry_client = TextualTelemetry(base_url, api_key, verify)

    def get_pipelines(self) -> List[Pipeline]:
        """Get the pipelines for the Tonic Textual instance.

        Returns
        -------
        List[Pipeline]
            A list of pipeline objects, ordered by their creation timestamp.
        Examples
        --------
        >>> latest_pipeline = textual.get_pipelines()[-1]
        """
        self.telemetry_client.log_function_call()

        with requests.Session() as session:
            response = self.client.http_get("/api/parsejobconfig", session=session)
            pipelines: List[Pipeline] = []
            for x in response:
                pipelines.append(Pipeline(x["name"], x["id"], self.client))
            return pipelines

    def create_pipeline(self, pipeline_name: str) -> Pipeline:
        """Create a new pipeline.

        Parameters
        ----------
        pipeline_name: str
            The name of the pipeline.

        Returns
        -------
        Pipeline
            The newly created pipeline.
        """
        self.telemetry_client.log_function_call()

        try:
            p = self.client.http_post(f"/api/parsejobconfig/local-files", data={"name": pipeline_name})
            return Pipeline(p.get('name'), p.get('id'), self.client)
        except RequestException as req_err:
            if hasattr(req_err, 'response') and req_err.response is not None:
                status_code = req_err.response.status_code
                error_message = req_err.response.text
                raise PipelineCreateError(f"Error {status_code}: {error_message}")
            else:
                raise req_err


    def delete_pipeline(self, pipeline_id: str):
        """Delete a pipeline.


        Parameters
        ----------
        pipeline_id: str
            The ID of the pipeline.
        """
        self.telemetry_client.log_function_call()

        try:
            result = self.client.http_delete(f"/api/parsejobconfig/{pipeline_id}")
            return result
        except RequestException as req_err:
            if hasattr(req_err, 'response') and req_err.response is not None:
                status_code = req_err.response.status_code
                error_message = req_err.response.text
                raise PipelineDeleteError(f"Error {status_code}: {error_message}")
            else:
                raise req_err

    def get_pipeline_by_id(self, pipeline_id: str) -> Union[Pipeline, None]:
        """Get the pipeline by ID.

        Parameters
        ----------
        pipeline_id: str
            The ID of the pipeline.

        Returns
        -------
        Union[Pipeline, None]
            The Pipeline object or None if no pipeline is found.
        """
        self.telemetry_client.log_function_call()

        pipelines = self.get_pipelines()
        found_pipelines = list(filter(lambda x: x.id == pipeline_id, pipelines))
        if len(found_pipelines) == 0:
            return None

        if len(found_pipelines) > 1:
            raise Exception(
                "Found more than 1 pipeline with this ID.  This shouldn't happen."
            )

        return found_pipelines[0]


    def parse_file(self, file: io.IOBase, file_name: str, timeout: int | None = None) -> FileParseResult:
        """Parse a given file.  Binary files should be opened with 'rb' option.

        Parameters
        ----------
        file: io.IOBase
            The opened file, available for reading, which will be parsed.
        file_name: str
            The name of the file
        timeout: int | None
            Optional timeout you can set, in seconds, that stops wainting for parsed result after specified time.

        Returns
        -------
        FileParseResult
            The parsed document
        """
                
        self.telemetry_client.log_function_call()

        files = {
            "document": (
                None,
                json.dumps({"fileName": file_name, "csvConfig": {}}),
                "application/json",
            ),
            "file": file,
        }

        response = self.client.http_post("/api/parse", files=files, timeout_seconds=timeout)
        document = response['document']
        file_parse_result = response['fileParseResult']

        return FileParseResult(file_parse_result, self.client, False, document = json.loads(document))


    def parse_s3_file(self, bucket: str, key: str, timeout: int | None = None) -> FileParseResult:
        """Parse a given file found in S3.  Uses boto3 to fetch files from S3.

        Parameters
        ----------
        bucket: str
            The bucket which contains the file to parse
        key: str
            The key of the file to parse
        timeout: int | None
            Optional timeout you can set, in seconds, that stops wainting for parsed result after specified time.

        Returns
        -------
        FileParseResult
            The parsed document
        """
                
        self.telemetry_client.log_function_call()
        import boto3
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)

        file_name = key.split("/")[-1]
        return self.parse_file(obj.get()['Body'].read(), file_name, timeout=timeout)