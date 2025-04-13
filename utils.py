import pandas as pd

def create_dataframe(names, categories, addresses, numbers, websites, ratings, reviews, geocoders, screenshot_paths, cities):
    data = {
        'Name': names,
        'Category': categories, 
        'Address': addresses,
        'Number': numbers,
        'Website': websites,
        'Rating': ratings,
        'Reviews': reviews,
        'Geocoder': geocoders,
        'Screenshot Path': screenshot_paths,
        'City': cities
    }
    return pd.DataFrame(data)

import os
import pandas as pd

def create_dataframe(names, categories, addresses, numbers, websites, ratings, reviews, geocoders, screenshot_paths, cities):
    data = {
        'Name': names,
        'Category': categories, 
        'Address': addresses,
        'Number': numbers,
        'Website': websites,
        'Rating': ratings,
        'Reviews': reviews,
        'Geocoder': geocoders,
        'Screenshot Path': screenshot_paths,
        'City': cities
    }
    return pd.DataFrame(data)

def export_data(dataframe, city):
    # Ensure scrape_files directory exists
    output_dir = os.path.join(os.getcwd(), "scrape_files")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save CSV file
    output_file_name = os.path.join(output_dir, f"{city}.xlsx")
    dataframe.to_excel(output_file_name, index=False)
    print(f"✅ Data exported to {output_file_name}")

