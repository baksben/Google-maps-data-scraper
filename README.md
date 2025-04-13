# Google-maps-data-scraper

A simple desktop app to scrape contact information for **notaries in Spain** from Google Maps using Selenium. Built with [Flet](https://flet.dev) for an easy-to-use graphical interface.

---

## ✨ Features

- Scrape business name, address, phone number, website, rating, reviews, geolocation, and screenshots.
- Works city-by-city across Spain.
- Export results to CSV.
- Friendly GUI — no coding knowledge required!

---

## 🚀 How to Run

### 1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Download the correct ChromeDriver
Make sure ChromeDriver matches your browser version. Download it here.

Update the path in:
- scraper.py
- app.py

### 3. python app.py
Run the app and follow the instructions in the GUI.

### 4. 📁 Output
The output will be CSV files per city (e.g. Blanes.csv) and screenshots saved under screenshots/<city>/.

### 👨‍💻 Author
Built by Bakwenye Benjamin

### Disclaimer
This project is for educational purposes. Be respectful of website usage policies and avoid scraping at high volumes.
