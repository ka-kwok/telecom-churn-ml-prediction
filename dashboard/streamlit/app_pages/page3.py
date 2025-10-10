import os
import streamlit as st

def page3_body():
    st.title("📊 Top 10 Churn Predictors")
    st.write("---")

    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu

    @st.cache_data
    def load_data():
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_cleaned.csv")
        df = pd.read_csv(csv_path)
        df_encoded = pd.get_dummies(df, drop_first=True)
        return df, df_encoded
    
    df, df_encoded = load_data()

    churned = df[df['Churn'] == 'Yes']
    retained = df[df['Churn'] == 'No']

    # Bar plot for top 10 features correlated with churn
    correlation_matrix = df_encoded.corr()
    correlation_with_churn = correlation_matrix["Churn_Yes"].abs().sort_values(ascending=False)
    top_10_features = correlation_with_churn.index[1:11]  # Exclude 'Churn_Yes' itself
    top_10_values = correlation_with_churn[1:11]  # Exclude 'Churn_Yes' itself
    
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
    internet_customers = df_encoded[df_encoded["InternetService_No"] == 0]

    # Recalculate correlation for add-ons with churn
    add_on_cols = [
        "OnlineSecurity_Yes", "OnlineBackup_Yes", "DeviceProtection_Yes",
        "TechSupport_Yes", "StreamingTV_Yes", "StreamingMovies_Yes"
    ]
    addon_corr_internet = internet_customers[add_on_cols + ["Churn_Yes"]].corr()["Churn_Yes"].abs().sort_values(ascending=False).head(6)
    addon_corr_internet = addon_corr_internet.drop("Churn_Yes").head(5)

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=addon_corr_internet.values, y=addon_corr_internet.index, palette="magma")

    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10)
        
    plt.title("Top 5 Add-ons Correlated with Churn (Internet Customers)", fontsize=16)
    plt.xlabel("Absolute Correlation with Churn", fontsize=10)
    plt.ylabel("Internet Add-on", fontsize=10)
    plt.show()
    st.pyplot(plt)

    st.write("---")

    top_features_cols = [
        "Contract", "tenure", "MonthlyCharges", "InternetService", "PaymentMethod",
        "OnlineSecurity", "TechSupport", "SeniorCitizen", "StreamingTV", "PaperlessBilling"
    ]
    st.write(f"Top Features:{top_features_cols}")