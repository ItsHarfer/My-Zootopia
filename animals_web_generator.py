"""
animals_web_generator.py

This script reads animal data from a JSON file and a template HTML file,
generates a list of formatted animal details, replaces a placeholder in the
HTML template with the generated content, and writes the final HTML to a new file.
"""

import json
from typing import Any

HTML_FILE = "animals_template.html"
JSON_FILE = "animals_data.json"
ANIMAL_HTML_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def load_data(file_path: str, is_json: bool = False) -> str | dict:
    """
    Reads data from the specified file path.

    :param file_path: Path to the file to read.
    :param is_json: Whether to parse the file as JSON. Defaults to False.
    :return: Parsed JSON data as a dictionary if is_json is True,
             otherwise the file content as a string.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file) if is_json else file.read()
    except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return "" if not is_json else {}


def save_data(file_path: str, html: str, is_json: bool = False) -> None:
    """
    Saves data to the specified file path.

    :param file_path: Path to the file to save.
    :param html: Content to write to the file.
    :param is_json: Whether to save the content as JSON. Defaults to False.
    :return: None
    """
    try:
        with open(file_path, "w") as file:
            file.write(json.dumps(html)) if is_json else file.write(html)
            return print("HTML saved successfully.")
    except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
        return print(f"Error saving file {file_path}: {e}")


def indented_line(line: str, level: int = 0) -> str:
    """
    Returns a formatted HTML line with indentation.

    :param line: The HTML line to format.
    :param level: The indentation level (each level adds two spaces). Defaults to 0.
    :return: A string with the line prefixed by the appropriate number of spaces and a newline character.
    """
    return "  " * level + line + "\n"


def format_characteristics(characteristics: dict, location: str) -> str:
    """
    Formats the characteristics and location of an animal into an HTML string.

    :param characteristics: Dictionary containing animal characteristics such as diet, type, temperament, etc.
    :param location: Location string of the animal.
    :return: Formatted HTML string representing the animal's characteristics.
    """
    output = ""
    diet = characteristics.get("diet", "")
    animal_type = characteristics.get("type", "")
    temperament = characteristics.get("temperament", "")
    avg_litter_size = characteristics.get("average_litter_size", "")
    lifespan = characteristics.get("lifespan", "")

    output += indented_line("<ul>", 2)
    if diet:
        output += indented_line(f"<li><strong>Diet:</strong> {diet}</li>", 3)
    if animal_type:
        output += indented_line(f"<li><strong>Type:</strong> {animal_type}</li>", 3)
    if location:
        output += indented_line(f"<li><strong>Location:</strong> {location}</li>", 3)
    if temperament:
        output += indented_line(
            f"<li><strong>Temperament:</strong> {temperament}</li>", 3
        )
    if avg_litter_size:
        output += indented_line(
            f"<li><strong>Average Litter Size:</strong> {avg_litter_size}</li>", 3
        )
    if lifespan:
        output += indented_line(f"<li><strong>Lifespan:</strong> {lifespan}</li>", 3)
    output += indented_line("</ul>", 2)

    return output


def generate_animal_card(name: str, subtitle: str, body_html: str) -> str:
    """
    Generates an HTML card for an animal with its name, subtitle, and detailed body content.

    :param name: The name of the animal.
    :param subtitle: A subtitle or scientific name of the animal.
    :param body_html: HTML formatted string containing detailed animal information.
    :return: An HTML string representing the animal card.
    """
    output = ""
    output += f'<li class="cards__item">\n'
    output += f'  <div class="card__title">{name}</div>\n'
    if subtitle:
        output += f'  <div class="card__subtitle"><em>{subtitle}</em></div>\n'
    output += f'  <div class="card__text">\n{body_html}</div>\n'
    output += f"</li>\n"
    return output


def serialize_animal(animal_obj: dict) -> str:
    """
    Serializes an animal object dictionary into an HTML card string.

    :param animal_obj: Dictionary representing an animal with keys like 'name', 'characteristics', 'locations', and 'taxonomy'.
    :return: An HTML string representing the serialized animal card.
    """
    name = animal_obj.get("name", "")
    characteristics = animal_obj.get("characteristics", {})
    location = animal_obj.get("locations", [])[0] if animal_obj.get("locations") else ""
    scientific_name = animal_obj.get("taxonomy", {}).get("scientific_name", "")
    body_html = format_characteristics(characteristics, location)
    return generate_animal_card(name, scientific_name, body_html)


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

    html_with_animals = html_without_animals.replace(PLACEHOLDER, output)
    return html_with_animals


def main() -> None:
    """
    Main function that orchestrates the replacement and saving of animal HTML content.

    :return: None
    """
    animal_html = replace_animals_info()
    save_data(ANIMAL_HTML_FILE, animal_html)


if __name__ == "__main__":
    main()
