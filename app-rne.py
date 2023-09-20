import streamlit as st
import requests
from io import BytesIO

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

def download_document(doc_id, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/actes/{doc_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
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
    data_list = []  # Pour stocker les données de chaque document
    if documents:
        for doc in documents:
            date_depot = doc.get('dateDepot')
            nom_document = doc.get('nomDocument')
            
            for type_rdd in doc.get('typeRdd', []):
                type_acte = type_rdd.get('typeActe')
                decision = type_rdd.get('decision')
            
            doc_id = doc.get('id')  # Assume 'id' is the key that contains the document ID
            download_button = None
            if doc_id:
                pdf_data = download_document(doc_id, token)
                if pdf_data:
                    # Créer un bouton de téléchargement en tant que chaîne HTML
                   import base64
                   download_button = f'<a href="data:application/pdf;base64,{base64.b64encode(pdf_data.read()).decode("utf-8")}" download="{doc_id}.pdf">Télécharger le document</a>'

                else:
                    st.error("Impossible de télécharger le document.")

            # Ajoutez les données du document actuel à data_list
            data_list.append({
                "Date de dépôt": date_depot,
                "Type d'acte": type_acte,
                "Décision": decision,
                "Télécharger le document": download_button
            })
        
        # Convertissez data_list en un DataFrame
        df = pd.DataFrame(data_list)

        # Affichez le DataFrame avec Streamlit
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
