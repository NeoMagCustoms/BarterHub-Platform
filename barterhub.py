import sqlite3
import os

# Create fresh database
db_path = "barterhub.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create categories table
cursor.execute("""
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
)
""")

# Insert helper functions
def insert_category(name, parent_id=None):
    cursor.execute(
        "INSERT INTO categories (name, parent_id) VALUES (?, ?)", 
        (name, parent_id)
    )
    return cursor.lastrowid

def insert_tree(tree, parent_id=None):
    if isinstance(tree, dict):
        for category, subtree in tree.items():
            node_id = insert_category(category, parent_id)
            insert_tree(subtree, node_id)
    elif isinstance(tree, list):
        for item in tree:
            insert_category(item, parent_id)

# Complete Categories & Subcategories for Launch
categories_tree = {
    "Electronics": {
        "Computers & Accessories": ["Laptops", "Desktops", "Components"],
        "Phones & Tablets": ["Smartphones", "Tablets"],
        "Gaming": ["Consoles", "Accessories"],
        "Home Entertainment": ["TVs", "Audio Systems"]
    },
    "Books, Movies & Music": {
        "Books": ["Fiction", "Non-Fiction"],
        "Movies": ["Action", "Comedy"],
        "Music": ["Rock", "Jazz"]
    },
    "Clothing & Accessories": {
        "Men's Clothing": ["Tops", "Bottoms"],
        "Women's Clothing": ["Tops", "Dresses"],
        "Accessories": ["Shoes", "Jewelry", "Bags"]
    },
    "Collectibles & Antiques": {
        "Collectibles": ["Coins", "Cards"],
        "Antiques": ["Furniture", "Decorative Art"]
    },
    "Food & Beverages": {
        "Seeds & Spices": ["Vegetable Seeds", "Herbs & Spices"]
    },
    "Home & Furniture": {
        "Furniture": ["Living Room", "Bedroom"],
        "Decor": ["Artwork", "Mirrors"],
        "Storage": ["Shelves", "Containers"]
    },
    "Miscellaneous": ["General Merchandise", "Craft Supplies", "Office Supplies"],
    "Pets & Animal Supplies": {
        "Dogs": ["Toys", "Beds"],
        "Cats": ["Litter & Accessories", "Toys"],
        "Small Animals": ["Food", "Cages"]
    },
    "Sports & Outdoor": ["Camping Gear", "Fitness Equipment", "Outdoor Recreation"],
    "Tools & Equipment": ["Hand Tools", "Power Tools", "Garden Tools"],
    "Toys & Games": ["Board Games", "Educational Toys", "Video Games"],
    "Vehicles & Transportation": {
        "Cars": ["Sedans", "SUVs", "Trucks"],
        "Bicycles": ["Mountain Bikes", "Road Bikes"],
        "Automotive Parts": ["Tires", "Accessories"],
        "Other Transportation": ["RVs", "Trailers"]
    }
}

# Populate database
insert_tree(categories_tree)

conn.commit()
conn.close()

print("✅ BarterHub database initialized and fully populated.")
