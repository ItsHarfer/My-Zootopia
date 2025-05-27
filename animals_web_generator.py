import json


def load_data(file_path: str):
    """
    Read the data from the file by file_path
    :param file_path:
    :return:
    """
    with open(file_path, "r") as handle:
        return json.load(handle)


def print_attributes(animal_list: list[dict[str | dict[str]]]) -> None:
    """
    Prints formatted attributes (name, diet, type, location) of each animal from a given list.

    :param animal_list: List of dictionaries, each containing details about an animal.
    :return: None
    """
    for animal in animal_list:

        name = animal.get("name", "")
        characteristics = animal.get("characteristics", {})
        diet = characteristics.get("diet", "")
        animal_type = characteristics.get("type", "")
        location = animal.get("locations", [])[0]

        if name: print(f"Name: {name.capitalize()}")
        if diet: print(f"Diet: {diet.capitalize()}")
        if animal_type: print(f"Type: {animal_type.capitalize()}")
        if location: print(f"Location: {location.capitalize()}")
        print()

def main():
    animals_data = load_data('animals_data.json')
    print_attributes(animals_data)

if __name__ == "__main__":
    main()
