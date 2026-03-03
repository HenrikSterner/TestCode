import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

# Hent rigtig aktiedata med yfinance
symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'NFLX', 'DIS', 'KO']
period = '1y'  # 1 år data

all_data = []

print("Henter aktiedata fra Yahoo Finance...")
for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        info = ticker.info
        
        # Beregn nogle nøgletal
        current_price = hist['Close'].iloc[-1]
        start_price = hist['Close'].iloc[0] 
        return_pct = ((current_price - start_price) / start_price) * 100
        volatility = hist['Close'].pct_change().std() * (252**0.5) * 100  # Annualiseret volatilitet
        avg_volume = hist['Volume'].mean()
        
        # Tilføj til liste
        all_data.append({
            'symbol': symbol,
            'company_name': info.get('longName', symbol),
            'sector': info.get('sector', 'Unknown'),
            'current_price': round(current_price, 2),
            'start_price': round(start_price, 2),
            'return_1year_pct': round(return_pct, 2),
            'volatility_pct': round(volatility, 2),
            'avg_volume': int(avg_volume),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else None
        })
        print(f"✓ {symbol} hentet")
    except Exception as e:
        print(f"✗ Fejl ved {symbol}: {e}")

# Gem til CSV
df = pd.DataFrame(all_data)
df.to_csv('stocks.csv', index=False)
print(f"\nGemt {len(df)} aktier til stocks.csv")
print(df.head())

# Gem til CSV
df = pd.DataFrame(all_data)
df.to_csv('stocks.csv', index=False)
print(f"\nGemt {len(df)} aktier til stocks.csv")
print(df.head())