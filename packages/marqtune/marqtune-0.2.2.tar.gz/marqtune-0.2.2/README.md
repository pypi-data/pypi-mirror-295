# Marqtune Python Client
## Overview
The Marqtune Python Client is a Python library that provides a convenient interface for interacting with the Marqtune API. This library allows users to perform various operations, such as training models, preparing data, evaluating models, managing tasks, and working with data management endpoints.

## Installation
To use the Marqtune Python Client, you need to install it first. You can install it using pip:

```bash
pip install marqtune
```

## Getting Started
### Initializing the Client
To get started, create an instance of the Client class by providing the URL to the Marqtune API and an API key:

```python
from marqtune import Client
from marqtune.enums import DatasetType

url = "https://marqtune.marqo.ai"
api_key = "your_api_key"

marqtune_client = Client(url=url, api_key=api_key)
```

### Create Training Dataset
A training dataset is used to train machine learning models. Here is how you can create a training dataset:
```python
# Define the data schema for the dataset
data_schema = {
    "my-text-1": "text",
    "my-text-2": "text",
    "my-image": "image_pointer",
    "my-score": "score"
}

# Create a training dataset
dataset = marqtune_client.create_dataset(
    dataset_name="training_dataset",
    file_path="path/to/your/dataset/file.csv",
    dataset_type=DatasetType.TRAINING,
    data_schema=data_schema,
    wait_for_completion=True
)

print(f"Training dataset created with ID: {dataset.describe()['datasetId']}")
```

Please refer to the documentation for more details on the format of dataset.

### Training a Model
With dataset ready to be used, a model can be trained based on a base model and dataset_id. The base model can be an 
open_clip model or a Marqtuned model. 

```python
marqtune_client.train_model(
        dataset_id="dataset_id",
        model_name="test_model",
        base_model="ViT-B-32",
        base_checkpoint="laion400m_e31",
        model_type=ModelType.OPEN_CLIP,
        max_training_time=600,
        instance_type=InstanceType.BASIC,
        hyperparameters={"parameter1": "value1", "parameter2": "value2"},
        wait_for_completion=True
    )
```

### Downloading a Model
After training a model, you can download it using the download_model method. You need to provide the model_id and the checkpoint number you want to download. If the checkpoint is not specified, the latest checkpoint will be downloaded.
```python
marqtune_client.model("model_id").download()
```

### Evaluating a Model
After you trained a model you can then evaluate it's performance and compare it to base model. There are 2 steps in evaluating a model:
* Create an evaluation dataset
* Evaluate the model

#### Create an Evaluation Dataset
An evaluation dataset is used for verification and evaluation of the trained model. Here is how you can create an evaluation dataset:
```python
# Define the data schema for the dataset
data_schema = {
    "my_query": "text",
    "my_text": "text",
    "image": "image_pointer",
    "score": "score"
}

# Create an evaluation dataset
dataset = marqtune_client.create_dataset(
    dataset_name="evaluation_dataset",
    file_path="path/to/your/dataset/file.csv",
    dataset_type=DatasetType.EVALUATION,
    data_schema=data_schema,
    query_column="my_query",
    result_columns=["my_text", "image"],
    wait_for_completion=True
)

evaluation_dataset_id = dataset.describe()['datasetId']
print(f"Evaluation dataset created with ID: {evaluation_dataset_id}")
```
#### Evaluate the Model
Once the evaluation dataset is ready, you can evaluate the model using the evaluate method. You need to provide the model_id, dataset_id, checkpoint, model_type, and hyperparameters. If wait_for_completion is set to True, the method will wait for the evaluation task to complete before returning.
```python
marqtune_client.evaluate(
        model="model_id",
        dataset_id="evaluation_dataset_id",
        checkpoint="epoch_4",
        model_type=ModelType.MARQTUNED,
        hyperparameters={"parameter1": "value1", "parameter2": "value2"},
        wait_for_completion=True
    )
```
Please refer to the documentation for more details on hyperparameters.

### Task Management
The Marqtune API provides several methods to manage tasks, such as creating datasets, training models, and evaluating models. Below are the methods available for task management:

#### Dataset Methods
* describe(): Describe the dataset.
* logs(): Get the logs for the dataset.
* download_logs(): Download the logs for the dataset.
* delete(): Delete the dataset, terminating any running operations.

#### Model Methods
* describe(): Describe the model.
* logs(): Get the logs for the model.
* download(): Download the model.
* download_logs(): Download the logs for the model.
* delete(): Delete the model, terminating any running operations.

#### Evaluation Methods
* describe(): Describe the evaluation.
* logs(): Get the logs for the evaluation.
* download_logs(): Download the logs for the evaluation.
* delete(): Delete the evaluation, terminating any running operations

### Bucket Management
Manage your system data by uploading input-data, downloading models and deleting objects when not needed.

## Documentation
For detailed information about each method and its parameters, refer to the docstrings in the source code.
