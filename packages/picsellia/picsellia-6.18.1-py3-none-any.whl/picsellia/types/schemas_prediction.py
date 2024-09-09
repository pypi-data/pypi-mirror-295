from typing import List

from pydantic import BaseModel, model_validator

from picsellia.types.enums import InferenceType


class PredictionFormat(BaseModel):
    @property
    def model_type(cls) -> InferenceType:
        raise Exception()


class ClassificationPredictionFormat(PredictionFormat):
    detection_classes: List[int]
    detection_scores: List[float]

    @property
    def model_type(cls) -> InferenceType:
        return InferenceType.CLASSIFICATION


class DetectionPredictionFormat(PredictionFormat):
    detection_classes: List[int]
    detection_boxes: List[List[int]]
    detection_scores: List[float]

    @property
    def model_type(cls) -> InferenceType:
        return InferenceType.OBJECT_DETECTION

    @model_validator(mode="before")
    @classmethod
    def check_sizes(cls, data):
        labels, scores, boxes = (
            data.get("detection_classes"),
            data.get("detection_scores"),
            data.get("detection_boxes"),
        )

        if (
            labels is None
            or scores is None
            or boxes is None is None
            or len(labels) != len(scores)
            or len(boxes) != len(labels)
        ):
            raise ValueError("incoherent lists")

        return data


class SegmentationPredictionFormat(PredictionFormat):
    detection_classes: List[int]
    detection_boxes: List[List[int]]
    detection_scores: List[float]
    detection_masks: List[List[List[int]]]

    @property
    def model_type(cls) -> InferenceType:
        return InferenceType.SEGMENTATION

    @model_validator(mode="before")
    @classmethod
    def check_sizes(cls, data):
        labels, boxes, scores, masks = (
            data.get("detection_classes"),
            data.get("detection_boxes"),
            data.get("detection_scores"),
            data.get("detection_masks"),
        )

        if (
            labels is None
            or scores is None
            or boxes is None
            or masks is None
            or len(labels) != len(scores)
            or len(boxes) != len(labels)
            or len(masks) != len(labels)
        ):
            raise ValueError("incoherent lists")

        return data
