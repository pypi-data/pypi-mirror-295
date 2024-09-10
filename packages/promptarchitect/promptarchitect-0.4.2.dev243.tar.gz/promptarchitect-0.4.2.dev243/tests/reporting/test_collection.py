
from promptarchitect.reporting.core import TestReporter
from promptarchitect.specification import PromptInput
from promptarchitect.validation.testcases import (
    ModelCosts,
    TestCaseOutcome,
    TestCaseStatus,
)


def test_collect_results_no_prompts_no_tests():
    prompt_specs = []
    test_outcomes = []

    report = TestReporter._collect_results(prompt_specs, test_outcomes)

    assert report.tests_failed == 0
    assert report.tests_passed == 0
    assert report.total_duration == 0.0
    assert report.total_costs == 0.0
    assert len(report.files) == 0


def test_collect_results(prompt_specification_with_multiple_tests):
    test_outcome_1 = TestCaseOutcome(
        test_id="test01",
        prompt_file=prompt_specification_with_multiple_tests.filename,
        status=TestCaseStatus.PASSED,
        duration=0.1,
        error_message=None,
        costs=ModelCosts(costs=0.5, input_tokens=100, output_tokens=100),
        input_sample=PromptInput(id="input-1", input="Sample input"),
    )

    test_outcome_2 = TestCaseOutcome(
        test_id="test02",
        prompt_file=prompt_specification_with_multiple_tests.filename,
        status=TestCaseStatus.PASSED,
        duration=0.1,
        error_message=None,
        costs=ModelCosts(costs=0.5, input_tokens=100, output_tokens=100),
        input_sample=PromptInput(id="input-1", input="Sample input"),
    )

    report = TestReporter._collect_results(
        [prompt_specification_with_multiple_tests], [test_outcome_1, test_outcome_2],
    )

    assert report.tests_failed == 0
    assert report.tests_passed == 2
    assert report.total_duration == 0.2
    assert report.total_costs == 1.0
    assert len(report.files) == 1
    assert report.files[0].tests_passed == 2
    assert report.files[0].tests_failed == 0
    assert len(report.files[0].tests) == 2
