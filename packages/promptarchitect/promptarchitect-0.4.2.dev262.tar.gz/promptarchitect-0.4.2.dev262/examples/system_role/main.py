from promptarchitect.prompting import EngineeredPrompt

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file="examples/system_role/generate_titles_ollama.prompt",
    output_path="examples/system_role/output_directory",
)

# Download the model in this case gemma2, but you can use any other model
# supported by Ollama (see https://ollama.com/library)
# Only the first time you run the prompt you need to download the model
prompt.completion.download_model("gemma2")
# Execute the prompt
response = prompt.run()

print(response)

print(f"System role file: {prompt.specification.metadata.system_role}")
print(f"System role text: {prompt.specification.metadata.system_role_text}")
