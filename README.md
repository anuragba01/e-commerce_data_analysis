# E-Commerce Revenue & Profitability Analysis

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue?style=for-the-badge&logo=github)](https://anuragba01.github.io/e-commerce_data_analysis/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

An end-to-end data science and business intelligence project designed to analyze and optimize e-commerce financial performance and customer behavior. This project leverages two distinct real-world datasets to identify the core drivers of revenue growth, pinpoint profit erosion leaks, and deploy predictive models to forecast transaction viability.

## 📊 Live Interactive Dashboard
The results of this analysis are visualized in a responsive, interactive web dashboard. You can access the live dashboard here:  
👉 **[Live E-Commerce Analytics Dashboard](https://anuragba01.github.io/e-commerce_data_analysis/)**

---

## 🔍 Project Overview & Objectives
This project investigates the dual pillars of e-commerce sustainability: **short-term financial profitability** and **long-term customer-driven revenue expansion**. 

### Core Analytical Objectives:
1.  **Profitability Analysis (Dataset 1):** Isolate the financial impact of discounting strategies, pricing power, and product category mix on net profit margins.
2.  **Customer Behavior & Marketplace Operations (Dataset 2):** Investigate Brazilian Olist marketplace data to understand customer retention, the influence of visual merchandising on sales velocity, and the effect of payment flexibility on Average Order Value (AOV).
3.  **Predictive Modeling:** Build machine learning models (Gradient Boosting) and statistical regression models (Ordinary Least Squares) to forecast transaction profitability and recommend margin-defense policies.

---

## 💡 Key Analytical Findings

*   **The Catastrophic Impact of Discount Erosion:** The regression and correlation analysis ($r = -0.831$) proved that promotional discounts exceeding a **30% ceiling** destroy net margins. At a 40% discount, transactions hit break-even ($-\$1.09$ average), and at 50%, they run at a severe loss ($-\$62.04$ average). Discounts do *not* drive a compensating surge in order volume.
*   **Pricing Power Wins Over Raw Volume:** Unit Price has a far stronger correlation to total revenue ($r = +0.739$) than Quantity Sold ($r = +0.333$). Scaling gross revenue is best achieved by selling premium items rather than pursuing aggressive high-volume, low-ticket sales.
*   **The "Retention Crisis":** Analysis of 100k+ Brazilian orders revealed a dismal **3.05% customer repeat purchase rate**. Surprisingly, high customer satisfaction does not drive brand loyalty: 5-star reviewers return at a nearly identical rate (3.31%) to 1-star reviewers (3.22%).
*   **Payment Installments as a Revenue Multiplier:** Allowing customers to utilize 10-tier installment payment plans unlocked massive purchasing power, multiplying the Average Order Value (AOV) by **271%** (from \$112 for upfront payments to \$415 for 10 installments).
*   **Visual Merchandising Drives Sales Velocity:** Listings with comprehensive photo galleries (7+ photos) sold an average of **4.37 units**, compared to only **2.62 units** for listings with no photos.

---

## 📁 Repository Structure

```text
├── analysis_plots/        # Pre-rendered charts and visualizations used in the dashboard
├── analysis_results/      # Extracted summary CSV data from the Python analysis pipelines
├── scripts/               # Core Python data science and machine learning codebase
│   ├── run_analysis.py            # Descriptive statistics and financial calculations (Dataset 1)
│   ├── run_olist_deep_dive.py     # Relational merges, RFM analysis, and operational analysis (Dataset 2)
│   ├── train_predictive_models.py # Trains Gradient Boosting regressor and OLS models
│   ├── analyze_conversion.py      # Cleans, imputes, and models product detail page conversion
│   ├── analyze_product_attributes.py # Regression on product description lengths and photo quantities
│   ├── generate_chart.py          # Script for building specific matplotlib charts
│   └── generate_all_charts.py     # Automated batch visualization generator
├── index.html             # Interactive frontend HTML dashboard layout
├── app.js                 # Dashboard user interaction and dataset-toggle controller logic
├── charts.js              # Chart.js configurations and data injection pipelines
├── styles.css             # Vanilla CSS design system (dark mode, glassmorphism, responsive grids)
├── tailwind-config.js     # Typography and spacing configuration parameters
└── .gitignore             # Configured to ignore raw datasets, virtual environments, and reports
```

---

## 🛠️ Technology Stack
*   **Data Analysis & Modeling:** Python 3.8+, Pandas, NumPy, Scikit-Learn, Statsmodels
*   **Visualizations:** Matplotlib, Seaborn
*   **Web Frontend:** HTML5, CSS3, JavaScript (ES6+), Chart.js, Tailwind CSS (configuration)

---

## 🚀 Getting Started

### Running the Interactive Dashboard locally:
Since the dashboard is a client-side static web application, you do not need a backend server:
1.  Clone this repository:
    ```bash
    git clone https://github.com/anuragba01/e-commerce_data_analysis.git
    cd e-commerce_data_analysis
    ```
2.  Open `index.html` directly in any modern web browser, or serve it using a local utility:
    ```bash
    # Using python to serve locally
    python3 -m http.server 8000
    ```
3.  Navigate to `http://localhost:8000` in your browser.

### Running the Python Data Pipelines:
If you wish to re-run the data analysis or train the predictive models:
1.  Ensure you have your raw dataset CSV files placed in a `files/` directory (these are ignored from Git).
2.  Set up a Python virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install pandas numpy scikit-learn statsmodels matplotlib seaborn
    ```
3.  Execute the main analysis deep dive:
    ```bash
    python scripts/run_olist_deep_dive.py
    python scripts/run_analysis.py
    ```
4.  Train and save the machine learning models:
    ```bash
    python scripts/train_predictive_models.py
    ```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
