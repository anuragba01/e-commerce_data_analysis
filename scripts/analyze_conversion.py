import pandas as pd
import numpy as np

# Load datasets
products = pd.read_csv('files/olist_products_dataset.csv')
order_items = pd.read_csv('files/olist_order_items_dataset.csv')

# Calculate total units sold per product
sales_per_product = order_items.groupby('product_id').size().reset_index(name='units_sold')

# Left join to products (products with 0 sales will have NaN)
merged = pd.merge(products, sales_per_product, on='product_id', how='left')
merged['units_sold'] = merged['units_sold'].fillna(0)
merged['sold_at_least_one'] = merged['units_sold'] > 0

# Fill missing values for analysis
merged['product_photos_qty_filled'] = merged['product_photos_qty'].fillna(-1)
merged['product_name_lenght_filled'] = merged['product_name_lenght'].fillna(0)
merged['product_description_lenght_filled'] = merged['product_description_lenght'].fillna(0)

print("\n--- Image Quantity vs Sales Performance ---")
# Group by image quantity
photo_stats = merged.groupby('product_photos_qty_filled').agg(
    total_listings=('product_id', 'count'),
    listings_with_sales=('sold_at_least_one', 'sum'),
    avg_units_sold=('units_sold', 'mean')
).reset_index()
photo_stats['percent_listings_sold'] = (photo_stats['listings_with_sales'] / photo_stats['total_listings']) * 100
print(photo_stats.sort_values('product_photos_qty_filled').head(12).to_string(index=False))


print("\n--- Name Length vs Sales Performance ---")
merged['name_bin'] = pd.cut(merged['product_name_lenght_filled'], bins=[-1, 0, 20, 30, 40, 50, 60, 100], labels=['Empty/Null', '1-20', '21-30', '31-40', '41-50', '51-60', '60+'])
name_stats = merged.groupby('name_bin', observed=True).agg(
    total_listings=('product_id', 'count'),
    listings_with_sales=('sold_at_least_one', 'sum'),
    avg_units_sold=('units_sold', 'mean')
).reset_index()
name_stats['percent_listings_sold'] = (name_stats['listings_with_sales'] / name_stats['total_listings']) * 100
print(name_stats.to_string(index=False))


print("\n--- Description Length vs Sales Performance ---")
merged['desc_bin'] = pd.cut(merged['product_description_lenght_filled'], bins=[-1, 0, 250, 500, 1000, 2000, 5000], labels=['Empty/Null', '1-250', '251-500', '501-1000', '1001-2000', '2000+'])
desc_stats = merged.groupby('desc_bin', observed=True).agg(
    total_listings=('product_id', 'count'),
    listings_with_sales=('sold_at_least_one', 'sum'),
    avg_units_sold=('units_sold', 'mean')
).reset_index()
desc_stats['percent_listings_sold'] = (desc_stats['listings_with_sales'] / desc_stats['total_listings']) * 100
print(desc_stats.to_string(index=False))

