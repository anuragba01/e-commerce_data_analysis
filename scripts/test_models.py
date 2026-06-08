import os
import joblib
import pandas as pd

def test_models():
    # Paths to the serialized models
    model1_path = "models/dataset1_profitability_model.pkl"
    model2_path = "models/dataset2_revenue_model.pkl"

    print("=== E-Commerce Machine Learning Model Tester ===\n")

    # --- 1. Test Dataset 1: Profitability Predictor ---
    if os.path.exists(model1_path):
        print("1. Loading Dataset 1 (Profitability Predictor)...")
        model1 = joblib.load(model1_path)
        print("   [Success] Model loaded.")

        # Test case: Unit Price=$150, Quantity=3, Discount=15% (0.15), Shipping Cost=$12.50
        test_data_1 = pd.DataFrame([{
            'Unit_Price': 150.0,
            'Quantity': 3,
            'Discount': 0.15,
            'Shipping_Cost': 12.50
        }])
        
        predicted_margin = model1.predict(test_data_1)[0]
        print(f"   --> Input Configuration: Price=$150, Qty=3, Discount=15%, Shipping=$12.50")
        print(f"   --> Predicted Profit Margin: {predicted_margin:.2f}%\n")
    else:
        print(f"   [Error] Model file not found at {model1_path}. Run train_predictive_models.py first.\n")

    # --- 2. Test Dataset 2: Listing Revenue Predictor ---
    if os.path.exists(model2_path):
        print("2. Loading Dataset 2 (Revenue Predictor)...")
        model2 = joblib.load(model2_path)
        print("   [Success] Model loaded.")

        # Test case: Freight=$18.50, 5 Installments, 5 Photos, 800 Char Description, 1200g Weight, 15000 cm³ Volume
        test_data_2 = pd.DataFrame([{
            'freight_value': 18.50,
            'payment_installments': 5,
            'product_photos_qty': 5,
            'product_description_lenght': 800,
            'product_weight_g': 1200,
            'product_volume_cm3': 15000
        }])
        
        predicted_revenue = model2.predict(test_data_2)[0]
        print(f"   --> Input Configuration: Freight=$18.50, Installments=5, Photos=5, Desc=800 chars, Weight=1200g, Vol=15000cm³")
        print(f"   --> Predicted Order Revenue (Price): ${predicted_revenue:.2f}\n")
    else:
        print(f"   [Error] Model file not found at {model2_path}. Run train_predictive_models.py first.\n")

if __name__ == "__main__":
    test_models()
