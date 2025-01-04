import pandas as pd

def calculate_performance(stocks):
    # Sample calculation for portfolio performance
    df = pd.DataFrame(stocks)
    df['total_investment'] = df['purchase_price'] * df['quantity']
    df['current_value'] = df['quantity'] * df['current_price']  # Add current_price field
    df['profit_loss'] = df['current_value'] - df['total_investment']
    return df
