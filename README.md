# My animal repository called 'My-Zootopia'

**My Zootopia** is a Python-based web generator that fetches real-time animal data from the API Ninjas Animal API and renders an interactive HTML page. Users can search for animals, filter by characteristics (like skin type), and explore fascinating facts. All of it is styled with dynamic content blocks.

---

## 📦 Features

- Fetches animal data via API (live or mock)
- Filters animals based on sub-attributes (e.g. skin type)
- Displays detailed cards for each animal
- Handles invalid inputs with helpful messages
- Fully decoupled data fetching and website generation
- HTML output ready to be opened in any browser

---

## 🧰 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ItsHarfer/My-Zootopia.git
   cd My-Zootopia
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root folder and add your API key:
   ```
   API_KEY="YOUR_API_KEY_HERE"
   ```

---

## 🚀 Usage

Run the web generator:
```bash
python animals_web_generator.py
```

You will be prompted to enter the name of an animal and filter by characteristics.

The resulting website will be saved as an HTML file and you can open it in your default browser.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project, open issues, and submit pull requests.

Please follow standard [PEP8](https://peps.python.org/peps/pep-0008/) guidelines and write clear commit messages.

---

## 📝 License

This project is licensed under an MIT-style license for **educational use only**.  
Commercial use or redistribution is not permitted without prior permission.  
See the [LICENSE](LICENSE) file for details.
