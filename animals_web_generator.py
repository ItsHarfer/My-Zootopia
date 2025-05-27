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
    with open(file_path, "r") as handle:
        if is_json:
            return json.load(handle)
        else:
            return handle.read()


def save_data(html: str) -> None:
    """
    Saves the provided HTML content to the output file.

    :param html: HTML content to be saved.
    :return: None
    """
    with open(ANIMAL_HTML_FILE, "w") as file:
        file.write(html)


def replace_animals_info() -> str:
    """
    Replaces the animal information placeholder in the HTML template
    with formatted animal data from the JSON file.

    :return: HTML string with animal information inserted.
    """
    html_without_animals = load_data(HTML_FILE)
    animals_data = load_data(JSON_FILE, True)
    animal_list = get_animal_list(animals_data)
    html_with_animals = html_without_animals.replace(
        "__REPLACE_ANIMALS_INFO__", animal_list
    )
    return html_with_animals


def get_animal_list(
    animal_list: list[dict[str, dict[str, str] | list[str] | str]],
) -> str:
    """
    Creates a formatted string of animal information.

    :param animal_list: List of dictionaries, each containing details about an animal.
    :return: Formatted string with each animal's details.
    """
    output = ""
    for animal in animal_list:
        name = animal.get("name", "")
        characteristics = animal.get("characteristics", {})
        diet = characteristics.get("diet", "")
        animal_type = characteristics.get("type", "")
        location = animal.get("locations", [])[0] if animal.get("locations") else ""

        if name:
            output += f"Name: {name.capitalize()}\n"
        if diet:
            output += f"Diet: {diet.capitalize()}\n"
        if animal_type:
            output += f"Type: {animal_type.capitalize()}\n"
        if location:
            output += f"Location: {location.capitalize()}\n"

        output += "\n"

    return output


def main() -> None:
    """
    Main function that orchestrates the replacement and saving of animal HTML content.

    :return: None
    """
    animal_html = replace_animals_info()
    save_data(animal_html)


if __name__ == "__main__":
    main()
