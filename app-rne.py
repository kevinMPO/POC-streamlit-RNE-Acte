import streamlit as st
import requests
from io import BytesIO
import pandas as pd
import base64

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

@st.cache(allow_output_mutation=True)
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

@st.cache(allow_output_mutation=True)
def download_document(doc_id, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/actes/{doc_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
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
                pdf_data = download_document(doc_id, token)
                if pdf_data:
                    # Créer un bouton de téléchargement en tant que chaîne HTML
                    download_button = f'<a href="data:application/pdf;base64,{pdf_data}" download="{doc_id}.pdf">Télécharger le document</a>'
                else:
                    download_button = "Impossible de télécharger le document"
                
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
