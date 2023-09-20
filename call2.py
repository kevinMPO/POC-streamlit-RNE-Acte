import streamlit as st
import openai
import os

# Streamlit config
st.set_page_config(
    page_title="Speech Emotion Recognition app",
    layout='wide',
    page_icon="musical_note",
    menu_items={
         'About': 'Call Kevin MAMERI',
     }
)

# Set page title, header and links to docs
st.header("🗣 Call transcription and analysis POC using Python, Streamlit and OpenAI✨")
st.caption(f"App developed by IntescIA ;)")

# Let the user input the OPENAI_API_KEY
openai_api_key = st.text_input("Please enter your OPENAI_API_KEY", type="password")

if openai_api_key:
    openai.api_key = openai_api_key
else:
    st.warning("Please enter your OPENAI_API_KEY to proceed.")
    st.stop()

upload_path = "upload_path/"

st.markdown("""---""")
st.subheader("Upload The Audio File Below")
uploaded_file = st.file_uploader("Choose an audio file", accept_multiple_files=False, label_visibility='hidden')

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_path = f"./{file_name}"

    with st.spinner(f"Processing Audio ... 💫"):
        audio_bytes = uploaded_file.read()
        with open(file_path,"wb") as f:
            f.write((uploaded_file).getbuffer())

        with open(file_path, "rb") as audio_file:
            transcribe = openai.Audio.transcribe("whisper-1", audio_file)
            txt_transcribe = transcribe.text

        st.title("Generated Original Audio Text 🔊")
        st.write(txt_transcribe)

    with st.spinner(f"Processing Text ... 💫"):
        model = "gpt-3.5-turbo-16k"
        system_input = "Tu es le chef d'entreprise steeve jobs, tu dois analyser l’échange de notre commercial avec un prospect qui présente notre applicatif, ta réponse dont contenir 3 parties : Les points positifs de cet échange. Les points à améliorer dans sa présentation. Les uses cases qui pour intéressant pour nos product owner."
        user_input = txt_transcribe
        res = openai.ChatCompletion.create(
          model=model,
          messages=[
                {"role": "system", "content": system_input},
                {"role": "user", "content": user_input},
            ]
        )
        st.title("Generated analysis 🔊")
        st.write(res.choices[0].message.content)