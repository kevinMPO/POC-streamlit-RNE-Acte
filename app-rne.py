import streamlit as st
import requests
import pandas as pd

# Fonctions pour obtenir le token et les documents
def get_token(stage=1):
    url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    payload = {
        "username": "kmameri@scores-decisions.com",
        "password": "POC-Kevin-2023!"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        st.write(f"Erreur : {response.status_code}")
        st.write(f"Réponse : {response.text}")
        return None

# Obtenir le token (étape 1)
token = get_token(stage=1)

def get_documents(siren, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("actes")
    else:
        st.write(f"Erreur lors de la récupération des documents : {response.status_code}")
        st.write(f"Réponse : {response.text}")
        return None


def get_document(doc_id, token=token):
    url = f"https://registre-national-entreprises.inpi.fr/api/actes/{doc_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None


def trigger_download(data, filename) -> str:
    import base64
    b64 = base64.b64encode(data).decode()
    dl_link = f"""
                <html>
                <head>
                <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
                <script>
                $('<a href="data:application/octet-stream;base64,{b64}" download="{filename}">')[0].click()
                </script>
                </head>
                </html>"""
    return dl_link


def callback_button(doc_id) -> None:
    import streamlit.components.v1 as components
    trigger = trigger_download(get_document(doc_id), f"{doc_id}.pdf")
    components.html(html=trigger, height=0, width=0)
    return

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


if token and siren:
    documents = get_documents(siren, token)
    data_list = []

    if documents:
        colms = st.columns((1, 2, 2, 1))
        fields = ["Date de dépôt", "Type d'acte", "Décision", "Télécharger le document"]
        for col, field_name in zip(colms, fields):
            col.write(field_name)
        for doc in documents:
            col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
            col1.write(doc["dateDepot"])
            if "typeRdd" in doc:
                col2.write("  \n".join(e.get("typeActe", "") for e in doc["typeRdd"]))
                col3.write("  \n".join(e.get("decision", "") for e in doc["typeRdd"]))
            button_phold = col4.empty()
            do_action = button_phold.button("PDF", on_click=callback_button, args=(doc["id"],), key=f"button_actes_{doc['id']}")
            if do_action:
                pass
                button_phold.empty()
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
