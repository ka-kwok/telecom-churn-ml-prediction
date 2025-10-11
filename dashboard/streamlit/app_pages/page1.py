import streamlit as st

def page1_body():
    from PIL import Image
    import base64

    # Custom CSS for gradient header styling
    st.markdown("""
        <style>
        .header {
            background: linear-gradient(90deg, #004e92, #000428);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 36px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        .header h3 {
            font-size: 18px;
            font-weight: normal;
            color: #E0E0E0;
            margin-top: 0;
        }
        </style>

        <div class="header">
            <h1>📊 Telecom Churn Analytics:</h1>
            <h3>Building Predictive Models to Improve Customer Retention</h3>
        </div>
    """, unsafe_allow_html=True)

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import random

    @st.cache_data
    def load_data():
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_encoded.csv")
        csv2_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_cleaned.csv")
        df_encoded = pd.read_csv(csv_path)
        df_cleaned = pd.read_csv(csv2_path)
        return df_encoded, df_cleaned

    df_encoded, df_cleaned = load_data()

    # Load your cleaned churn dataset
    df = df_cleaned

    # Ensure 'Churn' is binary (0 = No, 1 = Yes)
    if df['Churn'].dtype == object:
        df['Churn'] = df['Churn'].map({'No': 0, 'Yes': 1}).astype(int)

    # Calculate KPIs
    total_customers = len(df)
    churned_customers = df['Churn'].sum()
    churn_rate = churned_customers / total_customers * 100

    # Display KPI boxes
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churned Customers", f"{churned_customers:,}")
    col3.metric("Churn Rate", f"{churn_rate:.2f}%")
    col4.metric("Target Churn Rate", "20.00%", delta=f"{20 - churn_rate:.2f}%", delta_color="normal")


    '''
    Heatmap of Top 20 Churn Drivers
    '''
    # Calculate actual feature correlations with Churn from your dataset
    correlation_matrix = df_encoded.corr()
    churn_correlations = correlation_matrix["Churn_Yes"].abs().sort_values(ascending=False)

    # Select top 20 features (excluding Churn_Yes itself)
    top_20_features = churn_correlations.index[1:21]  # Skip 'Churn_Yes' itself
    top_20_values = churn_correlations.values[1:21]

    # Create pairs of features and values, then shuffle them randomly
    feature_value_pairs = list(zip(top_20_features, top_20_values))
    random.shuffle(feature_value_pairs)

    # Extract shuffled features and values
    shuffled_features, shuffled_values = zip(*feature_value_pairs)
    shuffled_features = list(shuffled_features)
    shuffled_values = list(shuffled_values)

    # Create full feature names for hover text (no truncation)
    full_feature_names = []
    for feature in shuffled_features:
        # Clean up encoded feature names for hover display (full names)
        if '_Yes' in feature:
            full_name = feature.replace('_Yes', '')
        elif '_No' in feature:
            full_name = feature.replace('_No', '')
        elif 'Contract_' in feature:
            full_name = feature.replace('Contract_', 'Contract: ')
        elif 'PaymentMethod_' in feature:
            full_name = feature.replace('PaymentMethod_', 'Payment: ')
        elif 'InternetService_' in feature:
            full_name = feature.replace('InternetService_', 'Internet: ')
        else:
            full_name = feature
        
        full_feature_names.append(full_name)

    # Create shortened feature names for annotations (display on heatmap)
    short_feature_names = []
    for full_name in full_feature_names:
        # Truncate long names for better display on heatmap
        if len(full_name) > 12:
            short_name = full_name[:10] + '..'
        else:
            short_name = full_name
        
        short_feature_names.append(short_name)

    # Reshape data to 4x5 grid (now in random order)
    heatmap_data = np.array(shuffled_values).reshape(4, 5)
    full_feature_names_grid = np.array(full_feature_names).reshape(4, 5)
    short_feature_names_grid = np.array(short_feature_names).reshape(4, 5)

    # Create custom hover text with FULL feature names and correlation values
    hover_text = []
    for i in range(4):
        hover_row = []
        for j in range(5):
            hover_row.append(f"{full_feature_names_grid[i, j]}<br>Correlation: {heatmap_data[i, j]:.3f}")
        hover_text.append(hover_row)

    # Create the Plotly heatmap
    fig = px.imshow(
        heatmap_data,
        color_continuous_scale='RdYlBu_r',  # Red-Yellow-Blue reversed for better correlation visualization
        zmin=0,
        zmax=0.8,  # Adjust based on your actual correlation range
        aspect="auto",
        title="<b>Top 20 Churn Drivers</b>",
    )

    # Update hovertemplate to show full feature name and correlation
    fig.update_traces(
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_text
    )

    # Add shortened feature names and correlation values as annotations
    annotations = []
    for i in range(4):  # 4 rows
        for j in range(5):  # 5 columns
            corr_value = heatmap_data[i, j]
            feature_name = short_feature_names_grid[i, j]  # Use shortened names for annotations
            
            # Create annotation text: Feature Name (Correlation Value)
            text_label = f"{feature_name}"
            
            # Choose text color based on correlation strength for better readability
            text_color = "white" if corr_value > 0.4 else "black"
            
            annotations.append(
                dict(
                    x=j,  # x-coordinate (column index)
                    y=i,  # y-coordinate (row index)     
                    text=text_label,
                    showarrow=False,
                    font=dict(
                        color=text_color,
                        size=9,
                        family="Arial Black"
                    ),
                    bgcolor='rgba(255, 255, 255, 0.1)' if corr_value > 0.4 else 'rgba(0, 0, 0, 0.1)',
                    borderpad=2
                )
            )

    # Update layout
    fig.update_layout(
        annotations=annotations,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, title=''),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, title=''),
        height=450,
        width=700,
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(
            title="Scale",
            titleside="right",
            tickmode="linear",
            tick0=0,
            dtick=0.1
        )
    )

    st.plotly_chart(fig)


    # Executive Summary Section
    with st.expander("🧠 Executive Summary"):

        st.markdown("""
        - 🔍 **Objective:** Predict customer churn using customers demographic, telecom service and contract features.")   
        - 🌐 **Key Drivers:** *Tenure*, *Contract Duration*, and *Internet Add-on Subscriptions* strongly influence churn.  
        - 📈 **Model Insight:** The Logistic Regression model achieves high interpretability and robust predictive accuracy.  
        - 🚀 **Business Impact:** Enables data-driven **customer retention**, **marketing optimization**, and **product strategy**.  
        - 🔄 **Future Enhancements:** Integration with real-time APIs and expanded behavioral features for improved model adaptability.

        """)
    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")
