from scraper import Scraper
import flet as ft
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of app.py
chrome_path = os.path.join(base_dir, "chromedriver-win64", "chromedriver.exe")

def main(page: ft.Page):
    # ---- Component Declarations ----
    txt_keyword = ft.TextField(label="Enter the city name!", width=400)
    download_button = ft.FilledButton(
        text="Download Excel",
        on_click=lambda e: download_csv(e),
        icon="download",
        visible=False
    )
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # ---- Functions ----
    def handle_click(e):
        if txt_keyword.value.strip() == "":
            txt_keyword.error_text = "Please enter a city name"
            page.update()
        else:
            scraper = Scraper(chrome_path=chrome_path)

            # Show snack bar while scraping
            snack_bar = ft.SnackBar(ft.Text(f"Scraping for city: {txt_keyword.value}..."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

            try:
                scraper.scrap(url="https://www.google.com/maps", cities=[txt_keyword.value])
                download_button.visible = True
                snack_bar = ft.SnackBar(ft.Text("Scraping completed!"))
                page.overlay.append(snack_bar)
                snack_bar.open = True
            except Exception as ex:
                snack_bar = ft.SnackBar(ft.Text(f"Error occurred: {str(ex)}"))
                page.overlay.append(snack_bar)
                snack_bar.open = True

            page.update()

    def download_csv(e):
        city_name = txt_keyword.value.strip()
        file_path = f"scrape_files\\{city_name}.xlsx"
        if os.path.exists(file_path):
            file_picker.save_file(
                dialog_title="Save Excel File",
                file_name=f"{city_name}.xlsx",
                on_result=lambda r: save_file(r, file_path)
            )
        else:
            snack_bar = ft.SnackBar(ft.Text("File not found"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    def save_file(result, file_path):
        if result and result.files:
            with open(file_path, "rb") as f:
                file_picker.write(result.files[0], f.read())
            snack_bar = ft.SnackBar(ft.Text(f"File saved as {result.files[0]}"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # ---- Page Config ----
    page.title = "Google Maps Web Scraper"
    page.window.maximized = False
    page.window.maximizable = False
    page.window.resizable = False

    # ---- Layout ----
    page.add(
        ft.Stack([
            ft.Image(
                src="source/wallpaper.png",
                width=page.width,
                height=page.height,
                fit=ft.ImageFit.COVER
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Text("Google Maps Web Scraper", color="white", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text("By Bakwenye Benjamin", color="white", size=20),
                        ft.Row(
                            [txt_keyword, ft.FilledButton(text="Scrap", on_click=handle_click, icon="search")],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        download_button
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        ])
    )


if __name__ == "__main__":
    ft.app(target=main)
