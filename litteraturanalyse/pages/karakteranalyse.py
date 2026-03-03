import streamlit as st
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

st.title("👥 2. Karakteranalyse")

st.markdown("""
I denne sektion analyserer vi:

* **Hvor ofte nævnes hver karakter?**
* **Hvornår i bogen optræder de?** (tidslinje)
* **Sammenhæng mellem karakterer** (optræder i samme kapitler)

👉 **Kan visualiseres som:**
- Tidslinje over karakterernes optræden
- Netværksgraf (hvem "kender" hvem)

**Eksempel:** "Hvem er egentlig hovedpersonen målt på data?"
""")

# Check if data is available, if not try to load it
if 'tekst' not in st.session_state or 'kapitler' not in st.session_state:
    st.warning("⚠️ Data ikke fundet i session. Forsøger at indlæse bog...")
    
    # Try to load the file directly
    try:
        with open('frankenstein.txt', 'r', encoding='utf-8') as file:
            tekst = file.read()
        
        kapitler = re.split(r'Chapter \d+', tekst)
        kapitler = [kapitel.strip() for kapitel in kapitler if kapitel.strip()]
        
        # Store in session state
        st.session_state.tekst = tekst
        st.session_state.kapitler = kapitler
        st.success("✅ Bog indlæst succesfuldt!")
        
    except FileNotFoundError:
        st.error("❌ Filen 'frankenstein.txt' blev ikke fundet.")
        uploaded_file = st.file_uploader("Upload bog (tekstfil)", type=['txt'])
        if uploaded_file is not None:
            tekst = str(uploaded_file.read(), "utf-8")
            kapitler = re.split(r'Chapter \d+', tekst)
            kapitler = [kapitel.strip() for kapitel in kapitler if kapitel.strip()]
            
            st.session_state.tekst = tekst
            st.session_state.kapitler = kapitler
            st.success("✅ Bog uploadet og indlæst!")
            st.rerun()

# Kør analysen hvis tekst er tilgængelig
st.subheader("📊 Hvem er egentlig hovedpersonen målt på data?")

if 'tekst' in st.session_state and 'kapitler' in st.session_state:
    tekst = st.session_state.tekst
    kapitler = st.session_state.kapitler
    
    # Definer karakterer (kan tilpasses efter bog)
    karakterer = ['Victor', 'Frankenstein', 'Elizabeth', 'Clerval', 'Walton', 'William', 'Justine', 'Monster', 'Creature']
    
    # Find hvor ofte hver karakter nævnes
    karakter_counts = {}
    for karakter in karakterer:
        count = len(re.findall(r'\b' + karakter + r'\b', tekst, re.IGNORECASE))
        karakter_counts[karakter] = count
    
    # Fjern karakterer der ikke nævnes
    karakter_counts = {k: v for k, v in karakter_counts.items() if v > 0}
    
    # Find karakterers position i bogen (kapitel)
    karakter_kapitler = {}
    for i, kapitel in enumerate(kapitler):
        for karakter in karakter_counts.keys():
            if re.search(r'\b' + karakter + r'\b', kapitel, re.IGNORECASE):
                if karakter not in karakter_kapitler:
                    karakter_kapitler[karakter] = []
                karakter_kapitler[karakter].append(i + 1)
    
    # Find sammenhæng mellem karakterer (co-occurrence)
    karakter_netværk = {}
    for i, kapitel in enumerate(kapitler):
        kapitlets_karakterer = []
        for karakter in karakter_counts.keys():
            if re.search(r'\b' + karakter + r'\b', kapitel, re.IGNORECASE):
                kapitlets_karakterer.append(karakter)
        
        # Find alle par af karakterer i samme kapitel
        for j, char1 in enumerate(kapitlets_karakterer):
            for char2 in kapitlets_karakterer[j+1:]:
                pair = tuple(sorted([char1, char2]))
                karakter_netværk[pair] = karakter_netværk.get(pair, 0) + 1
    
    # Vis resultater i kolonner
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Karakterfrekvens")
        if karakter_counts:
            sorted_karakterer = sorted(karakter_counts.items(), key=lambda x: x[1], reverse=True)
            karakter_df = pd.DataFrame(sorted_karakterer, columns=['Karakter', 'Antal'])
            st.dataframe(karakter_df)
            st.bar_chart(karakter_df.set_index('Karakter'))
            
            # Hvem er hovedpersonen?
            hovedperson = sorted_karakterer[0][0]
            st.success(f"🎭 **Hovedpersonen er:** {hovedperson} ({sorted_karakterer[0][1]} nævnelser)")
    
    with col2:
        st.markdown("### ⏰ Karaktertidslinje")
        if karakter_kapitler:
            # Opret timeline data
            timeline_data = []
            for karakter, kapitler_list in karakter_kapitler.items():
                for kapitel in kapitler_list:
                    timeline_data.append({'Karakter': karakter, 'Kapitel': kapitel})
            
            timeline_df = pd.DataFrame(timeline_data)
            if not timeline_df.empty:
                # Pivot for at vise karakterer over kapitler
                pivot = timeline_df.groupby(['Kapitel', 'Karakter']).size().unstack(fill_value=0)
                st.dataframe(pivot)
                st.line_chart(pivot)
    
    # Netværksgraf
    st.markdown("### 🕸️ Karakternetværk")
    if karakter_netværk:
        # Find de stærkeste forbindelser
        top_forbindelser = sorted(karakter_netværk.items(), key=lambda x: x[1], reverse=True)[:10]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top forbindelser:**")
            forbindelse_df = pd.DataFrame(top_forbindelser, columns=['Karakterpar', 'Fælles kapitler'])
            forbindelse_df['Karakterpar'] = forbindelse_df['Karakterpar'].apply(lambda x: f"{x[0]} ↔ {x[1]}")
            st.dataframe(forbindelse_df)
        
        with col2:
            st.markdown("**Netværksgraf:**")
            if len(top_forbindelser) > 0:
                # Simpel netværksvisualisering
                G = nx.Graph()
                for (char1, char2), weight in top_forbindelser[:8]:  # Begræns for klarhed
                    G.add_edge(char1, char2, weight=weight)
                
                col1_net, col2_net, col3_net = st.columns([1, 2, 1])
                with col2_net:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    pos = nx.spring_layout(G)
                    
                    # Tegn netværk
                    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800, ax=ax)
                    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
                    
                    # Tegn kanter med vægt
                    edges = G.edges()
                    weights = [G[u][v]['weight'] for u, v in edges]
                    nx.draw_networkx_edges(G, pos, width=[w/3 for w in weights], alpha=0.7, ax=ax)
                    
                    ax.set_title('Karakterforbindelser\n(tykkere linjer = hyppigere sammen)')
                    ax.axis('off')
                    st.pyplot(fig)
    
    # Karakterudvikling gennem bogen
    st.markdown("### 📈 Karakterudvikling gennem bogen")
    if karakter_kapitler:
        udvikling_data = []
        for karakter in karakter_counts.keys():
            if karakter in karakter_kapitler:
                kapitler_med_karakter = karakter_kapitler[karakter]
                for kapitel in range(1, len(kapitler) + 1):
                    optræder = 1 if kapitel in kapitler_med_karakter else 0
                    udvikling_data.append({
                        'Kapitel': kapitel,
                        'Karakter': karakter,
                        'Optræder': optræder
                    })
        
        if udvikling_data:
            udvikling_df = pd.DataFrame(udvikling_data)
            pivot_udvikling = udvikling_df.pivot(index='Kapitel', columns='Karakter', values='Optræder')
            
            # Vis som heatmap i begrænsede kolonner
            col1_heat, col2_heat, col3_heat = st.columns([1, 2, 1])
            with col2_heat:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(pivot_udvikling.T, cmap='Blues', cbar_kws={'label': 'Optræder i kapitel'}, ax=ax)
                ax.set_title('Karakteroptræden gennem bogen')
                ax.set_xlabel('Kapitel')
                ax.set_ylabel('Karakter')
                st.pyplot(fig)
            
else:
    st.warning("Indlæs først en bog på introduktionssiden for at se karakteranalysen.")