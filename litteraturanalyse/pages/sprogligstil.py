import streamlit as st
# indlæs bog
# indlæg bog fra tekstfil og analyser indholdet
import pandas as pd
from collections import Counter
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
