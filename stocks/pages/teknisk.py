import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Teknisk Analyse")
st.write("Opgaver om teknisk aktieanalyse for gymnasieelever")

# Indlæs data
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(script_dir, "stocks.csv")
df = pd.read_csv(csv_path)

st.write(f"Vi analyserer {len(df)} aktier teknisk")

# Opgave 1: Volatilitet og risiko
st.subheader("⚡ Opgave 1: Volatilitet og Risiko")
st.write("""
**Analyser aktie risiko:**
1. Hvilken aktie har højest volatilitet (størst risiko)?
2. Hvilken aktie har lavest volatilitet (mindst risiko)?  
3. Hvad er gennemsnitlig volatilitet for alle aktier?
4. Hvor mange aktier har volatilitet over gennemsnittet?
5. Kategoriser aktier: Lav risiko (<30%), Medium (30-45%), Høj (>45%)
""")

show_answer_1 = st.checkbox("Vis svar til opgave 1")
if show_answer_1:
    st.write("**Svar:**")
    highest_vol = df.loc[df['volatility_pct'].idxmax()]
    lowest_vol = df.loc[df['volatility_pct'].idxmin()]
    avg_vol = df['volatility_pct'].mean()
    above_avg = len(df[df['volatility_pct'] > avg_vol])
    
    st.write(f"1. Højest volatilitet: {highest_vol['symbol']} ({highest_vol['volatility_pct']:.1f}%)")
    st.write(f"2. Lavest volatilitet: {lowest_vol['symbol']} ({lowest_vol['volatility_pct']:.1f}%)")
    st.write(f"3. Gennemsnitlig volatilitet: {avg_vol:.1f}%")
    st.write(f"4. Aktier over gennemsnit: {above_avg}")
    
    # Kategorisering
    def risk_category(vol):
        if vol < 30:
            return "Lav risiko"
        elif vol < 45:
            return "Medium risiko"
        else:
            return "Høj risiko"
    
    df['risk_category'] = df['volatility_pct'].apply(risk_category)
    risk_counts = df['risk_category'].value_counts()
    
    st.write("5. Risiko kategorier:")
    for category, count in risk_counts.items():
        st.write(f"   • {category}: {count} aktier")

# Opgave 2: Momentum analyse
st.subheader("🚀 Opgave 2: Momentum og Trends")
st.write("""
**Analyser aktie momentum (1-års afkast):**
1. Hvilke aktier har positiv momentum (>0% afkast)?
2. Hvilke aktier har negativ momentum (<0% afkast)?
3. Hvad er det samlede afkast hvis du investerede lige meget i alle aktier?
4. Hvilken aktie har bedst og værst momentum?
5. Beregn Sharpe ratio approximation (afkast/volatilitet) for hver aktie
""")

show_answer_2 = st.checkbox("Vis svar til opgave 2")
if show_answer_2:
    st.write("**Svar:**")
    positive_momentum = df[df['return_1year_pct'] > 0]
    negative_momentum = df[df['return_1year_pct'] < 0]
    
    st.write(f"1. Positive momentum: {len(positive_momentum)} aktier")
    for _, row in positive_momentum.iterrows():
        st.write(f"   • {row['symbol']}: +{row['return_1year_pct']:.1f}%")
    
    st.write(f"2. Negative momentum: {len(negative_momentum)} aktier")  
    for _, row in negative_momentum.iterrows():
        st.write(f"   • {row['symbol']}: {row['return_1year_pct']:.1f}%")
    
    portfolio_return = df['return_1year_pct'].mean()
    st.write(f"3. Portfolio afkast (lige vægtning): {portfolio_return:.1f}%")
    
    best_momentum = df.loc[df['return_1year_pct'].idxmax()]
    worst_momentum = df.loc[df['return_1year_pct'].idxmin()]
    st.write(f"4. Bedst: {best_momentum['symbol']} ({best_momentum['return_1year_pct']:.1f}%)")
    st.write(f"   Værst: {worst_momentum['symbol']} ({worst_momentum['return_1year_pct']:.1f}%)")
    
    # Sharpe ratio approximation
    df['sharpe_approx'] = df['return_1year_pct'] / df['volatility_pct']
    best_sharpe = df.loc[df['sharpe_approx'].idxmax()]
    
    st.write("5. Sharpe ratios (approximation):")
    sharpe_sorted = df.sort_values('sharpe_approx', ascending=False)
    for _, row in sharpe_sorted.iterrows():
        st.write(f"   • {row['symbol']}: {row['sharpe_approx']:.2f}")

# Opgave 3: Support og Resistance
st.subheader("📈 Opgave 3: Support og Resistance Niveauer")
st.write("""
**Analyser kursniveauer:**
1. Gruppér aktier efter kursintervaller: <$100, $100-200, >$200
2. Er der sammenhæng mellem aktiekurs og volatilitet?
3. Hvilke aktier handler tæt på "runde tal" (slutter på 0 eller 5)?
4. Beregn kurs-spænd for hver aktie (højeste - laveste over året)
""")

show_answer_3 = st.checkbox("Vis svar til opgave 3")
if show_answer_3:
    st.write("**Svar:**")
    
    # Kursgrupperinger
    def price_group(price):
        if price < 100:
            return "Under $100"
        elif price < 200:
            return "$100-200"
        else:
            return "Over $200"
    
    df['price_group'] = df['current_price'].apply(price_group)
    price_groups = df['price_group'].value_counts()
    
    st.write("1. Kursintervaller:")
    for group, count in price_groups.items():
        st.write(f"   • {group}: {count} aktier")
    
    # Korrelation
    correlation = df['current_price'].corr(df['volatility_pct'])
    st.write(f"2. Korrelation kurs vs volatilitet: {correlation:.3f}")
    if abs(correlation) < 0.3:
        st.write("   → Svag sammenhæng")
    else:
        st.write("   → Moderat sammenhæng")
    
    # Runde tal
    def is_round_number(price):
        return price % 5 == 0
    
    round_numbers = df[df['current_price'].apply(is_round_number)]
    st.write("3. Aktier ved runde tal:")
    for _, row in round_numbers.iterrows():
        st.write(f"   • {row['symbol']}: ${row['current_price']}")
    
    # Estimeret kurs-spænd (baseret på volatilitet)
    df['estimated_range'] = df['current_price'] * (df['volatility_pct'] / 100)
    st.write("4. Estimerede års-spænd (baseret på volatilitet):")
    for _, row in df.iterrows():
        st.write(f"   • {row['symbol']}: ${row['estimated_range']:.2f} spænd")

# Opgave 4: Tekniske Indikatorer
st.subheader("📊 Opgave 4: Tekniske Indikatorer")
st.write("""
**Beregn simple tekniske indikatorer:**
1. RSI approximation: (Afkast + 50) normaliseret til 0-100 skala
2. Hvilke aktier er "overkøbt" (RSI > 70)?
3. Hvilke aktier er "oversolgt" (RSI < 30)?
4. Momentum score: (Afkast * 2 - Volatilitet) / 3
""")

show_answer_4 = st.checkbox("Vis svar til opgave 4")
if show_answer_4:
    st.write("**Svar:**")
    
    # RSI approximation
    max_return = df['return_1year_pct'].max()
    min_return = df['return_1year_pct'].min()
    df['rsi_approx'] = ((df['return_1year_pct'] - min_return) / (max_return - min_return)) * 100
    
    overbought = df[df['rsi_approx'] > 70]
    oversold = df[df['rsi_approx'] < 30]
    
    st.write("1. RSI approximation beregnet")
    st.write("2. Overkøbte aktier (RSI > 70):")
    for _, row in overbought.iterrows():
        st.write(f"   • {row['symbol']}: RSI {row['rsi_approx']:.1f}")
    
    st.write("3. Oversolgte aktier (RSI < 30):")
    for _, row in oversold.iterrows():
        st.write(f"   • {row['symbol']}: RSI {row['rsi_approx']:.1f}")
    
    # Momentum score
    df['momentum_score'] = (df['return_1year_pct'] * 2 - df['volatility_pct']) / 3
    momentum_sorted = df.sort_values('momentum_score', ascending=False)
    
    st.write("4. Momentum scores (højere er bedre):")
    for _, row in momentum_sorted.iterrows():
        st.write(f"   • {row['symbol']}: {row['momentum_score']:.1f}")

# Opgave 5: Chart Patterns
st.subheader("📈 Opgave 5: Chart Pattern Simulation")
st.write("""
**Simuler kursmønstre:**
1. Generer en simpel kursgraf for en valgt aktie
2. Identificér trend retning baseret på start vs slut pris
3. Beregn maksimale "drawdown" (største fald fra top)
4. Vurder om aktien er i en "bullish" eller "bearish" trend
""")

selected_stock = st.selectbox("Vælg aktie til analyse:", df['symbol'])

if st.button("Analyser valgte aktie"):
    stock_data = df[df['symbol'] == selected_stock].iloc[0]
    
    # Simuler kurshistorik baseret på start, slut og volatilitet
    np.random.seed(hash(selected_stock) % 1000)  # Konsistent for hver aktie
    days = 252  # 1 år
    daily_returns = np.random.normal(0, stock_data['volatility_pct'] / 100 / np.sqrt(252), days)
    
    # Juster så vi ender på det rigtige niveau
    cumulative_return = (stock_data['current_price'] / stock_data['start_price']) - 1
    adjustment = cumulative_return / days
    daily_returns += adjustment
    
    # Beregn kurser
    prices = [stock_data['start_price']]
    for ret in daily_returns:
        prices.append(prices[-1] * (1 + ret))
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(len(prices)), prices, linewidth=2, color='blue')
    ax.set_title(f'{selected_stock} - Simuleret Kursforløb (1 år)')
    ax.set_xlabel('Dage')
    ax.set_ylabel('Aktiekurs ($)')
    ax.grid(True, alpha=0.3)
    
    # Markér start og slut
    ax.scatter(0, prices[0], color='green', s=100, label=f'Start: ${prices[0]:.2f}')
    ax.scatter(len(prices)-1, prices[-1], color='red', s=100, label=f'Slut: ${prices[-1]:.2f}')
    ax.legend()
    
    st.pyplot(fig)
    
    # Analyse
    st.write("**Analyse:**")
    trend = "Bullish 📈" if prices[-1] > prices[0] else "Bearish 📉"
    st.write(f"1. Trend retning: {trend}")
    
    max_price = max(prices)
    max_drawdown = (max_price - min(prices[prices.index(max_price):])) / max_price * 100
    st.write(f"2. Maksimal drawdown: {max_drawdown:.1f}%")
    
    volatility_level = "Høj" if stock_data['volatility_pct'] > 40 else "Medium" if stock_data['volatility_pct'] > 25 else "Lav"
    st.write(f"3. Volatilitetsniveau: {volatility_level}")
    st.write(f"4. Samlet vurdering: {trend} trend med {volatility_level.lower()} volatilitet")

# Diskussionsspørgsmål
st.subheader("💭 Diskussionsspørgsmål")
st.write("""
- Hvorfor er volatilitet et mål for risiko?
- Kan teknisk analyse forudsige fremtidige kurser?
- Hvad er forskellen på momentum og trend?
- Hvordan påvirker markedsstemning tekniske indikatorer?
- Er det bedre at købe ved høj eller lav volatilitet?

**Teknisk Analyse Principper:**
- Trends: Kurser bevæger sig i tendenser
- Support/Resistance: Kurser respekterer niveauer
- Volume: Volumen bekræfter kurs bevægelser
- Momentum: Hastighed af kurs ændringer
""")