import matplotlib.pyplot as plt
import numpy as np
import os

# Create directory if not exists
os.makedirs('/home/anurag/qollab_project/anti/analysis_plots', exist_ok=True)

quarters = ['2021Q1', '2021Q2', '2021Q3', '2021Q4', 
            '2022Q1', '2022Q2', '2022Q3', '2022Q4', 
            '2023Q1', '2023Q2', '2023Q3', '2023Q4', 
            '2024Q1', '2024Q2', '2024Q3', '2024Q4']

hist_rev = [20, 80, 150, 230, 260, 280, 350, 420, 480, 550, 620, 600]
hist_q = quarters[:12]

# Forecast starts at 2023Q4
forecast_q = quarters[11:]
forecast_rev = [600, 640, 680, 700, 720]

# Truncated starts at 2023Q4
trunc_q = quarters[11:]
trunc_rev = [600, 450, 250, 150, 50]

plt.figure(figsize=(14, 6))

# Set background colors to match the image style slightly
plt.gca().set_facecolor('#f8fafc')
plt.gcf().patch.set_facecolor('#ffffff')

plt.plot(hist_q, hist_rev, color='#6366f1', marker='o', linestyle='-', linewidth=2, markersize=5, label='Historical Revenue')
plt.plot(forecast_q, forecast_rev, color='#10b981', marker='o', linestyle='--', linewidth=2, markersize=5, label='Forecast Projection')
plt.plot(trunc_q, trunc_rev, color='#ef4444', marker='o', linestyle=':', linewidth=2, markersize=5, label='Truncated Raw 2024')

# Fill between for historical to match the faint shadow in the original image
plt.fill_between(hist_q, hist_rev, color='#6366f1', alpha=0.05)

# Formatting
plt.title('E-Commerce Quarterly Sales Trend & Forecast', fontsize=14, pad=20, loc='left', color='#475569', fontweight='bold')
plt.grid(axis='y', linestyle='-', alpha=0.1, color='#000000')

# Formatting Y-axis to show $k
plt.yticks(np.arange(0, 900, 100), [f'${i}k' for i in range(0, 900, 100)])
plt.ylim(0, 800)

# Remove spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_color('#cbd5e1')

# Legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=3, frameon=False, fontsize=10, handletextpad=0.5)

plt.tight_layout()
plt.savefig('/home/anurag/qollab_project/anti/analysis_plots/quarterly_sales_trend.png', dpi=300, bbox_inches='tight')
print("Chart successfully generated at /home/anurag/qollab_project/anti/analysis_plots/quarterly_sales_trend.png")
