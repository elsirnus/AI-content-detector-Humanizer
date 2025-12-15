import re
import threading
import time
from typing import Optional

import streamlit as st
from flask import Flask, request, jsonify
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
AI Text Humanizer

This Streamlit page provides an interactive UI and also starts a small
local HTTP API (Flask) in a background thread so you can call:

- GET  /health
- POST /humanize  (JSON body)

The endpoints reuse the same processing pipeline as the UI and expose the
same options (p_syn, p_trans, preserve_linebreaks). The local API listens
on 127.0.0.1:8001 by default.
"""


# -----------------------------
# Flask API (background)
# -----------------------------
API_HOST = "127.0.0.1"
API_PORT = 8001

flask_app = Flask("humanizer_api")


@flask_app.route("/health", methods=["GET"])
def flask_health():
    return jsonify({"status": "ok"})


@flask_app.route("/humanize", methods=["POST"])
def flask_humanize():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    text = data.get("text", "")
    p_syn = data.get("p_syn", 0.2)
    p_trans = data.get("p_trans", 0.2)
    preserve_linebreaks = data.get("preserve_linebreaks", True)

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "`text` must be a non-empty string"}), 400

    # Processing (reuse helpers)
    orig_wc = count_words(text)
    orig_sc = count_sentences(text)

    no_refs_text, placeholders = extract_citations(text)

    if preserve_linebreaks:
        rewritten = preserve_linebreaks_rewrite(
            no_refs_text, p_syn=p_syn, p_trans=p_trans)
    else:
        rewritten = minimal_rewriting(
            no_refs_text, p_syn=p_syn, p_trans=p_trans)

    final_text = restore_citations(rewritten, placeholders)
    final_text = re.sub(r"[ \t]+([.,;:!?])", r"\1", final_text)
    final_text = re.sub(r"(\()[ \t]+", r"\1", final_text)
    final_text = re.sub(r"[ \t]+(\))", r"\1", final_text)
    final_text = re.sub(r"[ \t]{2,}", " ", final_text)
    final_text = re.sub(r"``\s*(.+?)\s*''", r'"\1"', final_text)

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

    return jsonify(resp)


def run_flask_app(host=API_HOST, port=API_PORT):
    # Use threaded=True to allow concurrent Streamlit and Flask operations

    flask_app.run(host=host, port=port, threaded=True)


# -----------------------------
# Streamlit UI (keeps docs/examples)
# -----------------------------
def _clean_final_text(final_text: str) -> str:
    final_text = re.sub(r"[ \t]+([.,;:!?])", r"\1", final_text)
    final_text = re.sub(r"(\()[ \t]+", r"\1", final_text)
    final_text = re.sub(r"[ \t]+(\))", r"\1", final_text)
    final_text = re.sub(r"[ \t]{2,}", " ", final_text)
    final_text = re.sub(r"``\s*(.+?)\s*''", r'"\1"', final_text)
    return final_text


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


def show_streamlit_api_page():
    st.set_page_config(page_title="AI Text Humanizer (API UI)", layout="wide")
    st.title("AI Text Humanizer — Interactive API & Local HTTP Endpoint")
    st.markdown(DESCRIPTION)

    col_main, col_side = st.columns([3, 1])
    with col_side:
        st.header("API Options & Example")
        p_syn = st.slider(
            "Synonym replacement intensity (p_syn)", 0.0, 1.0, 0.2, 0.01)
        p_trans = st.slider(
            "Transition insertion probability (p_trans)", 0.0, 1.0, 0.2, 0.01)
        preserve_linebreaks = st.checkbox("Preserve line breaks", value=True)

        st.markdown("**Example request**")
        st.json(EXAMPLE_REQ)
        if st.button("Load example into editor"):
            st.session_state["input_text"] = EXAMPLE_REQ["text"]

        st.markdown("---")
        st.markdown("**Local API status**")
        api_url = f"http://{API_HOST}:{API_PORT}"
        st.write(f"Local API: `{api_url}`")
        st.write("Available endpoints:")
        st.write("- GET /health")
        st.write("- POST /humanize (JSON body)")

    with col_main:
        default_text = st.session_state.get("input_text", EXAMPLE_REQ["text"])
        text = st.text_area("Input text to humanize",
                            value=default_text, height=220)

        c1, c2 = st.columns([3, 1])
        with c2:
            if st.button("Humanize"):
                st.session_state["do_humanize"] = True
            if st.button("API Health"):
                try:
                    import requests

                    h = requests.get(
                        f"http://{API_HOST}:{API_PORT}/health", timeout=2)
                    if h.ok:
                        st.success(h.json())
                    else:
                        st.error("Local API returned non-OK status")
                except Exception as e:
                    st.error(f"Local API not running: {e}")

        do_humanize = st.session_state.get("do_humanize", False)

        if do_humanize:
            if not text or not text.strip():
                st.error("`text` must be a non-empty string")
            else:
                with st.spinner("Humanizing..."):
                    orig_wc = count_words(text)
                    orig_sc = count_sentences(text)

                    no_refs_text, placeholders = extract_citations(text)

                    if preserve_linebreaks:
                        rewritten = preserve_linebreaks_rewrite(
                            no_refs_text, p_syn=p_syn, p_trans=p_trans)
                    else:
                        rewritten = minimal_rewriting(
                            no_refs_text, p_syn=p_syn, p_trans=p_trans)

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

                st.subheader("Humanized Text")
                st.code(final_text, language="text")

                st.subheader("Metrics")
                st.metric("Words Added", resp["words_added"])
                st.metric("Sentences Added", resp["sentences_added"])

                st.subheader("Response (JSON)")
                st.json(resp)

    st.markdown("---")
    st.markdown("## OpenAPI-like metadata & examples")
    st.markdown(
        "Although Streamlit is not an OpenAPI server, this page documents the same request/response contract and provides an interactive UI to exercise it."
    )

    with st.expander("Request schema and example"):
        st.markdown("Request fields:")
        st.markdown(
            "- text (string, required): The input text to humanize.\n"
            "- p_syn (float, optional): Synonym replacement intensity (0.0-1.0). Default 0.2.\n"
            "- p_trans (float, optional): Transition insertion probability (0.0-1.0). Default 0.2.\n"
            "- preserve_linebreaks (bool, optional): Whether to keep original line breaks. Default true."
        )
        st.json(EXAMPLE_REQ)

    with st.expander("Response schema and example"):
        st.markdown("Response fields:")
        st.markdown(
            "- humanized_text (string): The transformed human-like text result.\n"
            "- orig_word_count, orig_sentence_count (ints): Original text metrics.\n"
            "- new_word_count, new_sentence_count (ints): New text metrics.\n"
            "- words_added, sentences_added (ints): Differences between new and original."
        )
        st.json(EXAMPLE_RESP)

    st.markdown("---")
    st.markdown("### Notes")
    st.markdown(
        "- The local Flask API is intended for local programmatic access while you run the Streamlit UI.\n"
        "- The API listens on 127.0.0.1:8001 by default; change `API_PORT`/`API_HOST` in this file if needed.\n"
        "- Importing `pages/humanize_text.py` may trigger NLTK downloads or spaCy warnings at startup."
    )


def ensure_api_thread():
    # Avoid starting multiple Flask servers when Streamlit hot-reloads
    started = st.session_state.get("_api_thread_started", False)
    if not started:
        t = threading.Thread(target=run_flask_app, args=(
            API_HOST, API_PORT), daemon=True)
        t.start()
        # Give the server a moment to start in background
        time.sleep(0.3)
        st.session_state["_api_thread_started"] = True


if __name__ == "__main__":
    # When executed directly, run the Streamlit-style UI function.
    ensure_api_thread()
    show_streamlit_api_page()


class HumanizeRequest(BaseModel):
    text: str = Field(..., description="The input text to humanize. Must be non-empty.")
    p_syn: Optional[float] = Field(0.2, ge=0.0, le=1.0, description="Synonym replacement intensity (0.0-1.0)")
    p_trans: Optional[float] = Field(0.2, ge=0.0, le=1.0, description="Academic transition insertion probability (0.0-1.0)")
    preserve_linebreaks: Optional[bool] = Field(True, description="Whether to preserve original line breaks")

    class Config:
        schema_extra = {
            "example": {
                "text": "Recent studies (Smith et al., 2020) show promising results. It can't be ignored.",
                "p_syn": 0.3,
                "p_trans": 0.2,
                "preserve_linebreaks": True,
            }
        }


class HumanizeResponse(BaseModel):
    humanized_text: str = Field(..., description="The transformed human-like text result")
    orig_word_count: int
    orig_sentence_count: int
    new_word_count: int
    new_sentence_count: int
    words_added: int
    sentences_added: int

    class Config:
        schema_extra = {
            "example": {
                "humanized_text": "Moreover, Recent studies (Smith et al., 2020) show promising results. It cannot be ignored.",
                "orig_word_count": 11,
                "orig_sentence_count": 2,
                "new_word_count": 13,
                "new_sentence_count": 3,
                "words_added": 2,
                "sentences_added": 1,
            }
        }


@app.get("/health", tags=["humanize"], summary="Health check")
def health():
    """Returns OK when the service is healthy.

    Useful for simple uptime checks.
    """
    return {"status": "ok"}


@app.post(
    "/humanize",
    response_model=HumanizeResponse,
    tags=["humanize"],
    summary="Humanize input text",
    response_description="The transformed text and basic metrics",
)
def humanize(req: HumanizeRequest):
    """Transform AI-generated text into human-like prose.

    The endpoint will:
    - Preserve and protect citation strings (e.g., APA style) while rewriting
    - Optionally preserve original line breaks
    - Expand contractions, replace synonyms, and optionally add academic transitions

    Provide `p_syn` and `p_trans` to tune intensity of synonym replacement and
    transition insertion respectively (values between 0.0 and 1.0).
    """
    text = req.text or ""
    if not text.strip():
        raise HTTPException(status_code=400, detail="`text` must be a non-empty string")

    # Original stats
    orig_wc = count_words(text)
    orig_sc = count_sentences(text)

    # Protect citations
    no_refs_text, placeholders = extract_citations(text)

    # Choose rewrite mode
    if req.preserve_linebreaks:
        rewritten = preserve_linebreaks_rewrite(no_refs_text, p_syn=req.p_syn, p_trans=req.p_trans)
    else:
        rewritten = minimal_rewriting(no_refs_text, p_syn=req.p_syn, p_trans=req.p_trans)

    # Restore citations and normalize spacing similar to Streamlit page
    final_text = restore_citations(rewritten, placeholders)
    final_text = re.sub(r"[ \t]+([.,;:!?])", r"\1", final_text)
    final_text = re.sub(r"(\()[ \t]+", r"\1", final_text)
    final_text = re.sub(r"[ \t]+(\))", r"\1", final_text)
    final_text = re.sub(r"[ \t]{2,}", " ", final_text)
    final_text = re.sub(r"``\s*(.+?)\s*''", r'"\1"', final_text)

    new_wc = count_words(final_text)
    new_sc = count_sentences(final_text)

    return {
        "humanized_text": final_text,
        "orig_word_count": orig_wc,
        "orig_sentence_count": orig_sc,
        "new_word_count": new_wc,
        "new_sentence_count": new_sc,
        "words_added": new_wc - orig_wc,
        "sentences_added": new_sc - orig_sc,
    }


if __name__ == "__main__":
    # When executed directly, run the Streamlit-style UI function.
    ensure_api_thread()
    show_streamlit_api_page()
