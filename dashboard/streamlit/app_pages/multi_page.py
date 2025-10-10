import streamlit as st

class MultiPage:

    def __init__(self, app_name) -> None:
        self.pages = []
        self.app_name = app_name


        st.set_page_config(
            page_title=self.app_name,
            page_icon=":computer:",
        )

    def add_page(self, title, func) -> None:
        self.pages.append({"title": title, "function": func})

    def run(self) -> None:
        page = st.sidebar.title("📊 Dashboard")
        page = st.sidebar.radio(" \n", self.pages, format_func=lambda page: page["title"])
        page["function"]()
