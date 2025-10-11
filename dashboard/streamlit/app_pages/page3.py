import os
import streamlit as st

def page3_body():
    st.title("📊 Top 10 Churn Drivers")
    st.write("---")

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    @st.cache_data
    def load_data():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_cleaned.csv")
        df = pd.read_csv(csv_path)
        df_encoded = pd.get_dummies(df, drop_first=True)
        return df, df_encoded
    
    df, df_encoded = load_data()

    churned = df[df['Churn'] == 'Yes']
    retained = df[df['Churn'] == 'No']

    # KPI Metrics - Define top features using encoded dataframe
    correlation_matrix_temp = df_encoded.corr()
    correlation_with_churn_temp = correlation_matrix_temp["Churn_Yes"].abs().sort_values(ascending=False)
    
    # Get enough encoded features to ensure we have 10 unique ones
    seen_features = set()
    top_features_cols = []
    feature_data_mapping = {}  # Map display name to actual data source
    
    # Process encoded features one by one until we have 10 unique features
    for feature in correlation_with_churn_temp.index[1:]:  # Skip 'Churn_Yes' itself
        if len(top_features_cols) >= 10:
            break
            
        # Handle encoded categorical columns (e.g., 'InternetService_Fiber optic', 'Contract_Month-to-month')
        if '_' in feature and not feature.endswith(('_Yes', '_No')):
            # This is likely a categorical column with values
            original_name = feature.split('_')[0]  # Take the part before the first underscore
        elif '_Yes' in feature:
            original_name = feature.replace('_Yes', '')
        elif '_No' in feature:
            original_name = feature.replace('_No', '')
        else:
            original_name = feature
        
        # Check if this is a new unique feature
        if original_name not in seen_features:
            seen_features.add(original_name)
            
            # Determine which data source to use for metrics
            if original_name in df.columns:
                top_features_cols.append(original_name)
                feature_data_mapping[original_name] = 'original'
            else:
                # For encoded features, create a clean display name
                display_name = feature.replace('_', ' ').replace(' Yes', '').replace(' No', '')
                top_features_cols.append(display_name)
                feature_data_mapping[display_name] = feature  # Store the encoded column name

    # Layout: 5 columns per row
    for i in range(0, len(top_features_cols), 5):
        cols = st.columns(5)
        for j, feature in enumerate(top_features_cols[i:i+5]):
            with cols[j]:
                if df[feature].dtype == 'object':
                    # For categorical: show most frequent value
                    top_value = df[feature].mode()[0]
                    count = df[feature].value_counts()[top_value]
                    st.metric(label=f"{feature}", value=f"{top_value}", delta=f"{count:,} records")
                else:
                    # For numeric: show mean and std
                    mean_val = df[feature].mean()
                    std_val = df[feature].std()
                    st.metric(label=f"{feature}", value=f"{mean_val:.2f}", delta=f"±{std_val:.2f}")
    st.markdown("***Numeric drivers**: mean and std value, **categorical drivers**: most frequent value*")
    st.write("---")
    # Bar plot for top 10 features correlated with churn
    correlation_matrix = df_encoded.corr()
    correlation_with_churn = correlation_matrix["Churn_Yes"].abs().sort_values(ascending=False)
    top_10_features = correlation_with_churn.index[1:11]  # Exclude 'Churn_Yes' itself
    top_10_values = correlation_with_churn.values[1:11]  # Exclude 'Churn_Yes' itself
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=top_10_values, y=top_10_features, palette="viridis")

    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10)
        
    plt.title("Top 10 Features Correlated with Churn", fontsize=16)
    plt.xlabel("Absolute Correlation with Churn", fontsize=14)
    plt.ylabel("", fontsize=5)
    plt.show()
    st.pyplot(plt)

    st.write("---")

    # Filter for customers with internet service
    # Check which InternetService columns exist in the encoded dataframe
    internet_service_cols = [col for col in df_encoded.columns if col.startswith('InternetService_')]
    
    if internet_service_cols:
        # If we have InternetService columns, filter customers who have internet service
        # (i.e., not the reference category which was dropped)
        internet_mask = df_encoded[internet_service_cols].sum(axis=1) > 0
        internet_customers = df_encoded[internet_mask]
    else:
        # If no encoded columns, use original data
        internet_customers = df_encoded[df['InternetService'] != 'No']

    # Recalculate correlation for add-ons with churn
    potential_addon_cols = [
        "OnlineSecurity_Yes", "OnlineBackup_Yes", "DeviceProtection_Yes",
        "TechSupport_Yes", "StreamingTV_Yes", "StreamingMovies_Yes"
    ]
    
    # Filter to only include columns that actually exist in the dataframe
    add_on_cols = [col for col in potential_addon_cols if col in internet_customers.columns]
    
    if add_on_cols and "Churn_Yes" in internet_customers.columns:
        addon_corr_internet = internet_customers[add_on_cols + ["Churn_Yes"]].corr()["Churn_Yes"].abs().sort_values(ascending=False).head(6)
        addon_corr_internet = addon_corr_internet.drop("Churn_Yes").head(5)
    else:
        # Create dummy data if columns don't exist
        addon_corr_internet = pd.Series([], dtype=float)

    if len(addon_corr_internet) > 0:
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(x=addon_corr_internet.values, y=addon_corr_internet.index, palette="magma")

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10)
            
        plt.title("Top 5 Add-ons Correlated with Churn (Internet Customers)", fontsize=16)
        plt.xlabel("Absolute Correlation with Churn", fontsize=10)
        plt.ylabel("Internet Add-on", fontsize=10)
        plt.show()
        st.pyplot(plt)
    else:
        st.warning("⚠️ Add-on service data not available for correlation analysis.")

    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")