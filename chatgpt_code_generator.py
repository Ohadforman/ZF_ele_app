
import openai

# Replace "your_api_key_here" with your actual OpenAI API key
openai.api_key = 'your_api_key_here'

def get_python_code_from_chatgpt(prompt):
    # Adding a clarification to the prompt to return only Python code
    full_prompt = f"{prompt}\n\n### Please provide the Python code below:\n"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=full_prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["###"]  # Using a stop sequence to limit the response
    )
    code = response.choices[0].text.strip()
    return code

if __name__ == "__main__":
    user_prompt = input("Enter your prompt for Python code: ")
    python_code = get_python_code_from_chatgpt(user_prompt)
    print("Generated Python Code:\n", python_code)
