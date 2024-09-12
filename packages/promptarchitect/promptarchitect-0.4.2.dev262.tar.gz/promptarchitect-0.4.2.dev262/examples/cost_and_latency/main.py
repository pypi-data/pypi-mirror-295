from pathlib import Path

from src.promptarchitect.prompting import EngineeredPrompt
from src.promptarchitect.specification import (
    EngineeredPromptSpecification,
)

# Create the output directory if it does not exist
output_directory = Path("output_directory")
output_directory.mkdir(exist_ok=True)

# Define the path to the prompt and input file
prompt_path = Path("examples/cost_and_latency/prompts/generate_titles_claude.prompt")
input_file_path = Path("examples/cost_and_latency/input/podcast_description.txt")


# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    specification=EngineeredPromptSpecification.from_file(str(prompt_path))
)

# Execute the prompt
response = prompt.run(input_file=input_file_path)

print(response)

# Show the cost and duration for this prompt execution
print(f"Cost: {prompt.completion.cost:.6f}")  # Cost is in USD per million tokens
print(f"Latency: {prompt.completion.duration:.2f}s")  # Latency is in seconds
