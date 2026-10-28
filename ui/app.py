"""Interface Streamlit cliente de l'API de sentiment."""

import pandas as pd
import streamlit as st

from ui import client

st.set_page_config(page_title="Analyse de sentiment", page_icon="💬", layout="wide")
st.title("Analyse de sentiment des avis clients")

if "api_session" not in st.session_state:
    st.session_state.api_session = client.creer_session()
session = st.session_state.api_session

etat = client.sante(session)
if not etat.ok:
    st.error(etat.message)
    st.stop()

st.caption(f"API prête : {etat.message}")
onglet_avis, onglet_fichier, onglet_aide = st.tabs(
    ["Un avis", "Un fichier d'avis", "Comment ça marche"]
)

with onglet_avis:
    texte = st.text_area("Avis à analyser", "Livraison rapide, produit conforme.", height=130)
    if st.button("Analyser", type="primary"):
        resultat = client.predire(session, texte)
        if not resultat.ok:
            st.warning(resultat.message)
        elif resultat.label == "INDETERMINE":
            st.metric(client.VERDICTS[resultat.label], f"{resultat.score:.0%}")
            st.info("La confiance est sous le seuil d'abstention : un humain doit trancher.")
        else:
            st.metric(client.VERDICTS[resultat.label], f"{resultat.score:.0%}")

with onglet_fichier:
    st.write("Choisissez un fichier CSV contenant une colonne `review` ou `text`.")
    fichier = st.file_uploader("Choisir un fichier", type="csv")
    if fichier is not None:
        try:
            donnees = pd.read_csv(fichier)
            colonne = "review" if "review" in donnees.columns else "text"
            if colonne not in donnees.columns:
                raise KeyError("Le fichier doit contenir une colonne 'review' ou 'text'.")
        except (KeyError, pd.errors.ParserError, UnicodeDecodeError) as erreur:
            st.error(str(erreur))
        else:
            resultats = client.predire_lot(session, donnees[colonne].fillna("").astype(str).tolist())
            donnees["prediction"] = [
                resultat.label if resultat.ok else "REFUS OU ERREUR" for resultat in resultats
            ]
            donnees["verdict"] = [
                client.VERDICTS.get(resultat.label, resultat.message) if resultat.ok else resultat.message
                for resultat in resultats
            ]
            donnees["confiance"] = [resultat.score for resultat in resultats]
            st.write(client.resumer(resultats))
            st.dataframe(donnees, use_container_width=True)
            st.download_button(
                "Télécharger les résultats",
                donnees.to_csv(index=False).encode("utf-8"),
                "resultats.csv",
                "text/csv",
            )

with onglet_aide:
    st.markdown(
        """
**Ce que fait cette interface.** Elle envoie les avis à l'API et traduit les réponses
en verdicts compréhensibles. Le modèle reste chargé et utilisé côté API.

**Le seuil d'abstention.** Quand l'API renvoie `INDETERMINE`, la confiance est sous
le seuil d'abstention : un humain doit trancher.
        """
    )
