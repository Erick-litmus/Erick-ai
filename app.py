import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Page configuration for a premium feel
st.set_page_config(
    page_title="Erick AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (glassmorphism sidebar, sleek dark mode vibes, gradients)
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    
    /* Sidebar custom styling */
    .css-1d391kg {
        background-color: #0d1117;
    }
    
    /* Premium source citation card */
    .source-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .source-card a {
        color: #58a6ff !important;
        text-decoration: none;
        font-weight: 600;
    }
    
    .source-card a:hover {
        text-decoration: underline;
    }
    
    /* Glowing effect for search query */
    .query-tag {
        background: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        border-radius: 12px;
        padding: 3px 10px;
        font-size: 0.8rem;
        display: inline-block;
        margin-right: 5px;
        margin-top: 5px;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

# Check for API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key or api_key == "your_actual_api_key_here":
    st.error("🔑 **Gemini API Key missing!**")
    st.info("To run the assistant, please add `GEMINI_API_KEY` to your `.env` file (local development) or Streamlit Secrets (cloud deployment).")
    st.stop()

# Initialize Google Gen AI client
try:
    from google import genai
    from google.genai import types
except ImportError:
    st.error("📦 **Missing library!** The `google-genai` SDK is not installed in this environment. Please run `pip install -r requirements.txt` in your virtual environment.")
    st.stop()

# Set up GenAI Client
@st.cache_resource
def get_genai_client():
    return genai.Client()

client = get_genai_client()

# ================= SIDEBAR CONFIGURATION =================
st.sidebar.markdown("<h2 style='font-family: Outfit; font-weight:600;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)

# 1. Model Selection
model_choice = st.sidebar.selectbox(
    "Select AI Model",
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    index=0,
    help="Gemini 2.5 Flash is recommended for general chat. Pro is better for complex reasoning and coding."
)

# 2. System Instruction (AI Personality Preset)
st.sidebar.subheader("🤖 AI Personality")
preset = st.sidebar.selectbox(
    "Choose a preset",
    ["Friendly Assistant", "Professional Tech Lead", "Creative Writer", "Expert Educator", "Custom"],
    index=0
)

# Set defaults based on preset
preset_prompts = {
    "Friendly Assistant": "You are a helpful, smart, and friendly AI assistant. Answer the user's questions clearly and concisely.",
    "Professional Tech Lead": "You are an expert Senior Software Engineer and Tech Lead. Answer user technical questions with precise code blocks, best practices, and solid reasoning.",
    "Creative Writer": "You are a creative writer and editor. Use descriptive and engaging language. Write stories, brainstorm ideas, and help polish prose.",
    "Expert Educator": "You are a patient and knowledgeable educator. Explain complex concepts in simple terms with analogies and clear examples.",
    "Custom": ""
}

# If Custom, show text area; otherwise show disabled text area with preset
if preset == "Custom":
    system_instruction = st.sidebar.text_area(
        "Define custom instructions:",
        value="You are a helpful AI assistant.",
        height=100
    )
else:
    system_instruction = st.sidebar.text_area(
        "Active instructions:",
        value=preset_prompts[preset],
        height=100,
        disabled=True
    )

# 3. Google Search Grounding Toggle
st.sidebar.subheader("🌐 Grounding & Search")
enable_search = st.sidebar.toggle(
    "Enable Google Search",
    value=False,
    help="Enable real-time Google Search grounding. The AI will search the web for current information and cite its sources."
)

# 4. Action Buttons (Clear Chat & Download Chat)
st.sidebar.subheader("💾 Actions")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat function
if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Build transcript string for download
if len(st.session_state.messages) > 0:
    transcript = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        transcript += f"{role}: {msg['content']}\n\n"
        if "sources" in msg and msg["sources"]:
            transcript += "Sources Cited:\n"
            for src in msg["sources"]:
                transcript += f" - {src['title']} ({src['uri']})\n"
            transcript += "\n"
        transcript += "-"*40 + "\n\n"
        
    st.sidebar.download_button(
        label="📥 Download Chat Log",
        data=transcript,
        file_name="gemini_chat_transcript.txt",
        mime="text/plain",
        use_container_width=True
    )

# ================= MAIN CHAT AREA =================
st.markdown("<div class='main-title'>Erick AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your personal AI assistant — Powered by Google Gemini 2.5</div>", unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display search queries if present
        if "search_queries" in msg and msg["search_queries"]:
            st.markdown("🔍 **Search queries:** " + " ".join([f"<span class='query-tag'>{q}</span>" for q in msg["search_queries"]]), unsafe_allow_html=True)
            
        # Display sources if present
        if "sources" in msg and msg["sources"]:
            st.write("📖 **Sources:**")
            for src in msg["sources"]:
                st.markdown(f"<div class='source-card'>🌐 <a href='{src['uri']}' target='_blank'>{src['title']}</a></div>", unsafe_allow_html=True)

# User input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Prepare generation configuration
    tools = None
    if enable_search:
        tools = [types.Tool(google_search=types.GoogleSearch())]
        
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools
    )
    
    # Build history list of Content objects
    contents = []
    for msg in st.session_state.messages:
        gemini_role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
        
    # Generate content stream
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        search_queries = []
        sources = []
        
        try:
            # Stream response
            response_stream = client.models.generate_content_stream(
                model=model_choice,
                contents=contents,
                config=config
            )
            
            for chunk in response_stream:
                # Capture text response
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                
                # Capture search grounding metadata
                if chunk.candidates:
                    for candidate in chunk.candidates:
                        metadata = candidate.grounding_metadata
                        if metadata:
                            if metadata.web_search_queries:
                                for query in metadata.web_search_queries:
                                    if query not in search_queries:
                                        search_queries.append(query)
                            if metadata.grounding_chunks:
                                for gc in metadata.grounding_chunks:
                                    if gc.web:
                                        title = gc.web.title
                                        uri = gc.web.uri
                                        if not any(src['uri'] == uri for src in sources):
                                            sources.append({"title": title, "uri": uri})
                                            
            # Display final text response
            message_placeholder.markdown(full_response)
            
            # Display search queries
            if search_queries:
                st.markdown("🔍 **Search queries:** " + " ".join([f"<span class='query-tag'>{q}</span>" for q in search_queries]), unsafe_allow_html=True)
                
            # Display sources
            if sources:
                st.write("📖 **Sources:**")
                for src in sources:
                    st.markdown(f"<div class='source-card'>🌐 <a href='{src['uri']}' target='_blank'>{src['title']}</a></div>", unsafe_allow_html=True)
                    
            # Save assistant response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "search_queries": search_queries,
                "sources": sources
            })
            
        except Exception as e:
            st.error(f"❌ Error during response generation: {e}")
