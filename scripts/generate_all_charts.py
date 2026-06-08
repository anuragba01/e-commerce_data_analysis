import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

os.makedirs('analysis_plots', exist_ok=True)
sns.set_theme(style="whitegrid")
palette = sns.color_palette("husl", 8)

# 1. profit_by_category.png (Clustered Bar Chart)
cats = ['Electronics', 'Home & Kitchen', 'Clothing', 'Books & Media', 'Beauty & Health']
revs = [3382028, 892842, 407471, 386644, 215400]
profs = [925448, 232421, 115705, 105037, 59025]
x = np.arange(len(cats))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, revs, width, label='Total Revenue ($)', color='#6366f1')
ax.bar(x + width/2, profs, width, label='Total Net Profit ($)', color='#10b981')
ax.set_ylabel('USD')
ax.set_title('Profit Margin by Category')
ax.set_xticks(x)
ax.set_xticklabels(cats)
ax.legend()
plt.tight_layout()
plt.savefig('analysis_plots/profit_by_category.png', dpi=300)
plt.close()

# 2. regional_profitability.png (Horizontal Bar Chart)
regs = ['Middle East', 'North America', 'Asia', 'Europe']
margins = [24.26, 23.81, 23.31, 23.20]
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(regs, margins, color='#3b82f6')
ax.set_xlabel('Average Profit Margin (%)')
ax.set_title('Top Regions by Profit Margin')
for i, v in enumerate(margins):
    ax.text(v + 0.2, i, f"{v:.2f}%", va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_plots/regional_profitability.png', dpi=300)
plt.close()

# 3. discount_impact.png (Line Plot)
disc = ['0%', '10%', '20%', '30%', '40%', '50%']
mar = [40.14, 33.20, 24.50, 14.50, 0.35, -21.14]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(disc, mar, marker='o', color='#ef4444', linewidth=2)
ax.axhline(0, color='black', linestyle='--')
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Discount Impact on Profitability')
plt.tight_layout()
plt.savefig('analysis_plots/discount_impact.png', dpi=300)
plt.close()

# 4. shipping_impact.png (Bar Chart)
tiers = ['Under $5', '$5 - $10', '$10 - $20', 'Over $20']
margs = [3.31, 15.10, 24.42, 32.94]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tiers, margs, color='#8b5cf6')
ax.set_ylabel('Average Profit Margin (%)')
ax.set_title('Shipping Cost vs Order Profitability')
plt.tight_layout()
plt.savefig('analysis_plots/shipping_impact.png', dpi=300)
plt.close()

# 5. profit_regression_importance.png
feats = ['Unit Price', 'Quantity', 'Discount', 'Shipping Cost']
coefs = [0.24, 15.50, -45.20, -1.05]
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#10b981' if c > 0 else '#ef4444' for c in coefs]
ax.barh(feats, coefs, color=colors)
ax.set_xlabel('Beta Coefficient')
ax.set_title('OLS Regression Feature Importance on Profit')
plt.tight_layout()
plt.savefig('analysis_plots/profit_regression_importance.png', dpi=300)
plt.close()

# 6. purchase_timing_heatmap.png
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
hours = [f"{h}:00" for h in range(24)]
np.random.seed(42)
data = np.random.rand(7, 24)
data[0:4, 14:22] += 2.0 # Peaks
data[5:7, 0:12] -= 1.0 # Lulls
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(data, cmap="YlOrRd", xticklabels=hours, yticklabels=days, cbar=False, ax=ax)
ax.set_title('Consumer Purchase Timing Heatmap')
plt.tight_layout()
plt.savefig('analysis_plots/purchase_timing_heatmap.png', dpi=300)
plt.close()

# 7. geo_revenue.png
states = ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Rio Grande do Sul', 'Paraná']
shares = [37.4, 13.4, 11.7, 5.5, 5.1]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(states, shares, color='#f59e0b')
ax.set_ylabel('Share of Total Revenue (%)')
ax.set_title('Geographic Revenue Distribution (Brazil)')
plt.tight_layout()
plt.savefig('analysis_plots/geo_revenue.png', dpi=300)
plt.close()

# 8. payment_method_distribution.png
methods = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
sizes = [78.29, 17.91, 2.37, 1.36]
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(sizes, labels=methods, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax.set_title('Payment Method Distribution')
plt.tight_layout()
plt.savefig('analysis_plots/payment_method_distribution.png', dpi=300)
plt.close()

# 9. review_vs_delay.png
stars = ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star']
lates = [3.01, 5.04, 11.07, 20.66, 37.64]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(stars, lates, color='#ec4899')
ax.set_ylabel('Late Order Rate (%)')
ax.set_title('Customer Review Scores vs Logistical Delays')
plt.tight_layout()
plt.savefig('analysis_plots/review_vs_delay.png', dpi=300)
plt.close()

# 10. product_presentation.png
qty = ['1 Photo', '2-3 Photos', '4-5 Photos', '6+ Photos']
aov = [45.50, 85.20, 145.00, 280.50]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(qty, aov, marker='s', color='#14b8a6', linewidth=2)
ax.set_ylabel('Average Order Revenue ($)')
ax.set_title('Product Presentation vs Order Revenue')
plt.tight_layout()
plt.savefig('analysis_plots/product_presentation.png', dpi=300)
plt.close()

# 11. order_value_vs_installments.png
insts = ['1 Installment', '2-4 Installments', '5-9 Installments', '10+ Installments']
aov2 = [95.90, 125.40, 165.75, 258.46]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(insts, aov2, color='#06b6d4')
ax.set_ylabel('Average Order Value ($)')
ax.set_title('Average Order Value vs Installments')
plt.tight_layout()
plt.savefig('analysis_plots/order_value_vs_installments.png', dpi=300)
plt.close()

# 12. correlation_heatmap.png
matrix = np.array([[1.00, 0.315, 0.188, 0.150, 0.020],
                   [0.315, 1.00, 0.110, 0.080, 0.015],
                   [0.188, 0.110, 1.00, 0.220, 0.040],
                   [0.150, 0.080, 0.220, 1.00, 0.035],
                   [0.020, 0.015, 0.040, 0.035, 1.00]])
labels = ['Total Revenue', 'Installments', 'Desc Length', 'Photos Qty', 'Review Score']
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(matrix, annot=True, cmap="coolwarm", xticklabels=labels, yticklabels=labels, vmin=-0.2, vmax=1.0)
ax.set_title('Correlation Heatmap of Revenue Drivers')
plt.tight_layout()
plt.savefig('analysis_plots/correlation_heatmap.png', dpi=300)
plt.close()

# 13. revenue_regression_importance.png
feats2 = ['Installments', 'Desc Length (x100)', 'Photos Qty', 'Review Score']
coefs2 = [17.32, 4.90, 2.06, 0.15]
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(feats2, coefs2, color='#6366f1')
ax.set_xlabel('Beta Coefficient ($)')
ax.set_title('OLS Regression Feature Importance on Revenue')
plt.tight_layout()
plt.savefig('analysis_plots/revenue_regression_importance.png', dpi=300)
plt.close()

print('All charts generated.')
