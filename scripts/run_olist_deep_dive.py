import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('analysis_plots', exist_ok=True)
os.makedirs('analysis_results', exist_ok=True)

# Set styles
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['axes.edgecolor'] = '#dee2e6'
plt.rcParams['grid.color'] = '#e9ecef'
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

print("Loading Olist Datasets...")
orders = pd.read_csv('files/olist_orders_dataset.csv')
customers = pd.read_csv('files/olist_customers_dataset.csv')
items = pd.read_csv('files/olist_order_items_dataset.csv')
reviews = pd.read_csv('files/olist_order_reviews_dataset.csv')
payments = pd.read_csv('files/olist_order_payments_dataset.csv')
products = pd.read_csv('files/olist_products_dataset.csv')
sellers = pd.read_csv('files/olist_sellers_dataset.csv')

# Convert timestamps to datetime
for col in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
    orders[col] = pd.to_datetime(orders[col])

# -------------------------------------------------------------
# 1. RFM Segmentation
# -------------------------------------------------------------
print("Performing RFM Analysis...")
# Get customer unique ID and order price info
cust_orders = pd.merge(orders[['order_id', 'customer_id', 'order_purchase_timestamp']], customers[['customer_id', 'customer_unique_id']], on='customer_id')
order_values = items.groupby('order_id')['price'].sum().reset_index()
rfm_df = pd.merge(cust_orders, order_values, on='order_id')

# Reference date (max date in dataset + 1 day)
ref_date = rfm_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# Group by unique customer ID
rfm = rfm_df.groupby('customer_unique_id').agg(
    Recency=('order_purchase_timestamp', lambda x: (ref_date - x.max()).days),
    Frequency=('order_id', 'count'),
    Monetary=('price', 'sum')
).reset_index()

# Save RFM summary statistics
rfm_stats = rfm.describe()
rfm_stats.to_csv('analysis_results/olist_rfm_descriptive_stats.csv')

# Repeat Purchase Rate
repeat_rate = (rfm['Frequency'] > 1).mean() * 100
with open('analysis_results/olist_loyalty_metrics.txt', 'w') as f:
    f.write(f"Total Unique Customers: {len(rfm)}\n")
    f.write(f"Repeat Purchase Rate: {repeat_rate:.2f}%\n")
    f.write(f"Max purchases by one customer: {rfm['Frequency'].max()}\n")

# -------------------------------------------------------------
# 2. Logistics Lead-Time Decomposition
# -------------------------------------------------------------
print("Decomposing Lead Times...")
delivered = orders[orders['order_status'] == 'delivered'].copy()
delivered = delivered.dropna(subset=['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

# Phase durations (in days)
delivered['approval_delay'] = (delivered['order_approved_at'] - delivered['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
delivered['dispatch_delay'] = (delivered['order_delivered_carrier_date'] - delivered['order_approved_at']).dt.total_seconds() / (24 * 3600)
delivered['transit_delay'] = (delivered['order_delivered_customer_date'] - delivered['order_delivered_carrier_date']).dt.total_seconds() / (24 * 3600)
delivered['total_delivery_time'] = (delivered['order_delivered_customer_date'] - delivered['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

lead_time_summary = delivered[['approval_delay', 'dispatch_delay', 'transit_delay', 'total_delivery_time']].mean()
lead_time_summary.to_csv('analysis_results/olist_lead_time_decomposition.csv')

# Plot Lead Time Decomposition
plt.figure(figsize=(8, 5))
components = ['Approval Delay', 'Seller Dispatch', 'Carrier Transit', 'Total Time']
means = [lead_time_summary['approval_delay'], lead_time_summary['dispatch_delay'], lead_time_summary['transit_delay'], lead_time_summary['total_delivery_time']]
plt.bar(components[:3], means[:3], color=['#FF9999', '#66B3FF', '#99FF99'], edgecolor='#7f7f7f', width=0.5)
plt.title('Average Lead Time Components (Days)', fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Days', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.5, axis='y')

for i, val in enumerate(means[:3]):
    plt.annotate(f"{val:.2f}d", (i, val), textcoords="offset points", xytext=(0,5), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('analysis_plots/lead_time_decomposition.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# 3. Seller Concentration (Pareto 80-20 Rule)
# -------------------------------------------------------------
print("Analyzing Seller Concentration...")
seller_sales = items.groupby('seller_id')['price'].sum().sort_values(ascending=False).reset_index()
seller_sales['cum_sales'] = seller_sales['price'].cumsum()
total_sales = seller_sales['price'].sum()
seller_sales['cum_percent'] = (seller_sales['cum_sales'] / total_sales) * 100
seller_sales['seller_percent'] = (seller_sales.index + 1) / len(seller_sales) * 100

# Find percentage of sellers that generate 80% of sales
sellers_80 = seller_sales[seller_sales['cum_percent'] >= 80].iloc[0]
with open('analysis_results/olist_seller_concentration.txt', 'w') as f:
    f.write(f"Total Active Sellers: {len(seller_sales)}\n")
    f.write(f"Top {sellers_80['seller_percent']:.2f}% of sellers generate 80% of revenue.\n")

# Plot Lorenz Curve
plt.figure(figsize=(7, 6))
plt.plot(seller_sales['seller_percent'], seller_sales['cum_percent'], color='#8E44AD', linewidth=2.5, label='Actual Distribution')
plt.plot([0, 100], [0, 100], 'k--', label='Line of Equality')
plt.title('Seller Sales Lorenz Curve (Revenue Concentration)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('% of Sellers (Sorted by Sales)', fontsize=11)
plt.ylabel('% of Cumulative Sales', fontsize=11)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('analysis_plots/seller_lorenz_curve.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# 4. Product Physical Dimensions vs. Freight Cost
# -------------------------------------------------------------
print("Analyzing Freight vs. Dimensions...")
# Merge items and products
prod_items = pd.merge(items[['product_id', 'price', 'freight_value']], products[['product_id', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']], on='product_id')
prod_items = prod_items.dropna()

# Calculate product volume (in cm^3)
prod_items['product_volume_cm3'] = prod_items['product_length_cm'] * prod_items['product_height_cm'] * prod_items['product_width_cm']

# Correlation matrix
dim_corr = prod_items[['freight_value', 'product_weight_g', 'product_volume_cm3', 'price']].corr()
dim_corr.to_csv('analysis_results/olist_freight_dimension_correlation.csv')

# -------------------------------------------------------------
# 5. Credit Card Installments & Order Values
# -------------------------------------------------------------
print("Analyzing Installment Payments...")
cc_payments = payments[payments['payment_type'] == 'credit_card'].copy()
installment_summary = cc_payments.groupby('payment_installments')['payment_value'].agg(['count', 'mean'])
installment_summary.to_csv('analysis_results/olist_installments_summary.csv')

# Plot Installment Average Transaction Value
plt.figure(figsize=(9, 5))
valid_installments = installment_summary[installment_summary.index <= 15]
plt.bar(valid_installments.index, valid_installments['mean'], color='#F39C12', alpha=0.85, width=0.6, edgecolor='#D35400')
plt.title('Average Order Value vs. Number of Credit Card Installments', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Number of Installments', fontsize=11)
plt.ylabel('Average Payment Value ($)', fontsize=11)
plt.xticks(valid_installments.index)
plt.grid(True, linestyle=':', alpha=0.5, axis='y')
plt.tight_layout()
plt.savefig('analysis_plots/order_value_vs_installments.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# 6. Payment Processing Latency (Boleto vs Credit Card)
# -------------------------------------------------------------
print("Analyzing Payment Approval Latencies...")
# Merge orders and payments
order_p = pd.merge(orders[['order_id', 'order_purchase_timestamp', 'order_approved_at']], payments[['order_id', 'payment_type']], on='order_id')
order_p = order_p.dropna()
order_p['approval_delay_hours'] = (order_p['order_approved_at'] - order_p['order_purchase_timestamp']).dt.total_seconds() / 3600

latency_summary = order_p.groupby('payment_type')['approval_delay_hours'].agg(['count', 'mean', 'median'])
latency_summary.to_csv('analysis_results/olist_payment_approval_latency.csv')

print("Olist Deep Dive completed. CSVs generated in 'analysis_results/' and plots in 'analysis_plots/'!")
