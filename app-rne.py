import streamlit as st
import requests
import pandas as pd

# Fonctions pour obtenir le token et les documents

def get_token():
    url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    payload = {
        "username": "kmameri@scores-decisions.com",
        "password": "Intescia2022!"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        st.write(f"Erreur : {response.status_code}")  # Ajoutez cette ligne pour imprimer le code d'erreur
        st.write(f"Réponse : {response.text}")  # Ajoutez cette ligne pour imprimer le texte de la réponse
        return None
        
# Configuration Streamlit
st.set_page_config(
    page_title="Consultation des Actes d'Entreprises",
    layout='wide',
    page_icon="📑",
    menu_items={
         'About': 'Call Kevin MAMERI',
     }
)

# Titre de la page
st.header("Consultation des Actes d'Entreprises via SIREN")
st.caption("App développée par Kevin MAMERI")

# Entrée du SIREN
siren = st.text_input("Veuillez entrer le SIREN de l'entreprise:")

# Obtenir le token
token = get_token()

if token and siren:
    documents = get_documents(siren, token)
    data_list = []

    if documents:
        for doc in documents:
            date_depot = doc.get('dateDepot')
            nom_document = doc.get('nomDocument')
            
            for type_rdd in doc.get('typeRdd', []):
                type_acte = type_rdd.get('typeActe')
                decision = type_rdd.get('decision')
            
            doc_id = doc.get('id')
            download_button = None
            if doc_id:
                # Création d'un lien de téléchargement qui appellera une fonction pour télécharger le document lorsqu'il sera cliqué
                download_button = f'<a href="https://actes-pdf-rne.streamlit.app/download?doc_id={doc_id}&token={token}" target="_blank">Télécharger le document</a>'
                
            data_list.append({
                "Date de dépôt": date_depot,
                "Type d'acte": type_acte,
                "Décision": decision,
                "Télécharger le document": download_button
            })
        
        df = pd.DataFrame(data_list)
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
