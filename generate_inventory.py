#!/usr/bin/env python3
"""
Generate expanded shop inventory with 710 products
"""

import csv
import uuid
import random
import hashlib

# Product templates organized by category
PRODUCT_TEMPLATES = {
    'Soft Drinks • Water • Shakes': [
        ('Coca-Cola Original Taste', [330, 500, 1000, 1500], [0.99, 1.29, 1.99, 2.49]),
        ('Pepsi Max', [330, 500, 1500], [0.99, 1.29, 2.49]),
        ('Fanta Orange', [330, 500], [0.89, 1.19]),
        ('Sprite Zero', [330, 500], [0.99, 1.29]),
        ('Dr Pepper', [330, 500], [1.09, 1.39]),
        ('7UP Lemon & Lime', [330, 500], [0.89, 1.19]),
        ('Tango Orange', [330], [0.95]),
        ('Rio Tropical', [330], [1.05]),
        ('Irn-Bru Original', [330, 500], [0.99, 1.29]),
        ('Vimto Original', [330, 500], [0.89, 1.19]),
        ('Evian Natural Mineral Water', [500, 750, 1000, 1500], [0.99, 1.19, 1.39, 1.79]),
        ('Volvic Touch of Fruit', [500, 1500], [1.09, 1.99]),
        ('Highland Spring Water', [500, 1500], [0.89, 1.69]),
        ('San Pellegrino Sparkling', [330, 500], [1.29, 1.79]),
        ('Perrier Sparkling Water', [330, 750], [1.19, 2.29]),
    ],
    'Energy Drinks': [
        ('Monster Energy Original', [500], [1.89]),
        ('Monster Energy Ultra', [500], [1.89]),
        ('Red Bull Energy Drink', [250, 355, 473], [1.69, 2.29, 2.99]),
        ('Red Bull Sugar Free', [250, 355], [1.69, 2.29]),
        ('Lucozade Energy Original', [380, 500], [1.39, 1.69]),
        ('Lucozade Sport Orange', [500], [1.49]),
        ('Relentless Origin', [500], [1.79]),
        ('Rockstar Energy', [500], [1.69]),
    ],
    'Chocolate • Sweets • Treats': [
        ('Cadbury Dairy Milk', [45, 110, 180, 360], [0.79, 1.99, 3.49, 6.99]),
        ('Galaxy Smooth Milk', [42, 110, 200, 390], [0.75, 1.99, 3.49, 6.99]),
        ('Mars Bar', [51], [0.79]),
        ('Snickers Bar', [48, 75], [0.79, 1.29]),
        ('Twix Twin Bar', [50, 75], [0.79, 1.29]),
        ('Kit Kat 4 Finger', [41.5, 112], [0.69, 1.99]),
        ('Milkybar White Chocolate', [25, 100], [0.59, 1.99]),
        ('Kinder Bueno', [43, 86], [0.89, 1.79]),
        ('M&M\'s Peanut', [45, 90, 165], [0.99, 1.79, 2.99]),
        ('M&M\'s Chocolate', [45, 90], [0.99, 1.79]),
        ('Quality Street', [265, 650], [3.99, 8.99]),
        ('Celebrations', [300, 600], [4.99, 9.99]),
        ('Heroes', [290, 600], [4.99, 9.99]),
        ('Roses', [290, 600], [4.99, 9.99]),
        ('Haribo Starmix', [140, 160, 400], [1.19, 1.39, 2.99]),
        ('Haribo Tangfastics', [140, 400], [1.19, 2.99]),
        ('Skittles Original', [45, 55, 125], [0.79, 0.99, 1.99]),
        ('Starburst Original', [45, 192], [0.79, 1.99]),
    ],
    'Crisps • Snacks': [
        ('Walkers Ready Salted', [32.5, 65, 150], [0.59, 1.09, 2.49]),
        ('Walkers Cheese & Onion', [32.5, 65, 150], [0.59, 1.09, 2.49]),
        ('Walkers Salt & Vinegar', [32.5, 65, 150], [0.59, 1.09, 2.49]),
        ('Pringles Original', [165, 200], [2.29, 2.79]),
        ('Pringles Sour Cream', [165, 200], [2.29, 2.79]),
        ('Doritos Cool Original', [150, 180], [1.89, 2.49]),
        ('Doritos Tangy Cheese', [150, 180], [1.89, 2.49]),
        ('Cheetos Twisted', [85], [1.39]),
        ('Kettle Chips Sea Salt', [150], [2.19]),
        ('Kettle Chips Mature Cheddar', [150], [2.19]),
        ('McCoy\'s Salt & Malt Vinegar', [85], [1.49]),
        ('Tyrrells Sea Salt', [150], [2.49]),
    ],
    'Wines': [
        ('19 Crimes Chardonnay White Wine', [750], [11.29]),
        ('19 Crimes Red Blend', [750], [11.29]),
        ('Yellowtail Shiraz', [750], [8.99]),
        ('Yellowtail Chardonnay', [750], [8.99]),
        ('Barefoot Merlot', [750], [7.99]),
        ('Barefoot Pinot Grigio', [750], [7.99]),
        ('Hardy\'s VR Shiraz', [750], [6.99]),
        ('Blossom Hill White', [750], [5.99]),
        ('Echo Falls White Zinfandel', [750], [6.49]),
        ('Lambrini Original', [750], [3.99]),
    ],
    'Beers': [
        ('Stella Artois Lager', [440, 660], [1.89, 2.99]),
        ('Budweiser Lager', [440, 660], [1.69, 2.79]),
        ('Guinness Draught', [440, 500], [2.19, 2.59]),
        ('Heineken Lager', [440, 650], [1.99, 2.89]),
        ('Corona Extra', [330, 355], [1.99, 2.19]),
        ('Carlsberg Pilsner', [440, 568], [1.79, 2.49]),
        ('Peroni Nastro Azzurro', [330, 660], [1.99, 3.49]),
        ('San Miguel Lager', [330, 660], [1.89, 3.29]),
        ('Desperados Tequila Beer', [330, 650], [1.99, 3.49]),
        ('Old Speckled Hen', [500], [2.29]),
    ],
    'Spirits': [
        ('Jack Daniels Tennessee Whiskey', [700], [25.99]),
        ('Smirnoff Vodka', [350, 700], [13.99, 18.99]),
        ('Gordon\'s London Dry Gin', [350, 700], [11.99, 16.99]),
        ('Bacardi Carta Blanca Rum', [350, 700], [11.99, 17.49]),
        ('Captain Morgan Spiced Gold Rum', [350, 700], [11.99, 16.99]),
        ('Jameson Irish Whiskey', [350, 700], [15.99, 24.99]),
        ('Famous Grouse Scotch Whisky', [700], [19.99]),
        ('Bells Original Whisky', [700], [18.99]),
        ('Glenfiddich 12 Year Old', [700], [34.99]),
        ('Absolut Vodka', [700], [19.99]),
    ],
    'Liqueurs': [
        ('Baileys Original Irish Cream', [350, 700], [9.99, 15.99]),
        ('Baileys Strawberries & Cream', [700], [15.99]),
        ('Malibu Caribbean Rum', [700], [15.99]),
        ('Disaronno Amaretto', [700], [19.99]),
        ('Jagermeister', [350, 700], [12.99, 21.99]),
        ('Kahlua Coffee Liqueur', [700], [16.99]),
        ('Tia Maria Coffee Liqueur', [700], [15.99]),
    ],
    'Coffee • Tea': [
        ('Nescafe Gold Blend', [100, 200], [5.99, 9.99]),
        ('Nescafe Original', [100, 200], [4.99, 8.99]),
        ('Douwe Egberts Pure Gold', [95, 190], [5.49, 9.49]),
        ('Kenco Smooth', [100, 200], [5.99, 9.99]),
        ('Nestle Coffee Mate', [400, 500], [3.99, 4.99]),
        ('PG Tips Tea Bags', [80, 160, 240], [2.99, 4.99, 6.99]),
        ('Tetley Tea Bags', [80, 160, 240], [2.79, 4.79, 6.79]),
        ('Yorkshire Tea Bags', [80, 160, 240], [2.99, 4.99, 6.99]),
        ('Twinings English Breakfast', [80, 200], [3.49, 6.99]),
    ],
    'Breakfast Cereals': [
        ('Kellogg\'s Corn Flakes', [500, 750], [3.29, 4.49]),
        ('Kellogg\'s Coco Pops', [480, 720], [3.49, 4.99]),
        ('Kellogg\'s Frosties', [500, 750], [3.49, 4.99]),
        ('Kellogg\'s Special K', [500, 550], [3.99, 4.99]),
        ('Nestle Cheerios', [375, 600], [2.99, 4.49]),
        ('Nestle Shreddies', [415, 675], [2.99, 4.49]),
        ('Weetabix Original', [24, 48, 72], [2.49, 3.99, 5.49]),
        ('Quaker Oats So Simple', [324, 432], [2.99, 3.99]),
    ],
    'Biscuits • Cookies': [
        ('McVitie\'s Digestives', [300, 400, 500], [1.49, 1.99, 2.49]),
        ('McVitie\'s Chocolate Digestives', [266, 433], [1.79, 2.79]),
        ('McVitie\'s Hobnobs', [300, 500], [1.49, 2.49]),
        ('Oreo Original', [154, 220, 330], [1.29, 1.79, 2.79]),
        ('Jaffa Cakes', [110, 122, 300], [0.99, 1.19, 2.49]),
        ('Maryland Cookies', [145, 200], [1.29, 1.79]),
        ('Fox\'s Golden Crunch', [200], [1.49]),
        ('Jammie Dodgers', [140], [1.29]),
    ],
    'Bakery • Bread': [
        ('Warburtons Medium Sliced Bread', [400, 800], [0.99, 1.29]),
        ('Warburtons Toastie Bread', [800], [1.39]),
        ('Hovis Wholemeal Bread', [800], [1.39]),
        ('Hovis Soft White Bread', [800], [1.29]),
        ('Kingsmill Soft White Bread', [800], [1.19]),
        ('Kingsmill 50/50 Bread', [800], [1.29]),
        ('Warburtons Crumpets', [6, 8], [0.99, 1.29]),
        ('Warburtons Teacakes', [6], [1.09]),
    ],
    'Cheese • Dairy': [
        ('Cathedral City Mature Cheddar', [200, 350, 550], [3.29, 4.99, 7.49]),
        ('Philadelphia Soft Cheese', [180, 280], [2.29, 3.29]),
        ('Muller Corner Vanilla', [135], [0.75]),
        ('Muller Corner Strawberry', [135], [0.75]),
        ('Muller Rice Original', [190], [0.85]),
        ('Danone Activia Yogurt', [125], [0.69]),
        ('Yeo Valley Natural Yogurt', [500], [2.49]),
    ],
    'Butter • Spreads': [
        ('Lurpak Butter', [250, 500], [3.79, 6.99]),
        ('Lurpak Spreadable', [250, 500], [3.99, 7.29]),
        ('Anchor Butter', [250, 500], [3.49, 6.49]),
        ('Flora Original', [500], [2.99]),
        ('I Can\'t Believe It\'s Not Butter', [500], [2.79]),
    ],
    'Spreads • Jams': [
        ('Nutella Hazelnut Spread', [350, 400, 750], [3.49, 3.99, 6.99]),
        ('Bonne Maman Strawberry Jam', [370], [2.49]),
        ('Hartley\'s Best Raspberry Jam', [340], [1.99]),
        ('Marmite Original', [250], [3.49]),
        ('Peanut Butter Smooth', [340, 454], [2.29, 2.99]),
    ],
    'Condiments • Sauces': [
        ('Heinz Tomato Ketchup', [460, 910], [2.49, 3.99]),
        ('Heinz Mayonnaise', [400], [2.79]),
        ('Hellmann\'s Real Mayonnaise', [400, 600], [2.99, 4.49]),
        ('HP Brown Sauce', [255, 425], [2.19, 3.19]),
        ('Colman\'s English Mustard', [100], [1.99]),
        ('French\'s American Mustard', [226], [1.79]),
    ],
    'Cooking Ingredients': [
        ('Natco Coconut Milk', [400], [1.39]),
        ('Blue Dragon Soy Sauce', [150], [1.99]),
        ('Sharwood\'s Curry Paste', [227], [2.49]),
        ('Uncle Ben\'s Basmati Rice', [500, 1000], [2.49, 4.49]),
        ('Tilda Pure Basmati Rice', [500, 1000], [2.79, 4.99]),
    ],
    'Spices • Seasonings': [
        ('Rajah Curry Powder', [100], [2.19]),
        ('MDH Garam Masala', [100], [2.89]),
        ('Schwartz Mixed Herbs', [10], [1.49]),
        ('Schwartz Ground Cinnamon', [28], [1.99]),
        ('Schwartz Paprika', [30], [1.99]),
    ],
    'Indian Snacks': [
        ('Haldiram\'s Bhujia', [200, 400], [2.79, 4.99]),
        ('Haldiram\'s Aloo Bhujia', [200], [2.79]),
        ('Bikaji Aloo Bhujia', [400], [3.99]),
        ('Ajmi Pappadums', [200], [2.39]),
    ],
    'Rice • Grains': [
        ('Laila Basmati Rice', [2000, 5000, 10000], [5.99, 12.99, 22.99]),
        ('TRS Red Lentils', [1000, 2000], [3.99, 6.99]),
        ('TRS Chana Dal', [2000], [6.99]),
    ],
    'Household': [
        ('Andrex Classic Clean Toilet Tissue', [9, 18], [5.49, 9.99]),
        ('Andrex Gentle Clean Toilet Tissue', [9], [5.99]),
        ('Plenty Kitchen Roll', [2, 4], [3.29, 5.99]),
        ('Fairy Liquid Original', [433, 625, 900], [2.49, 2.99, 3.99]),
        ('Comfort Fabric Conditioner', [630, 1260], [2.99, 4.99]),
        ('Persil Washing Powder', [650, 1300], [4.29, 7.99]),
        ('Dettol Antibacterial Surface Spray', [500], [3.39]),
        ('Flash All Purpose Cleaner', [500], [2.99]),
        ('Cif Cream Cleaner', [500], [1.99]),
    ],
}

def generate_base_id_number(index):
    """Generate base UUID number for consistent ID generation"""
    return f"550e8400-e29b-41d4-a716-4466554{index:05d}"

def generate_image_hash(product_name):
    """
    Generate a consistent hash-based image ID for a product.
    Uses the base product name (without size) to ensure all size variants 
    of the same product have the same image URL.
    Format matches SumUp actual URLs: img_[UPPERCASE_ALPHANUMERIC_HASH]
    """
    # Create a hash from the base product name
    hash_input = product_name.encode('utf-8')
    hash_obj = hashlib.sha256(hash_input)
    # Get first 26 characters of the hash in uppercase alphanumeric format
    hash_hex = hash_obj.hexdigest().upper()
    # Convert to base32-like format (alphanumeric only, uppercase)
    hash_str = ''.join(c for c in hash_hex if c.isalnum())[:26]
    return hash_str


def generate_inventory():
    """Generate 710 product inventory"""
    products = []
    product_id = 1
    
    # Track how many products per category to balance distribution
    target_per_category = 710 // len(PRODUCT_TEMPLATES)
    
    for category, templates in PRODUCT_TEMPLATES.items():
        products_in_category = 0
        
        # Generate multiple variations per template
        for base_name, sizes, prices in templates:
            for i, size in enumerate(sizes):
                if product_id > 710:
                    break
                    
                # Create product name with size
                if 'ml' in str(size) or 'cl' in base_name.lower():
                    product_name = f"{base_name} {size}ml"
                elif size < 100:  # Small items in grams
                    product_name = f"{base_name} {size}g"
                elif size >= 1000:  # Large items
                    if category in ['Rice • Grains', 'Cooking Ingredients']:
                        product_name = f"{base_name} {size//1000}kg"
                    else:
                        product_name = f"{base_name} {size}ml"
                else:
                    product_name = f"{base_name} {size}g"
                
                # Price for this size variant
                price = prices[min(i, len(prices)-1)]
                
                # Random quantity between 0 and 50
                quantity = random.randint(0, 50)
                
                # Generate image URL using hash format (same for all sizes of same product)
                # Format: https://images.sumup.com/img_[HASH]
                image_hash = generate_image_hash(base_name)
                image_url = f"https://images.sumup.com/img_{image_hash}"
                
                # Generate UUID
                item_id = generate_base_id_number(product_id)
                
                products.append({
                    'Item name': product_name,
                    'Price': f"{price:.2f}",
                    'Quantity': str(quantity),
                    'Category': category,
                    'Image 1': image_url,
                    'Item id': item_id
                })
                
                product_id += 1
                products_in_category += 1
                
                if products_in_category >= target_per_category and product_id <= 710:
                    break
            
            if products_in_category >= target_per_category and product_id <= 710:
                break
    
    # If we still need more products to reach 710, add variations
    while len(products) < 710:
        # Pick random category and template
        category = random.choice(list(PRODUCT_TEMPLATES.keys()))
        template = random.choice(PRODUCT_TEMPLATES[category])
        base_name, sizes, prices = template
        
        # Pick random size
        idx = random.randint(0, len(sizes)-1)
        size = sizes[idx]
        price = prices[min(idx, len(prices)-1)]
        
        # Create product name
        if 'ml' in str(size) or 'cl' in base_name.lower():
            product_name = f"{base_name} {size}ml"
        elif size < 100:
            product_name = f"{base_name} {size}g"
        elif size >= 1000:
            if category in ['Rice • Grains', 'Cooking Ingredients']:
                product_name = f"{base_name} {size//1000}kg"
            else:
                product_name = f"{base_name} {size}ml"
        else:
            product_name = f"{base_name} {size}g"
        
        quantity = random.randint(0, 50)
        
        # Generate image URL using hash format (same for all sizes of same product)
        # Format: https://images.sumup.com/img_[HASH]
        image_hash = generate_image_hash(base_name)
        image_url = f"https://images.sumup.com/img_{image_hash}"
        
        item_id = generate_base_id_number(len(products) + 1)
        
        products.append({
            'Item name': product_name,
            'Price': f"{price:.2f}",
            'Quantity': str(quantity),
            'Category': category,
            'Image 1': image_url,
            'Item id': item_id
        })
    
    return products[:710]  # Ensure exactly 710

def main():
    """Generate and save inventory"""
    products = generate_inventory()
    
    # Write to CSV
    with open('shop_inventory.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Item name', 'Price', 'Quantity', 'Category', 'Image 1', 'Item id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    print(f"✓ Generated {len(products)} products")
    print(f"✓ Saved to shop_inventory.csv")
    
    # Show category distribution
    categories = {}
    for p in products:
        cat = p['Category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nCategory distribution:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:40} : {count:3} products")

if __name__ == '__main__':
    main()
