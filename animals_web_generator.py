"""
animals_web_generator.py

This script reads animal data from a JSON file and a template HTML file,
generates a list of formatted animal details, replaces a placeholder in the
HTML template with the generated content, and writes the final HTML to a new file.
"""

import json

import requests

from config import (
    PLACEHOLDER,
    JSON_FILE,
    ATTRIBUTE,
    SUB_ATTRIBUTE,
    HTML_FILE,
    ANIMAL_HTML_FILE,
    API_NINJA_KEY,
    API_NINJA_URL,
)


def load_remote_data(url: str, endpoint_name: str = "", query: str = "") -> list[dict]:
    """
    Sends a GET request to the specified API endpoint with an optional query.
    Returns the JSON response as a list of animal dictionaries.

    :param url: Base URL of the API.
    :param endpoint_name: Query parameter name (e.g., 'name').
    :param query: Query value (e.g., 'Fox').
    :return: List of animal data dictionaries.
    """
    try:
        response = requests.get(
            f"{url}?{endpoint_name}={query}",
            headers={"X-Api-Key": API_NINJA_KEY},
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data

    except requests.RequestException as e:
        print(f"Failed to fetch data from API: {e}")
        return []


def load_local_data(file_path: str, is_json: bool = False) -> str | dict:
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
    animals: list, attribute: str, sub_attribute: str = ""
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


def get_user_choice(prompt: str) -> str | None:
    """
    Prompts the user to enter a non-empty string input.

    :param prompt: The prompt message displayed to the user.
    :return: The user's input converted to lowercase, if not empty.
    """
    while True:
        try:
            user_choice = input(prompt).strip().lower()
            if user_choice:
                return user_choice
            else:
                print("Choice cannot be empty. Please type in an animal name.")
                continue

        except ValueError as e:
            print("Error: ", e)


def get_user_choice_with_answers(skin_types: list[str]) -> str:
    """
    Prompts the user to select a skin type from a list of options.

    :param skin_types: A list of available skin types.
    :return: The skin type selected by the user.
    """
    if not skin_types:
        print("No skin types found.")
        return ""

    skin_types = sorted(skin_types)
    print("** Available skin types **")
    for skin in skin_types:
        print(f"- {skin}")

    while True:
        choice = input("Enter a skin type: ").strip()
        if choice in skin_types:
            return choice
        print("Invalid choice. Please select one from the list above.")


def generate_html_by_filtered_attribute(
    animal_choice: str, animal_data: list[dict], skin_type: str
) -> str:
    """
    Generates a formatted HTML block for a list of animals filtered by a specific skin type.
    Includes a heading that reflects the user's search criteria.

    :param animal_choice: The name of the animal entered by the user.
    :param animal_data: A list of animal dictionaries matching the filter.
    :param skin_type: The skin type used to filter animals.
    :return: A complete HTML string containing the filtered result cards.
    """
    output = f"""
  <div class="card__result">
    <h2>You searched for: <em>{animal_choice}</em></h2>
    <p>Filtered by skin type: <strong>{skin_type}</strong></p>
  </div>
  """
    for animal in animal_data:
        output += serialize_animal(animal)
    return output


def generate_html_error_message(query: str) -> str:
    return f"""
  <div class="card__error">
    <h2>Oops! We couldn't find the animal "<em>{query}</em>".</h2>
    <p>Please try another name or check your spelling.</p>
  </div>
  """


def get_filtered_animals_html() -> str | None:
    """
    Loads animal data, groups it by a given attribute, asks the user to choose a skin type,
    and returns the HTML string for the animals matching that skin type.

    :return: HTML string containing cards for animals of the selected skin type.
    """
    while True:
        animal_choice = get_user_choice("Enter a name of an animal: ")
        animals = load_remote_data(API_NINJA_URL, "name", animal_choice)

        if not animals:
            print(f"No data found for {animal_choice}")
            return generate_html_error_message(animal_choice)

        grouped = group_by_attribute(animals, ATTRIBUTE, SUB_ATTRIBUTE)
        if not grouped:
            print("No valid skin types found for this animal.")
            continue

        skin_type = get_user_choice_with_answers(list(grouped.keys()))
        if skin_type and skin_type in grouped:
            return generate_html_by_filtered_attribute(
                animal_choice, grouped[skin_type], skin_type
            )

        print("Invalid skin type selected.")


def render_and_save_html(animal_html: str) -> None:
    """
    Loads the HTML template, replaces its placeholder with the provided animal HTML content,
    and saves the final HTML to a file.

    :param animal_html: HTML string with the filtered animal cards to be inserted.
    :return: None
    """
    html_template = load_local_data(HTML_FILE)
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
