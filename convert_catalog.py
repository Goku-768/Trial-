#!/usr/bin/env python3
"""
Facebook/Meta Catalog Converter
Converts shop inventory CSV to Facebook/Meta catalog format.
"""

import csv
import re
from typing import Dict, List, Optional


# Brand extraction patterns
BRANDS = {
    'drinks': [
        'Coca Cola', 'Coca-Cola', 'Pepsi', 'Fanta', 'Sprite', 'Dr Pepper', 
        'Monster', 'Red Bull', '7UP', 'Tango', 'Rio', 'Lucozade', 'Starbucks',
        'Evian', 'Volvic'
    ],
    'chocolate': [
        'Cadbury', 'Galaxy', 'Mars', 'Snickers', 'Kit Kat', 'KitKat', 'Twix', 
        'Milkybar', 'Kinder', "M&M's", 'M&M', 'Quality Street'
    ],
    'snacks': [
        'Walkers', 'Pringles', 'Doritos', 'Cheetos', 'Kettle', 'Haribo', 'Skittles'
    ],
    'food': [
        'Heinz', "Kellogg's", 'Kellogg', 'Nestle', 'Nescafe', "McVitie's", 'McVitie',
        'Muller', 'Hovis', 'Nutella', 'Oreo', 'Philadelphia', 'Cathedral City',
        'Lurpak', 'Anchor', 'Warburtons', 'Kingsmill'
    ],
    'alcohol': [
        'Jack Daniels', 'Smirnoff', "Gordon's", 'Gordon', 'Stella Artois', 
        'Budweiser', 'Guinness', 'Heineken', 'Corona', 'Carlsberg', 'Baileys', 
        'Bacardi', 'Captain Morgan', 'Jameson', '19 Crimes'
    ],
    'indian': [
        "Haldiram's", 'Haldiram', 'Parle', 'Laila', 'TRS', 'Ajmi', 'Bikaji', 
        'Natco', 'Rajah', 'MDH'
    ],
    'household': [
        'Andrex', 'Plenty', 'Fairy', 'Comfort', 'Persil', 'Dettol'
    ]
}

# Pre-compile brand patterns for better performance
ALL_BRANDS_SORTED = []
BRAND_PATTERNS = []

def _initialize_brand_patterns():
    """Initialize brand patterns once at module level."""
    global ALL_BRANDS_SORTED, BRAND_PATTERNS
    
    # Flatten all brands into a single list
    for category_brands in BRANDS.values():
        ALL_BRANDS_SORTED.extend(category_brands)
    
    # Sort by length descending to match longer brand names first
    ALL_BRANDS_SORTED.sort(key=len, reverse=True)
    
    # Pre-compile regex patterns for each brand
    BRAND_PATTERNS = [(brand, re.compile(re.escape(brand), re.IGNORECASE)) 
                      for brand in ALL_BRANDS_SORTED]

# Initialize patterns at module load
_initialize_brand_patterns()


def extract_brand(item_name: str) -> str:
    """
    Extract recognizable brand from item name.
    Returns the brand name if found, empty string otherwise.
    """
    # Check each pre-compiled brand pattern
    for brand, pattern in BRAND_PATTERNS:
        if pattern.search(item_name):
            return brand
    
    return ''


def format_price(price: str) -> str:
    """
    Format price as 'X.XX GBP'.
    """
    try:
        price_float = float(price)
        return f"{price_float:.2f} GBP"
    except (ValueError, TypeError):
        return "0.00 GBP"


def get_availability(quantity: str) -> str:
    """
    Determine availability based on quantity.
    """
    try:
        qty = int(float(quantity))
        return "in stock" if qty > 0 else "out of stock"
    except (ValueError, TypeError):
        return "out of stock"


def generate_product_link(item_id: str) -> str:
    """
    Generate product link using item ID.
    """
    return f"https://example.com/product/{item_id}"


def convert_to_facebook_catalog(input_csv: str, output_csv: str) -> None:
    """
    Convert shop inventory CSV to Facebook/Meta catalog format.
    
    Args:
        input_csv: Path to input inventory CSV file
        output_csv: Path to output catalog CSV file
    """
    
    # Define all Facebook catalog columns
    facebook_columns = [
        'id', 'title', 'description', 'availability', 'condition', 'price', 
        'link', 'image_link', 'brand', 'google_product_category', 
        'fb_product_category', 'quantity_to_sell_on_facebook', 'sale_price',
        'sale_price_effective_date', 'item_group_id', 'gender', 'color', 
        'size', 'age_group', 'material', 'pattern', 'shipping', 
        'shipping_weight', 'video[0].url', 'video[0].tag[0]', 'address.city', 
        'address.country', 'address.neighborhoods', 'address.postal_code', 
        'address.region', 'address.street_address', 'gtin', 'product_tags[0]', 
        'product_tags[1]', 'availability_polygon_coordinates[0].latitude', 
        'availability_polygon_coordinates[0].longitude', 
        'availability_polygon_coordinates[1].latitude', 
        'availability_polygon_coordinates[1].longitude', 
        'availability_polygon_coordinates[2].latitude', 
        'availability_polygon_coordinates[2].longitude', 
        'availability_polygon_coordinates[3].latitude', 
        'availability_polygon_coordinates[3].longitude', 
        'availability_circle_origin.latitude', 'availability_circle_origin.longitude', 
        'availability_circle_radius_unit', 'availability_circle_radius', 'style[0]'
    ]
    
    converted_products = []
    
    # Read input CSV
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Extract required fields from input
            item_name = row.get('Item name', '')
            price = row.get('Price', '0')
            quantity = row.get('Quantity', '0')
            category = row.get('Category', '')
            image_url = row.get('Image 1', '')
            item_id = row.get('Item id', '')
            
            # Create Facebook catalog row
            facebook_row = {col: '' for col in facebook_columns}
            
            # Populate required fields
            facebook_row['id'] = item_id
            facebook_row['title'] = item_name
            facebook_row['description'] = item_name
            facebook_row['availability'] = get_availability(quantity)
            facebook_row['condition'] = 'new'
            facebook_row['price'] = format_price(price)
            facebook_row['link'] = generate_product_link(item_id)
            facebook_row['image_link'] = image_url
            facebook_row['brand'] = extract_brand(item_name)
            facebook_row['google_product_category'] = category
            facebook_row['fb_product_category'] = category
            facebook_row['quantity_to_sell_on_facebook'] = quantity
            facebook_row['sale_price'] = format_price(price)
            
            converted_products.append(facebook_row)
    
    # Write output CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=facebook_columns)
        writer.writeheader()
        writer.writerows(converted_products)
    
    print(f"✓ Conversion complete!")
    print(f"✓ Processed {len(converted_products)} products")
    print(f"✓ Output saved to: {output_csv}")


def main():
    """Main entry point."""
    input_file = 'shop_inventory.csv'
    output_file = 'catalog_products.csv'
    
    print("=" * 60)
    print("Facebook/Meta Catalog Converter")
    print("=" * 60)
    print(f"\nReading from: {input_file}")
    print(f"Writing to: {output_file}\n")
    
    try:
        convert_to_facebook_catalog(input_file, output_file)
        print("\n" + "=" * 60)
        print("Conversion successful!")
        print("=" * 60)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        print("Please ensure shop_inventory.csv exists in the current directory.")
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise


if __name__ == '__main__':
    main()
