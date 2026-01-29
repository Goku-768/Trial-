# Facebook/Meta Catalog Converter

Convert shop inventory data to Facebook/Meta catalog format for product listings on Facebook and Instagram.

## Overview

This repository contains tools to convert shop inventory CSV files into the standardized Facebook/Meta catalog format, enabling automated product uploads to Facebook Shops and Instagram Shopping.

## Files in This Repository

- **`convert_catalog.py`** - Python script that performs the conversion from shop inventory to Facebook catalog format
- **`shop_inventory.csv`** - Source inventory data with product information (75+ sample products)
- **`catalog_products.csv`** - Generated Facebook/Meta catalog file (ready for upload)
- **`README.md`** - This documentation file

## What is the Facebook Catalog Format?

The Facebook/Meta catalog format is a standardized CSV structure used to upload product data to Facebook Business Manager. It includes required fields like product ID, title, price, and availability, plus optional fields for enhanced product display.

## How the Conversion Works

### Input Format (shop_inventory.csv)

The source inventory contains these fields:
- **Item name** - Product name/title
- **Price** - Product price (numeric)
- **Quantity** - Available stock quantity
- **Category** - Product category
- **Image 1** - Product image URL
- **Item id** - Unique product identifier (UUID)

### Output Format (catalog_products.csv)

The converter generates a Facebook-compatible CSV with 47 columns including:

#### Required Fields (Populated):
1. **id** → Item ID from source
2. **title** → Item name
3. **description** → Item name (same as title)
4. **availability** → "in stock" if Quantity > 0, else "out of stock"
5. **condition** → Always "new"
6. **price** → Formatted as "X.XX GBP" (e.g., "11.29 GBP")
7. **link** → Product URL: `https://example.com/product/{item_id}`
8. **image_link** → Image 1 URL from source
9. **brand** → Automatically extracted from item name
10. **google_product_category** → Category from source
11. **fb_product_category** → Category from source
12. **quantity_to_sell_on_facebook** → Quantity from source
13. **sale_price** → Left empty (populate only when there's an actual sale)

#### Optional Fields (Empty):
All other catalog fields (sale_price_effective_date, item_group_id, gender, color, size, etc.) are included but left empty as they're not present in the source data.

### Brand Extraction

The converter automatically detects and extracts brand names from product titles using pattern matching. Supported brand categories:

- **Drinks**: Coca Cola, Pepsi, Fanta, Sprite, Dr Pepper, Monster, Red Bull, 7UP, Tango, Rio, Lucozade, Starbucks, Evian, Volvic
- **Chocolate**: Cadbury, Galaxy, Mars, Snickers, Kit Kat, Twix, Milkybar, Kinder, M&M's, Quality Street
- **Snacks**: Walkers, Pringles, Doritos, Cheetos, Kettle, Haribo, Skittles
- **Food**: Heinz, Kellogg's, Nestle, Nescafe, McVitie's, Muller, Hovis, Nutella, Oreo, Philadelphia, Cathedral City, Lurpak, Anchor, Warburtons, Kingsmill
- **Alcohol**: Jack Daniels, Smirnoff, Gordon's, Stella Artois, Budweiser, Guinness, Heineken, Corona, Carlsberg, Baileys, Bacardi, Captain Morgan, Jameson, 19 Crimes
- **Indian Brands**: Haldiram's, Parle, Laila, TRS, Ajmi, Bikaji, Natco, Rajah, MDH
- **Household**: Andrex, Plenty, Fairy, Comfort, Persil, Dettol

If no recognizable brand is found, the field is left blank.

## How to Use with Facebook/Meta

### Step 1: Upload to Facebook Business Manager

1. Go to [Facebook Business Manager](https://business.facebook.com/)
2. Navigate to **Commerce Manager** → **Catalog**
3. Click **Add Items** → **Upload product info**
4. Select **Data feed** and upload `catalog_products.csv`
5. Map the columns (should auto-detect if column names match)
6. Review and complete the upload

### Step 2: Connect to Facebook Shop or Instagram Shopping

After uploading:
- **Facebook Shop**: Your products will appear in your Facebook Shop
- **Instagram Shopping**: Enable product tagging in Instagram posts and stories
- **Facebook Ads**: Use the catalog for dynamic product ads

### Step 3: Update Product URLs (Important!)

The generated catalog uses placeholder URLs (`https://example.com/product/{id}`). Before going live:
1. Update the `generate_product_link()` function in `convert_catalog.py` with your actual domain
2. Re-run the conversion to generate updated URLs

```python
def generate_product_link(item_id: str) -> str:
    return f"https://yourstore.com/product/{item_id}"
```

## How to Re-run the Conversion

### Prerequisites
- Python 3.6 or higher
- No additional packages required (uses standard library only)

### Steps to Regenerate Catalog

1. **Update source inventory** (if needed):
   - Edit `shop_inventory.csv` with current product data
   - Ensure columns match: Item name, Price, Quantity, Category, Image 1, Item id

2. **Run the conversion script**:
   ```bash
   python3 convert_catalog.py
   ```

3. **Output**:
   - The script will create/overwrite `catalog_products.csv`
   - You'll see a summary of products processed

### Example Output:
```
============================================================
Facebook/Meta Catalog Converter
============================================================

Reading from: shop_inventory.csv
Writing to: catalog_products.csv

✓ Conversion complete!
✓ Processed 75 products
✓ Output saved to: catalog_products.csv

============================================================
Conversion successful!
============================================================
```

## Customization Options

### Add More Brands

Edit the `BRANDS` dictionary in `convert_catalog.py`:

```python
BRANDS = {
    'drinks': ['Coca Cola', 'Pepsi', ...],
    'chocolate': ['Cadbury', 'Galaxy', ...],
    # Add your custom category
    'custom_category': ['Brand1', 'Brand2', ...],
}
```

### Change Price Currency

Modify the `format_price()` function:

```python
def format_price(price: str) -> str:
    """Format price with currency code."""
    try:
        price_float = float(price)
        return f"{price_float:.2f} USD"  # Change GBP to USD, EUR, etc.
    except (ValueError, TypeError):
        return "0.00 USD"
```

### Customize Availability Logic

Edit the `get_availability()` function:

```python
def get_availability(quantity: str) -> str:
    """Determine availability based on quantity."""
    try:
        qty = int(float(quantity))
        if qty > 10:
            return "in stock"
        elif qty > 0:
            return "available to order"
        else:
            return "out of stock"
    except (ValueError, TypeError):
        return "out of stock"
```

## Technical Notes

- **Encoding**: UTF-8 encoding for international characters
- **CSV Format**: Standard CSV with proper escaping for commas and quotes
- **Price Format**: Always 2 decimal places (e.g., "1.00 GBP", not "1 GBP")
- **Empty Fields**: All optional fields are included but left empty (as per Facebook spec)
- **Error Handling**: Graceful handling of missing/invalid values

## Troubleshooting

### Common Issues:

**"Input file not found"**
- Ensure `shop_inventory.csv` exists in the same directory as `convert_catalog.py`

**"Invalid price format"**
- Check that Price column contains numeric values only (no currency symbols)

**Missing brands**
- Brands are case-insensitive but must match patterns in BRANDS dictionary
- Add custom brands to the script if needed

**Facebook upload errors**
- Verify CSV has all required columns (id, title, description, availability, condition, price, link, image_link)
- Check that URLs are valid format (no spaces, proper http/https)
- Ensure price format includes currency code (e.g., "GBP", "USD")

## Support & Resources

- [Facebook Commerce Manager Help](https://www.facebook.com/business/help/commerce-manager)
- [Facebook Catalog Data Feed Specification](https://developers.facebook.com/docs/marketing-api/catalog/reference)
- [Instagram Shopping Setup](https://help.instagram.com/1187859655048322)

## License

This project is open source and available for use and modification.

---

**Generated**: January 2026  
**Format Version**: Facebook/Meta Catalog v2.0  
**Products**: 75+ sample products included
