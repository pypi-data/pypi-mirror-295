import pytest
from promptarchitect.specification import MetricTestSpecification, PreciseLimits
from pydantic import ValidationError


def test_metric_test_specification_initialization():
    score_test_spec = MetricTestSpecification(
        type="metric",
        metric="accuracy",
        input={"key1": "value1"},
        limit=PreciseLimits(min=0, max=100),
    )
    assert score_test_spec.type == "metric"
    assert score_test_spec.metric == "accuracy"
    assert score_test_spec.input == {"key1": "value1"}
    assert score_test_spec.limit.min == 0
    assert score_test_spec.limit.max == 100


def test_metric_test_specification_missing_fields():
    with pytest.raises(ValidationError):
        MetricTestSpecification(
            type="metric",
            metric="accuracy",
            input={"key1": "value1"},
            # Missing limit
        )


def test_metric_test_specification_invalid_limits():
    with pytest.raises(ValidationError):
        MetricTestSpecification(
            type="metric",
            metric="accuracy",
            input={"key1": "value1"},
            limit=PreciseLimits(min=100, max=0),
        )


def test_metric_test_specification_empty_input():
    score_test_spec = MetricTestSpecification(
        type="metric",
        metric="accuracy",
        input={},
        limit=PreciseLimits(min=0, max=100),
    )
    assert score_test_spec.input == {}


def test_metric_test_specification_invalid_metric():
    with pytest.raises(ValidationError):
        MetricTestSpecification(
            type="metric",
            metric=123,  # Invalid type for metric
            input={"key1": "value1"},
            limit=PreciseLimits(min=0, max=100),
        )
