#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import json
from itertools import zip_longest
from typing import List, Optional

import numpy as np
import pandas as pd

from dmm.custom_metric import SingleMetricResult
from dmm.metric.metric_base import MetricBase


class PromptSimilarityMetricBase(MetricBase):
    """This is a base class for calculating distance between LLM prompt and context vectors.

    This class pulls the data out of the `prompt_column`, and an array from the contexts in the `context_column`. It
    leaves the `calculate_distance()` to be implemented by the derived class.

     A simple example class could look like this:
     .. code-block:: python

    class EuclideanMinMetric(PromptSimilarityMetricBase):
        def calculate_distance(self, prompt_vector: np.ndarray, context_vectors: List[np.ndarray]) -> np.float64:
            distances = [
                np.linalg.norm(prompt_vector - context_vector)
                for context_vector in context_vectors
            ]
            return min(distances)
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        prompt_column: str = "_LLM_PROMPT_VECTOR",
        context_column: str = "_LLM_CONTEXT",
    ):
        super().__init__(
            name=name,
            description=description,
            need_scoring_data=True,
            need_predictions=False,
            need_actuals=False,
            need_training_data=False,
        )
        self.prompt_column = prompt_column
        self.context_column = context_column

    def calculate_distance(
        self, prompt_vector: np.ndarray, context_vectors: List[np.ndarray]
    ) -> np.float64:
        """
        Calculate the distance to be reported in the custom metrics for a single prompt-vector, and an array of
        context-vectors.

        Args:
            prompt_vector: a list of floats representing the prompt vector
            context_vectors: a list of lists of floats representing the `vector` fields of each larger context.

        Returns:
            A single float representing the distance between the prompt vector and the context vectors
        """
        raise NotImplementedError

    def score(
        self,
        scoring_data: pd.DataFrame,
        timestamps: np.ndarray,
        association_ids: np.ndarray,
        **kwargs,
    ) -> List[SingleMetricResult]:
        """This calculates the distance between the prompt vector and the context vectors for each prediction."""
        if self.prompt_column not in scoring_data.columns:
            raise ValueError(
                f"Did not find {self.prompt_column} column in scoring data"
            )
        if self.context_column not in scoring_data.columns:
            raise ValueError(
                f"Did not find {self.context_column} column in scoring data"
            )

        prompts = [json.loads(_) for _ in scoring_data[self.prompt_column].tolist()]
        contexts = [json.loads(_) for _ in scoring_data[self.context_column].tolist()]

        metric_results = []
        for prompt, context, ts, a_id in zip_longest(
            prompts, contexts, timestamps, association_ids
        ):
            if not isinstance(prompt, list) or not isinstance(context, list):
                continue

            prompt_vector = np.array(prompt)
            context_vectors = [np.array(_.get("vector")) for _ in context]

            # this calls into the derived class implementation for the calculation
            value = self.calculate_distance(prompt_vector, context_vectors)
            metric_results.append(
                SingleMetricResult(value=value, timestamp=ts, association_id=a_id)
            )

        return metric_results
