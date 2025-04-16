import connectdb
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
import gensim.downloader as api

word2vec_model = api.load('word2vec-google-news-300')

import streamlit as st

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

crsr, connection = connectdb.connect()

def get_sentence_vector(sentence, model):
    words = sentence.split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return np.zeros(model.vector_size)  
    return np.mean(word_vectors, axis=0)

def sqlexample(text):
    try:
        with open('DDL.sql', 'r') as create_file:
            create_command = create_file.read()
            crsr.execute(create_command)
            logging.info("Example table created successfully.")

        embedding = word2vec_model[text]
 
        crsr.execute(
            "INSERT INTO example (content, embedding) VALUES (%s, %s)",
            (text, embedding)
        )

        return text, embedding
 
    except Exception as error:
        logging.error(f"An error occurred: {error}")
 
    finally:
        if crsr is not None:
            crsr.close()
            logging.warning("Cursor closed.")
 
        if connection is not None:
            connection.commit()
            connection.close()
            logging.warning("Database connection terminated.")
 
st.set_page_config(page_title="Text to Embedding Viewer", layout="wide")

st.title("Text to Embedding Generator")

text_input = st.text_area("Enter text to embed:", height=150)
if st.button("Generate Embedding") and text_input.strip():
    try:
        logging.debug("In the loop.")
        text, embedding = sqlexample(text_input)
        
        st.success("Embedding generated successfully!")
        st.markdown("### Embedding (768-dimensional vector):")
        st.json(embedding)
 
    except Exception as e:
        st.error(f"Error: {e}")

