# Streamlit app til visualisering af aktiedata
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Konfigurer siden
st.set_page_config(page_title="Aktie Analyse", initial_sidebar_state="collapsed")

# Indlæs aktie data
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "stocks.csv")
df = pd.read_csv(csv_path)

st.title("📈 Aktieanalyse Dashboard")
st.write(f"Analyserer {len(df)} aktier fra forskellige sektorer")

# Vis oversigt
st.subheader("📊 Aktie Oversigt")
st.dataframe(df)

# Performance sammenligning
st.subheader("🚀 Performance Sammenligning (1-års afkast)")
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['green' if x > 0 else 'red' for x in df['return_1year_pct']]
bars = ax.bar(df['symbol'], df['return_1year_pct'], color=colors, alpha=0.7)
ax.set_xlabel('Aktie Symbol')
ax.set_ylabel('Afkast (%)')
ax.set_title('1-års afkast per aktie')
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax.grid(True, alpha=0.3)

# Tilføj værdier på søjlerne
for bar, value in zip(bars, df['return_1year_pct']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
            f'{value:.1f}%', ha='center', va='bottom' if height > 0 else 'top')

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Volatilitet vs Afkast
st.subheader("⚡ Risiko vs Afkast Analyse")
fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(df['volatility_pct'], df['return_1year_pct'], 
                    s=100, alpha=0.7, c=df['current_price'], cmap='viridis')

# Tilføj labels til punkter
for i, row in df.iterrows():
    ax.annotate(row['symbol'], (row['volatility_pct'], row['return_1year_pct']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)

ax.set_xlabel('Volatilitet (%)')
ax.set_ylabel('1-års afkast (%)')
ax.set_title('Risiko vs Afkast - Størrelse = Aktiekurs')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax.axvline(x=df['volatility_pct'].mean(), color='red', linestyle='--', alpha=0.5, label='Gennemsnit volatilitet')

plt.colorbar(scatter, label='Aktiekurs ($)')
plt.legend()
st.pyplot(fig)

# Sektor analyse
st.subheader("🏭 Sektor Performance")
sector_performance = df.groupby('sector').agg({
    'return_1year_pct': 'mean',
    'volatility_pct': 'mean',
    'symbol': 'count'
}).round(2)
sector_performance.columns = ['Gennemsnit Afkast (%)', 'Gennemsnit Volatilitet (%)', 'Antal Aktier']

st.dataframe(sector_performance)

# Sektor visualisering
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gennemsnit afkast per sektor
ax1.bar(sector_performance.index, sector_performance['Gennemsnit Afkast (%)'], 
        color='lightblue', alpha=0.7)
ax1.set_title('Gennemsnitlig afkast per sektor')
ax1.set_ylabel('Afkast (%)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# Volatilitet per sektor
ax2.bar(sector_performance.index, sector_performance['Gennemsnit Volatilitet (%)'], 
        color='lightcoral', alpha=0.7)
ax2.set_title('Gennemsnitlig volatilitet per sektor')
ax2.set_ylabel('Volatilitet (%)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# Market Cap analyse
st.subheader("💰 Market Cap Fordeling")
df['market_cap_billions'] = df['market_cap'] / 1e9

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['symbol'], df['market_cap_billions'], color='gold', alpha=0.7)
ax.set_xlabel('Aktie Symbol')
ax.set_ylabel('Market Cap (Milliarder $)')
ax.set_title('Market Capitalization per aktie')
plt.xticks(rotation=45)
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# P/E Ratio analyse
st.subheader("📊 P/E Ratio Sammenligning")
df_pe = df.dropna(subset=['pe_ratio'])  # Fjern aktier uden P/E ratio

if len(df_pe) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_pe['symbol'], df_pe['pe_ratio'], color='lightgreen', alpha=0.7)
    ax.set_xlabel('Aktie Symbol')
    ax.set_ylabel('P/E Ratio')
    ax.set_title('Price-to-Earnings Ratio per aktie')
    ax.axhline(y=df_pe['pe_ratio'].mean(), color='red', linestyle='--', 
               label=f'Gennemsnit: {df_pe["pe_ratio"].mean():.1f}')
    plt.xticks(rotation=45)
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Ingen P/E ratio data tilgængelig")

# Korrelations analyse
st.subheader("🔗 Korrelations Matrix")
correlation_data = df[['current_price', 'return_1year_pct', 'volatility_pct', 'market_cap', 'pe_ratio']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, ax=ax)
ax.set_title('Korrelation mellem nøgletal')
st.pyplot(fig)

# Key metrics dashboard
st.subheader("📈 Nøgletal Dashboard")
col1, col2, col3, col4 = st.columns(4)

with col1:
    best_performer = df.loc[df['return_1year_pct'].idxmax()]
    st.metric("🚀 Bedste Afkast", 
              f"{best_performer['symbol']}", 
              f"{best_performer['return_1year_pct']:.1f}%")

with col2:
    lowest_volatility = df.loc[df['volatility_pct'].idxmin()]
    st.metric("😌 Lavest Risiko", 
              f"{lowest_volatility['symbol']}", 
              f"{lowest_volatility['volatility_pct']:.1f}%")

with col3:
    biggest_company = df.loc[df['market_cap'].idxmax()]
    st.metric("🏢 Største Selskab", 
              f"{biggest_company['symbol']}", 
              f"${biggest_company['market_cap_billions']:.0f}B")

with col4:
    avg_return = df['return_1year_pct'].mean()
    st.metric("📊 Gennemsnit Afkast", 
              f"{avg_return:.1f}%", 
              f"Medián: {df['return_1year_pct'].median():.1f}%")

# Top og bund performere
st.subheader("🏆 Top og Bund Performere")
col1, col2 = st.columns(2)

with col1:
    st.write("**Top 3 Performere (afkast):**")
    top_performers = df.nlargest(3, 'return_1year_pct')[['symbol', 'company_name', 'return_1year_pct', 'volatility_pct']]
    st.dataframe(top_performers)

with col2:
    st.write("**Bund 3 Performere (afkast):**")
    bottom_performers = df.nsmallest(3, 'return_1year_pct')[['symbol', 'company_name', 'return_1year_pct', 'volatility_pct']]
    st.dataframe(bottom_performers)