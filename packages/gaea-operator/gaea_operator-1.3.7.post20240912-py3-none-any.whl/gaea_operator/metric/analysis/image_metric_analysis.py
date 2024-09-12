#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/23
# @Author  : yanxiaodong
# @File    : label_count_metric.py
"""
from typing import List, Dict, Any
import os
import numpy as np
import math

from ..operator import RatioStatistic
from ..types.metric import \
    AnnotationRatioMetricResult, \
    ImageAnnotationRatioMetric, \
    LabelAnnotationRatio
from gaea_operator.utils import write_file


class ImageMetricAnalysis(object):
    """
    Label statistic metric analysis.
    """
    manual_task_kind = "Manual"

    def __init__(self, category: str, labels: List = None, images: List[Dict] = None, ):
        self.labels = labels
        self.images = images
        self.category = category

        self.image_dict = {}
        self.img_id_str2int = {}
        self.labels = []
        self.label_id2index = {}
        self.label_index2id = {}
        self.label_id2name = {}
        self.label_name2id = {}
        self.label_index2name = {}
        self.metric = None
        self.task_kind = self.manual_task_kind

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        self.metric.reset()

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        if images is None:
            return
        self.images = images
        self.image_dict = {item["image_id"]: item for item in images}
        self.img_id_str2int = {key: idx + 1 for idx, key in enumerate(self.image_dict)}

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        if labels is None:
            return
        self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
        self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
        self.label_index2id = {idx: label["id"] for idx, label in enumerate(self.labels)}
        self.label_id2name = {label["id"]: label["name"] for label in self.labels}
        self.label_name2id = {label["name"]: label["id"] for idx, label in enumerate(self.labels)}
        self.label_index2name = {idx: label["name"] for idx, label in enumerate(self.labels)}
        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        self.metric = RatioStatistic(num_classes=len(self.labels), labels=self.labels)

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        self.task_kind = kwargs.get("task_kind", self.manual_task_kind)
        annotations = predictions if predictions is not None else references
        assert annotations is not None, "annotations should be not None"
        assert self.images is not None, "images should be not None"

        annotated_array, image_array = self._format_input(annotations)

        self.metric.update(annotated_images=annotated_array, images=image_array)

    def _format_input(self, annotations: List[Dict]):
        """
        Format predictions and references.
        """
        num_images = len(self.images)  # 使用 self.images 计算总图像数量
        annotated_array = np.zeros((num_images, len(self.labels)))  # 每个图像和标签的标注数量
        image_id_2_index = {item["image_id"]: idx for idx, item in enumerate(self.images)}
        image_array = np.ones((num_images, len(self.labels)))

        for item in annotations:
            if item["image_id"] not in image_id_2_index:
                continue
            if item.get("annotations") is not None:
                for anno in item["annotations"]:
                    if self.category == "Image/TextDetection" or self.category == "Image/OCR":
                        anno["labels"] = [{"id": 0, "name": "文字"}]
                    for label in anno.get("labels", []):
                        label_id = label.get("id")
                        if label_id is None:
                            continue
                        if isinstance(label_id, str):
                            label_id = int(label_id)
                        if math.isnan(label_id):
                            continue
                        if int(label_id) not in self.label_id2index:
                            continue
                        column_index = self.label_id2index[int(label_id)]
                        annotated_array[image_id_2_index[item["image_id"]], column_index] = 1  # 增加标注数量

        return annotated_array, image_array

    def _format_result(self, metric_result: Any):
        """
        Format metric results into the desired structure.
        """
        results = []

        # metric_result 是一个包含 annotated_array, image_array 和 ratio 的元组
        annotated_image, image, ratio = metric_result
        annotation_result_list = list()
        for idx, label_name in self.label_index2name.items():
            # 创建 AnnotationRatioMetricResult 对象
            annotation_result = AnnotationRatioMetricResult(
                labelName=label_name,
                imageCount=image[idx],
                annotatedImageCount=annotated_image[idx],
                ratio=ratio[idx]
            )
            annotation_result_list.append(annotation_result)
        # 创建 LabelAnnotationRatio 对象
        label_annotation_ratio = LabelAnnotationRatio(
            name="AnnotationRatio",
            displayName="标注比例统计",
            result=annotation_result_list
        )

        # 将结果添加到列表中
        results.append(label_annotation_ratio)

        # 创建 ImageAnnotationRatioMetric 对象
        image_annotation_metric = ImageAnnotationRatioMetric(
            labels=self.labels,
            metrics=results
        )

        # 返回度量的字典表示形式
        return image_annotation_metric.dict()

    def compute(self):
        """
        Compute metric.
        """

        metric_result = self._format_result(metric_result=self.metric.compute())

        return metric_result

    def save(self, metric_result: Dict, output_uri: str):
        """
        Save metric.
        """
        if os.path.splitext(output_uri)[1] == "":
            output_dir = output_uri
            file_name = "annotated_ratio.json"
        else:
            output_dir = os.path.dirname(output_uri)
            file_name = os.path.basename(output_uri)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        write_file(obj=metric_result, output_dir=output_dir, file_name=file_name)

    def __call__(self, predictions: List[Dict], references: List[Dict], output_uri: str):
        self.update(predictions=predictions, references=references)
        metric_result = self.compute()

        self.save(metric_result=metric_result, output_uri=output_uri)
