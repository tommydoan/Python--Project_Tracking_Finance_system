from datetime import datetime
import streamlit as st
import requests
import pandas as pd

url ='http://localhost:8000'
def get_analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date =st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))
    if st.button('Get Analytics'):
        payload = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
        # Make the POST request and check the response
        try:
            response = requests.post(f'{url}/analytics/', json=payload)
            if response.status_code == 200:
                analytics_data = response.json()  # Parse the JSON data

                # Check if the response is in the expected format (a dictionary)
                if isinstance(analytics_data, dict):
                    # Create the DataFrame from the response
                    data = {
                        "Category": list(analytics_data.keys()),
                        "Total": [analytics_data[category]["total"] for category in analytics_data],
                        "Percentage": [analytics_data[category]["percentage"] for category in analytics_data]
                    }

                    df = pd.DataFrame(data)
                    df_sorted = df.sort_values(by="Percentage", ascending=False)

                    # Display title and bar chart
                    st.title("Expense Breakdown By Category")
                    st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], use_container_width=True)

                    # Format and display the table
                    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
                    df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

                    st.table(df_sorted)
                else:
                    st.error("Unexpected response format")
            else:
                st.error(f"Failed to get analytics data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")