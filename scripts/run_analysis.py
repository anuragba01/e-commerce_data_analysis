import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create directories for saving results
os.makedirs('analysis_plots', exist_ok=True)
os.makedirs('analysis_results', exist_ok=True)

# Set matplotlib style for premium look
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['axes.edgecolor'] = '#dee2e6'
plt.rcParams['grid.color'] = '#e9ecef'
plt.rcParams['text.color'] = '#212529'
plt.rcParams['axes.labelcolor'] = '#212529'
plt.rcParams['xtick.color'] = '#495057'
plt.rcParams['ytick.color'] = '#495057'
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# Part 1: Profitability Analysis (ecommerce_sales_dataset.csv)
# -------------------------------------------------------------
print("Analyzing Profitability Dataset...")
df_prof = pd.read_csv('profit/ecommerce_sales_dataset.csv')

# Descriptive Statistics
desc_stats = df_prof.describe()
desc_stats.to_csv('analysis_results/profitability_descriptive_stats.csv')

# Category Analysis
cat_perf = df_prof.groupby('Category')[['Revenue', 'Profit', 'Profit_Margin_%']].agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Profit_Margin_%': 'mean'
}).sort_values(by='Profit', ascending=False)
cat_perf.to_csv('analysis_results/category_performance.csv')

# Plot 1: Profit & Revenue by Category
fig, ax1 = plt.subplots(figsize=(10, 6))
categories = cat_perf.index
x = np.arange(len(categories))
width = 0.35

rects1 = ax1.bar(x - width/2, cat_perf['Revenue'], width, label='Revenue', color='#4A90E2')
ax1.set_ylabel('Revenue ($)', color='#4A90E2')
ax1.tick_params(axis='y', labelcolor='#4A90E2')
ax1.set_title('Revenue vs. Net Profit by Product Category', fontsize=14, pad=15, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(categories, rotation=15)

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, cat_perf['Profit'], width, label='Profit', color='#2ECC71')
ax2.set_ylabel('Net Profit ($)', color='#2ECC71')
ax2.tick_params(axis='y', labelcolor='#2ECC71')

fig.tight_layout()
plt.savefig('analysis_plots/profit_by_category.png', dpi=300)
plt.close()

# Discount Impact Analysis
discount_perf = df_prof.groupby('Discount')[['Profit', 'Profit_Margin_%', 'Quantity', 'Revenue']].mean()
discount_perf.to_csv('analysis_results/discount_impact.csv')

# Plot 2: Discount Impact on Margin
plt.figure(figsize=(9, 5.5))
plt.plot(discount_perf.index * 100, discount_perf['Profit_Margin_%'], marker='o', linewidth=2.5, color='#E74C3C', label='Average Profit Margin (%)')
plt.axhline(0, color='#7F8C8D', linestyle='--', linewidth=1)
plt.title('Impact of Promotion Discounts on Net Profit Margin (%)', fontsize=13, pad=15, fontweight='bold')
plt.xlabel('Discount Applied (%)', fontsize=11)
plt.ylabel('Average Profit Margin (%)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

# Annotate values
for d, m in zip(discount_perf.index * 100, discount_perf['Profit_Margin_%']):
    plt.annotate(f"{m:.1f}%", (d, m), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('analysis_plots/discount_impact.png', dpi=300)
plt.close()

# Correlation Matrix
num_cols = df_prof.select_dtypes(include=[np.number]).columns
corr_matrix = df_prof[num_cols].corr()
corr_matrix.to_csv('analysis_results/profitability_correlations.csv')

# Plot 3: Correlation Heatmap (using matplotlib)
plt.figure(figsize=(10, 8))
im = plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(im)
plt.title('Correlation Matrix of Profitability Metrics', fontsize=14, pad=15, fontweight='bold')
plt.xticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns, rotation=45, ha='right')
plt.yticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns)

# Write correlation values in cells
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        val = corr_matrix.iloc[i, j]
        plt.text(j, i, f"{val:.2f}", ha='center', va='center', 
                 color='white' if abs(val) > 0.5 else 'black', fontsize=9)

plt.tight_layout()
plt.savefig('analysis_plots/correlation_heatmap.png', dpi=300)
plt.close()

# Regression Analysis using OLS via NumPy
# Predictors: Unit_Price, Quantity, Discount, Shipping_Cost
# Target: Profit
X_cols = ['Unit_Price', 'Quantity', 'Discount', 'Shipping_Cost']
Y_col = 'Profit'

Y = df_prof[Y_col].values
X = df_prof[X_cols].values
# Add intercept
X_intercept = np.hstack([np.ones((X.shape[0], 1)), X])

# Solve OLS: beta = (X^T X)^-1 X^T Y
beta, residuals, rank, s = np.linalg.lstsq(X_intercept, Y, rcond=None)

# Metrics
Y_pred = X_intercept @ beta
ss_tot = np.sum((Y - np.mean(Y))**2)
ss_res = np.sum((Y - Y_pred)**2)
r_sq = 1 - (ss_res / ss_tot)

# Save coefficients
coef_df = pd.DataFrame({
    'Feature': ['Intercept'] + X_cols,
    'Coefficient': beta
})
coef_df.to_csv('analysis_results/regression_coefficients.csv', index=False)

with open('analysis_results/regression_summary.txt', 'w') as f:
    f.write("=== MULTIPLE LINEAR REGRESSION SUMMARY (NumPy OLS) ===\n")
    f.write(f"Target Variable: {Y_col}\n")
    f.write(f"Predictors: {', '.join(X_cols)}\n")
    f.write(f"R-squared: {r_sq:.4f}\n\n")
    f.write("Coefficients:\n")
    for feat, coef in zip(['Intercept'] + X_cols, beta):
        f.write(f"  {feat:15s}: {coef:12.4f}\n")

# -------------------------------------------------------------
# Part 2: Operations & Customer Satisfaction (Olist Relational)
# -------------------------------------------------------------
print("Analyzing Olist Relational Database...")
# Load datasets
orders = pd.read_csv('files/olist_orders_dataset.csv')
customers = pd.read_csv('files/olist_customers_dataset.csv')
items = pd.read_csv('files/olist_order_items_dataset.csv')
reviews = pd.read_csv('files/olist_order_reviews_dataset.csv')
payments = pd.read_csv('files/olist_order_payments_dataset.csv')

# Drop invalid dates and convert to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Filter delivered orders
delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
delivered_orders = delivered_orders.dropna(subset=['order_delivered_customer_date'])

# Calculate times (in days)
delivered_orders['actual_delivery_days'] = (delivered_orders['order_delivered_customer_date'] - delivered_orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
delivered_orders['estimated_delivery_days'] = (delivered_orders['order_estimated_delivery_date'] - delivered_orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
delivered_orders['delivery_delay_days'] = (delivered_orders['order_delivered_customer_date'] - delivered_orders['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)
delivered_orders['is_late'] = delivered_orders['delivery_delay_days'] > 0

# Merge reviews to calculate delay vs review score
order_reviews = pd.merge(delivered_orders[['order_id', 'delivery_delay_days', 'actual_delivery_days', 'is_late']], reviews[['order_id', 'review_score']], on='order_id')

# Save review delay summary
review_delay_summary = order_reviews.groupby('review_score')[['delivery_delay_days', 'actual_delivery_days', 'is_late']].mean()
review_delay_summary.to_csv('analysis_results/olist_review_delay_summary.csv')

# Plot 4: Delivery Delay vs Review Score
plt.figure(figsize=(9, 5.5))
plt.bar(review_delay_summary.index, review_delay_summary['delivery_delay_days'], color='#E74C3C', alpha=0.85, width=0.6, edgecolor='#C0392B')
plt.axhline(0, color='#34495E', linestyle='-', linewidth=1)
plt.title('Average Delivery Delay (Days) vs. Customer Review Score', fontsize=13, pad=15, fontweight='bold')
plt.xlabel('Customer Review Score (Stars)', fontsize=11)
plt.ylabel('Average Delay (Days) -> Positive is Late', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.5, axis='y')

for score, delay in zip(review_delay_summary.index, review_delay_summary['delivery_delay_days']):
    plt.annotate(f"{delay:+.1f} days", (score, delay), textcoords="offset points", 
                 xytext=(0, 5 if delay >= 0 else -15), ha='center', fontsize=9, fontweight='bold',
                 color='#C0392B' if delay > 0 else '#27AE60')

plt.tight_layout()
plt.savefig('analysis_plots/review_vs_delay.png', dpi=300)
plt.close()

# Payment Method Analysis
payment_summary = payments.groupby('payment_type')['payment_value'].agg(['count', 'sum'])
payment_summary['percent_volume'] = (payment_summary['sum'] / payment_summary['sum'].sum()) * 100
payment_summary.to_csv('analysis_results/olist_payment_summary.csv')

# Plot 5: Payment Method Share
plt.figure(figsize=(7, 7))
labels = [label.replace('_', ' ').title() for label in payment_summary.index]
plt.pie(payment_summary['sum'], labels=labels, autopct='%1.1f%%', startangle=140, 
        colors=['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0'])
plt.title('Olist Transaction Volume Share by Payment Method', fontsize=13, pad=15, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_plots/payment_method_distribution.png', dpi=300)
plt.close()

# Geographic Analysis (Merge customer state)
customer_orders = pd.merge(delivered_orders[['order_id', 'customer_id']], customers[['customer_id', 'customer_state']], on='customer_id')
order_items = pd.merge(items[['order_id', 'price', 'freight_value']], customer_orders, on='order_id')
state_perf = order_items.groupby('customer_state').agg(
    order_count=('order_id', 'nunique'),
    total_sales=('price', 'sum'),
    avg_freight=('freight_value', 'mean')
).sort_values(by='total_sales', ascending=False)
state_perf.to_csv('analysis_results/olist_state_performance.csv')

print("Analysis and Visualization completed. Results stored in 'analysis_results/' and plots in 'analysis_plots/'!")
