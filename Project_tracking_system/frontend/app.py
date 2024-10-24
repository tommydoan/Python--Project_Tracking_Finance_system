import streamlit as st
from add_update_ui import get_update_tab
from analytics_by_category import get_analytics_tab
from analytics_by_month import  get_analytics_month_tab
url ='http://localhost:8000'

st.title("Expenses Tracking System")
## Create some tabs
tab1, tab2, tab3  = st.tabs(['Add/Update', 'Analytics by Category', 'Analytics by Month'])
## Add get function with request and check the code response
with tab1:
    get_update_tab()
with tab2:
    get_analytics_tab()
with tab3 :
    get_analytics_month_tab()