from enum import Enum


class DatasetType(str, Enum):
    """
    Enum for dataset type.
    """
    TRAINING = "training"
    EVALUATION = "evaluation"


class InstanceType(str, Enum):
    """
    Enum for instance type.
    """
    BASIC = "marqtune.basic"
    PERFORMANCE = "marqtune.performance"


class DataSchemaTypes(str, Enum):
    """
    Enum for data schema types.
    """
    TEXT = "text"
    IMAGE_POINTER = "image_pointer"
    SCORE = "score"
    DOC_ID = "doc_id"
