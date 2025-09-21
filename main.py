import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_ID = os.environ.get('DATABASE_ID')
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
base_url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

def get_current_month_pages():
    current_date = datetime.today()
    # current_date = datetime(2025, 8, 31)
    current_date_iso = current_date.isoformat()
    first_day_of_month = current_date.replace(day=1).isoformat()
    filter = {
        "filter" :
            {
                "and": 
                [
                    {
                        "timestamp": "created_time",
                        "created_time": {
                            "after":first_day_of_month
                        }
                    },
                    {
                        "timestamp": "created_time",
                        "created_time": {
                            "before":current_date_iso
                        }
                    }
                ]
            }

    }

    headers = {'Authorization':'Bearer '+NOTION_TOKEN,
              'Notion-Version': '2022-06-28',
              'Content-Type':'application/json'}

    res = requests.post(base_url, headers=headers, json=filter)
    data = res.json()
    print(res)
    result = data['results']
    return result

# def get_spending(results):
#     spendings_categories = []
#     for result in results:
#         spending = result['properties']['Spending']['number']
#         category = result['properties']['Tags']['select']['name']
#         spendings_categories.append((category, spending))
    
#     df = pd.DataFrame(spendings_categories, columns=['Category', 'Spending'])
#     grouped_data = df.groupby('Category')['Spending'].sum()
#     return grouped_data

def get_spending(results):
    spendings_categories = []
    spendings = []
    categories = []
    for result in results:
        spending = result['properties']['Spending']['number']
        category = result['properties']['Tags']['select']['name']
        spendings.append(spending)
        categories.append(category)
    return categories, spendings

if __name__ == '__main__':
    current_month_spending = get_current_month_pages()
    cat, spend = get_spending(current_month_spending)
    
    fig = go.Figure(data=[go.Pie(labels=cat , values=spend)])
    st.plotly_chart(fig, use_container_width=False)