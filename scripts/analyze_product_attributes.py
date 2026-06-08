import pandas as pd
import numpy as np

# Load the datasets
products = pd.read_csv('files/olist_products_dataset.csv')
order_items = pd.read_csv('files/olist_order_items_dataset.csv')

# Merge to get sales data per product
merged = pd.merge(order_items, products, on='product_id', how='inner')

print("--- Analysis by Product Photos Quantity ---")
photo_stats = merged.groupby('product_photos_qty').agg(
    total_sold=('order_id', 'count'),
    avg_price=('price', 'mean')
).reset_index()
# Calculate percentage of total sales
total_sales = photo_stats['total_sold'].sum()
photo_stats['sales_percentage'] = (photo_stats['total_sold'] / total_sales) * 100
print(photo_stats.sort_values('product_photos_qty').head(10).to_string(index=False))

print("\n--- Analysis by Product Name Length ---")
# Bin the name lengths
merged['name_length_bin'] = pd.cut(merged['product_name_lenght'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
name_stats = merged.groupby('name_length_bin').agg(
    total_sold=('order_id', 'count'),
    avg_price=('price', 'mean')
).reset_index()
name_stats['sales_percentage'] = (name_stats['total_sold'] / total_sales) * 100
print(name_stats.to_string(index=False))

print("\n--- Analysis by Product Description Length ---")
# Bin the description lengths
merged['desc_length_bin'] = pd.cut(merged['product_description_lenght'], bins=[0, 250, 500, 1000, 2000, 5000], labels=['0-250', '251-500', '501-1000', '1001-2000', '2000+'])
desc_stats = merged.groupby('desc_length_bin').agg(
    total_sold=('order_id', 'count'),
    avg_price=('price', 'mean')
).reset_index()
desc_stats['sales_percentage'] = (desc_stats['total_sold'] / total_sales) * 100
print(desc_stats.to_string(index=False))

print("\n--- Correlations ---")
cols_to_correlate = ['price', 'freight_value', 'product_photos_qty', 'product_name_lenght', 'product_description_lenght']
print(merged[cols_to_correlate].corr())

