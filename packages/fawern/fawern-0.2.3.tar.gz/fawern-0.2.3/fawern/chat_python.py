import os
import subprocess
from groq import Groq
from dotenv import load_dotenv

from .base_assistant import BaseAssistant
from .save_to_md import save_generated_data_to_md

def get_code_from_input(input_data):
    """
    Checks if the input is a file path or Python code. 
    If it's a file path, reads the content of the file. 
    Otherwise, assumes it's Python code and returns it directly.

    Args:
        input_data (str): Either a file path or Python code.

    Returns:
        str: The Python code from the file or the input directly.
    """
    if os.path.isfile(input_data):
        try:
            with open(input_data, 'r') as file:
                code = file.read()
                return code
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    else:
        return input_data

class CodeFileNameGenerator(BaseAssistant):
    """
    CodeFileNameGenerator is a utility class for generating meaningful file names based on Python code content.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=50, top_p=1):
        """
        Initializes the CodeFileNameGenerator class with model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)

    def generate_file_name(self, code):
        """
        Generates a meaningful file name based on the provided Python code.

        Args:
            code (str): The Python code from which to generate a file name.

        Returns:
            str: A file name that reflects the primary functionality of the code.
        """
        code = get_code_from_input(code)

        prompt =  f"Based on the provided Python code description, generate a simple and contextually appropriate file name as a string. The file name should reflect the main purpose of the code in a straightforward manner, without any file extensions. Here is the input: {code}"

        file_name = self._get_completion(prompt)
        file_name = file_name.strip().split("\n")[0].strip().replace(" ", "_").replace('"', '').replace("'", '')

        return file_name


class ChatPython(BaseAssistant):
    """
    ChatPython is an AI Python developer that generates Python code based on a given input prompt.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=1, max_tokens=1000, top_p=1):
        """
        Initializes the ChatPython class with model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)
        self.generated_code = ''
        self.prompt = ''
        self.file_name = ''
        self.root_directory = os.getcwd()

    def generate_code(self, prompt, write_code_to_file=True, run_code=True):
        """
        Generates Python code based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating Python code.
            run_code (bool): Whether to run the generated code.
        """

        if not write_code_to_file:
            run_code = False
            
        self.prompt = f"Please generate Python code that is concise, functional, and directly implements the following requirements in English: {prompt}. Exclude any explanations, comments, or extra text. The code should adhere to Python best practices, ensure readability, and be ready for execution."
        self.generated_code = self._get_completion(self.prompt)
        self.generated_code = self._remove_python_prefix(self.generated_code)

        if run_code:
            self._write_code_to_file()
            self._run_generated_code()
        return self.generated_code

    def _remove_python_prefix(self, code):
        """
        Removes the 'python' prefix from the generated code if it exists.
        """
        prefix = "python"
        code = code.replace("`", '')
        lines = code.splitlines()
        try:
            if lines[0].strip().startswith(prefix):
                lines[0] = lines[0].strip()[len(prefix):].strip()
                return "\n".join(lines)
            else:
                return code
        except Exception as e:
            raise Exception(f"Try again, {e}")

    def _generate_file_name(self):
        """
        Generates a meaningful and contextually appropriate file name based on the code description.
        """
        prompt_for_file_name = f"Based on the provided Python code description, generate a meaningful and contextually appropriate file name that ends with '.py'. The file name should reflect the primary functionality of the code. Here is the input: {self.prompt}"
        generated_file_name = self._get_completion(prompt_for_file_name)
        generated_file_name = generated_file_name.strip().split("\n")[0].strip().replace("`", "").replace('"', '')
        return generated_file_name

    def _write_code_to_file(self):
        """
        Writes the generated code to a file with the generated file name in the current working directory.
        """
        path = ""
        self.file_name = self._generate_file_name()
        try:
            full_path = os.path.join(self.root_directory, path)
            os.makedirs(full_path, exist_ok=True)
            saved_path = os.path.join(full_path, self.file_name)
            print(f"Writing code to {saved_path}")
        except Exception as e:
            raise Exception(f"Cannot create directory: {e}, Please try again or give a valid path")

        if self.generated_code:
            with open(saved_path, "w") as file:
                file.write(self.generated_code)
            print(f"Code written to {self.file_name}")
        else:
            raise Exception("No code generated yet")

    def _run_generated_code(self):
        """
        Executes the generated Python code in a subprocess.
        """
        try:
            result = subprocess.run(["python", self.file_name], capture_output=True, text=True, cwd=self.root_directory)
            return result.stdout
        except Exception as e:
            raise Exception(f"Cannot run code: {e}")

class CodeAnalyzer(BaseAssistant):
    """
    CodeAnalyzer is a Python code analysis AI tool that can analyze, refactor, and optimize Python code based on a given input prompt.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=1000, top_p=1):
        """
        Initializes the CodeAnalyzer class with API key, model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)

    def analyze_code(self, code):
        """
        Performs a comprehensive analysis of the provided Python code, focusing on errors and inefficiencies.
        """
        code = get_code_from_input(code)
        prompt = f"Perform a comprehensive analysis of the following Python code, focusing on syntax errors, logical inconsistencies, and potential inefficiencies. Provide actionable suggestions to enhance code quality and performance. Here is the code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def find_syntax_errors(self, code):
        """
        Identifies and corrects syntax errors in the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Identify and correct any syntax errors in the following Python code. Provide a revised version of the code with all corrections applied:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def suggest_optimizations(self, code):
        """
        Suggests optimizations to improve the efficiency and readability of the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Evaluate the efficiency of the following Python code and suggest optimizations where applicable. Aim to improve performance, readability, and maintainability. Here is the code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def refactor_code(self, code):
        """
        Refactors the provided Python code to improve readability and maintainability without changing functionality.
        """
        code = get_code_from_input(code)
        prompt = f"Refactor the following Python code to improve readability and maintainability, without changing its functionality:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def get_code_explanation(self, code):
        """
        Provides a detailed explanation of the provided Python code, describing its functionality.
        """
        code = get_code_from_input(code)
        prompt = f"Provide a detailed explanation of the following Python code, describing what each part of the code does:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def fix_code(self, code):
        """
        Analyzes and fixes any issues found in the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Analyze and fix any issues found in the following Python code. Provide the corrected version:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def find_errors(self, code):
        """
        Identifies and explains any errors in the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Identify and explain any errors in the following Python code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def suggest_improvements(self, code):
        """
        Suggests improvements for enhancing the performance, readability, and maintainability of the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Suggest improvements for the following Python code to enhance its performance, readability, and maintainability:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def check_security_issues(self, code):
        """
        Checks the provided Python code for any security vulnerabilities or potential issues.
        """
        code = get_code_from_input(code)
        prompt = f"Check the following Python code for any security vulnerabilities or potential issues:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code

    def generate_test_cases(self, code):
        """
        Generates test cases to ensure the correctness of the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Generate test cases for the following Python code to ensure it works correctly:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class CodeFormatter(BaseAssistant):
    """
    CodeFormatter formats Python code according to PEP8 standards.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=1000, top_p=1):
        """
        Initializes the CodeFormatter class with model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)

    def format_code(self, code):
        """
        Formats the provided Python code according to PEP8 standards.
        """
        code = get_code_from_input(code)
        prompt = f"Format the following Python code according to PEP8 standards:\n\n{code}"

        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class ErrorLogAnalyzer(BaseAssistant):
    """
    ErrorLogAnalyzer logs and analyzes Python errors, providing suggestions for fixing them.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=1000, top_p=1):
        """
        Initializes the ErrorLogAnalyzer class with model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)
        self.error_logs = []

    def analyze_errors(self, error_message):
        """
        Analyzes logged errors and provides suggestions for fixing them.
        """

        prompt = f"Analyze the following Python error log and provide suggestions for fixing this:\n\n{error_message}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class CodeReviewer(BaseAssistant):
    """
    CodeReviewer provides functionality to review Python code and provide feedback on its structure, clarity, and overall quality.
    """

    def review_code(self, code):
        """
        Reviews the provided Python code as a senior developer would.
        """
        code = get_code_from_input(code)
        prompt = f"Review the following Python code as a senior developer would. Provide feedback on its structure, clarity, maintainability, and overall quality:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class DocumentationGenerator(BaseAssistant):
    """
    DocumentationGenerator generates detailed docstrings and inline comments for Python code.
    """

    def generate_docstrings(self, code):
        """
        Generates detailed docstrings and inline comments for the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Generate detailed docstrings and inline comments for the following Python code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class ConvertToPython(BaseAssistant):
    """
    ConvertToPython converts code from other languages to Python code.
    """

    def convert_code(self, code):
        """
        Converts the provided code from another language to Python.
        """
        # code = get_code_from_input(code)
        prompt = f"Convert the given code to Python code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class CodeVisualizer(BaseAssistant):
    """
    CodeVisualizer generates visual representations, such as flowcharts or class diagrams, for Python code.
    """

    def visualize_code(self, code):
        """
        Creates a flowchart or class diagram for the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Create a flowchart or class diagram for the following Python code:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class BugFixer(BaseAssistant):
    """
    BugFixer automatically identifies and fixes bugs in Python code.
    """

    def fix_bugs(self, code):
        """
        Automatically identifies and fixes any bugs in the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Automatically identify and fix any bugs in the following Python code. Provide the corrected version:\n\n{code}"
        
        generated_code = self._get_completion(prompt)
        
        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code


class UnitTestGenerator(BaseAssistant):
    """
    UnitTestGenerator generates unit tests for Python code.
    """

    def generate_tests(self, code):
        """
        Generates unit tests for the provided Python code.
        """
        code = get_code_from_input(code)
        prompt = f"Generate unit tests for the following Python code. Ensure that all functions and methods are covered:\n\n{code}"
        
        generated_code = self._get_completion(prompt)

        file_name_generator = CodeFileNameGenerator()
        file_name = file_name_generator.generate_file_name(code)
        
        save_generated_data_to_md(file_name, generated_code)
        return generated_code