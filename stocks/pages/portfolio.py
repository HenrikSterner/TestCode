import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Portefølje Analyse")
st.write("Opgaver om portefølje sammensætning og risikostyring")

# Indlæs data
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(script_dir, "stocks.csv")
df = pd.read_csv(csv_path)

st.write(f"Vi bygger og analyserer porteføljer med {len(df)} aktier")

# Opgave 1: Simpel Portefølje Konstruktion
st.subheader("🏗️ Opgave 1: Byg din første portefølje")
st.write("""
**Lav en lige-vægtet portefølje:**
1. Beregn portefølje afkast hvis du investerer lige meget i alle aktier
2. Beregn portefølje volatilitet (gennemsnit af alle volatiliteter)
3. Sammenlign med S&P 500 benchmark (antag 10% afkast, 16% volatilitet)
4. Hvad er Sharpe ratio for din portefølje?
5. Hvor mange procent af aktierne gav positiv afkast?
""")

show_answer_1 = st.checkbox("Vis portefølje resultater")
if show_answer_1:
    st.write("**Equal-Weight Portefølje Resultater:**")
    
    portfolio_return = df['return_1year_pct'].mean()
    portfolio_volatility = df['volatility_pct'].mean()  # Simpel gennemsnit (ignorer korrelation)
    
    st.write(f"1. Portefølje afkast: {portfolio_return:.2f}%")
    st.write(f"2. Portefølje volatilitet: {portfolio_volatility:.2f}%")
    
    # Benchmark sammenligning
    benchmark_return = 10.0
    benchmark_vol = 16.0
    
    st.write("3. Sammenligning med S&P 500:")
    st.write(f"   Din portefølje: {portfolio_return:.1f}% afkast, {portfolio_volatility:.1f}% volatilitet")
    st.write(f"   S&P 500:        {benchmark_return:.1f}% afkast, {benchmark_vol:.1f}% volatilitet")
    
    outperformance = portfolio_return - benchmark_return
    risk_diff = portfolio_volatility - benchmark_vol
    st.write(f"   → {outperformance:+.1f}% outperformance, {risk_diff:+.1f}% ekstra risiko")
    
    # Sharpe ratio (antag risk-free rate = 2%)
    risk_free_rate = 2.0
    portfolio_sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
    benchmark_sharpe = (benchmark_return - risk_free_rate) / benchmark_vol
    
    st.write(f"4. Sharpe ratios:")
    st.write(f"   Din portefølje: {portfolio_sharpe:.2f}")
    st.write(f"   S&P 500:        {benchmark_sharpe:.2f}")
    
    positive_stocks = len(df[df['return_1year_pct'] > 0])
    positive_pct = (positive_stocks / len(df)) * 100
    st.write(f"5. Positive aktier: {positive_stocks}/{len(df)} ({positive_pct:.0f}%)")

# Opgave 2: Sektor Diversifikation
st.subheader("🎯 Opgave 2: Diversifikations Analyse")
st.write("""
**Analyser risiko spredning:**
1. Hvor mange sektorer er repræsenteret i porteføljen?
2. Lav en sektor-vægtet portefølje (lige vægt per sektor)
3. Sammenlign sektor-vægtet vs aktie-vægtet performance
4. Hvilken sektor har størst indflydelse på total risiko?
5. Beregn koncentrationsrisiko (top 3 aktiers vægt)
""")

show_answer_2 = st.checkbox("Vis diversifikations analyse")
if show_answer_2:
    st.write("**Diversifikations Resultater:**")
    
    sectors = df['sector'].unique()
    st.write(f"1. Antal sektorer: {len(sectors)}")
    for sector in sectors:
        count = len(df[df['sector'] == sector])
        st.write(f"   • {sector}: {count} aktier")
    
    # Sektor-vægtet portefølje
    sector_weights = df.groupby('sector').size() / len(df)
    sector_performance = df.groupby('sector').agg({
        'return_1year_pct': 'mean',
        'volatility_pct': 'mean'
    })
    
    sector_weighted_return = (sector_performance['return_1year_pct'] * sector_weights).sum()
    sector_weighted_vol = (sector_performance['volatility_pct'] * sector_weights).sum()
    
    st.write("2. Sektor-vægtet portefølje:")
    st.write(f"   Afkast: {sector_weighted_return:.2f}%")
    st.write(f"   Volatilitet: {sector_weighted_vol:.2f}%")
    
    st.write("3. Sammenligning:")
    equal_weight_return = df['return_1year_pct'].mean()
    st.write(f"   Aktie-vægtet:  {equal_weight_return:.2f}%")
    st.write(f"   Sektor-vægtet: {sector_weighted_return:.2f}%")
    st.write(f"   Forskel: {sector_weighted_return - equal_weight_return:+.2f}%")
    
    # Sektor risiko bidrag
    sector_risk_contribution = sector_performance['volatility_pct'] * sector_weights
    highest_risk_sector = sector_risk_contribution.idxmax()
    st.write(f"4. Største risiko bidrag: {highest_risk_sector}")
    
    # Koncentrationsrisiko (antag lige vægt)
    individual_weight = 100 / len(df)
    top_3_weight = 3 * individual_weight
    st.write(f"5. Koncentrationsrisiko: Top 3 aktier = {top_3_weight:.1f}% af porteføljen")

# Opgave 3: Risiko-Afkast Optimering
st.subheader("⚖️ Opgave 3: Optimal Portefølje Allokering")
st.write("""
**Find den bedste balance:**
1. Identificer aktier med bedst Sharpe ratio
2. Byg en "high Sharpe" portefølje med top 5 aktier
3. Byg en "low volatility" portefølje med 5 mindst risikable
4. Byg en "balanced" portefølje med mix af begge strategier
5. Hvilken strategi har bedst risiko-justeret afkast?
""")

show_answer_3 = st.checkbox("Vis optimering resultater")
if show_answer_3:
    st.write("**Portefølje Optimering:**")
    
    # Beregn Sharpe ratio for hver aktie
    risk_free = 2.0
    df['sharpe_ratio'] = (df['return_1year_pct'] - risk_free) / df['volatility_pct']
    
    # High Sharpe portefølje
    top_sharpe = df.nlargest(5, 'sharpe_ratio')
    high_sharpe_return = top_sharpe['return_1year_pct'].mean()
    high_sharpe_vol = top_sharpe['volatility_pct'].mean()
    high_sharpe_sharpe = (high_sharpe_return - risk_free) / high_sharpe_vol
    
    st.write("1. Top 5 Sharpe ratio aktier:")
    for _, row in top_sharpe.iterrows():
        st.write(f"   • {row['symbol']}: Sharpe {row['sharpe_ratio']:.2f}")
    
    st.write("2. High Sharpe portefølje:")
    st.write(f"   Afkast: {high_sharpe_return:.2f}%")
    st.write(f"   Volatilitet: {high_sharpe_vol:.2f}%")
    st.write(f"   Sharpe: {high_sharpe_sharpe:.2f}")
    
    # Low volatility portefølje
    low_vol = df.nsmallest(5, 'volatility_pct')
    low_vol_return = low_vol['return_1year_pct'].mean()
    low_vol_volatility = low_vol['volatility_pct'].mean()
    low_vol_sharpe = (low_vol_return - risk_free) / low_vol_volatility
    
    st.write("3. Low Volatility portefølje:")
    st.write(f"   Aktier: {', '.join(low_vol['symbol'])}")
    st.write(f"   Afkast: {low_vol_return:.2f}%")
    st.write(f"   Volatilitet: {low_vol_volatility:.2f}%")
    st.write(f"   Sharpe: {low_vol_sharpe:.2f}")
    
    # Balanced portefølje (50/50 mix)
    balanced_return = (high_sharpe_return + low_vol_return) / 2
    balanced_vol = (high_sharpe_vol + low_vol_volatility) / 2
    balanced_sharpe = (balanced_return - risk_free) / balanced_vol
    
    st.write("4. Balanced portefølje (50/50 mix):")
    st.write(f"   Afkast: {balanced_return:.2f}%")
    st.write(f"   Volatilitet: {balanced_vol:.2f}%")
    st.write(f"   Sharpe: {balanced_sharpe:.2f}")
    
    # Sammenlign strategier
    strategies = {
        'High Sharpe': high_sharpe_sharpe,
        'Low Volatility': low_vol_sharpe,
        'Balanced': balanced_sharpe
    }
    
    best_strategy = max(strategies, key=strategies.get)
    st.write(f"5. Bedste strategi: **{best_strategy}** (Sharpe: {strategies[best_strategy]:.2f})")

# Opgave 4: Monte Carlo Simulation
st.subheader("🎲 Opgave 4: Fremtids Scenarier")
st.write("""
**Simuler mulige udfald:**
1. Lav 3 scenarier: Optimistisk (+50% på alle afkast), Realistisk (samme), Pessimistisk (-50%)
2. Beregn portefølje værdi efter 1 år for hvert scenarie ($10,000 start)
3. Hvad er best-case og worst-case udfald?
4. Beregn "Value at Risk" (5% værste udfald)
5. Hvilke aktier påvirker mest i hvert scenarie?
""")

show_answer_4 = st.checkbox("Vis scenario analyse")
if show_answer_4:
    st.write("**Scenario Analyse ($10,000 start kapital):**")
    
    initial_investment = 10000
    equal_weight = initial_investment / len(df)
    
    # Scenarier
    scenarios = {
        'Pessimistisk': 0.5,  # -50%
        'Realistisk': 1.0,    # Samme
        'Optimistisk': 1.5    # +50%
    }
    
    scenario_results = {}
    
    for scenario, multiplier in scenarios.items():
        scenario_returns = df['return_1year_pct'] * multiplier
        individual_values = equal_weight * (1 + scenario_returns / 100)
        total_value = individual_values.sum()
        total_return = ((total_value - initial_investment) / initial_investment) * 100
        
        scenario_results[scenario] = {
            'total_value': total_value,
            'total_return': total_return,
            'individual_values': individual_values
        }
        
        st.write(f"{scenario}: ${total_value:,.0f} ({total_return:+.1f}%)")
    
    st.write("2. Scenarie resultater completed oven for")
    
    best_case = max(scenario_results.values(), key=lambda x: x['total_value'])['total_value']
    worst_case = min(scenario_results.values(), key=lambda x: x['total_value'])['total_value']
    
    st.write("3. Best/Worst case:")
    st.write(f"   Best case: ${best_case:,.0f}")
    st.write(f"   Worst case: ${worst_case:,.0f}")
    st.write(f"   Range: ${best_case - worst_case:,.0f}")
    
    # Value at Risk (simpel beregning)
    pessimistic_loss = initial_investment - scenario_results['Pessimistisk']['total_value']
    st.write(f"4. Value at Risk (pessimistisk scenarie): ${pessimistic_loss:,.0f} tab")
    
    st.write("5. Største påvirkninger per scenarie:")
    for scenario, results in scenario_results.items():
        # Find aktie med største afvigelse fra gennemsnit
        avg_value = results['total_value'] / len(df)
        deviations = abs(results['individual_values'] - avg_value)
        biggest_impact = deviations.idxmax()
        biggest_impact_stock = df.iloc[biggest_impact]['symbol']
        st.write(f"   {scenario}: {biggest_impact_stock}")

# Opgave 5: Rebalancing Strategi
st.subheader("⚖️ Opgave 5: Portfolio Rebalancing")
st.write("""
**Lav en rebalancing plan:**
1. Antag nogle aktier er steget meget, andre faldet
2. Beregn ny portefølje vægtning efter 1 år
3. Hvor meget skal købes/sælges for at komme tilbage til lige vægt?
4. Hvad er omkostningen ved rebalancing (antag 0.5% i fees)?
5. Er rebalancing profitable efter omkostninger?
""")

if st.button("Simuler rebalancing"):
    st.write("**Rebalancing Simulation:**")
    
    # Simuler 1-års performance
    initial_investment = 10000
    equal_weight_initial = initial_investment / len(df)
    
    # Efter 1 år
    after_1year = equal_weight_initial * (1 + df['return_1year_pct'] / 100)
    total_portfolio_value = after_1year.sum()
    
    # Nuværende vægte
    current_weights = (after_1year / total_portfolio_value) * 100
    target_weight = 100 / len(df)  # Lige vægt
    
    st.write("1. Efter 1 års performance simuleret")
    st.write(f"2. Portfolio værdi nu: ${total_portfolio_value:,.0f}")
    
    # Afvigelser fra target
    weight_deviations = current_weights - target_weight
    
    st.write("   Største afvigelser fra lige vægt:")
    overweight = weight_deviations.nlargest(3)
    underweight = weight_deviations.nsmallest(3)
    
    for i in overweight.index:
        stock = df.iloc[i]['symbol']
        st.write(f"   Overvægt: {stock} ({weight_deviations[i]:+.1f}% fra target)")
    
    for i in underweight.index:
        stock = df.iloc[i]['symbol']
        st.write(f"   Undervægt: {stock} ({weight_deviations[i]:+.1f}% fra target)")
    
    # Rebalancing beregninger
    target_value_per_stock = total_portfolio_value / len(df)
    trading_needed = abs(after_1year - target_value_per_stock).sum()
    
    st.write(f"3. Total handel nødvendig: ${trading_needed:,.0f}")
    
    # Omkostninger
    fee_rate = 0.005  # 0.5%
    total_fees = trading_needed * fee_rate
    
    st.write(f"4. Rebalancing omkostninger (0.5%): ${total_fees:,.0f}")
    
    # Er det profitabelt?
    # Antag rebalancing giver 1% bedre afkast næste år
    improved_return = total_portfolio_value * 0.01
    net_benefit = improved_return - total_fees
    
    st.write(f"5. Profitabilitet vurdering:")
    st.write(f"   Forventet forbedring: ${improved_return:,.0f}")
    st.write(f"   Netto benefit: ${net_benefit:,.0f}")
    
    if net_benefit > 0:
        st.write("   → ✅ Rebalancing anbefales")
    else:
        st.write("   → ❌ Rebalancing frarådes")

# Portfolio Visualisering
st.subheader("📊 Portfolio Visualisering")

# Lav en simpel portefølje pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Sektor fordeling
sector_counts = df['sector'].value_counts()
ax1.pie(sector_counts.values, labels=sector_counts.index, autopct='%1.1f%%')
ax1.set_title('Sektor Fordeling')

# Performance fordeling
performance_bins = ['Meget Negativ (<-20%)', 'Negativ (-20% til 0%)', 
                   'Positiv (0% til 20%)', 'Meget Positiv (>20%)']
                   
def performance_category(return_pct):
    if return_pct < -20:
        return 'Meget Negativ (<-20%)'
    elif return_pct < 0:
        return 'Negativ (-20% til 0%)'
    elif return_pct < 20:
        return 'Positiv (0% til 20%)'
    else:
        return 'Meget Positiv (>20%)'

perf_categories = df['return_1year_pct'].apply(performance_category).value_counts()
ax2.pie(perf_categories.values, labels=perf_categories.index, autopct='%1.1f%%')
ax2.set_title('Performance Fordeling')

plt.tight_layout()
st.pyplot(fig)

# Diskussionsspørgsmål
st.subheader("💭 Diskussionsspørgsmål")
st.write("""
- Hvorfor er diversifikation vigtigt for risikostyring?
- Hvornår skal man rebalancere sin portefølje?
- Er det bedre at fokusere på få aktier eller mange?
- Hvordan påvirker korrelation mellem aktier portfolio risiko?
- Hvad er forskellen på systematisk og usystematisk risiko?

**Portefølje Management Principper:**
- Diversifikation: Spred risikoen
- Asset Allocation: Strategi før stock picking
- Rebalancing: Behold ønsket risikoprofil
- Risk Management: Begræns downside
- Long-term perspective: Tid i markedet beats timing
""")