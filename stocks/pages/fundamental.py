import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

st.title("🏢 Fundamental Analyse")
st.write("Opgaver om fundamental aktieanalyse og virksomhedsvurdering")

# Indlæs data
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(script_dir, "stocks.csv")
df = pd.read_csv(csv_path)
df['market_cap_billions'] = df['market_cap'] / 1e9

st.write(f"Vi analyserer {len(df)} virksomheders fundamentals")

# Opgave 1: P/E Ratio Analyse
st.subheader("📊 Opgave 1: P/E Ratio Vurdering")
st.write("""
**Analyser Price-to-Earnings ratios:**
1. Hvilke aktier har P/E ratio data tilgængelig?
2. Hvad er gennemsnitlig P/E ratio?
3. Hvilke aktier anses for "billige" (P/E < 15) vs "dyre" (P/E > 25)?
4. Er der sammenhæng mellem P/E ratio og afkast?
5. Sammenlign P/E ratios på tværs af sektorer
""")

show_answer_1 = st.checkbox("Vis svar til opgave 1")
if show_answer_1:
    st.write("**Svar:**")
    df_pe = df.dropna(subset=['pe_ratio'])
    
    st.write(f"1. Aktier med P/E data: {len(df_pe)} ud af {len(df)}")
    for _, row in df_pe.iterrows():
        st.write(f"   • {row['symbol']}: P/E {row['pe_ratio']:.1f}")
    
    if len(df_pe) > 0:
        avg_pe = df_pe['pe_ratio'].mean()
        st.write(f"2. Gennemsnitlig P/E ratio: {avg_pe:.1f}")
        
        cheap_stocks = df_pe[df_pe['pe_ratio'] < 15]
        expensive_stocks = df_pe[df_pe['pe_ratio'] > 25]
        
        st.write("3. Billige aktier (P/E < 15):")
        for _, row in cheap_stocks.iterrows():
            st.write(f"   • {row['symbol']}: P/E {row['pe_ratio']:.1f}")
        
        st.write("   Dyre aktier (P/E > 25):")
        for _, row in expensive_stocks.iterrows():
            st.write(f"   • {row['symbol']}: P/E {row['pe_ratio']:.1f}")
        
        correlation = df_pe['pe_ratio'].corr(df_pe['return_1year_pct'])
        st.write(f"4. Korrelation P/E vs afkast: {correlation:.3f}")
        
        sector_pe = df_pe.groupby('sector')['pe_ratio'].mean().round(1)
        st.write("5. Gennemsnit P/E per sektor:")
        for sector, pe in sector_pe.items():
            st.write(f"   • {sector}: {pe}")

# Opgave 2: Market Cap Analyse
st.subheader("💰 Opgave 2: Markedsværdi Klassifikation")
st.write("""
**Analyser virksomhedsstørrelser:**
1. Klassificer virksomheder: Small cap (<$10B), Mid cap ($10-100B), Large cap (>$100B)
2. Hvilken kategori har bedst afkast i gennemsnit?
3. Hvilken kategori har højest volatilitet?
4. Beregn markedsandele for hver virksomhed (market cap / total)
5. Er der sammenhæng mellem størrelse og stabilitet?
""")

show_answer_2 = st.checkbox("Vis svar til opgave 2")
if show_answer_2:
    st.write("**Svar:**")
    
    def market_cap_category(market_cap_b):
        if market_cap_b < 10:
            return "Small Cap"
        elif market_cap_b < 100:
            return "Mid Cap"
        else:
            return "Large Cap"
    
    df['cap_category'] = df['market_cap_billions'].apply(market_cap_category)
    
    cap_counts = df['cap_category'].value_counts()
    st.write("1. Virksomhedsklassifikation:")
    for category, count in cap_counts.items():
        st.write(f"   • {category}: {count} virksomheder")
    
    cap_performance = df.groupby('cap_category').agg({
        'return_1year_pct': 'mean',
        'volatility_pct': 'mean'
    }).round(2)
    
    best_return_cat = cap_performance['return_1year_pct'].idxmax()
    st.write(f"2. Bedst afkast: {best_return_cat} ({cap_performance.loc[best_return_cat, 'return_1year_pct']:.1f}%)")
    
    highest_vol_cat = cap_performance['volatility_pct'].idxmax()
    st.write(f"3. Højest volatilitet: {highest_vol_cat} ({cap_performance.loc[highest_vol_cat, 'volatility_pct']:.1f}%)")
    
    total_market_cap = df['market_cap_billions'].sum()
    df['market_share'] = (df['market_cap_billions'] / total_market_cap * 100).round(2)
    
    st.write("4. Markedsandele:")
    market_share_sorted = df.sort_values('market_share', ascending=False)
    for _, row in market_share_sorted.iterrows():
        st.write(f"   • {row['symbol']}: {row['market_share']:.1f}%")
    
    size_stability_corr = df['market_cap_billions'].corr(-df['volatility_pct'])  # Negativ volatilitet = højere stabilitet
    st.write(f"5. Korrelation størrelse vs stabilitet: {size_stability_corr:.3f}")

# Opgave 3: Sektor Sammenligning
st.subheader("🏭 Opgave 3: Sektor Fundamental Analyse")
st.write("""
**Sammenlign sektorer fundamentalt:**
1. Hvilken sektor har højest gennemsnitlig markedsværdi?
2. Hvilken sektor har mest "value" aktier (lavest P/E)?
3. Hvilken sektor har bedst risiko-justeret afkast (Sharpe ratio)?
4. Beregn sektor diversifikation - hvor mange sektorer er repræsenteret?
5. Lav en sektor scoring baseret på afkast, volatilitet og P/E
""")

show_answer_3 = st.checkbox("Vis svar til opgave 3")
if show_answer_3:
    st.write("**Svar:**")
    
    sector_analysis = df.groupby('sector').agg({
        'market_cap_billions': 'mean',
        'pe_ratio': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
        'return_1year_pct': 'mean',
        'volatility_pct': 'mean',
        'symbol': 'count'
    }).round(2)
    
    sector_analysis.columns = ['Avg Market Cap (B)', 'Avg P/E', 'Avg Return (%)', 'Avg Volatility (%)', 'Count']
    
    highest_mcap_sector = sector_analysis['Avg Market Cap (B)'].idxmax()
    st.write(f"1. Højest markedsværdi: {highest_mcap_sector} (${sector_analysis.loc[highest_mcap_sector, 'Avg Market Cap (B)']:.1f}B)")
    
    # Value sektor (lavest P/E)
    value_sector = sector_analysis['Avg P/E'].idxmin()
    st.write(f"2. Mest 'value': {value_sector} (P/E: {sector_analysis.loc[value_sector, 'Avg P/E']:.1f})")
    
    # Sharpe ratio per sektor
    sector_analysis['Sharpe_Approx'] = sector_analysis['Avg Return (%)'] / sector_analysis['Avg Volatility (%)']
    best_sharpe_sector = sector_analysis['Sharpe_Approx'].idxmax()
    st.write(f"3. Bedst risiko-justeret: {best_sharpe_sector} (Sharpe: {sector_analysis.loc[best_sharpe_sector, 'Sharpe_Approx']:.2f})")
    
    unique_sectors = len(df['sector'].unique())
    st.write(f"4. Sektor diversifikation: {unique_sectors} forskellige sektorer")
    
    # Sektor scoring (højere return, lavere volatilitet, lavere P/E = bedre)
    sector_analysis['Score'] = (
        (sector_analysis['Avg Return (%)'] - sector_analysis['Avg Return (%)'].mean()) / sector_analysis['Avg Return (%)'].std() +
        -(sector_analysis['Avg Volatility (%)'] - sector_analysis['Avg Volatility (%)'].mean()) / sector_analysis['Avg Volatility (%)'].std() +
        -(sector_analysis['Avg P/E'].fillna(sector_analysis['Avg P/E'].mean()) - sector_analysis['Avg P/E'].fillna(sector_analysis['Avg P/E'].mean()).mean()) / sector_analysis['Avg P/E'].fillna(sector_analysis['Avg P/E'].mean()).std()
    ).round(2)
    
    st.write("5. Sektor scoring (højere er bedre):")
    sector_scores = sector_analysis['Score'].sort_values(ascending=False)
    for sector, score in sector_scores.items():
        st.write(f"   • {sector}: {score:.2f}")

# Opgave 4: Value vs Growth
st.subheader("📈 Opgave 4: Value vs Growth Investering")
st.write("""
**Sammenlign investeringsstile:**
1. Definer Value aktier (P/E < gennemsnit, lav volatilitet)
2. Definer Growth aktier (høj afkast, høj P/E)
3. Hvilken stil har præsteret bedst det sidste år?
4. Beregn risiko-justeret afkast for hver stil
5. Hvilke aktier passer ikke i nogen kategori?
""")

show_answer_4 = st.checkbox("Vis svar til opgave 4")
if show_answer_4:
    st.write("**Svar:**")
    
    # Definer kategorier
    avg_pe = df['pe_ratio'].mean()
    avg_vol = df['volatility_pct'].mean()
    
    # Value: Lav P/E og lav volatilitet
    value_stocks = df[
        (df['pe_ratio'].fillna(avg_pe) < avg_pe) & 
        (df['volatility_pct'] < avg_vol)
    ]
    
    # Growth: Høj afkast og høj P/E
    growth_stocks = df[
        (df['return_1year_pct'] > df['return_1year_pct'].mean()) &
        (df['pe_ratio'].fillna(avg_pe) > avg_pe)
    ]
    
    st.write("1. Value aktier (lav P/E + lav volatilitet):")
    for _, row in value_stocks.iterrows():
        pe_display = f"{row['pe_ratio']:.1f}" if pd.notna(row['pe_ratio']) else "N/A"
        st.write(f"   • {row['symbol']}: P/E {pe_display}, Vol {row['volatility_pct']:.1f}%")
    
    st.write("2. Growth aktier (høj afkast + høj P/E):")
    for _, row in growth_stocks.iterrows():
        pe_display = f"{row['pe_ratio']:.1f}" if pd.notna(row['pe_ratio']) else "N/A"
        st.write(f"   • {row['symbol']}: Afkast {row['return_1year_pct']:.1f}%, P/E {pe_display}")
    
    if len(value_stocks) > 0 and len(growth_stocks) > 0:
        value_return = value_stocks['return_1year_pct'].mean()
        growth_return = growth_stocks['return_1year_pct'].mean()
        
        winner = "Value" if value_return > growth_return else "Growth"
        st.write(f"3. Bedst præstation: {winner}")
        st.write(f"   Value afkast: {value_return:.1f}%")
        st.write(f"   Growth afkast: {growth_return:.1f}%")
        
        value_sharpe = value_return / value_stocks['volatility_pct'].mean()
        growth_sharpe = growth_return / growth_stocks['volatility_pct'].mean()
        
        st.write(f"4. Risiko-justeret afkast:")
        st.write(f"   Value Sharpe: {value_sharpe:.2f}")
        st.write(f"   Growth Sharpe: {growth_sharpe:.2f}")
    
    # Andre aktier
    value_symbols = set(value_stocks['symbol'])
    growth_symbols = set(growth_stocks['symbol'])
    all_symbols = set(df['symbol'])
    other_symbols = all_symbols - value_symbols - growth_symbols
    
    st.write("5. Aktier uden klar kategori:")
    for symbol in other_symbols:
        st.write(f"   • {symbol}")

# Opgave 5: DCF Simplified
st.subheader("💰 Opgave 5: Simplified Værdiansættelse")
st.write("""
**Lav simpel værdiansættelse:**
1. Antag virksomheder vokser med deres afkast rate årligt
2. Beregn "fair value" med P/E * forventet vækst
3. Sammenlign fair value med aktuel kurs
4. Hvilke aktier er "underpricede" (fair value > aktuel kurs)?
5. Lav en investerings-anbefaling baseret på analysen
""")

show_answer_5 = st.checkbox("Vis værdiansættelse")
if show_answer_5:
    st.write("**Simplified Værdiansættelse:**")
    
    # Kun aktier med P/E data
    df_valuation = df.dropna(subset=['pe_ratio']).copy()
    
    # Antag vækst rate = afkast rate (simpel antagelse)
    df_valuation['growth_rate'] = df_valuation['return_1year_pct'] / 100
    
    # Fair value beregning (meget simpel)
    df_valuation['fair_value'] = df_valuation['current_price'] * (1 + df_valuation['growth_rate']) * (df_valuation['pe_ratio'] / 20)  # 20 = "normal" P/E
    
    df_valuation['value_gap'] = df_valuation['fair_value'] - df_valuation['current_price']
    df_valuation['value_gap_pct'] = (df_valuation['value_gap'] / df_valuation['current_price']) * 100
    
    st.write("1-3. Værdiansættelse completed")
    
    undervalued = df_valuation[df_valuation['value_gap_pct'] > 10]  # >10% underpriced
    st.write("4. Underpricede aktier (>10% gap):")
    
    if len(undervalued) > 0:
        for _, row in undervalued.iterrows():
            st.write(f"   • {row['symbol']}: Aktuel ${row['current_price']:.2f}, Fair ${row['fair_value']:.2f} ({row['value_gap_pct']:.1f}%)")
    else:
        st.write("   Ingen klart underpricede aktier identificeret")
    
    st.write("5. **Investerings anbefalinger:**")
    
    # Sorter efter value gap
    recommendations = df_valuation.sort_values('value_gap_pct', ascending=False)
    
    for i, (_, row) in enumerate(recommendations.head(3).iterrows()):
        rec_type = "🟢 KØB" if row['value_gap_pct'] > 5 else "🟡 HOLD" if row['value_gap_pct'] > -5 else "🔴 SÆLG"
        st.write(f"   {i+1}. {rec_type} {row['symbol']}: {row['value_gap_pct']:.1f}% værdigab")
        st.write(f"      Begrundelse: P/E {row['pe_ratio']:.1f}, Afkast {row['return_1year_pct']:.1f}%")

# Diskussionsspørgsmål
st.subheader("💭 Diskussionsspørgsmål")
st.write("""
- Hvad er vigtigst: P/E ratio eller vækstpotentiale?
- Hvorfor kan lave P/E ratios være både godt og dårligt?
- Er market cap en god indikator for virksomhedens succes?
- Hvad er forskellen på Value og Growth investering?
- Hvor pålidelig er fundamental analyse i praksis?

**Fundamental Analyse Principper:**
- P/E Ratio: Pris i forhold til indtjening
- Market Cap: Markedets vurdering af virksomheden
- Sektor Analyse: Sammenlign æbler med æbler
- Value vs Growth: Forskellige investeringsstile
- DCF: Diskonterede fremtidige cash flows
""")