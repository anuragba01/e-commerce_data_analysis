import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

def train_dataset1_profitability_model():
    print("Training Dataset 1: Profitability Model")
    
    ds1_path = "profit/ecommerce_sales_dataset.csv"
    if not os.path.exists(ds1_path):
        print(f"Dataset not found at {ds1_path}. Make sure you are in the project root.")
        return

    df = pd.read_csv(ds1_path)
    
    # We want to forecast 'Profit_Margin_%' based on price, quantity, discount, and shipping cost
    features = ['Unit_Price', 'Quantity', 'Discount', 'Shipping_Cost']
    target = 'Profit_Margin_%'
    
    # Clean data (ensure numeric, drop NaNs)
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"Model Accuracy (R-squared): {r2:.4f}")
    print(f"Mean Absolute Error: {mae:.2f}%")
    
    print("\nFeature Importances:")
    importances = pd.DataFrame({'Feature': features, 'Importance (%)': model.feature_importances_ * 100})
    importances = importances.sort_values(by='Importance (%)', ascending=False)
    print(importances.to_string(index=False))
    
    # Save the model
    os.makedirs("models", exist_ok=True)
    save_path = "models/dataset1_profitability_model.pkl"
    joblib.dump(model, save_path)
    print(f"Model saved to: {save_path}")


def train_dataset2_revenue_model():
    print("\nTraining Dataset 2: Revenue Prediction Model")
    
    base_dir = "files"
    orders_path = os.path.join(base_dir, "olist_orders_dataset.csv")
    
    if not os.path.exists(orders_path):
        print("Dataset 2 files not found. Check the 'files/' directory.")
        return
        
    orders = pd.read_csv(orders_path)
    items = pd.read_csv(os.path.join(base_dir, "olist_order_items_dataset.csv"))
    payments = pd.read_csv(os.path.join(base_dir, "olist_order_payments_dataset.csv"))
    products = pd.read_csv(os.path.join(base_dir, "olist_products_dataset.csv"))

    # Aggregate item data to order level
    order_summary = items.groupby('order_id').agg({
        'price': 'sum',            # Total revenue per order
        'freight_value': 'sum',
        'order_item_id': 'max',    # Number of items in order
        'product_id': 'first'
    }).reset_index()

    # Aggregate payment data
    payment_summary = payments.groupby('order_id').agg({
        'payment_installments': 'max'
    }).reset_index()

    # Merge everything
    df = orders[['order_id']].copy()
    df = df.merge(order_summary, on='order_id', how='inner')
    df = df.merge(payment_summary, on='order_id', how='left')
    df = df.merge(products, on='product_id', how='left')
    
    # Calculate volume
    df['product_volume_cm3'] = df['product_length_cm'] * df['product_height_cm'] * df['product_width_cm']

    features = [
        'freight_value', 
        'payment_installments', 
        'product_photos_qty', 
        'product_description_lenght',
        'product_weight_g',
        'product_volume_cm3'
    ]
    target = 'price' # Predicting the monetary value (revenue) of the items
    
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"Model Accuracy (R-squared): {r2:.4f}")
    print(f"Mean Absolute Error: ${mae:.2f}")
    
    print("\nFeature Importances:")
    importances = pd.DataFrame({'Feature': features, 'Importance (%)': model.feature_importances_ * 100})
    importances = importances.sort_values(by='Importance (%)', ascending=False)
    print(importances.to_string(index=False))
    
    # Save the model
    os.makedirs("models", exist_ok=True)
    save_path = "models/dataset2_revenue_model.pkl"
    joblib.dump(model, save_path)
    print(f"Model saved to: {save_path}")


if __name__ == "__main__":
    train_dataset1_profitability_model()
    train_dataset2_revenue_model()
