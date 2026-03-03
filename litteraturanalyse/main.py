import streamlit as st
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Konfigurer siden
st.set_page_config(
    page_title="Litteraturanalyse", page_icon="📚", layout="wide")

import re
# indlæs tekstfil
with open('frankenstein.txt', 'r', encoding='utf-8') as file:
    tekst = file.read()
# del tekst i kapitler (antager kapitler er adskilt af "Chapter X")
kapitler = re.split(r'Chapter \d+', tekst)
# fjern tomme kapitler
kapitler = [kapitel.strip() for kapitel in kapitler if kapitel.strip()]
# analyser længde af kapitler
kapitel_længder = [len(kapitel.split()) for kapitel in kapitler]
df_kapitler = pd.DataFrame({
    'Kapitel': range(1, len(kapitler) + 1),
    'Længde (ord)': kapitel_længder
})
print("Længde af kapitler:")
print(df_kapitler)



st.title("📊 Sproglig stil")
st.markdown("""
I det følgende vil vi bestemme: 

* Ordhyppighed (top 10 / top 100 ord)
* Mest brugte navne (karakterer)
* Gennemsnitlig sætningslængde
* Hyppighed af lange vs. korte ord
* Andel af forskellige ord (vocabulary richness)

Det giver os en idé om forfatterens stil og om sproget er simpelt eller komplekst
""")

st.header("Ordhyppighed")
st.subheader("Graf over Top 10 ord")

# Ordhyppighedsanalyse
ord_liste = re.findall(r'\b\w+\b', tekst.lower())
ord_tælling = Counter(ord_liste)
mest_almindelige_ord = ord_tælling.most_common(10)
# Vis graf
df_ord = pd.DataFrame(mest_almindelige_ord, columns=['Ord', 'Tælling'])
st.bar_chart(df_ord.set_index('Ord'))

# vis en wordcloud hvis muligt
try: 
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(ord_tælling))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
except ImportError:
    st.info("Installer 'wordcloud' og 'matplotlib' for at se en wordcloud.")

    

# Mest brugte navne i bogen
## Antager navne starter med stort bogstav og søg efter dem
navne = re.findall(r'\b[A-Z][a-z]+\b', tekst)
navne_tælling = Counter(navne)
mest_brugte_navne = navne_tælling.most_common(10)
st.subheader("Mest brugte navne")
df_navne = pd.DataFrame(mest_brugte_navne, columns=['Navn', 'Tælling'])
st.bar_chart(df_navne.set_index('Navn'))

# Gennemsnitlig sætningslængde
sætninger = re.split(r'[.!?]+', tekst)
sætnings_længder = [len(sætning.split()) for sætning in sætninger if sætning.strip()]
gennemsnitlig_sætnings_længde = sum(sætnings_længder) / len(sætnings_længder) if sætnings_længder else 0
st.subheader("Gennemsnitlig sætningslængde")
st.write(f"Gennemsnitlig sætningslængde: {gennemsnitlig_sætnings_længde:.2f} ord")


# Hyppighed af lange vs korte ord
## Definer lange ord som dem med mere end 6 bogstaver
## korte ord som dem med 6 eller færre bogstaver

lange_ord = [ord for ord in ord_liste if len(ord) > 6]
korte_ord = [ord for ord in ord_liste if len(ord) <= 6]
st.subheader("Hyppighed af lange vs korte ord")
st.write(f"Antal lange ord (>6 bogstaver): {len(lange_ord)}")
st.write(f"Antal korte ord (<=6 bogstaver): {len(korte_ord)}")              

# Andel af forskellige ord
## Unikke ord vs totale ord
 
unikke_ord = set(ord_liste)
andel_unikke_ord = len(unikke_ord) / len(ord_liste) * 100 if ord_liste else 0                                    
st.subheader("Andel af unikke ord")
st.write(f"Andel af unikke ord: {andel_unikke_ord:.2f}%")


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

# sentimentanalyse:

st.header("📈 Sentimentanalyse")

st.write("Sentimentaanalyse undersøger de følelsesmæssige toner i teksten for at afgøre, om de er positive, negative eller neutrale. Dette kan give indsigt i stemningen og temaerne i bogen.")
from textblob import TextBlob

# lav sentimentanalyse pr. kapitel
st.write("Polaritet pr. kapitel:")
sentiment_data = []
for i, kapitel in enumerate(kapitler):
    blob = TextBlob(kapitel)
    sentiment = blob.sentiment.polarity  # Værdi mellem -1 (negativ) og 1 (positiv)
    sentiment_data.append({'Kapitel': i + 1, 'Sentiment': sentiment})
sentiment_df = pd.DataFrame(sentiment_data)
st.line_chart(sentiment_df.set_index('Kapitel'))

# vis på sætningsniveau
st.write("Sentimentfordeling på sætningsniveau:")
sætninger = re.split(r'[.!?]+', tekst)
sætning_sentiment = [TextBlob(sætning).sentiment.polarity for sætning in sætninger if sætning.strip()]
sentiment_series = pd.Series(sætning_sentiment)
fig, ax = plt.subplots()
ax.hist(sentiment_series, bins=20, edgecolor='black')
ax.set_xlabel('Sentiment Polarity')
ax.set_ylabel('Antal sætninger')
ax.set_title('Sentimentfordeling')
st.pyplot(fig)
forbindelse_df['Karakterpar'] = forbindelse_df['Karakterpar'].apply(lambda x: f"{x[0]} ↔ {x[1]}")

# diskursanalyse implementering:
st.header("🗣️ Diskursanalyse")  
st.write("Diskursanalyse undersøger, hvordan sprog bruges til at konstruere mening og magtforhold i teksten. Det kan hjælpe os med at forstå, hvordan karakterer og temaer præsenteres og interagerer.")

# --- 1. Nøgleord i kontekst (KWIC) ---
st.subheader("1. Nøgleord i kontekst (KWIC)")
st.write("Se hvordan et bestemt ord bruges i sin kontekst i teksten.")

søgeord = st.text_input("Skriv et nøgleord:", value="monster")
kontekst_vindue = st.slider("Antal ord på hver side af nøgleordet:", 3, 15, 7)

if søgeord:
    ord_liste_kwic = tekst.split()
    kwic_resultater = []
    for i, ord in enumerate(ord_liste_kwic):
        if re.search(r'\b' + re.escape(søgeord) + r'\b', ord, re.IGNORECASE):
            start = max(0, i - kontekst_vindue)
            slut = min(len(ord_liste_kwic), i + kontekst_vindue + 1)
            kontekst = " ".join(ord_liste_kwic[start:i]) + f" **[{ord}]** " + " ".join(ord_liste_kwic[i+1:slut])
            kwic_resultater.append(kontekst)
    st.write(f"Fandt **{len(kwic_resultater)}** forekomster af '{søgeord}':")
    for res in kwic_resultater[:15]:
        st.markdown(f"> {res}")

# --- 2. Modalverber og sikkerhed/usikkerhed ---
st.subheader("2. Modalverber – sikkerhed og usikkerhed")
st.write("Modalverber afslører, i hvilken grad karakterer udtrykker sikkerhed, tvivl, forpligtelse eller mulighed.")

modalverber = {
    "Høj sikkerhed (must, will, shall)": ["must", "will", "shall"],
    "Mulighed (could, might, may)": ["could", "might", "may"],
    "Forpligtelse (should, ought)": ["should", "ought"],
    "Vilje/ønske (would, wish)": ["would", "wish"],
}
modal_data = []
for kategori, ord_gruppe in modalverber.items():
    antal = sum(len(re.findall(r'\b' + ord + r'\b', tekst, re.IGNORECASE)) for ord in ord_gruppe)
    modal_data.append({"Kategori": kategori, "Antal": antal})

modal_df = pd.DataFrame(modal_data)
st.bar_chart(modal_df.set_index("Kategori"))

# --- 3. Personlige pronominer og magtforhold ---
st.subheader("3. Personlige pronominer – stemmer og perspektiver")
st.write("Hvem taler? Hvem omtales? Analysen af pronominer afslører fortællerens perspektiv og magtrelationer.")

pronominer = {
    "Jeg (I, me, my, myself)": ["I", "me", "my", "myself"],
    "Vi (we, us, our)": ["we", "us", "our", "ourselves"],
    "Du (you, your)": ["you", "your", "yourself"],
    "Han (he, him, his)": ["he", "him", "his"],
    "Hun (she, her)": ["she", "her"],
    "De (they, them, their)": ["they", "them", "their"],
}
pronomen_data = []
for label, ord_gruppe in pronominer.items():
    antal = sum(len(re.findall(r'\b' + ord + r'\b', tekst, re.IGNORECASE)) for ord in ord_gruppe)
    pronomen_data.append({"Pronomen": label, "Antal": antal})

pronomen_df = pd.DataFrame(pronomen_data)
st.bar_chart(pronomen_df.set_index("Pronomen"))

# --- 4. Evaluerende sprog – positiv vs. negativ framing ---
st.subheader("4. Evaluerende sprog – framing af begreber")
st.write("Hvilke ord bruges til at beskrive centrale begreber positivt eller negativt?")

positive_ord = ["beautiful", "good", "happy", "joy", "love", "hope", "kind", "gentle", "noble", "great"]
negative_ord = ["terrible", "evil", "monster", "horror", "ugly", "dark", "wretched", "miserable", "dreadful", "despair"]

pos_antal = {ord: len(re.findall(r'\b' + ord + r'\b', tekst, re.IGNORECASE)) for ord in positive_ord}
neg_antal = {ord: len(re.findall(r'\b' + ord + r'\b', tekst, re.IGNORECASE)) for ord in negative_ord}

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Positive ord:**")
    pos_df = pd.DataFrame(list(pos_antal.items()), columns=["Ord", "Antal"]).sort_values("Antal", ascending=False)
    st.dataframe(pos_df)
with col2:
    st.markdown("**Negative ord:**")
    neg_df = pd.DataFrame(list(neg_antal.items()), columns=["Ord", "Antal"]).sort_values("Antal", ascending=False)
    st.dataframe(neg_df)

# --- 5. Tematisk nøgleordsanalyse ---
st.subheader("5. Tematisk analyse – dominerende diskurser")
st.write("Hvilke temaer dominerer teksten? Søg efter ordgrupper knyttet til centrale temaer.")

temaer = {
    "Natur og romantik": ["nature", "mountain", "sea", "storm", "beautiful", "sublime", "wind", "forest"],
    "Videnskab og skabelse": ["science", "create", "experiment", "knowledge", "discovery", "laboratory"],
    "Død og forfald": ["death", "dead", "dying", "grave", "corpse", "destruction", "decay"],
    "Ensomhed og isolation": ["alone", "lonely", "isolation", "abandoned", "outcast", "forsaken"],
    "Familie og tilhørsforhold": ["family", "father", "mother", "brother", "sister", "friend", "love"],
}

tema_data = []
for tema, ord_gruppe in temaer.items():
    antal = sum(len(re.findall(r'\b' + ord + r'\b', tekst, re.IGNORECASE)) for ord in ord_gruppe)
    tema_data.append({"Tema": tema, "Antal nøgleord": antal})

tema_df = pd.DataFrame(tema_data).sort_values("Antal nøgleord", ascending=False)
st.bar_chart(tema_df.set_index("Tema"))

# --- 6. Diskursudvikling pr. kapitel ---
st.subheader("6. Diskursudvikling – hvordan temaer bevæger sig gennem bogen")
st.write("Spor hvordan temaer vokser og aftager gennem bogens kapitler.")

valgt_tema = st.selectbox("Vælg et tema at spore:", list(temaer.keys()))
tema_pr_kapitel = []
for i, kapitel in enumerate(kapitler):
    antal = sum(len(re.findall(r'\b' + ord + r'\b', kapitel, re.IGNORECASE)) for ord in temaer[valgt_tema])
    tema_pr_kapitel.append({"Kapitel": i + 1, "Forekomster": antal})

tema_kap_df = pd.DataFrame(tema_pr_kapitel)
st.line_chart(tema_kap_df.set_index("Kapitel"))


