from scraper import Scraper
import flet as ft
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of app.py
chrome_path = os.path.join(base_dir, "chromedriver-win64", "chromedriver.exe")

def main(page: ft.Page):
    def handle_click(e):
        if txt_keyword.value.strip() == "":
            txt_keyword.error_text = "Please enter a city name"
            page.update()
        else:
            scraper = Scraper(chrome_path=chrome_path)  # Update with your path to chromedriver
            
            # Show a snack bar while scraping
            snack_bar = ft.SnackBar(ft.Text(f"Scraping for city: {txt_keyword.value}..."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

            try:
                scraper.scrap(url="https://www.google.com/maps", cities=[txt_keyword.value])
                
                # Show success message and enable download
                download_button.visible = True
                snack_bar = ft.SnackBar(ft.Text("Scraping completed!"))
                page.overlay.append(snack_bar)
                snack_bar.open = True
            except Exception as ex:
                # Show error message if something goes wrong
                snack_bar = ft.SnackBar(ft.Text(f"Error occurred: {str(ex)}"))
                page.overlay.append(snack_bar)
                snack_bar.open = True

            page.update()

    def download_csv(e):
        city_name = txt_keyword.value.strip()
        file_path = f"scrape_files\{city_name}.xlsx"
        if os.path.exists(file_path):
            # Open FilePicker to allow the user to download the file
            file_picker.save_file(
                dialog_title="Save Excel File",
                file_name=f"{city_name}.xlsx",
                on_result=lambda r: save_file(r, file_path)
            )

        else:
            # Show a snack bar if the file is not found
            snack_bar = ft.SnackBar(ft.Text("File not found"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    def save_file(result, file_path):
        if result != None and result.files != None:
            # The user has selected a location to save the file
            with open(file_path, "rb") as f:
                file_picker.write(result.files[0], f.read())
            snack_bar = ft.SnackBar(ft.Text(f"File saved as {result.files[0]}"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # Global Config
    page.title = "Google Maps Web Scraper"
    
    # New way to configure the window
    page.window.maximized = False
    page.window.maximizable = False
    page.window.resizable = False

    # Create UI Components
    # page.add(ft.Container(
    #     content=ft.Column([
    #         ft.Text(
    #             value="Google Maps Web Scraper",
    #             color="white",
    #             size=30,
    #             weight=ft.FontWeight.BOLD
    #         ),
    #         ft.Text(
    #             value="By Bakwenye Benjamin",
    #             color="white",
    #             size=20,
    #         )
    #     ]),
    #     image_src='../source/wallpaper.jpg',
    #     image_fit=ft.ImageFit.COVER,
    #     width=page.width,
    #     expand=True,
    # ))
    page.add(
    ft.Container(
        content=ft.Column([
            ft.Text("Google Maps Web Scraper", color="white", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("By Bakwenye Benjamin", color="white", size=20)
        ]),
        width=page.width,
        height=400,
        bgcolor=ft.colors.BLACK,
        image=ft.Image(
            src="source/wallpaper.jpg",
            fit=ft.ImageFit.COVER
        )
    )
)


    txt_keyword = ft.TextField(label="Enter the city name!", width=400)
    page.add(ft.Row([
        txt_keyword,
        ft.FilledButton(
            text="Scrap",
            on_click=handle_click,
            icon="search"
        )
    ]))

    # Download Button (Initially Hidden)
    download_button = ft.FilledButton(
        text="Download Excel",
        on_click=download_csv,
        icon="download",
        visible=False
    )
    page.add(download_button)

    # Initialize FilePicker for file download
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
