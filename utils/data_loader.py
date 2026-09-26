import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2026-09-25", freq="D")
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty']
    countries = ['United States', 'Canada', 'United Kingdom', 'India', 'Germany']
    states = {
        'United States': ['California', 'Texas', 'New York'],
        'Canada': ['Ontario', 'Quebec', 'British Columbia'],
        'United Kingdom': ['England', 'Scotland', 'Wales'],
        'India': ['Maharashtra', 'Karnataka', 'Delhi'],
        'Germany': ['Bavaria', 'Berlin', 'Hamburg']
    }

    records = []
    for _ in range(3000):
        dt = np.random.choice(dates)
        cat = np.random.choice(categories)
        country = np.random.choice(countries)
        state = np.random.choice(states[country])
        customer_type = np.random.choice(['New', 'Returning'], p=[0.4, 0.6])
        segment = np.random.choice(['Consumer', 'Corporate', 'Home Office'])
        
        qty = np.random.randint(1, 5)
        unit_price = np.random.uniform(15.0, 500.0)
        cost_margin = np.random.uniform(0.5, 0.8)
        revenue = round(qty * unit_price, 2)
        cost = round(revenue * cost_margin, 2)
        profit = round(revenue - cost, 2)
        
        prod_id = f"PROD-{np.random.randint(100, 120)}"
        cust_id = f"CUST-{np.random.randint(1000, 1500)}"

        records.append({
            'date': dt,
            'order_id': f"ORD-{np.random.randint(10000, 99999)}",
            'customer_id': cust_id,
            'customer_type': customer_type,
            'segment': segment,
            'category': cat,
            'product_id': prod_id,
            'country': country,
            'state': state,
            'quantity': qty,
            'revenue': revenue,
            'profit': profit
        })

    df = pd.DataFrame(records)
    return df

# Global cached dataset
RAW_DF = generate_mock_data()

def filter_data(df, category, country):
    filtered = df.copy()
    if category and category != 'All':
        filtered = filtered[filtered['category'] == category]
    if country and country != 'All':
        filtered = filtered[filtered['country'] == country]
    return filtered