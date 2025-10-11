# 🎯 Churn Prediction App - User Guide

## Overview
The Churn Prediction App is an AI-powered tool that predicts customer churn probability based on the trained Logistic Regression model from your telecom churn analysis project.

## Features

### ✨ **Real-time Predictions**
- Input customer data through intuitive sidebar controls
- Get instant churn probability predictions
- Visual gauge showing risk level (Low/Medium/High)

### 📊 **Explainable AI**
- Feature impact analysis showing which factors drive the prediction
- Individual customer profile summary
- Top 10 features influencing the specific prediction

### 🎯 **Business Actions**
- **HIGH RISK (>70%)**: Immediate retention campaign, personal outreach, special discounts
- **MEDIUM RISK (40-70%)**: Targeted email campaigns, loyalty programs, satisfaction surveys  
- **LOW RISK (<40%)**: Maintain service level, upselling opportunities, VIP programs

### 🛡️ **Ethical AI Compliance**
- Age and gender features excluded to prevent bias
- Fair predictions across all customer segments

## How to Use

### 1. **Navigate to Churn Prediction Page**
- Launch the Streamlit app
- Go to the "Churn Prediction" page (Page 4)

### 2. **Input Customer Data**
Use the sidebar to enter customer information:

**📋 Customer Information:**
- Dependents: Whether customer has dependents
- Partner: Whether customer has a partner

**📋 Contract Details:**
- Tenure (months): How long customer has been with company
- Monthly Charges: Customer's monthly bill amount
- Phone Service: Phone service subscription

**📋 Service Details:**
- Contract: Month-to-month, One year, or Two year
- Payment Method: Electronic check, Mailed check, Bank transfer, Credit card
- Internet Service: DSL, Fiber optic, or No service
- Paperless Billing: Yes or No
- Multiple Lines: Phone line options
- Online Security: Security add-on service
- Online Backup: Backup add-on service
- Device Protection: Device protection service
- Tech Support: Technical support service
- Streaming TV: TV streaming service
- Streaming Movies: Movie streaming service

### 3. **Get Prediction**
- Click the "🎯 Predict Churn" button in the sidebar
- View the results in the main panel

### 4. **Interpret Results**

**🎯 Prediction Results:**
- **Probability Gauge**: Visual representation of churn risk
- **Risk Level**: Color-coded classification (Green/Yellow/Red)
- **Recommended Actions**: Business strategies based on risk level

**📊 Key Factors:**
- **Feature Impact Chart**: Shows which factors increase/decrease churn probability
- **Customer Profile**: Summary of entered information

## Model Performance

- **Algorithm**: Logistic Regression with C=1.0
- **Test Accuracy**: 81.7%
- **Precision**: 68.8%
- **Recall**: 53.7%
- **ROC-AUC**: 85.0%

## Technical Details

### Data Processing
- Uses one-hot encoded features from the final model
- Automatically handles feature engineering (CustomerType, NumInternetServices)
- Ensures feature alignment with training data

### Prediction Logic
- Loads pre-trained model with optimal hyperparameters
- Applies same preprocessing as training pipeline
- Provides probability scores and binary predictions

### Visualization
- Interactive Plotly gauge for probability display
- Horizontal bar charts for feature importance
- Color-coded risk levels for easy interpretation

## Tips for Best Results

1. **Accurate Data Entry**: Ensure all customer information is correct
2. **Complete Profiles**: Fill in all available customer details
3. **Regular Updates**: Update customer information as it changes
4. **Action Planning**: Use recommended actions as starting points for retention strategies

## Troubleshooting

**Common Issues:**
- **Model Loading Error**: Check that dataset files exist in `dataset/processed/`
- **Feature Mismatch**: Ensure all categorical values match training data
- **Performance Issues**: Model caching should improve response times after first use

**Contact Support:**
- Check data file paths if prediction fails
- Verify all required packages are installed
- Review console logs for detailed error messages