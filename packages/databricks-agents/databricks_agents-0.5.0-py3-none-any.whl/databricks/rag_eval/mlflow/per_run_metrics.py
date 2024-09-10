"""Generate the metrics logged into MLflow."""

import collections
from typing import Dict, List, Mapping, Optional

import numpy as np

from databricks.rag_eval import schemas
from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.judges import builtin_judge
from databricks.rag_eval.utils import rating_utils

_AVERAGE_SUFFIX = "/average"
_PERCENTAGE_SUFFIX = "/percentage"


def generate_per_run_metrics(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Generates per-run MLflow metrics.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of aggregated MLflow metrics
    """

    result = {
        **{
            f"{schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "ground_truth_retrieval_metrics"
            ).items()
        },
        # Per-chunk retrieval assessments
        **{
            f"{schemas.get_retrieval_llm_metric_col_name(metric_name)}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "llm_judged_retrieval_metrics"
            ).items()
        },
        # Per-request answer assessments
        **{
            f"{schemas.get_response_llm_rating_col_name(assessment_name)}{_PERCENTAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_per_request_assessment(
                eval_results, assessment_config.AssessmentType.ANSWER
            ).items()
        },
        # Per-request retrieval assessments
        **{
            f"{schemas.get_retrieval_llm_rating_col_name(assessment_name, is_per_chunk=False)}{_PERCENTAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_per_request_assessment(
                eval_results, assessment_config.AssessmentType.RETRIEVAL_LIST
            ).items()
        },
    }

    # Overall assessment
    overall_assessment_rate = _compute_pass_rate_overall_assessment(eval_results)
    if overall_assessment_rate is not None:
        result[f"{schemas.OVERALL_ASSESSMENT_RATING_COL}{_PERCENTAGE_SUFFIX}"] = (
            overall_assessment_rate
        )

    # Other generation avg metrics
    for metric_name in [
        "total_input_token_count",
        "total_output_token_count",
        "total_token_count",
        "latency_seconds",
    ]:
        metric_value = _compute_avg_for_metric(eval_results, metric_name)
        if metric_value is not None:
            result[f"agent/{metric_name}{_AVERAGE_SUFFIX}"] = metric_value

    # Count error in judges
    for assessment_name, error_count in _count_error_in_judges(eval_results).items():
        result[f"judge/{assessment_name}/error_count"] = error_count

    return result


def _compute_avg_for_metric_group(
    eval_results: List[entities.EvalResult],
    metric_group_name: str,
) -> Dict[str, float]:
    """
    Compute the average a group of metrics across all eval results.
    The metric group is expected to be a Mapping[str, float] in each EvalResult.

    :param eval_results: List of EvalResult objects
    :param metric_group_name: Name of the metric group
    :return: Dictionary of average value for each metric in the group
    """
    metric_value_sums = collections.defaultdict(float)
    metric_value_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        metric_group: Mapping[str, float] = getattr(eval_result, metric_group_name, {})
        for (
            metric_name,
            metric_value,
        ) in metric_group.items():
            metric_name = builtin_judge.translate_to_eval_assessment_name(metric_name)
            metric_value_sums[metric_name] += metric_value
            metric_value_counts[metric_name] += 1
    return {
        metric_name: metric_value_sums[metric_name] / metric_value_counts[metric_name]
        for metric_name in metric_value_sums
        if metric_value_counts[metric_name] > 0
    }


def _compute_avg_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> Optional[float]:
    """
    Compute the average of a metric across all eval results.

    Returns None if the metric is not present in any of the eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Average of the metric
    """
    metric_values = [
        getattr(eval_result, metric_name, None)
        for eval_result in eval_results
        if getattr(eval_result, metric_name, None) is not None
    ]

    return np.average(metric_values) if metric_values else None


def _count_true_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> int:
    """
    Count the number of `True` of a metric across all eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Count of the metric
    """
    return np.count_nonzero(
        [getattr(eval_result, metric_name, None) for eval_result in eval_results]
    )


def _compute_true_rate_per_request_assessment(
    eval_results: List[entities.EvalResult],
    expected_assessment_type: assessment_config.AssessmentType,
) -> Dict[str, float]:
    """
    Compute the rate of `True` in per-request assessment results.

    rate of `True` = count of `True` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :param expected_assessment_type: Type of per-request assessment to compute results for (e.g., answer, retrieval_list)
    :return: Dictionary of rate of `True` for each per-request assessment
    """
    true_counts = collections.defaultdict(int)
    non_null_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:

            # TODO(ML-45046): remove assessment type lookup in harness, rely on service
            # Get the assessment type from the built-in metrics. If the metric is not found, use the provided assessment type.
            try:
                builtin_assessment_config = builtin_judge.get_builtin_assessment_config_with_service_assessment_name(
                    assessment_result.assessment_name
                )
                assessment_type = builtin_assessment_config.assessment_type
            except ValueError:
                assessment_type = assessment_result.assessment_type

            if (
                isinstance(assessment_result, entities.PerRequestAssessmentResult)
                and assessment_type == expected_assessment_type
            ):
                true_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value
                    == entities.CategoricalRating.YES
                )
                non_null_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value is not None
                )

    return {
        assessment_name: true_counts[assessment_name] / non_null_counts[assessment_name]
        for assessment_name in true_counts
        if non_null_counts[assessment_name] > 0
    }


def _compute_pass_rate_overall_assessment(
    eval_results: List[entities.EvalResult],
) -> Optional[float]:
    """
    Compute the rate of `YES` in the overall assessment results.

    rate of `YES` = count of `YES` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :return: Rate of `YES` for the overall assessment, or None if no non-null values
    """
    pass_count = 0
    non_null_counts = 0
    for eval_result in eval_results:
        if (
            eval_result.overall_assessment
            and eval_result.overall_assessment.categorical_value is not None
        ):
            pass_count += (
                eval_result.overall_assessment.categorical_value
                == entities.CategoricalRating.YES
            )
            non_null_counts += 1
    return pass_count / non_null_counts if non_null_counts > 0 else None


def _count_error_in_judges(
    eval_results: List[entities.EvalResult],
) -> Dict[str, int]:
    """
    Count the number of errors in the assessment results.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of count of errors for each assessment
    """
    error_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            if isinstance(assessment_result, entities.PerRequestAssessmentResult):
                if _is_real_error_rating(assessment_result.rating):
                    error_counts[assessment_result.assessment_name] += 1
            elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
                for positional_rating in assessment_result.positional_rating.values():
                    if _is_real_error_rating(positional_rating):
                        error_counts[assessment_result.assessment_name] += 1

    return error_counts


def _is_real_error_rating(rate: entities.Rating) -> bool:
    """Check if the rate is a real error. Missing input error is not considered as a real error."""
    return rate.error_message is not None and not rating_utils.is_missing_input_error(
        rate.error_message
    )
