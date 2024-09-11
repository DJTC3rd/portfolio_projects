import pandas as pd

# Define the exchange rates (Example rates; update with current values)
exchange_rates = {
    'USD': 1.00,
    'CAD': 0.74,
    'EUR': 1.08,
    'BRL': 0.20,
    'INR': 0.012,
    'ZAR': 0.053,
    'SEK': 0.093,
    'NOK': 0.10,
    'DKK': 0.15,
    'PLN': 0.24,
    'MXN': 0.055,
    'ARS': 0.013,
    'COP': 0.00021,
    'CLP': 0.0012,
    'PEN': 0.27,
    'VES': 0.019,
    'CNY': 0.14,
    'JPY': 0.0070,
    'AUD': 0.65,
    'NZD': 0.61,
    'NGN': 0.0022,
    'KES': 0.0073,
    'EGP': 0.032,
    'MAD': 0.10,
    'GHS': 0.083,
    'ETB': 0.021,
    'TZS': 0.00043,
    'UGX': 0.00027,
    'DZD': 0.0074,
    'SAR': 0.27,
    'KRW': 0.00075,
    'IDR': 0.000067,
    'VND': 0.000042,
    'THB': 0.029,
    'MYR': 0.23,
    'RUB': 0.013,
    'TRY': 0.038,
    'PKR': 0.0036,
    'BDT': 0.0091,
    'PHP': 0.018
}

# Create DataFrame
df_exchange_rates = pd.DataFrame(list(exchange_rates.items()), columns=['Currency', 'Exchange_Rate_to_USD'])

# Display the DataFrame
print(df_exchange_rates)
df_exchange_rates.to_csv('Z:\\Projects\\Portfolio Projects\\Spotify Analysis\\exchange_rates.csv',index = False)