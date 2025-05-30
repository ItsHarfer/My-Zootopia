"""
animals_web_generator.py

This script reads animal data from a JSON file and a template HTML file,
generates a list of formatted animal details, replaces a placeholder in the
HTML template with the generated content, and writes the final HTML to a new file.
"""

import json

from config import (
    PLACEHOLDER,
    JSON_FILE,
    ATTRIBUTE,
    SUB_ATTRIBUTE,
    HTML_FILE,
    ANIMAL_HTML_FILE,
)


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


def group_by_attribute(
    animals: dict, attribute: str, sub_attribute: str = ""
) -> dict[str, list[dict]]:
    """
    Groups a list of animals by a specified attribute, optionally using a sub-attribute.

    :param animals: List of animal dictionaries to be grouped.
    :param attribute: Top-level attribute key to group by.
    :param sub_attribute: Optional nested attribute key within the top-level attribute.
    :return: Dictionary where keys are attribute values and values are lists of matching animals.
    """
    grouped = {}
    for animal in animals:
        if sub_attribute:
            key = animal.get(attribute, {}).get(sub_attribute, "Unknown")
        else:
            key = animal.get(attribute, "Unknown")

        if key not in grouped:
            grouped[key] = []
        grouped[key].append(animal)

    return grouped


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


def replace_placeholder_with_html_content(html: str, output: str) -> str:
    """
    Replaces the animal information placeholder in the HTML template
    with formatted animal data from the JSON file.

    :return: HTML string with animal information inserted.
    """

    if PLACEHOLDER not in html:
        print(f"Error: Placeholder '{PLACEHOLDER}' not found in HTML template.")
        return html
    return html.replace(PLACEHOLDER, output)


def get_user_choice_with_answers(skin_types: list[str]) -> str:
    """
    Prompts the user to select a skin type from a list of options.

    :param skin_types: A list of available skin types.
    :return: The skin type selected by the user.
    """
    skin_types = sorted(skin_types)
    print("** Available skin types **")
    for skin in skin_types:
        print(f"- {skin}")

    while True:
        choice = input("Enter a skin type: ").strip()
        if choice in skin_types:
            return choice
        print("Invalid choice. Please select one from the list above.")


def generate_html_by_filtered_attribute(animal_data: list[dict], skin_type: str) -> str:
    """
    Generates the HTML for a list of animals filtered by a specific skin type.

    :param animal_data: A list of animal dictionaries to display.
    :param skin_type: The skin type used to filter animals.
    :return: HTML string containing the formatted animal cards.
    """
    output = ""
    output += f"<h2>Filtered by: {skin_type}</h2>"
    for animal in animal_data:
        output += serialize_animal(animal)
    return output


def get_filtered_animals_html() -> str:
    """
    Loads animal data, groups it by a given attribute, asks the user to choose a skin type,
    and returns the HTML string for the animals matching that skin type.

    :return: HTML string containing cards for animals of the selected skin type.
    """
    animals = load_data(JSON_FILE, is_json=True)
    grouped = group_by_attribute(animals, ATTRIBUTE, SUB_ATTRIBUTE)
    skin_type = get_user_choice_with_answers(list(grouped.keys()))
    return generate_html_by_filtered_attribute(grouped[skin_type], skin_type)


def render_and_save_html(animal_html: str) -> None:
    """
    Loads the HTML template, replaces its placeholder with the provided animal HTML content,
    and saves the final HTML to a file.

    :param animal_html: HTML string with the filtered animal cards to be inserted.
    :return: None
    """
    html_template = load_data(HTML_FILE)
    final_html = replace_placeholder_with_html_content(html_template, animal_html)
    save_data(ANIMAL_HTML_FILE, final_html)


def main() -> None:
    """
    Main function that orchestrates loading data, filtering animals by user-selected skin type,
    generating HTML, and saving the final result to a file.

    :return: None
    """
    animal_html = get_filtered_animals_html()
    render_and_save_html(animal_html)


if __name__ == "__main__":
    main()
