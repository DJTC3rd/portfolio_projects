import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
from collections import OrderedDict
import uuid

# Initialize Faker
fake = Faker()

# Parameters
total_records = 20000
subscription_ids = ['S01', 'S02', 'S03', 'S04', 'S05']
# subscription_weights = [0.66, 0.22, 0.08, 0.03, 0.01]

subscription_probabilities = {
    'High-Income': [0.4116, 0.3087, 0.1624, 0.0878, 0.0295],  
    'Middle-Income': [0.7371, 0.2127, 0.0501, 0.0001, 0.0],  
    'Low-Income': [0.905, 0.085, 0.008, 0.002, 0.000] 
}

# Define country breakdown
country_distribution = {
    'Europe': 0.34,
    'North America': 0.24,
    'Latin America': 0.22,
    'Rest of World': 0.20
}

# Define specific countries in each region with tiers
countries = {
    'Europe': ['Germany', 'France', 'United Kingdom', 'Spain', 'Italy', 'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Poland'],
    'North America': ['United States', 'Canada'],
    'Latin America': ['Brazil', 'Mexico', 'Argentina', 'Colombia', 'Chile', 'Peru', 'Venezuela'],
    'Rest of World': [
        'India', 'China', 'Japan', 'Australia', 'New Zealand',
        'South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Morocco',
        'Ghana', 'Ethiopia', 'Tanzania', 'Uganda', 'Algeria',
        'Saudi Arabia', 'South Korea', 'Indonesia', 'Vietnam', 'Thailand', 
        'Malaysia', 'Russia', 'Turkey', 'Pakistan', 'Bangladesh', 
        'Philippines'
    ]
}

# Define CPM rates based on wealth tiers
cpm_rates = {
    'High-Income': 10.00,  # Example CPM rate for high-income countries
    'Middle-Income': 5.00, # Example CPM rate for middle-income countries
    'Low-Income': 2.00     # Example CPM rate for low-income countries
}

# Spotify plan prices in local currencies
spotify_prices = {
    'United States': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'USD'},
    'Canada': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'CAD'},
    'Germany': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'EUR'},
    'France': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'EUR'},
    'United Kingdom': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'GBP'},
    'Spain': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'EUR'},
    'Italy': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'EUR'},
    'Netherlands': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'EUR'},
    'Sweden': {'Individual': 99.00, 'Family': 149.00, 'Student': 49.00, 'Duo': 129.00, 'Currency': 'SEK'},
    'Norway': {'Individual': 109.00, 'Family': 169.00, 'Student': 54.00, 'Duo': 139.00, 'Currency': 'NOK'},
    'Denmark': {'Individual': 99.00, 'Family': 149.00, 'Student': 49.00, 'Duo': 129.00, 'Currency': 'DKK'},
    'Poland': {'Individual': 19.99, 'Family': 29.99, 'Student': 9.99, 'Duo': 24.99, 'Currency': 'PLN'},
    'Brazil': {'Individual': 16.90, 'Family': 26.90, 'Student': 8.50, 'Duo': 21.90, 'Currency': 'BRL'},
    'Mexico': {'Individual': 115.00, 'Family': 149.00, 'Student': 57.00, 'Duo': 129.00, 'Currency': 'MXN'},
    'Argentina': {'Individual': 199.00, 'Family': 299.00, 'Student': 99.00, 'Duo': 249.00, 'Currency': 'ARS'},
    'Colombia': {'Individual': 14.99, 'Family': 23.99, 'Student': 7.49, 'Duo': 19.99, 'Currency': 'COP'},
    'Chile': {'Individual': 5650.00, 'Family': 8490.00, 'Student': 2990.00, 'Duo': 6890.00, 'Currency': 'CLP'},
    'Peru': {'Individual': 16.90, 'Family': 26.90, 'Student': 8.50, 'Duo': 21.90, 'Currency': 'PEN'},
    'Venezuela': {'Individual': 5.00, 'Family': 10.00, 'Student': 3.00, 'Duo': 8.00, 'Currency': 'VES'},
    'India': {'Individual': 119.00, 'Family': 179.00, 'Student': 59.00, 'Duo': 149.00, 'Currency': 'INR'},
    'China': {'Individual': 9.99, 'Family': 14.99, 'Student': 4.99, 'Duo': 12.99, 'Currency': 'CNY'},
    'Japan': {'Individual': 980.00, 'Family': 1480.00, 'Student': 480.00, 'Duo': 1280.00, 'Currency': 'JPY'},
    'Australia': {'Individual': 11.99, 'Family': 17.99, 'Student': 5.99, 'Duo': 15.99, 'Currency': 'AUD'},
    'New Zealand': {'Individual': 14.99, 'Family': 21.99, 'Student': 7.49, 'Duo': 18.99, 'Currency': 'NZD'},
    'South Africa': {'Individual': 59.99, 'Family': 99.99, 'Student': 29.99, 'Duo': 79.99, 'Currency': 'ZAR'},
    'Nigeria': {'Individual': 900.00, 'Family': 1400.00, 'Student': 450.00, 'Duo': 1200.00, 'Currency': 'NGN'},
    'Kenya': {'Individual': 299.00, 'Family': 499.00, 'Student': 149.00, 'Duo': 399.00, 'Currency': 'KES'},
    'Egypt': {'Individual': 49.99, 'Family': 89.99, 'Student': 24.99, 'Duo': 74.99, 'Currency': 'EGP'},
    'Morocco': {'Individual': 49.99, 'Family': 89.99, 'Student': 24.99, 'Duo': 74.99, 'Currency': 'MAD'},
    'Ghana': {'Individual': 16.99, 'Family': 24.99, 'Student': 9.99, 'Duo': 19.99, 'Currency': 'GHS'},
    'Ethiopia': {'Individual': 99.99, 'Family': 149.99, 'Student': 49.99, 'Duo': 129.99, 'Currency': 'ETB'},
    'Tanzania': {'Individual': 6000.00, 'Family': 10000.00, 'Student': 3000.00, 'Duo': 8000.00, 'Currency': 'TZS'},
    'Uganda': {'Individual': 20000.00, 'Family': 30000.00, 'Student': 10000.00, 'Duo': 25000.00, 'Currency': 'UGX'},
    'Algeria': {'Individual': 349.00, 'Family': 499.00, 'Student': 149.00, 'Duo': 399.00, 'Currency': 'DZD'},
    'Saudi Arabia': {'Individual': 19.99, 'Family': 29.99, 'Student': 9.99, 'Duo': 24.99, 'Currency': 'SAR'},
    'South Korea': {'Individual': 10900.00, 'Family': 16350.00, 'Student': 5450.00, 'Duo': 13500.00, 'Currency': 'KRW'},
    'Indonesia': {'Individual': 49990.00, 'Family': 79990.00, 'Student': 24990.00, 'Duo': 64990.00, 'Currency': 'IDR'},
    'Vietnam': {'Individual': 59000.00, 'Family': 109000.00, 'Student': 29000.00, 'Duo': 89000.00, 'Currency': 'VND'},
    'Thailand': {'Individual': 129.00, 'Family': 199.00, 'Student': 65.00, 'Duo': 169.00, 'Currency': 'THB'},
    'Malaysia': {'Individual': 14.90, 'Family': 22.90, 'Student': 8.50, 'Duo': 19.90, 'Currency': 'MYR'},
    'Russia': {'Individual': 169.00, 'Family': 269.00, 'Student': 99.00, 'Duo': 229.00, 'Currency': 'RUB'},
    'Turkey': {'Individual': 17.99, 'Family': 26.99, 'Student': 8.99, 'Duo': 22.99, 'Currency': 'TRY'},
    'Pakistan': {'Individual': 299.00, 'Family': 499.00, 'Student': 149.00, 'Duo': 399.00, 'Currency': 'PKR'},
    'Bangladesh': {'Individual': 199.00, 'Family': 299.00, 'Student': 99.00, 'Duo': 249.00, 'Currency': 'BDT'},
    'Philippines': {'Individual': 129.00, 'Family': 179.00, 'Student': 79.00, 'Duo': 149.00, 'Currency': 'PHP'}
}

# Function to determine wealth tier based on the country
def get_tier(country):
    if country in countries['Europe'] or country in ['United States', 'Canada', 'Japan', 'Australia', 'New Zealand']:
        return 'High-Income'
    elif country in ['Brazil', 'Mexico', 'Argentina', 'Russia', 'Turkey', 'China', 'South Africa', 'Saudi Arabia', 
                     'South Korea', 'Malaysia', 'Thailand', 'Colombia', 'Chile', 'Poland', 'Italy', 'Spain']:
        return 'Middle-Income'
    else:
        return 'Low-Income'

# Function to calculate CPM rate based on country tier
def get_cpm_rate(country):
    tier = get_tier(country)
    return cpm_rates[tier]

# Function to choose a country based on the specified distribution
def choose_country():
    region = np.random.choice(list(country_distribution.keys()), p=list(country_distribution.values()))
    return random.choice(countries[region])

# Define a function to calculate revenue
def calculate_revenue(subscription_id, ad_views, country):
    if subscription_id == 'S01':
        cpm = get_cpm_rate(country)
        return (cpm / 1000) * ad_views, 'USD'
    else:
        # Use local currency prices for other subscription types
        plan_type = {
            'S02': 'Individual',
            'S03': 'Family',
            'S04': 'Student',
            'S05': 'Duo'
        }[subscription_id]
        return spotify_prices[country][plan_type], spotify_prices[country]['Currency']

# Function to generate ad views based on subscription type
def generate_ad_views(subscription_id):
    if subscription_id == 'S01':
        return int(np.random.normal(78, 10))  # Average 78 ad views
    else:
        return 0

# Function to generate payment dates for non-S01 subscriptions
def generate_first_payment(join_date, subscription_id):
    if subscription_id == 'S01':
        return pd.Timestamp(join_date + timedelta(days=random.randint(0, 365)))
    else:
        return pd.Timestamp(join_date + timedelta(days=random.randint(0, 30)))

# Generate random age with 18+ constraint
def generate_age():
    return random.randint(18, 80)

# Generate session_id
def generate_session_id():
    return uuid.uuid4().hex

# Function to generate subscription based on tier probabilities
def choose_subscription(tier):
    return np.random.choice(subscription_ids, p=subscription_probabilities[tier])

# Generate data
def generate_data():
    records = []
    user_id_counter = 1
    
    for _ in range(total_records):
        country = choose_country()
        tier = get_tier(country)
        subscription_id = choose_subscription(tier)
        join_date = pd.Timestamp(fake.date_between(start_date=datetime(2020, 1, 1), end_date=datetime(2022, 12, 31)))
        first_payment = generate_first_payment(join_date, subscription_id)
        payment_dates = []
        payment_dates.append(first_payment)
        age = generate_age()
        #Random Percentages from StatCan
        gender = fake.random_element(OrderedDict([
                    ("Male", 0.495),         
                    ("Female", 0.495),        
                    ("Other", 0.01),        
                ]))

        if subscription_id == 'S01':
            #Arbitrailly capping this for simplicity. I Want the dataset to have good coverage without being excessivly bloated due to ads
            num_reccuring = np.minimum(np.random.randint((datetime(2022, 12, 31) - join_date).days), 40)
            payment_dates.extend(pd.Timestamp(first_payment + timedelta(days=num)) for num in range(1,num_reccuring))
        else:
            #sloppy, don't care, works fine for this purpose
            num_reccuring = np.floor(((datetime(2022, 12, 31) - join_date).days)/30)
            if num_reccuring != 0:
                num_reccuring = int(np.minimum(np.random.randint(num_reccuring), 12))
                payment_dates.extend(pd.Timestamp(first_payment + timedelta(days=num*30)) for num in range(1,num_reccuring))
        
                        
        for payment_date in payment_dates:
            ad_views = generate_ad_views(subscription_id)
            revenue = calculate_revenue(subscription_id, ad_views, country)
            records.append({
                'user_id': user_id_counter,
                'subscription_id': subscription_id,
                'session_id': generate_session_id(),
                'Revenue': revenue[0],
                'Currency': revenue[1],
                'Join_Date':join_date,
                'Payment_date': payment_date,
                'ad_views': ad_views,
                'Country': country,
                'Gender': gender,
                'Age': age
            })
        
        user_id_counter += 1  # Increment for the next new user

    return pd.DataFrame(records)

# Generate the dataset
df = generate_data()

# Display the first few rows of the generated dataset
df_info = df[['user_id','Join_Date', 'subscription_id', 'Country', 'Gender', 'Age']].drop_duplicates()
df_transactions = df[['user_id', 'Revenue', 'Payment_date', 'ad_views','Currency']]


print("DataFrame with user information:")
print(df_info)
print("\nDataFrame with transaction details:")
print(df_transactions)

df_info.to_csv(path_or_buf='Z:\\Projects\\Portfolio Projects\\Spotify Analysis\\user_info.csv',index = False)
df_transactions.to_csv('Z:\\Projects\\Portfolio Projects\\Spotify Analysis\\user_transactions.csv',index = False)