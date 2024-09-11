# PromptArchitect

## About Engineered Prompts PromptArchitect

### Engineered Prompts: Structured Inputs for Automated Processes

In the rapidly evolving landscape of artificial intelligence, the concept of an "engineered prompt" is gaining prominence, particularly in environments that leverage large language models (LLMs) and other AI systems. Engineered prompts are meticulously crafted inputs designed to interact with AI models in a way that ensures consistent and reliable outputs. These prompts are not just queries but structured tools that are integral to the automated processes in which they function.

## Definition and Purpose

An engineered prompt is a carefully designed input that is used to generate a specific type of response from an AI model. Unlike casual or ad-hoc prompts, engineered prompts are developed through a rigorous process that considers the nuances of the model’s language understanding and output capabilities. They are akin to code in software development, serving as a fundamental component that interacts with the AI to execute specific tasks reliably.

## Characteristics of Engineered Prompts

- **Precision and Clarity**: Engineered prompts are precise, unambiguous, and tailored to elicit a specific type of response or behavior from an AI model.
- **Reusability**: These prompts are designed to be reusable across similar tasks or models, ensuring efficiency and consistency in automated processes.
- **Scalability**: Engineered prompts can be scaled or modified according to different requirements or in response to changes in the AI model’s behavior.

## Development and Maintenance

Just like any software code, engineered prompts require a structured development and maintenance process to ensure they remain effective and safe for use:

- **Versioning**: Keeping track of different versions of prompts is crucial, especially as models and requirements evolve. Versioning allows developers to manage changes systematically, revert to previous versions if needed, and understand the evolution of prompt effectiveness over time.
- **Documentation**: Comprehensive documentation is essential for engineered prompts. It should detail the design rationale, expected outputs, model compatibility, and any dependencies. This documentation is vital for both current use and future modifications.
- **Testing and Validation**: Rigorous testing is a cornerstone of prompt development. This includes unit testing to verify prompt functionality, integration testing to ensure compatibility with the AI model, and validation testing to confirm that the prompt generates the expected outputs.
- **Performance Tests**: Performance testing evaluates how well the prompt works in terms of speed and resource utilization, ensuring that the prompt is efficient even at scale.
- **Regression Testing**: This is particularly critical when the underlying AI model is updated or when switching to a model from a different provider. Regression tests help verify that updates or changes do not negatively affect the performance of the prompt.

## Use Cases

Engineered prompts are used in diverse fields such as customer service, content generation, automated programming help, and more. In each case, the prompt acts as a bridge between the user’s needs and the model’s capabilities, facilitating a controlled and predictable AI interaction.

## New Feature: Default Model Configuration

PromptArchitect now supports specifying a default model per provider. This ensures that when no model is specified in a prompt file, the default model for the provider is used.

### Configuration

Update your provider configuration files to include a `default_model` key. Below is an example of a provider configuration file:

```json
{
    "gpt-3.5-turbo-instruct": {
        "input_tokens": 0.0000015,
        "output_tokens": 0.000002
    },
    "gpt-4o-mini": {
        "input_tokens": 0.00000015,
        "output_tokens": 0.0000006
    },
    "gpt-4o": {
        "input_tokens": 0.00005,
        "output_tokens": 0.000015
    },
    "default_model": "gpt-4o"
}
```

## More Information

- [Testing Language Models (and Prompts) Like We Test Software](https://towardsdatascience.com/testing-large-language-models-like-we-test-software-92745d28a359)
- [Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://homes.cs.washington.edu/~marcotcr/acl20_checklist.pdf)

## Installation

Use the following command to install PromptArchitect:

```bash
pip install promptarchitect
```

## Usage

Below is an example of how to use the EngineeredPrompt class from the PromptArchitect module:

```python
from promptarchitect import EngineeredPrompt

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(prompt_file_path='path_to_prompt_file.prompt', output_path='output_directory')

# Execute the prompt
response = prompt.execute(input_file='path_to_input_file.txt')
print(response)
```

## Examples

We have added a set of examples to help you get started with Engineered Prompts. You can find these examples in the `examples` folder. These include:

- **Quick start**: See how to setup an Engineered Prompt for different providers and models.
- **Defining test cases**: Define semantic and format tests
- **System role**: Use a custom system role with the prompts
- **Configuring models**
- **Custom meta model options**: If you want to add control flow data to your Engineered Prompt
**- Retrieving cost and duration**: How to get the cost and duration per executed prompt.
- **Chaining prompts**: Using the output of a prompt as input for other prompts. It also shows how to iterate over a list of prompt files.
- **Using templates in combination with prompts**: You can add template string to a prompt file and how to substitute this with Engineered Prompt.
- **Automatic Caching with Expiration**: Learn how to use caching to optimize performance and manage execution costs.

## Support for Ollama Models

PromptArchitect  supports the use of open-source models running locally via [Ollama](https://ollama.ai). This feature allows you to leverage powerful, locally hosted models such as Gemma2, Llama3.1, and Mistral, giving you greater control and flexibility over your AI model deployments.

### Supported Models

- **Gemma2**: A robust and versatile model ideal for various natural language processing tasks.
- **Llama3.1**: An advanced model offering cutting-edge performance in language understanding and generation.
- **Mistral**: A lightweight, efficient model designed for quick responses and lower resource usage.

### Requirements

Install [Ollama](https://ollama.ai) for your operation system. Before using a model, make sure to download it first.

```python
from promptarchitect import EngineeredPrompt
prompt.completion.download_model("gemma2")
```

### Ollama Configuration

To use these models, update your configuration file to include Ollama as the provider, specifying the model you wish to use. Below is an example configuration:

```json
{
    "ollama": {
        "gemma2": {
            "input_tokens": 0.0,
            "output_tokens": 0.0
        },
        "llama3.1": {
            "input_tokens": 0.0,
            "output_tokens": 0.000004,
            "default": true
        },
    }
}
```

### Ollama Usage

Here's how you can use the `.prompt` file with Ollama models:

```yaml
---
provider: ollama
model: gemma2
prompt_version: 1.0
temperature: 0.2
input: examples/inputs/podcast_titels/beschrijving.txt
output: title-ollama.txt
test_path: examples/tests/podcast_titels
---
# Instructions
Generate 5 titles for a podcast
```

### Benefits of Using Ollama Models

- **Local Control**: Run models locally on your own hardware, ensuring data privacy and reducing dependency on cloud services.
- **Cost Efficiency**: Avoid cloud computing costs by using local resources.
- **Flexibility**: Easily switch between different models like Gemma2, Llama3.1, and Mistral to suit your specific needs.

## Language Detection Test Type

### Overview

The `language` test type allows you to validate the output of an engineered prompt against specific language rules and standards. This is particularly useful when your prompts must generate content that conforms to the linguistic and grammatical norms of a specific language.

### Configuration

To use the `language` test type, add it to the `tests` section in your prompt file's front matter. You must specify the language using the `lang_code` property, which accepts any of the 55 ISO 639-1 language codes. The system will validate that the generated content adheres to the rules and norms of the specified language.

### Example

Below is an example of how to configure a `language` test in your prompt file:

```markdown
---
provider: openai
model: gpt-4o-mini
test_path: ./tests
parameters:
    temperature: 0.7
    max_tokens: 2500
tests:
    test_01: 
        type: language
        lang_code: en
---

Write a poem about prompt engineering using the following input:

{{input}}
```

In this example:

- `type: language`: Specifies that the test type is for language validation.
- `lang_code: en`: Specifies that the output should conform to English language standards.

### Supported Languages

The `lang_code` property supports 55 languages as defined by the ISO 639-1 standard. Below are a few examples of the supported language codes:

- `en` - English
- `nl` - Dutch
- `fr` - French
- `es` - Spanish
- `de` - German

For a full list of supported languages and their corresponding codes, please refer to the [ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

### Error Handling

If you specify a `lang_code` that is not supported or is incorrectly formatted, the system will return an error, notifying you of the invalid code. Ensure that you use a valid ISO 639-1 language code to avoid these errors.

### Notes

- The `language` test type is designed to ensure that your prompts produce outputs that are linguistically accurate for the specified language.
- This test type can be combined with other test types (e.g., `question`, `score`) to create comprehensive validation strategies for your prompts.

## New Feature: Dashboard themes

We’ve added a new dashboard theme called github-pajamas-theme, inspired by the GitHub Pajamas Design System. This theme serves as an example of how you can create and customize your own themes for the PromptArchitect dashboard, allowing for a more personalized and branded user experience.

### Custom Theme Creation

Creating your own theme is simple. Start by duplicating the github-pajamas-theme files and modifying the styles to match your brand guidelines. This flexibility allows you to fully integrate the PromptArchitect dashboard into your existing design systems

## Command Line Interface (CLI) Usage

PromptArchitect can also be run directly from the command line, providing flexibility in how you use and integrate it into your workflows. The CLI allows you to specify the path for the dashboard templates of your choice.

### Basic CLI Commands

Here’s how you can use PromptArchitect from the CLI:

```bash
promptarchitect --prompts [PATH_TO_PROMPTS] --completions [PATH_TO_COMPLETIONS] --templates [PATH_TO_TEMPLATES] --report [PATH_TO_REPORTS]
```

### Example

```bash
promptarchitect --prompts examples/prompts --completions examples/completions --templates custom_theme --report custom_report
```

This command runs PromptArchitect using specific paths for prompts, completions, templates, and the report output.

To see all available options, run:

```bash
promptarchitect --help
```

This will display the full list of commands and options available for customizing how PromptArchitect operates.

## CLI Usage

Below is an example of how to use the EngineeredPrompt class from the PromptArchitect module:

```python
from promptarchitect import EngineeredPrompt

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(prompt_file_path='path_to_prompt_file.prompt', output_path='output_directory')

# Execute the prompt
response = prompt.execute(input_file='path_to_input_file.txt')
print(response)
```

## Feature: Template String Substitution

PromptArchitect  includes a powerful feature in the `PromptFile` class that allows for dynamic template string substitution within prompt files. This feature enables you to define placeholders in your prompt templates and substitute them with specific values at runtime, making your prompts more flexible and reusable.

### Example Usage

See the examples: `examples/template_strings_in_prompt`

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

We welcome contributions! Please see the CONTRIBUTING.md for more details.

## Contact

For any questions or issues, please open an issue on this GitHub repository or contact the maintainers.
