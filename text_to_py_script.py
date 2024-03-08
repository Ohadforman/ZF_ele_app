
# This Python script takes text input and saves it as a Python (.py) file.

def save_text_as_py_file(text, file_name):
    # Construct the full file path
    file_path = file_name + '.py'
    # Write the text to a file
    with open(file_path, 'w') as file:
        file.write(text)
    print(f"File saved as {file_path}")

# Example usage
if __name__ == "__main__":
    text_input = """# Example Python code
print("Hello, Python!")"""
    save_text_as_py_file(text_input, "example_script")
