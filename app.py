import streamlit as st

from src.data_loader import load_medicines
from src.search import create_documents
from src.rag import (
    split_documents,
    create_vector_store,
    search_medicines
)
from src.llm import (
    embeddings,
    generate_answer
)
from src.prompts import create_prompt
from src.safety import add_safety_message


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Generic Medicine AI",
    page_icon="💊",
    layout="centered"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("💊 Generic Medicine AI")

st.write(
    "Ask questions about medicines available "
    "in the knowledge base."
)

st.info(
    "This application provides general educational "
    "information only. It does not diagnose conditions "
    "or prescribe medicines."
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Clear Chat
# --------------------------------------------------

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# --------------------------------------------------
# Load and Build Vector Store
# --------------------------------------------------

@st.cache_resource
def build_vector_store():

    df = load_medicines()

    documents = create_documents(df)

    chunks = split_documents(
        documents
    )

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return vector_store


vector_store = build_vector_store()


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# --------------------------------------------------
# User Input
# --------------------------------------------------

query = st.chat_input(
    "Ask a question about a medicine..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if query:

    # Display user question
    with st.chat_message("user"):

        st.write(query)


    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    # --------------------------------------------------
    # Dosage Safety Check
    # --------------------------------------------------

    dosage_words = [
        "dosage",
        "dose",
        "how much",
        "how many mg",
        "how many ml",
        "take how much",
        "how often"
    ]

    query_lower = query.lower()

    is_dosage_question = any(
        word in query_lower
        for word in dosage_words
    )


    # --------------------------------------------------
    # If User Asks About Dosage
    # --------------------------------------------------

    if is_dosage_question:

        final_answer = (
            "Dosage information is not provided "
            "by this application. Please refer to "
            "the medicine's official label or ask "
            "a qualified healthcare professional."
        )

        results = []


    # --------------------------------------------------
    # Normal Medicine Question
    # --------------------------------------------------

    else:

        # --------------------------------------------------
        # Exact Medicine Match
        # --------------------------------------------------

        exact_results = []

        for document in (
            vector_store.docstore._dict.values()
        ):

            medicine_name = (
                document.metadata
                .get("medicine_name", "")
                .lower()
            )

            if (
                medicine_name
                and medicine_name in query_lower
            ):

                exact_results.append(
                    document
                )


        # --------------------------------------------------
        # Semantic Search
        # --------------------------------------------------

        if exact_results:

            results = exact_results

        else:

            results = search_medicines(
                vector_store,
                query,
                k=3
            )


        # --------------------------------------------------
        # Create Context
        # --------------------------------------------------

        context = "\n\n".join(
            result.page_content
            for result in results
        )


        # --------------------------------------------------
        # Create RAG Prompt
        # --------------------------------------------------

        prompt = create_prompt(
            context,
            query
        )


        # --------------------------------------------------
        # Generate Answer
        # --------------------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            answer = generate_answer(
                prompt
            )


        # --------------------------------------------------
        # Add Safety Message
        # --------------------------------------------------

        final_answer = add_safety_message(
            answer
        )


    # --------------------------------------------------
    # Display Assistant Answer
    # --------------------------------------------------

    with st.chat_message("assistant"):

        st.write(
            final_answer
        )


    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer
        }
    )


    # --------------------------------------------------
    # Retrieved Information
    # --------------------------------------------------

    if results:

        with st.expander(
            "View Retrieved Information"
        ):

            for i, result in enumerate(
                results,
                start=1
            ):

                st.markdown(
                    f"### Result {i}"
                )

                st.write(
                    result.page_content
                )