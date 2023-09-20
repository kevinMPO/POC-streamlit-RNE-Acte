import streamlit as st
import requests

# Fonctions pour obtenir le token et les documents
def get_token():
    url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    payload = {
        "username": "kmameri@scores-decisions.com",
        "password": "Intesciarne2022!"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None

def get_documents(siren, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("actes")
    else:
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

import pandas as pd

if token and siren:
    documents = get_documents(siren, token)
    if documents:
        data = []
        for doc in documents:
            date_depot = doc.get('dateDepot')
            id_doc = doc.get('id')
            type_rdds = doc.get('typeRdd', [])
            for type_rdd in type_rdds:
                type_acte = type_rdd.get('typeActe')
                decision = type_rdd.get('decision')
                data.append([id_doc, date_depot, type_acte, decision])
        
        df = pd.DataFrame(data, columns=['id_doc','Date de dépôt', "Type d'acte", 'Décision'])
        st.write(df)
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")

