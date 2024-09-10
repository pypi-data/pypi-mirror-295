import pytest
from pydantic import ValidationError
from promptarchitect.specification import ScoreTestSpecification, PreciseLimits


def test_score_test_specification_initialization():
    score_test_spec = ScoreTestSpecification(
        type="score",
        metric="accuracy",
        input={"key1": "value1"},
        limit=PreciseLimits(min=0, max=100),
    )
    assert score_test_spec.type == "score"
    assert score_test_spec.metric == "accuracy"
    assert score_test_spec.input == {"key1": "value1"}
    assert score_test_spec.limit.min == 0
    assert score_test_spec.limit.max == 100


def test_score_test_specification_missing_fields():
    with pytest.raises(ValidationError):
        ScoreTestSpecification(
            type="score",
            metric="accuracy",
            input={"key1": "value1"},
            # Missing limit
        )


def test_score_test_specification_invalid_limits():
    with pytest.raises(ValidationError):
        ScoreTestSpecification(
            type="score",
            metric="accuracy",
            input={"key1": "value1"},
            limit=PreciseLimits(min=100, max=0),
        )


def test_score_test_specification_empty_input():
    score_test_spec = ScoreTestSpecification(
        type="score", metric="accuracy", input={}, limit=PreciseLimits(min=0, max=100),
    )
    assert score_test_spec.input == {}


def test_score_test_specification_invalid_metric():
    with pytest.raises(ValidationError):
        ScoreTestSpecification(
            type="score",
            metric=123,  # Invalid type for metric
            input={"key1": "value1"},
            limit=PreciseLimits(min=0, max=100),
        )
