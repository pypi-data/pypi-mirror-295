"""Log the evaluation results to MLflow using the MLflow evaluation logging API."""

import time
from typing import List, Optional

from mlflow import evaluation as mlflow_eval
from mlflow.entities import metric as mlflow_metric

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities

_CHUNK_INDEX_KEY = "chunk_index"
_IS_OVERALL_ASSESSMENT_KEY = "is_overall_assessment"


def log_eval_results(
    eval_results: List[entities.EvalResult],
) -> List[mlflow_eval.Evaluation]:
    """
    Log the evaluation results to MLflow using the MLflow evaluation logging API.

    :param eval_results: List of EvalResult objects
    :return: List of logged MLflow Evaluation objects
    """
    return mlflow_eval.log_evaluations(
        evaluations=[
            _eval_result_to_mlflow_evaluation(eval_result)
            for eval_result in eval_results
        ],
    )


def _eval_result_to_mlflow_evaluation(
    eval_result: entities.EvalResult,
) -> mlflow_eval.Evaluation:
    """
    Convert an EvalResult object to an MLflow Evaluation object.

    :param eval_result: EvalResult object
    :return: MLflow Evaluation object
    """
    eval_item = eval_result.eval_item
    # Inputs
    inputs = {
        schemas.REQUEST_COL: eval_item.question,
    }
    # Outputs
    outputs = {}
    if eval_item.retrieval_context:
        outputs[schemas.RETRIEVED_CONTEXT_COL] = (
            eval_item.retrieval_context.to_output_dict()
        )
    if eval_item.answer:
        outputs[schemas.RESPONSE_COL] = eval_item.answer
    # Targets
    targets = {}
    if eval_item.ground_truth_answer:
        targets[schemas.EXPECTED_RESPONSE_COL] = eval_item.ground_truth_answer
    if eval_item.ground_truth_retrieval_context:
        targets[schemas.EXPECTED_RETRIEVED_CONTEXT_COL] = (
            eval_item.ground_truth_retrieval_context.to_output_dict()
        )
    if eval_item.grading_notes:
        targets[schemas.GRADING_NOTES_COL] = eval_item.grading_notes
    # Assessments
    assessments = []
    for assessment_result in eval_result.assessment_results:
        assessments.extend(_assessment_result_to_mlflow_assessments(assessment_result))
    # Overall assessment
    overall_assessment = _get_overall_assessment(eval_result)
    if overall_assessment:
        assessments.append(overall_assessment)
    # Metrics
    metrics = _eval_result_to_mlflow_metrics(eval_result)

    evaluation = mlflow_eval.Evaluation(
        inputs=inputs,
        outputs=outputs,
        inputs_id=eval_item.question_id,
        request_id=eval_item.trace.info.request_id if eval_item.trace else None,
        targets=targets,
        assessments=assessments,
        metrics=metrics,
    )

    return evaluation


def _eval_result_to_mlflow_metrics(
    eval_result: entities.EvalResult,
) -> List[mlflow_metric.Metric]:
    """Get a list of MLflow Metric objects from an EvalResult object."""
    return [
        _construct_mlflow_metrics(
            key=k,
            value=v,
        )
        for k, v in eval_result.get_metrics_dict().items()
        # TODO: add ground_truth_document_ratings once mlflow supports chunk-level metrics
        if k != schemas.GROUND_TRUTH_DOCUMENT_RATING_COL
    ]


def _construct_mlflow_metrics(key: str, value: float) -> mlflow_metric.Metric:
    """
    Construct an MLflow Metric object from key and value.
    Timestamp is the current time and step is 0.
    """
    return mlflow_metric.Metric(
        key=key,
        value=value,
        timestamp=int(time.time() * 1000),
        step=0,
    )


def _assessment_result_to_mlflow_assessments(
    assessment_result: entities.AssessmentResult,
) -> List[mlflow_eval.Assessment]:
    """
    Convert an AssessmentResult object to a list of MLflow Assessment object.

    A single PerChunkAssessmentResult object can be converted to multiple MLflow Assessment objects.

    :param assessment_result: AssessmentResult object
    :return: MLflow Assessment object
    """
    if isinstance(assessment_result, entities.PerRequestAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=assessment_result.rating.categorical_value,
                rationale=assessment_result.rating.rationale,
                error_message=assessment_result.rating.error_message,
                error_code=assessment_result.rating.error_code,
            )
        ]
    elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=rating.categorical_value,
                rationale=rating.rationale,
                error_message=rating.error_message,
                error_code=rating.error_code,
                metadata={_CHUNK_INDEX_KEY: index},
            )
            for index, rating in assessment_result.positional_rating.items()
        ]
    else:
        raise ValueError(
            f"Unsupported assessment result type: {type(assessment_result)}"
        )


def _convert_to_ai_judge_assessment_source(
    assessment_source: entities.AssessmentSource,
) -> mlflow_eval.AssessmentSource:
    """
    Convert an AssessmentSource object to a MLflow AssessmentSource object.
    Source type is always AI_JUDGE.
    """
    return mlflow_eval.AssessmentSource(
        source_type=mlflow_eval.AssessmentSourceType.AI_JUDGE,
        source_id=assessment_source.source_id,
    )


def _get_overall_assessment(
    eval_result: entities.EvalResult,
) -> Optional[mlflow_eval.Assessment]:
    """
    Get optional overall assessment from a EvalResult object.

    :param eval_result: A EvalResult object
    :return: Optional overall assessment
    """
    return (
        mlflow_eval.Assessment(
            name=schemas.OVERALL_ASSESSMENT,
            source=_convert_to_ai_judge_assessment_source(
                entities.AssessmentSource.builtin()
            ),
            value=eval_result.overall_assessment.categorical_value,
            rationale=eval_result.overall_assessment.rationale,
            metadata={_IS_OVERALL_ASSESSMENT_KEY: True},
        )
        if eval_result.overall_assessment
        else None
    )
