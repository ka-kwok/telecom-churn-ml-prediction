import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px

def page4_body():
    st.title("💻 Churn Prediction App")
    st.markdown("##### *AI-Powered Customer Retention Tool*")
    st.write("---")
    st.write("👈 Enter customer details on sidebar and click **Predict Churn** to see the result")
    
    # Load and prepare data
    @st.cache_data
    def load_and_prepare_data():
        try:
            # Get project root directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_encoded.csv")
            
            df_encoded = pd.read_csv(csv_path)
            
            # Drop bias-prone features (ethical AI compliance)
            drop_cols = ["gender_Male", "SeniorCitizen_Yes"]
            df_model = df_encoded.drop(columns=drop_cols, errors='ignore')
            
            # Split features and target
            X = df_model.drop(["Churn_Yes"], axis=1)
            y = df_model["Churn_Yes"]
            
            # Remove TotalCharges to avoid multicollinearity (highly correlated with tenure & MonthlyCharges)
            X = X.drop(["TotalCharges"], axis=1)
            
            return X, y, df_model
        except FileNotFoundError as e:
            st.error(f"Dataset file not found: {str(e)}")
            st.error(f"Expected location: {csv_path}")
            st.error("Please ensure the dataset files are in the correct location.")
            return None, None, None
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.error(f"Attempted path: {csv_path}")
            return None, None, None

    # Train model
    @st.cache_resource
    def train_final_model():
        X, y, df_model = load_and_prepare_data()
        if X is None:
            return None, None, None
            
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=89)
        best_model = LogisticRegression(C=1.0, max_iter=1000, random_state=89)
        best_model.fit(X_train, y_train)
        
        # Get feature importance
        feature_importance = pd.DataFrame({
            'Feature': X_train.columns,
            'Coefficient': best_model.coef_[0],
            'Importance': np.abs(best_model.coef_[0])
        }).sort_values('Importance', ascending=False)
        
        # Scaling parameters from original raw data with z-score normalization
        scaling_params = {
            'tenure': {'mean': 32.371149, 'std': 24.559481},
            'MonthlyCharges': {'mean': 64.761692, 'std': 30.090047},
            'NumInternetServices': {'mean': 2.037910, 'std': 1.847682}
        }
        
        return best_model, feature_importance, X_train.columns.tolist(), scaling_params

    # Load model and feature importance
    model, feature_importance, feature_columns, scaling_params = train_final_model()
    
    if model is None:
        st.error("Unable to load model. Please check data files.")
        return

    # Customer input sidebar
    st.sidebar.write("")
    st.sidebar.subheader("👤 Customer Information")
    
    # Create input fields
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        partner = st.selectbox("👫 Partner", ['Yes', 'No'])

    with col2:
        dependents = st.selectbox("👶 Dependents", ['Yes', 'No'])

    st.sidebar.write("📋 Contract Details")
    col3, col4 = st.sidebar.columns(2)

    with col3:
        tenure = st.number_input("📅 Tenure (months)", min_value=0, max_value=72, value=12)
        contract = st.selectbox("📄 Contract", ['Month-to-month', 'One year', 'Two year'])    
    
    with col4: 
        monthly_charges = st.number_input("💰 Monthly Charges ($)", min_value=18.0, max_value=120.0, value=65.0)
        
    st.sidebar.write("📋 Service Details")
    col5, col6 = st.sidebar.columns(2)
    
    with col5:
        
        payment_method = st.selectbox("� Payment Method", 
                                    ['Electronic check', 'Mailed check', 
                                     'Bank transfer (automatic)', 'Credit card (automatic)'])
        phone_service = st.selectbox("📞 Phone Service", ['Yes', 'No'])
        internet_service = st.selectbox("🌐 Internet Service", ['DSL', 'Fiber optic', 'No'])
        paperless_billing = st.selectbox("📧 Paperless Billing", ['Yes', 'No'])
        streaming_tv = st.sidebar.selectbox("📺 Streaming TV", ['Yes', 'No', 'No internet service'])
        streaming_movies = st.sidebar.selectbox("🎬 Streaming Movies", ['Yes', 'No', 'No internet service'])

    with col6:
        tech_support = st.sidebar.selectbox("� Tech Support", ['Yes', 'No', 'No internet service'])
        multiple_lines = st.selectbox("📱 Multiple Lines", ['Yes', 'No', 'No phone service'])
        online_security = st.selectbox("🛡️ Online Security", ['Yes', 'No', 'No internet service'])
        online_backup = st.selectbox("💾 Online Backup", ['Yes', 'No', 'No internet service'])
        device_protection = st.selectbox("📱 Device Protection", ['Yes', 'No', 'No internet service'])
        
    
    # Customer Type (derived feature)
    if phone_service == 'Yes' and internet_service != 'No':
        customer_type = 'Both'
    elif phone_service == 'Yes' and internet_service == 'No':
        customer_type = 'Phone only'
    elif phone_service == 'No' and internet_service != 'No':
        customer_type = 'Internet only'
    else:
        customer_type = 'Neither'
    
    # Number of Internet Services
    internet_services = [online_security, online_backup, device_protection, 
                        tech_support, streaming_tv, streaming_movies]
    num_internet_services = sum(1 for service in internet_services if service == 'Yes')

    def prepare_input_data(tenure_val, monthly_charges_val, num_services_val,
                          partner_val, dependents_val, phone_service_val, multiple_lines_val,
                          internet_service_val, online_security_val, online_backup_val,
                          device_protection_val, tech_support_val, streaming_tv_val, 
                          streaming_movies_val, contract_val, paperless_billing_val,
                          payment_method_val, customer_type_val):
        input_data = {}
        
        # Initialize all features to 0
        for col in feature_columns:
            input_data[col] = 0
            
        # Set numerical features with scaling
        input_data['tenure'] = (tenure_val - scaling_params['tenure']['mean']) / scaling_params['tenure']['std']
        input_data['MonthlyCharges'] = (monthly_charges_val - scaling_params['MonthlyCharges']['mean']) / scaling_params['MonthlyCharges']['std']
        input_data['NumInternetServices'] = (num_services_val - scaling_params['NumInternetServices']['mean']) / scaling_params['NumInternetServices']['std']
        
        # Set categorical features
        if f'Partner_{partner_val}' in feature_columns:
            input_data[f'Partner_{partner_val}'] = 1
        if f'Dependents_{dependents_val}' in feature_columns:
            input_data[f'Dependents_{dependents_val}'] = 1
        if f'PhoneService_{phone_service_val}' in feature_columns:
            input_data[f'PhoneService_{phone_service_val}'] = 1
        if f'MultipleLines_{multiple_lines_val}' in feature_columns:
            input_data[f'MultipleLines_{multiple_lines_val}'] = 1
        if f'InternetService_{internet_service_val}' in feature_columns:
            input_data[f'InternetService_{internet_service_val}'] = 1
        if f'OnlineSecurity_{online_security_val}' in feature_columns:
            input_data[f'OnlineSecurity_{online_security_val}'] = 1
            
        if f'OnlineBackup_{online_backup_val}' in feature_columns:
            input_data[f'OnlineBackup_{online_backup_val}'] = 1
        if f'DeviceProtection_{device_protection_val}' in feature_columns:
            input_data[f'DeviceProtection_{device_protection_val}'] = 1
        if f'TechSupport_{tech_support_val}' in feature_columns:
            input_data[f'TechSupport_{tech_support_val}'] = 1
        if f'StreamingTV_{streaming_tv_val}' in feature_columns:
            input_data[f'StreamingTV_{streaming_tv_val}'] = 1
        if f'StreamingMovies_{streaming_movies_val}' in feature_columns:
            input_data[f'StreamingMovies_{streaming_movies_val}'] = 1
        if f'Contract_{contract_val}' in feature_columns:
            input_data[f'Contract_{contract_val}'] = 1
        if f'PaperlessBilling_{paperless_billing_val}' in feature_columns:
            input_data[f'PaperlessBilling_{paperless_billing_val}'] = 1
        if f'PaymentMethod_{payment_method_val}' in feature_columns:
            input_data[f'PaymentMethod_{payment_method_val}'] = 1
        if f'CustomerType_{customer_type_val}' in feature_columns:
            input_data[f'CustomerType_{customer_type_val}'] = 1
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure all feature columns are present and in correct order
        input_df = input_df.reindex(columns=feature_columns, fill_value=0)
        
        return input_df

    # Make prediction
    if st.sidebar.button("🎯 Predict Churn", type="primary"):
        input_data = prepare_input_data(
            tenure, monthly_charges, num_internet_services,
            partner, dependents, phone_service, multiple_lines,
            internet_service, online_security, online_backup,
            device_protection, tech_support, streaming_tv,
            streaming_movies, contract, paperless_billing,
            payment_method, customer_type
        )
        
        # Make prediction
        churn_probability = model.predict_proba(input_data)[0][1]
        churn_prediction = model.predict(input_data)[0]
        
        # Display Results
        # Create columns for layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=churn_probability * 100,
                title={"text": "Churn Probability (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "red" if churn_prediction == 1 else "green"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgreen"},
                        {'range': [50, 100], 'color': "lightcoral"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        # Prediction interpretation
        if churn_probability > 0.7:
            st.error(f"🚨 **HIGH RISK**: {churn_probability:.1%} chance of churn")
            st.markdown("**Recommended Actions:**")
            st.markdown("- 🎯 Immediate retention campaign")
            st.markdown("- 📞 Personal outreach call")
            st.markdown("- 💰 Special discount offer")
        elif churn_probability > 0.4:
            st.warning(f"⚠️ **MEDIUM RISK**: {churn_probability:.1%} chance of churn")
            st.markdown("**Recommended Actions:**")
            st.markdown("- 📧 Targeted email campaign")
            st.markdown("- 🎁 Loyalty program enrollment")
            st.markdown("- 📊 Service satisfaction survey")
        else:
            st.success(f"✅ **LOW RISK**: {churn_probability:.1%} chance of churn")
            st.markdown("**Recommended Actions:**")
            st.markdown("- 😊 Maintain current service level")
            st.markdown("- 📈 Upselling opportunities")
            st.markdown("- 🌟 VIP program consideration")
        
        # Feature Impact Analysis
        st.subheader("📊 Key Factors Influencing Prediction")
        
        # Get top influential features for this prediction
        input_array = input_data.values[0]
        feature_contributions = model.coef_[0] * input_array
        
        # Create DataFrame for visualization
        contrib_df = pd.DataFrame({
            'Feature': feature_columns,
            'Contribution': feature_contributions,
            'Value': input_array
        })
        
        # Filter only non-zero contributions and get top 10
        contrib_df = contrib_df[contrib_df['Value'] != 0].copy()
        contrib_df['Abs_Contribution'] = np.abs(contrib_df['Contribution'])
        top_contrib = contrib_df.nlargest(10, 'Abs_Contribution')
        
        # Create horizontal bar chart
        fig = px.bar(
            top_contrib, 
            x='Contribution', 
            y='Feature',
            orientation='h',
            color='Contribution',
            color_continuous_scale='RdYlGn_r',
            title="Top 10 Features Impacting Prediction"
        )
        fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer Profile Summary
        st.subheader("👤 Customer Profile Summary")
        profile_col1, profile_col2 = st.columns(2)
        
        with profile_col1:
            st.markdown(f"""
            **📊 Account Details:**
            - Tenure: {tenure} months
            - Monthly Charges: ${monthly_charges:.2f}
            - Contract: {contract}
            - Payment: {payment_method}
            """)
            
        with profile_col2:
            st.markdown(f"""
            **🏠 Customer Info:**
            - Partner: {partner}
            - Dependents: {dependents}
            - Phone Service: {phone_service}
            - Internet: {internet_service}
            - Add-on Services: {num_internet_services}
            """)

    # Model information
    with st.expander("📈 Model Performance Information"):
        st.markdown("""
        **Model Details:**
        - Algorithm: Logistic Regression
        - Test Accuracy: 81.7%
        - Precision: 68.8%
        - Recall: 53.7%
        - ROC-AUC: 85.0%
        
        **Ethical AI Compliance:**
        - Age and gender features excluded to prevent bias
        - Fair prediction across all customer segments
        """)
        
        # Top Feature Importance
        st.subheader("🔝 Top 10 Most Important Features")
        top_features = feature_importance.head(10)
        
        fig = px.bar(
            top_features,
            x='Importance',
            y='Feature',
            orientation='h',
            title="Global Feature Importance"
        )
        fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")
