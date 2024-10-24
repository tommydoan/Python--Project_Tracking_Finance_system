import streamlit as st
import requests
import pandas as pd
url ='http://localhost:8000'

def get_analytics_month_tab():
    st.title("Expenses Breakdown by Month")
    payload = {
            'start_date': "2024-08-01",
            'end_date': "2024-09-30"
        }

    try:
        response = requests.post(f'{url}/analytics-month/', json=payload)
        if response.status_code == 200:
            analytics_data = response.json()  # Parse the JSON data
            if isinstance(analytics_data, list):
                # Create the DataFrame from the response
                data = {
                    "month": [item['month'] for item in analytics_data],
                    "total": [item['total'] for item in analytics_data]
                }

                df = pd.DataFrame(data)
                df_sorted = df.sort_values(by="month", ascending=True)

                st.bar_chart(data=df_sorted.set_index("month")['total'], use_container_width=True)

                # Format and display the table
                df_sorted["total"] = df_sorted["total"].map("{:.2f}".format)
                st.table(df_sorted)
            else:
                st.error("Unexpected response format")
        else:
            st.error(f"Failed to get analytics data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")