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

    # Simplified CSS for KPI metrics with fixed tooltips
    st.markdown("""
    <style>
    .kpi-container {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 14px;
        margin: 6px 2px;
        text-align: center;
        position: relative;
        cursor: pointer;
        transition: background-color 0.2s ease;
        border: 1px solid #e9ecef;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-container:hover {
        background: #e3f2fd;
        border-color: #2196f3;
    }
    
    .kpi-title {
        font-size: 11px;
        color: #6c757d;
        margin-bottom: 6px;
        font-weight: 600;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .kpi-value {
        font-size: 18px;
        font-weight: bold;
        color: #495057;
        margin-bottom: 2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .kpi-delta {
        font-size: 10px;
        color: #6c757d;
        font-weight: 500;
    }
    
    .tooltip {
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%) translateY(-100%);
        background: #343a40;
        color: white;
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 10px;
        z-index: 1000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease;
        max-width: 200px;
        white-space: normal;
        text-align: left;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 4px solid transparent;
        border-top-color: #343a40;
    }
    
    .kpi-container:hover .tooltip {
        opacity: 1;
    }
    
    .tooltip-line {
        display: block;
        margin: 1px 0;
        font-size: 9px;
    }
    
    .tooltip-header {
        font-weight: bold;
        color: #ffc107;
        margin-bottom: 4px;
        font-size: 10px;
    }
    
    /* Handle top row tooltips */
    .kpi-row-1 .tooltip {
        top: auto;
        bottom: -10px;
        transform: translateX(-50%) translateY(100%);
    }
    
    .kpi-row-1 .tooltip::after {
        top: auto;
        bottom: 100%;
        border-top-color: transparent;
        border-bottom-color: #343a40;
    }
    </style>
    """, unsafe_allow_html=True)

    # Helper function to shorten feature names
    def shorten_feature_name(name, max_length=15):
        if len(name) <= max_length:
            return name
        # Try to abbreviate common words
        abbreviations = {
            'InternetService': 'Internet',
            'PaymentMethod': 'Payment',
            'PaperlessBilling': 'Paperless',
            'MonthlyCharges': 'Monthly$',
            'TotalCharges': 'Total$',
            'StreamingTV': 'TV',
            'StreamingMovies': 'Movies',
            'OnlineSecurity': 'Security',
            'OnlineBackup': 'Backup',
            'DeviceProtection': 'Protection',
            'TechSupport': 'Support'
        }
        
        for full, short in abbreviations.items():
            if full in name:
                name = name.replace(full, short)
        
        # If still too long, truncate with ellipsis
        if len(name) > max_length:
            return name[:max_length-1] + "…"
        return name

    # Layout: 5 columns per row with simplified tooltips
    for row_idx, i in enumerate(range(0, len(top_features_cols), 5)):
        cols = st.columns(5)
        row_class = "kpi-row-1" if row_idx == 0 else ""
        
        for j, feature in enumerate(top_features_cols[i:i+5]):
            with cols[j]:
                # Get correlation value for this feature
                feature_encoded_name = feature_data_mapping.get(feature, feature)
                if isinstance(feature_encoded_name, str) and feature_encoded_name in correlation_with_churn_temp.index:
                    corr_value = correlation_with_churn_temp[feature_encoded_name]
                else:
                    # Try to find the encoded version
                    possible_encoded = [col for col in correlation_with_churn_temp.index if col.startswith(str(feature))]
                    corr_value = correlation_with_churn_temp[possible_encoded[0]] if possible_encoded else 0.0

                # Shorten feature name for display
                display_name = shorten_feature_name(feature)
                
                # Check if feature exists in original dataframe
                if feature in df.columns:
                    if df[feature].dtype == 'object':
                        # For categorical: show most frequent value
                        top_value = df[feature].mode()[0]
                        count = df[feature].value_counts()[top_value]
                        
                        # Shorten top value if too long
                        display_value = top_value if len(str(top_value)) <= 12 else str(top_value)[:10] + "…"
                        
                        # Simplified tooltip
                        tooltip_content = f"""
                        <span class="tooltip-header">{feature}</span>
                        <span class="tooltip-line">Correlation: {corr_value:.3f}</span>
                        <span class="tooltip-line">Most common: {top_value}</span>
                        <span class="tooltip-line">Count: {count:,} records</span>
                        <span class="tooltip-line">Categories: {df[feature].nunique()}</span>
                        """
                        
                        st.markdown(f"""
                        <div class="kpi-container {row_class}">
                            <div class="tooltip">{tooltip_content}</div>
                            <div class="kpi-title">{display_name}</div>
                            <div class="kpi-value">{display_value}</div>
                            <div class="kpi-delta">{count:,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        # For numeric: show mean and std
                        mean_val = df[feature].mean()
                        std_val = df[feature].std()
                        
                        # Simplified tooltip
                        tooltip_content = f"""
                        <span class="tooltip-header">{feature}</span>
                        <span class="tooltip-line">Correlation: {corr_value:.3f}</span>
                        <span class="tooltip-line">Mean: {mean_val:.2f}</span>
                        <span class="tooltip-line">Std: {std_val:.2f}</span>
                        <span class="tooltip-line">Range: {df[feature].min():.1f} - {df[feature].max():.1f}</span>
                        """
                        
                        st.markdown(f"""
                        <div class="kpi-container {row_class}">
                            <div class="tooltip">{tooltip_content}</div>
                            <div class="kpi-title">{display_name}</div>
                            <div class="kpi-value">{mean_val:.1f}</div>
                            <div class="kpi-delta">±{std_val:.1f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    # For encoded features that don't exist in original dataframe
                    display_feature = shorten_feature_name(feature.replace('_', ' ').title())
                    
                    tooltip_content = f"""
                    <span class="tooltip-header">{feature}</span>
                    <span class="tooltip-line">Correlation: {corr_value:.3f}</span>
                    <span class="tooltip-line">Type: Encoded</span>
                    <span class="tooltip-line">Binary feature</span>
                    """
                    
                    st.markdown(f"""
                    <div class="kpi-container {row_class}">
                        <div class="tooltip">{tooltip_content}</div>
                        <div class="kpi-title">{display_feature}</div>
                        <div class="kpi-value">Binary</div>
                        <div class="kpi-delta">0/1</div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("**💡*Numeric drivers show mean ± std deviation • Categorical drivers show most frequent value*")
    st.write("---")

    # Bar plots for top 10 features correlated with churn
    # List top 10 features correlated with churn
    correlation_matrix = df_encoded.corr()
    correlation_with_churn = correlation_matrix["Churn_Yes"].abs().sort_values(ascending=False)
    top_10_features = correlation_with_churn.index[1:11]  # Exclude 'Churn_Yes' itself
    top_10_values = correlation_with_churn.values[1:11]

    # Prepare DataFrame for plotting
    plot_df = pd.DataFrame({
        "Feature": top_10_features,
        "Correlation": top_10_values
    })

    # Bar plot with hue assigned to 'Feature'
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=plot_df,
        x="Correlation",
        y="Feature",
        hue="Feature",
        palette="viridis",
        legend=False
    )

    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10)

    plt.title("Top 10 Features Correlated with Churn", fontsize=16)
    plt.xlabel("Absolute Correlation with Churn", fontsize=14)
    plt.ylabel("Feature", fontsize=14)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown("---")

    # Barplot for add-ons correlation with churn among internet service customers
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
    st.pyplot(plt)

    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")