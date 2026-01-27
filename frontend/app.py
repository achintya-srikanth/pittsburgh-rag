import streamlit as st
import requests

st.set_page_config(page_title="Pittsburgh AI Assistant", page_icon="🏙️")

st.title("🏙️ Pittsburgh Knowledge Assistant")
st.markdown("Ask anything about the Steel City! My knowledge comes from the URLs you ingest.")

# Sidebar for Ingestion
with st.sidebar:
    st.header("Admin: Add Knowledge")
    url_to_ingest = st.text_input("Enter URL (Wikipedia, News, etc.)", placeholder="https://...")
    if st.button("Ingest Website"):
        if url_to_ingest:
            with st.spinner("Scraping and Vectorizing..."):
                try:
                    # Talk to the Backend API
                    response = requests.post("http://backend:8000/ingest", json={"url": url_to_ingest})
                    if response.status_code == 200:
                        st.success("Successfully ingested!")
                    else:
                        st.error(f"Failed: {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please enter a URL first.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Talk to the Backend API for the answer
                response = requests.post("http://backend:8000/ask", json={"question": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer")
                    sources = data.get("sources", [])
                    
                    full_response = f"{answer}\n\n**Sources:** {', '.join(sources)}"
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("Backend returned an error.")
            except Exception as e:
                st.error(f"Could not reach backend: {e}")