import requests
from openapi_core import Spec
from openapi_core.validation.schemas import OAS31Validator
import black
import os

def fetch_openapi_spec(url: str) -> dict:
    """Fetch the OpenAPI (Swagger) spec from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def validate_spec(spec_dict: dict) -> None:
    """Validate the OpenAPI spec using OAS31Validator."""
    validator = OAS31Validator(spec_dict)
    validator.validate(spec_dict)  # Pass spec_dict as the instance to validate

def get_description(path_item: dict, method: str) -> str:
    """Extract the description for a specific path and method."""
    return path_item[method].get('description', '').replace('\n', ' ').strip()

def generate_literals_from_paths(spec_dict: dict, output_file: str) -> None:
    """Generate Python Literal type hints for GET, POST, PUT, DELETE paths with descriptions."""
    spec = Spec.from_dict(spec_dict)
    paths = spec['paths']

    get_lines = ["from typing import Literal\n\nGETPaths = Literal["]
    post_lines = ["POSTPaths = Literal["]
    put_lines = ["PUTPaths = Literal["]
    delete_lines = ["DELETEPaths = Literal["]

    for path_name, path_item in paths.items():
        path_name_literal = f'"{path_name}"'
        if "get" in path_item:
            description = get_description(path_item, "get")
            get_lines.append(f"    {path_name_literal},  # {description}")
        if "post" in path_item:
            description = get_description(path_item, "post")
            post_lines.append(f"    {path_name_literal},  # {description}")
        if "put" in path_item:
            description = get_description(path_item, "put")
            put_lines.append(f"    {path_name_literal},  # {description}")
        if "delete" in path_item:
            description = get_description(path_item, "delete")
            delete_lines.append(f"    {path_name_literal},  # {description}")

    # Close the Literal definitions
    get_lines.append("]\n")
    post_lines.append("]\n")
    put_lines.append("]\n")
    delete_lines.append("]\n")

    # Combine lines into single code strings
    get_code = "\n".join(get_lines)
    post_code = "\n".join(post_lines)
    put_code = "\n".join(put_lines)
    delete_code = "\n".join(delete_lines)

    # Format the code with black (optional)
    try:
        get_code = black.format_str(get_code, mode=black.FileMode())
        post_code = black.format_str(post_code, mode=black.FileMode())
        put_code = black.format_str(put_code, mode=black.FileMode())
        delete_code = black.format_str(delete_code, mode=black.FileMode())
    except black.parsing.InvalidInput:
        print("Skipping black formatting due to invalid input error")

    # Write the formatted code to the output file in the same directory as this script
    with open(output_file, 'w') as f:
        f.write(get_code)
        f.write("\n")
        f.write(post_code)
        f.write("\n")
        f.write(put_code)
        f.write("\n")
        f.write(delete_code)

    print(f"API path Literals with descriptions generated successfully in {output_file}.")

if __name__ == "__main__":
    # URL to the OpenAPI (Swagger) JSON file
    swagger_url = "https://api.cymulate.com/docs/swagger.json"

    # Output Python file for the generated literals, placed in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_literal_file = os.path.join(script_dir, "api_paths.py")

    # Fetch and load the OpenAPI spec
    spec_dict = fetch_openapi_spec(swagger_url)

    # Validate the spec
    validate_spec(spec_dict)

    # Generate the Literal type hints from the paths and save them to a file
    generate_literals_from_paths(spec_dict, output_literal_file)
