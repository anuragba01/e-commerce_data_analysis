# E-Commerce Revenue & Profitability Analysis

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue?style=for-the-badge&logo=github)](https://anuragba01.github.io/e-commerce_data_analysis/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

An e-commerce data analysis project focused on revenue, profitability, pricing, discounts, and customer purchasing behavior. Using two datasets, the project examines factors affecting profit margins, repeat purchases, average order value, and product sales. The findings are presented in an interactive dashboard, supported by statistical analysis and predictive modeling.

## Live Interactive Dashboard

Explore the analysis and visualizations in the live dashboard:

**[E-Commerce Analytics Dashboard](https://anuragba01.github.io/e-commerce_data_analysis/)**

---

## Project Overview

This project examines e-commerce performance from two perspectives: financial profitability and customer purchasing behavior.

### Key Objectives

1. **Revenue and Profitability:** Analyze the relationship between pricing, discounts, sales volume, product categories, and profit margins.
2. **Customer Behavior:** Examine repeat purchases, customer satisfaction, payment methods, and order values using Brazilian Olist marketplace data.
3. **Product Listings:** Investigate how product photos and descriptions relate to sales and conversion.
4. **Statistical Analysis and Prediction:** Use correlation, regression, and machine learning models to identify important business factors and estimate transaction profitability.

---

## Key Findings

- **Discounts and Profitability:** Discount levels showed a strong negative relationship with profit (\(r = -0.831\)). Transactions with discounts of 40% recorded an average loss of $1.09, increasing to $62.04 at 50% discounts. The analysis did not find a corresponding increase in order volume sufficient to offset these losses.

- **Pricing and Revenue:** Unit price had a stronger correlation with revenue (\(r = 0.739\)) than quantity sold (\(r = 0.333\)) in the analyzed dataset.

- **Customer Retention:** Analysis of more than 100,000 Brazilian marketplace orders found a repeat purchase rate of 3.05%. Repeat purchase rates were similar among customers who left 5-star and 1-star reviews: 3.31% and 3.22%, respectively.

- **Installment Payments and Order Value:** Orders paid in 10 installments had an average order value of $415, compared with $112 for upfront payments. This is an association in the data and does not establish that installment payments caused the difference.

- **Product Photos and Sales:** Listings with seven or more photos averaged 4.37 units sold, compared with 2.62 units for listings without photos.

---

## Repository Structure

```text
├── analysis_plots/             # Charts and visualizations
├── analysis_results/           # Summary data exported as CSV files
├── scripts/                    # Python analysis and modeling scripts
│   ├── run_analysis.py         # Financial and descriptive analysis
│   ├── run_olist_deep_dive.py  # Customer and marketplace analysis
│   ├── train_predictive_models.py
│   │                            # Regression and prediction models
│   ├── analyze_conversion.py   # Product page conversion analysis
│   ├── analyze_product_attributes.py
│   │                            # Product descriptions and photo analysis
│   ├── generate_chart.py       # Individual chart generation
│   └── generate_all_charts.py  # Batch chart generation
├── index.html                  # Dashboard layout
├── app.js                      # Dashboard interactions
├── charts.js                   # Chart.js configurations and data
├── styles.css                  # Dashboard styling and responsive layout
├── tailwind-config.js          # Tailwind configuration
└── .gitignore                  # Excluded files and directories
```

---

## Technology Stack

- **Data Analysis:** Python, Pandas, NumPy
- **Statistical Analysis and Modeling:** Scikit-learn, Statsmodels
- **Data Visualization:** Matplotlib, Seaborn, Chart.js
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Styling Configuration:** Tailwind CSS

---

## Getting Started

### Run the Dashboard Locally

The dashboard is a static web application and does not require a backend server.

1. Clone the repository:

   ```bash
   git clone https://github.com/anuragba01/e-commerce_data_analysis.git
   cd e-commerce_data_analysis
   ```

2. Start a local server:

   ```bash
   python3 -m http.server 8000
   ```

3. Open `http://localhost:8000` in your browser.

### Run the Python Analysis

1. Place the required dataset CSV files in the `files/` directory. Raw datasets are excluded from Git.

2. Create a virtual environment and install the dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pandas numpy scikit-learn statsmodels matplotlib seaborn
   ```

3. Run the analysis scripts:

   ```bash
   python scripts/run_analysis.py
   python scripts/run_olist_deep_dive.py
   ```

4. Train the prediction models:

   ```bash
   python scripts/train_predictive_models.py
   ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
