"""
animals_web_generator.py

This script reads animal data from a JSON file and a template HTML file,
generates a list of formatted animal details, replaces a placeholder in the
HTML template with the generated content, and writes the final HTML to a new file.
"""

import json


HTML_FILE = "animals_template.html"
JSON_FILE = "animals_data.json"
ANIMAL_HTML_FILE = "animals.html"


def load_data(file_path: str, is_json: bool = False) -> str | dict:
    """
    Reads data from the specified file path.

    :param file_path: Path to the file to read.
    :param is_json: Boolean indicating if the file should be parsed as JSON.
    :return: Parsed JSON data as a dictionary if is_json is True,
             otherwise the file content as a string.
    """
    try:
        with open(file_path, "r") as handle:
            return json.load(handle) if is_json else handle.read()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return "" if not is_json else {}


def save_data(html: str) -> None:
    """
    Saves the provided HTML content to the output file.

    :param html: HTML content to be saved.
    :return: None
    """
    with open(ANIMAL_HTML_FILE, "w") as file:
        file.write(html)


def serialize_animal(animal_obj):
    name = animal_obj.get("name", "")
    characteristics = animal_obj.get("characteristics", {})
    diet = characteristics.get("diet", "")
    animal_type = characteristics.get("type", "")
    location = animal_obj.get("locations", [])[0] if animal_obj.get("locations") else ""

    output = ""
    output += f'<li class="cards__item">\n'
    output += f'  <div class="card__title">{name}</div><br/>\n'
    output += f'  <p class="card__text">\n'

    if diet:
        output += f"    <strong>Diet:</strong> {diet}<br/>\n"
    if animal_type:
        output += f"    <strong>Type:</strong> {animal_type}<br/>\n"
    if location:
        output += f"    <strong>Location:</strong> {location}<br/>\n"

    output += f"  </p>\n"
    output += f"</li>\n"
    return output


def replace_animals_info() -> str:
    """
    Replaces the animal information placeholder in the HTML template
    with formatted animal data from the JSON file.

    :return: HTML string with animal information inserted.
    """
    output = ""
    html_without_animals = load_data(HTML_FILE)
    animals_data = load_data(JSON_FILE, True)

    for animal_obj in animals_data:
        output += serialize_animal(animal_obj)

    html_with_animals = html_without_animals.replace("__REPLACE_ANIMALS_INFO__", output)
    return html_with_animals


def main() -> None:
    """
    Main function that orchestrates the replacement and saving of animal HTML content.

    :return: None
    """
    animal_html = replace_animals_info()
    save_data(animal_html)


if __name__ == "__main__":
    main()
