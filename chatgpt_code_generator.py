import openai
import os

def extract_details_from_response(response_text):
    """Extracts functionality description, SKiDL code, and components list from the response using unique markers."""
    # Markers for each section
    functionality_marker = "Functionality Description:"
    code_marker = "SKiDL Python Code:"
    components_marker = "Components List:"

    try:
        # Extract functionality description
        functionality_start = response_text.index(functionality_marker) + len(functionality_marker)
        code_start = response_text.index(code_marker)
        functionality_description = response_text[functionality_start:code_start].strip()

        # Extract SKiDL code
        code_end = response_text.index(components_marker)
        code = response_text[code_start + len(code_marker):code_end].strip()

        # Extract components list
        components = response_text[code_end + len(components_marker):].strip()

        return functionality_description, code, components
    except ValueError:
        return None, None, None

def generate_circuit_from_description(description, code_filename, components_filename):
    # Ensure your OPENAI_API_KEY environment variable is set
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Send the description to the ChatGPT API with specific instructions for formatting the response
    enhanced_prompt = f"Based on this description: '{description}', describe the functionality, generate SKiDL Python code, and list all components needed. Use 'Functionality Description:', 'SKiDL Python Code:', and 'Components List:' as markers for each section."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant adept at electronic circuit design with SKiDL. Clearly separate the functionality description, SKiDL code, and components list using the provided markers."},
            {"role": "user", "content": enhanced_prompt}
        ]
    )

    # Extract the response text
    response_text = response.choices[0].message['content']
    
    # Extract the functionality description, SKiDL code, and components list from the response
    functionality_description, code, components = extract_details_from_response(response_text)

    if functionality_description and code and components:
        print(f"\nFunctionality Understood:\n{functionality_description}\n")
        
        # Ask for user's approval to proceed
        approval = input("Do you approve this functionality description? (yes/no): ").lower()
        if approval != "yes":
            print("Operation cancelled by the user.")
            return

        # Proceed with saving the files after approval
        code = code.replace("```python", "").replace("```", "").strip()
        with open(f"{code_filename}.py", 'w') as file:
            file.write(code)
        with open(f"{components_filename}.txt", 'w') as file:
            file.write(components)
        
        print(f"SKiDL circuit design saved to: {code_filename}.py")
        print(f"Components list saved to: {components_filename}.txt")
    else:
        print("The response did not include a valid functionality description, circuit design, or components list.")

if __name__ == "__main__":
    # Prompt for user input
    description = input("Enter the description of the circuit/gadget functionality: ")
    code_filename = input("Enter the desired name for your Python file (without .py extension): ")
    components_filename = input("Enter the desired name for your components list file (without .txt extension): ")
    
    # Generate the circuit design and components list
    generate_circuit_from_description(description, code_filename, components_filename)
