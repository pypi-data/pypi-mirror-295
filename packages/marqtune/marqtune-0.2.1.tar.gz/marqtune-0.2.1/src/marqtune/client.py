import csv
import tarfile
import time
from abc import ABC
from typing import Optional

from marqtune import enums
from marqtune.httprequests import HttpRequests
from marqtune.config import Config
from marqtune.enums import DatasetType, InstanceType


class BaseResource(ABC):
    WAIT_STATUS = ["uploading", "provisioning", "initializing"]
    LOGS_STATUS = ["running"]
    TERMINAL_STATUS = ["ready", "deleted", "failed", "finished", "stopped"]

    def __init__(self, resource_id: str, http: HttpRequests, base_path: str):
        self._resource_id = resource_id
        self._http = http
        self._base_path = base_path

    def describe(self):
        return self._http.get(path=f"{self._base_path}/{self._resource_id}")

    def logs(self, from_time: Optional[int] = None, to_time: Optional[int] = None):
        params = []
        if from_time is not None:
            params.append(f"from={from_time}")
        if to_time is not None:
            params.append(f"to={to_time}")

        query_string = "&".join(params)

        return self._http.get(path=f"{self._base_path}/{self._resource_id}/logs?{query_string}")

    def download_logs(self):
        download_url = self._http.get(path=f"{self._base_path}/{self._resource_id}/logs/url")["downloadUrl"]

        response = self._http._operation("get")(download_url, stream=True)
        file_path = f"{self._resource_id}.log"

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print(f"Logs downloaded to {file_path}")

        return file_path

    def delete(self):
        return self._http.delete(path=f"{self._base_path}/{self._resource_id}")

    def wait_for_completion(self):
        """
        Wait for the resource to complete, printing progress and logs to the console
        """
        last_timestamp: Optional[float] = None
        last_status: Optional[str] = None
        last_print_was_status: bool = False
        dots_printed = 0

        def print_status(status: str):
            nonlocal last_status
            nonlocal last_print_was_status
            nonlocal dots_printed
            if last_status != status:
                if last_print_was_status:
                    print()

                print(status, end="")
                last_status = status
                last_print_was_status = True
                dots_printed = 0
            else:
                if dots_printed > 2:
                    dots_printed = 0
                dots_printed += 1
                print(f"\r{status}{'.' * dots_printed}", end="", flush=True)

        while True:
            description = self.describe()
            status = description["status"]
            secondary_status = description["secondaryStatus"]
            status_lower = status.lower()
            secondary_status_lower = secondary_status.lower()
            if secondary_status != status:
                status_to_print = f"{status}: {secondary_status}"
            else:
                status_to_print = status

            if secondary_status_lower in BaseResource.WAIT_STATUS:
                print_status(status_to_print)
            elif secondary_status_lower in BaseResource.LOGS_STATUS or status_lower in BaseResource.TERMINAL_STATUS:
                if last_print_was_status:
                    print_status(status_to_print)
                    print()
                    last_print_was_status = False

                logs = self.logs(from_time=last_timestamp)
                if len(logs) > 0:
                    last_timestamp = logs[-1]["timestamp"] + 1  # Add 1 milisecond to avoid duplicate logs
                    log_messages = [log["message"] for log in logs]
                    print("\n".join(log_messages))
                if status_lower in BaseResource.TERMINAL_STATUS:
                    print_status(status_to_print)
                    print()
                    if status_lower == "failed":
                        # Attempt to print failureReason if present
                        failure_reason = description.get("failureReason")
                        if failure_reason:
                            print(f"Failure Reason: {failure_reason}")
                    break
            else:
                raise ValueError(f"Unknown status: {status_to_print}")

            time.sleep(2)


class Dataset(BaseResource):
    BASE_PATH = "datasets"

    def __init__(self, dataset_id: str, http: HttpRequests):
        super().__init__(dataset_id, http, Dataset.BASE_PATH)
        self.dataset_id = dataset_id
        self._http = http

    @classmethod
    def create(cls, http: HttpRequests, dataset_name: str, file_path: str, dataset_type: DatasetType,
               data_schema: dict, image_download_headers: Optional[dict] = None, query_columns: list[str] = None,
               result_columns: list[str] = None, wait_for_completion: bool = True) -> "Dataset":

        request_body = {
            "datasetName": dataset_name,
            "datasetType": dataset_type,
            "dataSchema": data_schema
        }

        if image_download_headers is not None:
            request_body["imageDownloadHeaders"] = image_download_headers

        if dataset_type == enums.DatasetType.EVALUATION:
            if data_schema is None or query_columns is None or result_columns is None:
                raise ValueError("data_schema, query_columns and result_columns are required for evaluation dataset")
            request_body["queryColumns"] = query_columns
            request_body["resultColumns"] = result_columns

        cls.validate_dataset_files_locally(file_path, data_schema, dataset_type)

        response = http.post(
            path=f"{Dataset.BASE_PATH}",
            body=request_body,
        )

        dataset_id = response["datasetId"]
        upload_url = response["uploadUrl"]

        print(f'Dataset was initialised. Dataset ID: {dataset_id}')
        print("Attempting to upload file...")
        # Upload file
        # if file larger than 1gb then multipart
        with open(file_path, 'rb') as file:
            upload_response = http._operation("put")(upload_url, data=file)
        upload_response.raise_for_status()

        print("File uploaded successfully. Job will start soon")

        dataset = Dataset(dataset_id, http)

        if wait_for_completion:
            dataset.wait_for_completion()
            print(f"Dataset creation completed. Dataset ID: {dataset_id}")

        return dataset

    @classmethod
    def validate_dataset_files_locally(cls, file_path: str, data_schema: dict, dataset_type: DatasetType):
        # validate file is csv if training, and csv or tar if evaluation
        if dataset_type == DatasetType.TRAINING:
            if not file_path.endswith(".csv"):
                raise ValueError("Training dataset must be a csv file")

        if dataset_type == DatasetType.EVALUATION:
            if not file_path.endswith(".csv") and not tarfile.is_tarfile(file_path):
                raise ValueError("Evaluation dataset must be a csv file or a tar file")

        # validate if file type is tar it contains 2 expected files
        if tarfile.is_tarfile(file_path):
            expected_files = "queries.csv", "documents.jsonl"
            macos_metadata_files_to_ignore = "._queries.csv", "._documents.jsonl"
            with tarfile.open(file_path, 'r') as tar:
                files = [
                    tarinfo.name for tarinfo in tar.getmembers() if not tarinfo.name in macos_metadata_files_to_ignore
                ]
                if not all(file in files for file in expected_files) or len(files) != len(expected_files):
                    raise ValueError(f"Files in tar must be exactly {expected_files}")

        # validate all columns are present in data schema
        if not tarfile.is_tarfile(file_path):
            with open(file_path, 'r') as file:
                data = csv.DictReader(file)
                columns = data.fieldnames
            cls.validate_all_columns_from_data_schema_are_present_in_the_csv_headers(data_schema, columns)

    @classmethod
    def validate_all_columns_from_data_schema_are_present_in_the_csv_headers(cls, data_schema, columns):
        missing_columns = [field for field in data_schema.keys() if field not in columns]
        if missing_columns:
            raise ValueError(
                f"All fields in the data schema must be present in the dataset file headers. "
                f"Following fields from the data schema are missing in the dataset headers: {' '.join(missing_columns)}"
                f". Please fix your data schema or use a dataset that contains all the required fields."
            )

    @classmethod
    def list(cls, http: HttpRequests):
        return http.get(path=f"{Dataset.BASE_PATH}")

    def describe(self):
        """
        Describe the dataset.
        """
        return super().describe()

    def logs(self, from_time: Optional[int] = None, to_time: Optional[int] = None):
        """
        Get the logs for the dataset.

        Args:
            from_time: The start time for the logs in milliseconds since epoch
            to_time: The end time for the logs in milliseconds since epoch
        """
        return super().logs(from_time, to_time)

    def download_logs(self):
        """
        Download the logs for the dataset to `<dataset_id>.log`
        """
        return super().download_logs()

    def delete(self):
        """
        Delete the dataset, terminating any running operations
        """
        return super().delete()


class Model(BaseResource):
    BASE_PATH = "models"

    def __init__(self, model_id: str, http: HttpRequests):
        super().__init__(model_id, http, Model.BASE_PATH)
        self.model_id = model_id
        self._http = http

    @classmethod
    def train(cls, http: HttpRequests, dataset_id: str, model_name: str, base_model: str,
              instance_type: InstanceType, hyperparameters: dict,
              max_training_time: Optional[int] = None,
              wait_for_completion: Optional[bool] = True) -> "Model":
        request_body = {
            "datasetId": dataset_id,
            "modelName": model_name,
            "baseModel": base_model,
            "instanceType": instance_type,
            "hyperparameters": hyperparameters
        }
        if max_training_time is not None:
            request_body["maxTrainingTime"] = max_training_time

        response = http.post(
            path=f"{Model.BASE_PATH}/train",
            body=request_body,
        )

        model_id = response["modelId"]

        print(f'Model creation was initialised. Model ID: {model_id}')

        model = Model(model_id, http)

        if wait_for_completion:
            model.wait_for_completion()
            print(f"Model creation completed. Model ID: {model_id}")

        return model

    @classmethod
    def list(cls, http: HttpRequests):
        return http.get(path=f"{Model.BASE_PATH}")

    def download(self, checkpoint: Optional[str] = None, path: Optional[str] = None):
        """
        Download the model to a file.

        Args:
            path: The path to save the model to. If not provided, the model will be saved to `<model_id>`
            checkpoint: The checkpoint to download. If not provided, the latest checkpoint will be downloaded.
        """
        query_string = ""
        if checkpoint:
            query_string = f"?checkpoint={checkpoint}"
        download_url = self._http.get(f"{self.BASE_PATH}/{self.model_id}/download/url" + query_string)["downloadUrl"]

        response = self._http._operation("get")(download_url, stream=True)

        # Get the total file size from headers
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        chunk_size = 1024
        num_bars = 50

        filepath = path if path else self.model_id + "_" + (checkpoint if checkpoint else "latest") + ".pt"

        with open(filepath, "wb") as f:
            if total_size_in_bytes == 0:  # no content length header
                f.write(response.content)
            else:
                download_size = 0
                for data in response.iter_content(chunk_size=chunk_size):
                    download_size += len(data)
                    f.write(data)
                    done = int(num_bars * download_size / total_size_in_bytes)
                    # Display the progress bar
                    print(
                        f"\rDownloading: [{'█' * done}{'.' * (num_bars - done)}] "
                        f"{download_size * 100 / total_size_in_bytes:.2f}%",
                        end=''
                    )
        print("\nDownload completed.")
        return filepath

    def release(self, checkpoint: str):
        """
        Release a checkpoint, making it available for creating new indexes in Marqo Cloud.

        Args:
            checkpoint: The checkpoint to release
        """
        return self._http.post(f"{self.BASE_PATH}/{self.model_id}/released-checkpoints/{checkpoint}")

    def describe(self):
        """
        Describe the model.
        """
        return super().describe()

    def logs(self, from_time: Optional[int] = None, to_time: Optional[int] = None):
        """
        Get the logs for the model.

        Args:
            from_time: The start time for the logs in milliseconds since epoch
            to_time: The end time for the logs in milliseconds since epoch
        """
        return super().logs(from_time, to_time)

    def download_logs(self):
        """
        Download the logs for the model to `<model_id>.log`
        """
        return super().download_logs()

    def delete(self):
        """
        Delete the model, terminating any running operations
        """
        return super().delete()


class Evaluation(BaseResource):
    BASE_PATH = "evaluation"

    def __init__(self, evaluation_id: str, http: HttpRequests):
        super().__init__(evaluation_id, http, Evaluation.BASE_PATH)
        self.evaluation_id = evaluation_id
        self._http = http

    @classmethod
    def evaluate(cls, http: HttpRequests, dataset_id: str, model: str,
                 hyperparameters: dict, wait_for_completion: bool = True) -> "Evaluation":
        request_body = {
            "datasetId": dataset_id,
            "model": model,
            "hyperparameters": hyperparameters
        }

        response = http.post(
            path=f"{Evaluation.BASE_PATH}",
            body=request_body,
        )

        evaluation_id = response["evaluationId"]

        print(f'Evaluation was initialised. Evaluation ID: {evaluation_id}')

        evaluation = Evaluation(evaluation_id, http)

        if wait_for_completion:
            evaluation.wait_for_completion()
            print(f"Evaluation completed. Evaluation ID: {evaluation_id}")

        return evaluation

    @classmethod
    def list(cls, http: HttpRequests):
        return http.get(path=f"{Evaluation.BASE_PATH}")

    def describe(self):
        """
        Describe the evaluation.
        """
        return super().describe()

    def logs(self, from_time: Optional[int] = None, to_time: Optional[int] = None):
        """
        Get the logs for the evaluation.

        Args:
            from_time: The start time for the logs in milliseconds since epoch
            to_time: The end time for the logs in milliseconds since epoch
        """
        return super().logs(from_time, to_time)

    def download_logs(self):
        """
        Download the logs for the evaluation to `<evaluation_id>.log`
        """
        return super().download_logs()

    def delete(self):
        """
        Delete the evaluation, terminating any running operations
        """
        return super().delete()


class Client:
    """
    A client for interacting with the Marqtune API.

    This client provides methods to perform operations such as creating datasets, training models and
    evaluating models using the Marqtune platform.
    """

    def __init__(
            self, url: str = "marqtune.marqo.ai",
            api_key: str = None
    ) -> None:
        """
        Initializes the Marqtune API client.

        Args:
            url: The URL of the Marqtune API (e.g., "http://localhost:8332")
            api_key: The API key for authentication with the Marqtune API
        """
        self.config = Config(
            url=url,
            api_key=api_key
        )
        self.http = HttpRequests(self.config)

    def create_dataset(self, dataset_name: str, file_path: str, dataset_type: DatasetType,
                       data_schema: dict, image_download_headers: Optional[dict] = None, query_columns: list = None,
                       result_columns: list = None, wait_for_completion: bool = True) -> Dataset:
        """
        Creates a dataset for training or evaluation.

        Args:
            dataset_name: The name of the dataset.
            file_path: The path to the dataset file.
            dataset_type: The type of the dataset (training or evaluation).
            data_schema: The schema of the dataset.
            image_download_headers: The headers for downloading images. Useful for downloading non-public images
                where authentication headers are required.
            query_columns: The columns that will be used as query during evaluation. Only valid for evaluation datasets.
            result_columns: The columns that will be used as results during evaluation.
                Only valid for evaluation datasets.
            wait_for_completion: Whether to wait for the dataset creation to complete. When set to True, the method
                will block until the dataset is ready, and will print progress and logs to the console.
                When set to False, the method will return immediately without waiting for the dataset to be ready.

        Returns:
            The created dataset
        """
        return Dataset.create(
            self.http,
            dataset_name,
            file_path,
            dataset_type,
            data_schema,
            image_download_headers,
            query_columns,
            result_columns,
            wait_for_completion
        )

    def list_datasets(self):
        """
        Lists all datasets.
        """
        return Dataset.list(self.http)

    def train_model(self, dataset_id: str, model_name: str, base_model: str,
                    instance_type: InstanceType, hyperparameters: dict,
                    max_training_time: Optional[int] = None, wait_for_completion: Optional[bool] = True) -> Model:
        """
        Trains a new model.
        Args:
            dataset_id: The ID of the dataset to use for training
            model_name: The name of the trained model
            base_model: Base model to train from. If `modelType` is `open_clip`, this must be the name of an OpenCLIP model.
                If `modelType` is `marqtuned` , this must be a Maqrtune Model ID.
            instance_type: The Marqtune instance type to use for training
            hyperparameters: Training hyperparameters
            max_training_time: The maximum time to train the model (in seconds). The training will stop after this time
                even if it has not completed. Optional, defaults to 86400 seconds (24 hours).
            wait_for_completion: Whether to wait for training to complete. When set to True, the method
                will block until training is complete, and will print progress and logs to the console.
                When set to False, the method will return immediately without waiting for training to complete.
        Returns:
            The trained model
        """
        return Model.train(
            self.http,
            dataset_id,
            model_name,
            base_model,
            instance_type,
            hyperparameters,
            max_training_time,
            wait_for_completion
        )

    def list_models(self):
        """
        Lists all models.
        """
        return Model.list(self.http)

    def evaluate(self, dataset_id: str, model: str,
                 hyperparameters: dict, wait_for_completion: bool = True) -> Evaluation:
        """
        Evaluates a model.

        Args:
            dataset_id: Evaluation dataset ID
            model: Model to evaluate. If `modelType` is `open_clip`, this must be the name of an OpenCLIP model.
                If `modelType` is `marqtuned` , this must be a Maqrtune Model ID.
            hyperparameters: Evaluation hyperparameters
            wait_for_completion: Whether to wait for evaluation to complete. When set to True, the method
                will block until evaluation is complete, and will print progress and logs to the console.
                When set to False, the method will return immediately without waiting for evaluation to complete.
        Returns:
            The evaluation object
        """
        return Evaluation.evaluate(
            self.http,
            dataset_id,
            model,
            hyperparameters,
            wait_for_completion
        )

    def list_evaluations(self):
        """
        Lists all evaluations.
        """
        return Evaluation.list(self.http)

    def dataset(self, dataset_id: str) -> Dataset:
        """
        Gets a dataset object by ID.

        Args:
            dataset_id: The ID of the dataset
        """
        return Dataset(dataset_id, self.http)

    def model(self, model_id: str) -> Model:
        """
        Gets a model object by ID.
        Args:
            model_id: The ID of the model
        """
        return Model(model_id, self.http)

    def evaluation(self, evaluation_id: str) -> Evaluation:
        """
        Gets an evaluation object by ID.

        Args:
            evaluation_id: The ID of the evaluation
        """
        return Evaluation(evaluation_id, self.http)
