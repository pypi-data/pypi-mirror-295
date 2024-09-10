"""Core types used in the validation module."""

from abc import ABC, abstractmethod
from enum import Enum
from functools import cache
from os import PathLike
from typing import Literal, Optional

from pydantic import BaseModel

from promptarchitect.prompting import EngineeredPrompt
from promptarchitect.specification import PromptInput


class SessionConfiguration(BaseModel):
    """Configures the test session.

    Attributes
    ----------
    prompt_path: PathLike
        The path to the directory containing the prompts.
    output_path: PathLike
        The path to the directory where the generated prompts will be saved.
    template_path: PathLike
        The path to the directory containing the templates for the test report.
    report_path: PathLike
        The path to the directory where the test report will be saved.
    report_format: Literal["html", "json"]
        The format of the test report
    report_theme: str
        The theme to use for the test report.

    """

    prompt_path: PathLike
    output_path: PathLike
    template_path: PathLike | None = None
    report_path: PathLike
    report_format: Literal["html", "json"]
    report_theme: str


class ModelCosts(BaseModel):
    """Model to represent the costs of a model.

    Attributes
    ----------
    input_tokens: int
        The number of tokens in the input.
    output_tokens: int
        The number of tokens in the output.
    costs: float
        The costs of the model in dollars.

    """

    input_tokens: int
    output_tokens: int
    costs: float


class TestCaseStatus(str, Enum):
    """Enum to represent the various states of a test case."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


class TestCaseOutcome(BaseModel):
    """Models the outcome of a test case.

    Attributes
    ----------
    status: TestCaseStatus
        The status of the test case.
    error_message: Optional[str]
        The error message if the test case failed or errored.
    duration: int
        The duration of the test case in milliseconds.

    """

    test_id: str
    prompt_file: str
    status: TestCaseStatus
    error_message: Optional[str] = None
    duration: float
    costs: ModelCosts
    input_sample: PromptInput


class TestCase(ABC):
    """Represents a test case.

    A test case is a concrete implementation of a test specification for a single prompt
    and input sample combination. When you have a single prompt file, with 2 input
    samples, and 2 tests, you'll have a total of 4 test cases for the prompt file.

    Attributes
    ----------
    test_id: str
        The unique identifier for the test case.
    prompt: EngineeredPrompt
        The engineered prompt that the test case is for.

    """

    test_id: str
    prompt: EngineeredPrompt
    input_sample: PromptInput

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
    ) -> None:
        self.test_id = test_id
        self.prompt = prompt
        self.input_sample = input_sample

    @abstractmethod
    def run() -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        raise NotImplementedError()

    @cache  # noqa: B019
    def _run_prompt(self, prompt: EngineeredPrompt, input_sample: PromptInput) -> str:
        return prompt.run(
            input_text=input_sample.input,
            properties=input_sample.properties,
        )
