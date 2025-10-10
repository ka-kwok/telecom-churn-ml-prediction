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


    # Executive Summary Section
    st.markdown("""
    ### 🧠 **Executive Summary**

    - 🔍 **Objective:** Predict customer churn using customers demographic, telecom service and contract features.  
    - 🌐 **Key Drivers:** *Tenure*, *Contract Duration*, and *Internet Add-on Subscriptions* strongly influence churn.  
    - 📈 **Model Insight:** The AdaBoost Classifier achieves high interpretability and robust predictive accuracy.  
    - 🚀 **Business Impact:** Enables data-driven **customer retention**, **marketing optimization**, and **product strategy**.  
    - 🔄 **Future Enhancements:** Integration with real-time APIs and expanded behavioral features for improved model adaptability.

    """)
    st.markdown("---")
    st.markdown("📍 Data source: Telecom Customer Churn Dataset")
