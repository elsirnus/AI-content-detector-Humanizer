import re
import streamlit as st
import sys
import os

# Add the project root to sys.path so imports from pages/ work
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import processing helpers from the existing Streamlit page
from pages.humanize_text import (
    extract_citations,
    restore_citations,
    minimal_rewriting,
    preserve_linebreaks_rewrite,
    count_words,
    count_sentences,
)

DESCRIPTION = """
AI Text Humanizer — Streamlit API Simulator

This Streamlit app simulates the FastAPI endpoints (/health and /humanize) through an interactive UI.
It provides the same functionality: health check and text humanization with options for synonym
replacement intensity, transition insertion, and line break preservation.

Use the controls below to "call" the endpoints and view JSON-like responses.
"""

EXAMPLE_REQ = {
    "text": "Recent studies (Smith et al., 2020) show promising results. It can't be ignored.",
    "p_syn": 0.3,
    "p_trans": 0.2,
    "preserve_linebreaks": True,
}

EXAMPLE_RESP = {
    "humanized_text": "Moreover, Recent studies (Smith et al., 2020) show promising results. It cannot be ignored.",
    "orig_word_count": 11,
    "orig_sentence_count": 2,
    "new_word_count": 13,
    "new_sentence_count": 3,
    "words_added": 2,
    "sentences_added": 1,
}

def _clean_final_text(final_text: str) -> str:
    final_text = re.sub(r"[ \t]+([.,;:!?])", r"\1", final_text)
    final_text = re.sub(r"(\()[ \t]+", r"\1", final_text)
    final_text = re.sub(r"[ \t]+(\))", r"\1", final_text)
    final_text = re.sub(r"[ \t]{2,}", " ", final_text)
    final_text = re.sub(r"``\s*(.+?)\s*''", r'"\1"', final_text)
    return final_text

st.set_page_config(page_title="AI Text Humanizer (Streamlit API)", layout="wide")
st.title("AI Text Humanizer — Streamlit API Simulator")
st.markdown(DESCRIPTION)

# Health endpoint simulator
st.header("GET /health")
st.markdown("Simulates the health check endpoint.")
if st.button("Call /health"):
    st.json({"status": "ok"})

st.markdown("---")

# Humanize endpoint simulator
st.header("POST /humanize")
st.markdown("Simulates the humanize endpoint. Fill in the request fields and click 'Call /humanize' to see the response.")

col1, col2 = st.columns([2, 1])

with col1:
    text = st.text_area("text (string, required)", value=EXAMPLE_REQ["text"], height=150)
    p_syn = st.slider("p_syn (float, 0.0-1.0)", 0.0, 1.0, EXAMPLE_REQ["p_syn"], 0.01)
    p_trans = st.slider("p_trans (float, 0.0-1.0)", 0.0, 1.0, EXAMPLE_REQ["p_trans"], 0.01)
    preserve_linebreaks = st.checkbox("preserve_linebreaks (bool)", value=EXAMPLE_REQ["preserve_linebreaks"])

with col2:
    st.markdown("**Request JSON Preview**")
    req_json = {
        "text": text,
        "p_syn": p_syn,
        "p_trans": p_trans,
        "preserve_linebreaks": preserve_linebreaks,
    }
    st.json(req_json)

    if st.button("Call /humanize"):
        if not text.strip():
            st.error("`text` must be a non-empty string")
        else:
            with st.spinner("Processing..."):
                orig_wc = count_words(text)
                orig_sc = count_sentences(text)

                no_refs_text, placeholders = extract_citations(text)

                if preserve_linebreaks:
                    rewritten = preserve_linebreaks_rewrite(no_refs_text, p_syn=p_syn, p_trans=p_trans)
                else:
                    rewritten = minimal_rewriting(no_refs_text, p_syn=p_syn, p_trans=p_trans)

                final_text = restore_citations(rewritten, placeholders)
                final_text = _clean_final_text(final_text)

                new_wc = count_words(final_text)
                new_sc = count_sentences(final_text)

                resp = {
                    "humanized_text": final_text,
                    "orig_word_count": orig_wc,
                    "orig_sentence_count": orig_sc,
                    "new_word_count": new_wc,
                    "new_sentence_count": new_sc,
                    "words_added": new_wc - orig_wc,
                    "sentences_added": new_sc - orig_sc,
                }

            st.subheader("Response JSON")
            st.json(resp)

st.markdown("---")
st.markdown("## API Documentation & Examples")
st.markdown("This app simulates the following API contract:")

with st.expander("Request Schema"):
    st.markdown("""
    - **text** (string, required): The input text to humanize.
    - **p_syn** (float, optional): Synonym replacement intensity (0.0-1.0). Default 0.2.
    - **p_trans** (float, optional): Transition insertion probability (0.0-1.0). Default 0.2.
    - **preserve_linebreaks** (bool, optional): Whether to keep original line breaks. Default true.
    """)

with st.expander("Response Schema"):
    st.markdown("""
    - **humanized_text** (string): The transformed human-like text result.
    - **orig_word_count** (int): Original word count.
    - **orig_sentence_count** (int): Original sentence count.
    - **new_word_count** (int): New word count.
    - **new_sentence_count** (int): New sentence count.
    - **words_added** (int): Words added.
    - **sentences_added** (int): Sentences added.
    """)

with st.expander("Example Request & Response"):
    st.markdown("**Example Request:**")
    st.json(EXAMPLE_REQ)
    st.markdown("**Example Response:**")
    st.json(EXAMPLE_RESP)

st.markdown("---")
st.markdown("### Notes")
st.markdown("""
- This is a UI simulator for the API endpoints. For actual HTTP API calls, use the FastAPI version or the background Flask API in `api/humanize_api.py`.
- The processing logic is imported from `pages/humanize_text.py`.
- Deployable on Streamlit Cloud: commit this folder and deploy from GitHub.
""")