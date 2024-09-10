"""Implementation of test cases for the prompt validation."""

import json
import re

import langdetect
import opentelemetry.trace
from bs4 import BeautifulSoup
from langdetect import DetectorFactory

from promptarchitect.completions import create_completion
from promptarchitect.prompting import EngineeredPrompt
from promptarchitect.specification import (
    FormatTestSpecification,
    LanguageTestSpecification,
    PromptInput,
    PromptOutputFormat,
    PropertyTestSpecification,
    PropertyUnit,
    QuestionTestSpecification,
    ScoreTestSpecification,
    TestSpecificationTypes,
)
from promptarchitect.validation.core import (
    ModelCosts,
    TestCase,
    TestCaseOutcome,
    TestCaseStatus,
)

tracer = opentelemetry.trace.get_tracer(__name__)


class PropertyTestCase(TestCase):
    """Implementation of a test case for a property based test.

    This test case validates that the text exhibits a particular property
    like a number of words, sentences, or lines.

    Attributes
    ----------
    specification: PropertyTestSpecification
        The specification for the property test.

    """

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
        specification: PropertyTestSpecification,
    ) -> None:
        """Initialize the property test case.

        Parameters
        ----------
        test_id: str
            The unique identifier for the test case.
        prompt: EngineeredPrompt
            The engineered prompt to be used in the test case.
        input_sample: PromptInput
            The input sample to be used in the test case.
        specification: PropertyTestSpecification
            The specification for the property test.

        """
        super().__init__(test_id, prompt, input_sample)
        self.specification = specification

    def run(self) -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        with tracer.start_as_current_span("PropertyTestCase.run") as span:
            response = self._run_prompt(self.prompt, self.input_sample)

            items = []

            if self.specification.unit == PropertyUnit.WORDS:
                items = response.split()
            elif self.specification.unit == PropertyUnit.SENTENCES:
                items = re.split(r"[.!?]", response)
            elif self.specification.unit == PropertyUnit.LINES:
                items = response.split("\n")
            elif self.specification.unit == PropertyUnit.PARAGRAPHS:
                items = response.split("\n\n")
            elif self.specification.unit == PropertyUnit.CHARACTERS:
                items = list(response)
            else:
                error_message = f"Unknown unit {self.specification.unit}."
                raise ValueError(error_message)

            # We strip out empty lines, words, sentences, etc.
            # People sometimes have extra characters like line endings in the output of
            # the prompt.

            if self.specification.unit != PropertyUnit.CHARACTERS:
                items = [item for item in items if item.strip()]

            error_message = None

            if self.specification.equals is not None:
                status = (
                    TestCaseStatus.PASSED
                    if len(items) == self.specification.equals
                    else TestCaseStatus.FAILED
                )

                error_message = (
                    (
                        f"Expected {self.specification.equals} "
                        f"{self.specification.unit}, "
                        f"but got {len(items)}."
                    )
                    if status == TestCaseStatus.FAILED
                    else None
                )
            else:
                status = (
                    TestCaseStatus.PASSED
                    if self.specification.limit.between(len(items))
                    else TestCaseStatus.FAILED
                )

                error_message = (
                    (
                        f"Expected between {self.specification.limit.min} and "
                        f"{self.specification.limit.max} {self.specification.unit}, "
                        f"but got {len(items)}."
                    )
                    if status == TestCaseStatus.FAILED
                    else None
                )

            span.set_attribute("test.id", self.test_id)
            span.set_attribute("prompt.filename", self.prompt.specification.filename)
            span.set_attribute("input.sample.filename", self.input_sample.filename)
            span.set_attribute("test.cost", self.prompt.completion.cost)
            span.set_attribute("test.input_tokens", self.prompt.completion.input_tokens)
            span.set_attribute(
                "test.output_tokens",
                self.prompt.completion.output_tokens,
            )

            return TestCaseOutcome(
                test_id=self.test_id,
                prompt_file=self.prompt.specification.filename,
                status=status,
                error_message=error_message,
                duration=0,
                costs=ModelCosts(input_tokens=0, output_tokens=0, costs=0.0),
                input_sample=self.input_sample,
            )


class ScoreTestCase(TestCase):
    """Implementation of a test case for a score based test.

    Attributes
    ----------
    specification: ScoreTestSpecification
        The specification for the score test.

    """

    specification: ScoreTestSpecification

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
        specification: ScoreTestSpecification,
    ) -> None:
        """Initialize the question test case.

        Parameters
        ----------
        test_id: str
            The unique identifier for the test case.
        prompt: EngineeredPrompt
            The engineered prompt to be used in the test case.
        input_sample: PromptInput
            The input sample to be used in the test case.
        specification: QuestionTestSpecification
            The specification for the question test.

        """
        super().__init__(test_id, prompt, input_sample)

        self.specification = specification

    def run(self) -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        with tracer.start_as_current_span("ScoreTestCase.run") as span:
            raise NotImplementedError()

            span.set_attribute("test.id", self.test_id)
            span.set_attribute("prompt.filename", self.prompt.specification.filename)
            span.set_attribute("input.sample.filename", self.input_sample.filename)
            span.set_attribute("test.cost", self.prompt.completion.cost)
            span.set_attribute("test.input_tokens", self.prompt.completion.input_tokens)
            span.set_attribute(
                "test.output_tokens",
                self.prompt.completion.output_tokens,
            )


class QuestionTestCase(TestCase):
    """Implementation of a test case for a question based test.

    Attributes
    ----------
    specification: QuestionTestSpecification
        The specification for the question test

    """

    specification: QuestionTestSpecification

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
        specification: QuestionTestSpecification,
    ) -> None:
        """Initialize the question test case.

        Parameters
        ----------
        test_id: str
            The unique identifier for the test case.
        prompt: EngineeredPrompt
            The engineered prompt to be used in the test case.
        input_sample: PromptInput
            The input sample to be used in the test case.
        specification: QuestionTestSpecification
            The specification for the question test.

        """
        super().__init__(test_id, prompt, input_sample)
        self.specification = specification

    def run(self) -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        with tracer.start_as_current_span("QuestionTestCase.run") as span:
            response = self._run_prompt(self.prompt, self.input_sample)

            # We'll need a second completion object specifically for the question
            # completion. This completion uses the same model as the prompt completion,
            # but has a different system role, prompt, and temperature setting.

            question_completion = create_completion(
                self.prompt.specification.metadata.provider,
                self.prompt.specification.metadata.model,
                self.prompt.specification.metadata,
                (
                    "You're a world-class prompt validator. You're asked a question "
                    "about a prompt. Please answer the question with YES or NO. When "
                    "the answer is NO, please explain why.\n\n"
                ),
            )

            question_completion.parameters["temperature"] = 0.0

            question_response = question_completion.completion(
                f"{self.specification.prompt}\n\n{response}",
            )

            status = (
                TestCaseStatus.PASSED
                if "YES" in question_response
                else TestCaseStatus.FAILED
            )

            error_message = (
                (
                    "The question was not answered with a positive response."
                    f"Got response: {question_response}"
                )
                if status == TestCaseStatus.FAILED
                else None
            )

            span.set_attribute("test.id", self.test_id)
            span.set_attribute("prompt.filename", self.prompt.specification.filename)
            span.set_attribute("input.sample.filename", self.input_sample.filename)
            span.set_attribute("test.cost", self.prompt.completion.cost)
            span.set_attribute("test.input_tokens", self.prompt.completion.input_tokens)
            span.set_attribute(
                "test.output_tokens",
                self.prompt.completion.output_tokens,
            )

            return TestCaseOutcome(
                test_id=self.test_id,
                prompt_file=self.prompt.specification.filename,
                status=status,
                error_message=error_message,
                duration=self.prompt.completion.duration,
                costs=ModelCosts(
                    input_tokens=0,
                    output_tokens=0,
                    costs=self.prompt.completion.cost,
                ),
                input_sample=self.input_sample,
            )


class FormatTestCase(TestCase):
    """Implementation of a test case for a format based test.

    Attributes
    ----------
    specification: FormatTestSpecification
        The specification for the format test.

    """

    specification: FormatTestSpecification

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
        specification: FormatTestSpecification,
    ) -> None:
        """Initialize the format test case.

        Parameters
        ----------
        test_id: str
            The unique identifier for the test case.
        prompt: EngineeredPrompt
            The engineered prompt to be used in the test case.
        input_sample: PromptInput
            The input sample to be used in the test case.
        specification: FormatTestSpecification
            The specification for the format test.

        """
        super().__init__(test_id, prompt, input_sample)
        self.specification = specification

    def run(self) -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        with tracer.start_as_current_span("FormatTestCase.run") as span:
            response = self._run_prompt(self.prompt, self.input_sample)

            if self.specification.format == PromptOutputFormat.HTML:
                status = (
                    TestCaseStatus.PASSED
                    if self._is_valid_html(response)
                    else TestCaseStatus.FAILED
                )

                error_message = (
                    "The output is not valid HTML."
                    if status == TestCaseStatus.FAILED
                    else None
                )
            elif self.specification.format == PromptOutputFormat.JSON:
                status = (
                    TestCaseStatus.PASSED
                    if self._is_valid_json(response)
                    else TestCaseStatus.FAILED
                )

                error_message = (
                    "The output is not valid JSON."
                    if status == TestCaseStatus.FAILED
                    else None
                )
            elif self.specification.format == PromptOutputFormat.MARKDOWN:
                status = (
                    TestCaseStatus.PASSED
                    if self._is_valid_markdown(response)
                    else TestCaseStatus.FAILED
                )

                error_message = (
                    "The output is not valid Markdown."
                    if status == TestCaseStatus.FAILED
                    else None
                )
            else:
                status = TestCaseStatus.PASSED
                error_message = None

            span.set_attribute("test.id", self.test_id)
            span.set_attribute("prompt.filename", self.prompt.specification.filename)
            span.set_attribute("input.sample.filename", self.input_sample.filename)
            span.set_attribute("test.cost", self.prompt.completion.cost)
            span.set_attribute("test.input_tokens", self.prompt.completion.input_tokens)
            span.set_attribute(
                "test.output_tokens",
                self.prompt.completion.output_tokens,
            )

            return TestCaseOutcome(
                test_id=self.test_id,
                prompt_file=self.prompt.specification.filename,
                status=status,
                error_message=error_message,
                duration=0,
                costs=ModelCosts(input_tokens=0, output_tokens=0, costs=0.0),
                input_sample=self.input_sample,
            )

    def _is_valid_html(self, data: str) -> bool:
        soup = BeautifulSoup(data, "html.parser")
        return data.startswith("<") and bool(soup.find())

    def _is_valid_json(self, data: str) -> bool:
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    def _is_valid_markdown(self, _data: str) -> bool:
        # Everything that's HTML or plain-text is also valid markdown.
        # If this ever changes, we'll add a proper check here.
        return True


class LanguageTestCase(TestCase):
    """Implementation of a test case for a language based test."""

    specification: LanguageTestSpecification

    def __init__(
        self,
        test_id: str,
        prompt: EngineeredPrompt,
        input_sample: PromptInput,
        specification: LanguageTestSpecification,
    ) -> None:
        """
        Initialize the test case.

        Parameters
        ----------
        test_id : str
            The unique identifier for the test case.
        prompt : EngineeredPrompt
            The engineered prompt to be used in the test case.
        input_sample : PromptInput
            The input sample to be used in the test case.
        specification : LanguageTestSpecification
            The specification for the language test.

        """
        super().__init__(test_id, prompt, input_sample)
        self.specification = specification

    def run(self) -> TestCaseOutcome:
        """Run the test case.

        Returns
        -------
        TestCaseOutcome
            The outcome of the test case.

        """
        with tracer.start_as_current_span("LanguageTestCase.run") as span:
            response = self._run_prompt(self.prompt, self.input_sample)

            # Language detection algorithm is non-deterministic, which means that if you
            # try to run it on a text which is either too short or too ambiguous, you
            # might get different results everytime you run it.

            # To enforce consistent results, call following code before the first
            # language detection:
            DetectorFactory.seed = 0

            # We'll use the langdetect library to detect the language of the response.
            # But not the complete response, because that could be too long.
            # We'll just use the first 100 characters.
            language_response = langdetect.detect(response[:100])

            status = (
                TestCaseStatus.PASSED
                if self.specification.lang_code in language_response
                else TestCaseStatus.FAILED
            )

            error_message = (
                f"The language of the prompt output does not match the specified "
                f"language. Got response: {language_response}"
                if status == TestCaseStatus.FAILED
                else None
            )

            span.set_attribute("test.id", self.test_id)
            span.set_attribute("prompt.filename", self.prompt.specification.filename)
            span.set_attribute("input.sample.filename", self.input_sample.filename)
            span.set_attribute("test.cost", self.prompt.completion.cost)
            span.set_attribute("test.input_tokens", self.prompt.completion.input_tokens)
            span.set_attribute(
                "test.output_tokens",
                self.prompt.completion.output_tokens,
            )

            return TestCaseOutcome(
                test_id=self.test_id,
                input_sample=self.input_sample,
                prompt_file=self.prompt.specification.filename,
                status=status,
                error_message=error_message,
                duration=self.prompt.completion.duration,
                costs=ModelCosts(
                    input_tokens=0,
                    output_tokens=0,
                    costs=self.prompt.completion.cost,
                ),
            )


def create_test_case(
    test_id: str,
    prompt: EngineeredPrompt,
    spec: TestSpecificationTypes,
    input_sample: PromptInput,
) -> TestCase:
    """Create a test case based on the provided specification type.

    Parameters
    ----------
    test_id : str
        The identifier for the test case in the specification.
    prompt: EngineeredPrompt
        The engineered prompt to be used in the test case.
    spec: TestSpecificationTypes
        The specification type for the test case.
    input_sample: PromptInput
        The input sample to be used in the test case.

    Returns
    -------
    TestCase
        An instance of a test case based on the specification type.

    """
    if isinstance(spec, QuestionTestSpecification):
        return QuestionTestCase(test_id, prompt, input_sample, spec)
    if isinstance(spec, ScoreTestSpecification):
        return ScoreTestCase(test_id, prompt, input_sample, spec)
    if isinstance(spec, FormatTestSpecification):
        return FormatTestCase(test_id, prompt, input_sample, spec)
    if isinstance(spec, LanguageTestSpecification):
        return LanguageTestCase(test_id, prompt, input_sample, spec)
    if isinstance(spec, PropertyTestSpecification):
        return PropertyTestCase(test_id, prompt, input_sample, spec)

    error_message = "Unknown test specification type."
    raise ValueError(error_message)
