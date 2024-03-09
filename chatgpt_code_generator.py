from flask import Flask, render_template, request, session, redirect, url_for
import openai
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

def extract_details_from_response(response_text):
    functionality_marker = "Functionality Description:"
    code_marker = "SKiDL Python Code:"
    components_marker = "Components List:"
    try:
        functionality_start = response_text.index(functionality_marker) + len(functionality_marker)
        code_start = response_text.index(code_marker)
        functionality_description = response_text[functionality_start:code_start].strip()

        code_end = response_text.index(components_marker)
        code = response_text[code_start + len(code_marker):code_end].strip()

        components = response_text[code_end + len(components_marker):].strip()

        # Remove Markdown backticks if they exist
        code = code.replace("```python", "").replace("```", "").strip()

        return functionality_description, code, components
    except ValueError as e:
        print("Error extracting details:", e)
        return None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        description = request.form.get('description')
        session['description'] = description  # Store description in session
        openai.api_key = os.getenv("OPENAI_API_KEY")
        enhanced_prompt = f"Based on this description: '{description}', describe the functionality, generate SKiDL Python code, and list all components needed. Use 'Functionality Description:', 'SKiDL Python Code:', and 'Components List:' as markers for each section."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant adept at electronic circuit design with SKiDL. Clearly separate the functionality description, SKiDL code, and components list using the provided markers."},
                {"role": "user", "content": enhanced_prompt}
            ]
        )

        response_text = response.choices[0].message['content']
        functionality_description, code, components = extract_details_from_response(response_text)

        if functionality_description and code and components:
            # Store the results in session for use in the approval step
            session['functionality_description'] = functionality_description
            session['code'] = code
            session['components'] = components
            return redirect(url_for('approve'))
        else:
            return render_template('error.html', message="Failed to extract details.")
    return render_template('index.html')

@app.route('/approve', methods=['GET', 'POST'])
def approve():
    if request.method == 'POST':
        if 'approve' in request.form:
            # User approved the functionality description, proceed to save files
            code_filename = "generated_skidl_code"
            components_filename = "components_list"
            with open(f"{code_filename}.py", 'w') as code_file:
                code_file.write(session.get('code', ''))
            with open(f"{components_filename}.txt", 'w') as components_file:
                components_file.write(session.get('components', ''))
            return render_template('success.html')
        else:
            # User did not approve, redirect to start for resubmission
            return redirect(url_for('index'))

    # Render approval page with functionality description
    functionality_description = session.get('functionality_description', '')
    return render_template('approve.html', functionality_description=functionality_description)

if __name__ == '__main__':
    app.run(debug=True)
