import os
import streamlit as st

def page2_body():
    import pandas as pd
    import plotly.express as px
    import matplotlib.pyplot as plt
    

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contract Type and Tenure", "Senior Customers", "Internet Add-on Services", "Churn Rates Explorer", "Churn Drivers Map"])

    @st.cache_data
    def load_data():
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_cleaned.csv")
        df = pd.read_csv(csv_path)
        return df

    df = load_data()

    # Sidebar filters
    st.sidebar.header("🔍 Filter")
    selected_contracts = st.sidebar.multiselect("Contract Type", df["Contract"].unique(), default=df["Contract"].unique())
    selected_churn = st.sidebar.multiselect("Churn Status", df["Churn"].unique(), default=df["Churn"].unique())
    tenure_range = st.sidebar.slider("Tenure Range (Months)", int(df["tenure"].min()), int(df["tenure"].max()), (0, 72))

    # Apply filters
    df = df[
        (df["Contract"].isin(selected_contracts)) &
        (df["Churn"].isin(selected_churn)) &
        (df["tenure"].between(tenure_range[0], tenure_range[1]))
    ]

    # Section: Tenure vs Churn by Contract
    with tab1:
    
        fig1 = px.box(df, x="Contract", y="tenure", color="Churn",
                    title="Churn Distribution: Tenure & Contract Type",
                    labels={"tenure": "Tenure (Months)", "Contract": "Contract Type", "Churn": "Churn"},
                    points="all",
                    hover_data=["MonthlyCharges", "PaymentMethod", "InternetService"])
        fig1.update_layout(boxmode="group", height=500)
        st.plotly_chart(fig1, use_container_width=True)

        # Churn count by Tenure with filters
        churn_count = df[df["Churn"] == "Yes"].groupby("tenure").size()
        fig2 = px.bar(churn_count, x=churn_count.index, y=churn_count.values,
                    labels={"tenure": "Tenure (Months)", "y": "Number of Churns"},
                    title="Number of Churns by Tenure")
        st.plotly_chart(fig2, use_container_width=True)

    # Section: Senior customers analysis
    with tab2:

        # Stacked bar chart for senior vs churn with plotly
        selected_churn = df["Churn"].map({0: "Retained", 1: "Churned"}).unique().tolist()
        filtered_churn = df.groupby("SeniorCitizen")["Churn"].value_counts(normalize=True).unstack().fillna(0).reset_index()

        # Rename churn columns for clarity
        filtered_churn = filtered_churn.rename(columns={0: "No", 1: "Yes"})
        columns_to_keep = ["SeniorCitizen", "No", "Yes"]
        melted = filtered_churn.melt(id_vars="SeniorCitizen", value_vars=["No", "Yes"],
                                    var_name="Churn", value_name="Rate")
        melted["SeniorCitizen"] = melted["SeniorCitizen"].map({"No": "Non-Senior", "Yes": "Senior"})

        fig = px.bar(melted, x="SeniorCitizen", y="Rate", color="Churn", barmode="stack",
                    text="Rate", title="Churn Rate by Senior Status",
                    labels={"Rate": "Proportion", "SeniorCitizen": "Customer Type"})
        fig.update_traces(texttemplate='%{text:.1%}', textposition='inside')
        fig.update_layout(yaxis_tickformat=".0%", yaxis_range=[0, 1], height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Section: Service Usage by Senior Status and Churn Status
        service_features = ['OnlineSecurity', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'OnlineBackup', 'DeviceProtection']
        senior_services = df.groupby('SeniorCitizen')[service_features].apply(lambda x: x.eq('Yes').mean()).reset_index()
        senior_services['SeniorCitizen'] = senior_services['SeniorCitizen'].map({'No': 'Non-Senior', 'Yes': 'Senior'})
        melted_services = senior_services.melt(id_vars='SeniorCitizen', var_name='Service', value_name='UsageRate')

        fig = px.bar(
            melted_services,
            x='Service',
            y='UsageRate',
            color='SeniorCitizen',
            barmode='group',
            title='🔍 Internet Service Usage Comparison: Seniors vs Non-Seniors',
            labels={'UsageRate': 'Usage Rate'}
        )
        fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')
        fig.layout.height = 550
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Bar plot for NumInternetServices vs Churn rate
        selected_churn = ["No", "Yes"]
        filtered_df = df[df["InternetService"] != "No"]
        filtered_churn = filtered_df.groupby("NumInternetServices")["Churn"].value_counts(normalize=True).unstack().fillna(0).reset_index()

        # Melt the dataframe for plotly
        melted_churn = filtered_churn.melt(id_vars="NumInternetServices", value_vars=selected_churn,
                                        var_name="Churn", value_name="Rate")

        fig = px.bar(melted_churn, x="NumInternetServices", y="Rate", color="Churn",
                    barmode="group", title="📡 Churn Rate vs Number of Internet Add-on Services",
                    labels={"Rate": "Churn Rate", "NumInternetServices": "Number of Internet Services"})
        fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        # Proportion of the target variable 'Churn' by online security feature
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        online_security_counts_no = df[df['OnlineSecurity'] == "No"]['Churn'].value_counts()
        ax[0].pie(online_security_counts_no.values, labels=online_security_counts_no.index, autopct='%1.1f%%')
        ax[0].set_title('Proportion of Churn without Online Security')
        online_security_counts = df[df['OnlineSecurity'] == "Yes"]['Churn'].value_counts()
        ax[1].pie(online_security_counts.values, labels=online_security_counts.index, autopct='%1.1f%%')
        ax[1].set_title('Proportion of Churn with Online Security')
        ax[1].legend(title='Churn')
        # add an arrow annotation between the two pie charts
        ax[0].annotate(
            "", 
            xy=(1.15, 0.5), xytext=(1.05, 0.5), 
            xycoords='axes fraction', textcoords='axes fraction', 
            arrowprops=dict(arrowstyle="->", color="Purple", lw=2)
        )   
        st.pyplot(fig)

        # Proportion of the target variable 'Churn' by tech support feature
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        tech_support_counts_no = df[df['TechSupport'] == "No"]['Churn'].value_counts()
        ax[0].pie(tech_support_counts_no.values, labels=tech_support_counts_no.index, autopct='%1.1f%%')
        ax[0].set_title('Proportion of Churn without Tech Support')
        tech_support_counts = df[df['TechSupport'] == "Yes"]['Churn'].value_counts()
        ax[1].pie(tech_support_counts.values, labels=tech_support_counts.index, autopct='%1.1f%%')
        ax[1].set_title('Proportion of Churn with Tech Support')
        ax[1].legend(title='Churn')
        ax[0].annotate(
            "", 
            xy=(1.15, 0.5), xytext=(1.05, 0.5), 
            xycoords='axes fraction', textcoords='axes fraction', 
            arrowprops=dict(arrowstyle="->", color="Purple", lw=2)
        )   
        st.pyplot(fig)
        
    with tab4:
        import plotly.graph_objects as go

        st.title("Interactive Churn Rates Explorer")
        col1, col2 = st.columns(2)
        with col1:
            feature = st.selectbox("Feature", sorted([c for c in df.columns if df[c].dtype == object]))
        with col2:
            value = st.selectbox("Value to compare", sorted(df[feature].unique().tolist()))
        show_both = st.checkbox("Show both chosen value and others", value=True)

        # Ensure Churn numeric 0/1 and human labels
        if df['Churn'].dtype == object:
            df['Churn'] = df['Churn'].map({'No': 0, 'Yes': 1}).astype(int)
        labels = ['Retained', 'Churned']
        colors = ['#66c2a5', '#fc8d62']

        def pie_counts(subdf):
            counts = subdf['Churn'].value_counts().reindex([0, 1], fill_value=0)
            return counts.values

        # Selected value vs others
        sub_selected = df[df[feature] == value]
        sub_other = df[df[feature] != value]

        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=labels,
            values=pie_counts(sub_selected),
            name=f"{feature} = {value}",
            hole=0.4,
            marker=dict(colors=colors),
            domain={'x': [0, 0.45]}
        ))
        if show_both:
            fig.add_trace(go.Pie(
                title=f"{feature} NOT {value}",
                labels=labels,
                values=pie_counts(sub_other),
                name=f"{feature} NOT {value}",
                hole=0.4,
                marker=dict(colors=colors),
                domain={'x': [0.55, 1.0]}
            ))
        #value by default


        fig.update_layout(title_text=f"Churn proportions by {feature}", annotations=[dict(text=value, x=0.20, y=0.5, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
        
    with tab5:
        @st.cache_data
        def load_data():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            csv_path = os.path.join(project_root, "dataset", "processed", "telecom_customer_churn_cleaned.csv")
            df = pd.read_csv(csv_path)
            return df

        df = load_data()

        df["Tenure"] = pd.cut(
            df["tenure"],
            bins=[0, 12, 24, 48, 72],
            labels=["0-12", "13-24", "25-48", "49-72"]
        )
        df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

        # Parallel Categories Plot for tenure, contract type, senior citizen, num of internet service, online security, tech support Features vs Churn
        fig = px.parallel_categories(
            df,
            dimensions=["NumInternetServices", "Contract", "Tenure", "SeniorCitizen", "OnlineSecurity", "TechSupport",  "Churn"],
            color="Churn",
            color_continuous_scale=px.colors.sequential.RdBu_r,
            title="🔄 Parallel Categories Plot for Selected Features vs Churn"
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")

    