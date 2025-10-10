import streamlit as st
from app_pages.multi_page import MultiPage

from app_pages.page1 import page1_body
from app_pages.page2 import page2_body
from app_pages.page3 import page3_body
from app_pages.page4 import page4_body


app = MultiPage(app_name="Telecom Churn Analytics Dashboard")

app.add_page("Introduction", page1_body)
app.add_page("Churn Analysis", page2_body)
app.add_page("Top 10 Churn Predictors", page3_body)
app.add_page("Churn Prediction", page4_body)


app.run()