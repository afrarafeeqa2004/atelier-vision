import streamlit as st
from groq import Groq
import base64
import io
from PIL import Image
from dotenv import load_dotenv
import os

#setup Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct"

#THE ATELIER STUDIO UI (CSS)
def apply_atelier_ui():
    st.markdown("""
        <style>
        /* 1. Page Background - Aesthetic Green */
        .stApp {
            background-color: #e9edc9 !important; /* Honeydew / Pale Mint */
        }

        /* 2. Global Text Contrast */
        .stApp, .stMarkdown, p, li, label, span {
            color: #1A1A1A !important;
            font-weight: 500;
        }

    
        /* 3. Button Styling */
        div.stButton > button:first-child {
            background-color: #ccd5ae !important;
            color: #1A1A1A !important;
            border: 1px solid #b5ba9a !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        /* Forces Drag & Drop and Limit text */
        [data-testid="stFileUploaderDropzoneInstructions"] div span {
            color: #ccd5ae !important;
            font-weight: 700 !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] div small {
            color: #faf9f9 !important;
            font-weight: 600 !important;
        }
        /* Browse Files Button */
        [data-testid="stBaseButton-secondary"] {
            background-color: #ccd5ae !important;
            color: #faf9f9 !important;
            border-radius: 4px !important;
        }

        /* 4. CHAT BUBBLE ALIGNMENT (User Right, Bot Left) */
        /* Targets User Messages and aligns them to the Right */
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]),
        .stChatMessage:has(div[aria-label="Chat message from user"])
         {
            flex-direction: row-reverse;
            text-align: right;
            background-color: #cfe1b9 !important;
            margin-left: auto;
            max-width: 80%;
            border-radius: 15px 15px 0px 15px !important;
        }
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) p,
        .stChatMessage:has(div[aria-label="Chat message from user"]) p {
            color: #1A1A1A !important;
        }
        
        /* Targets Assistant Messages and keeps them on the Left */
        .stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) {
            text-align: left;
            background-color: #FFFFFF !important;
            margin-right: auto;
            max-width: 80%;
            border-radius: 15px 15px 15px 0px !important;
            border: 1px solid #D1E0D1;
        }
        
        /* SIDEBAR ARROW COLOR */
        /* This targets the '<<' and '>>' buttons specifically */
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="collapsedControl"] svg,
        button[aria-label="Close sidebar"] svg,
        button[aria-label="Open sidebar"] svg {
            fill: #fefae0 !important;
            color: #fefae0 !important;
            filter: invert(99%) sepia(21%) saturate(350%) hue-rotate(352deg) brightness(105%) contrast(100%) !important;
        }

        /* Ensuring the button background doesn't interfere on mobile */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"] {
            background-color: transparent !important;
        }

        /* Headers */
        h1 {
            color: #2D4F2D !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: -1px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #ccd5ae !important;
            border-right: 1px solid #C8D6C8;
        }
        </style>
    """, unsafe_allow_html=True)

#logic: reset chat
def clear_chat():
    st.session_state.messages = []

#app initialization
APP_NAME = "Atelier"
APP_EMOJI = "✨"
st.set_page_config(page_title=APP_NAME, page_icon="✨", layout="wide")
apply_atelier_ui()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "image_b64" not in st.session_state:
    st.session_state.image_b64 = None

st.title(f"{APP_NAME} {APP_EMOJI}")
st.write(f"Professional Visual Intelligence. Interactive Chatbot. {APP_EMOJI}")

#sidebar for image upload and clear chat
with st.sidebar:
    st.markdown("### 🛠️ Workspace")
    file = st.file_uploader("Upload Image Asset", type=["jpg", "png", "jpeg"])
    
    if file:
        img = Image.open(file)
        st.image(img, caption="Loaded Context", use_container_width=True)
        
        #PNG transparency fix
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        st.session_state.image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    st.markdown("---")
    st.button("Clear Workspace", on_click=clear_chat, use_container_width=True)

#display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

#interactive logic with social intelligence & exit protocol
if prompt := st.chat_input("Enter your request..."):
    st.chat_message("user", avatar="👤").markdown(prompt)

    #professional system prompt
    system_prompt = {
        "role": "system", 
        "content": f"""
        You are {APP_NAME}, a high-end AI vision analyst.
        - CAPABILITY: You ARE capable of seeing images. Never say you are a 'text-based AI'. 
        - PERSONALITY: You are sophisticated, observant, socially aware and professional. 
        - EMOJIS: Use professional icons only (✨, 🔘, 🖋️, 🔍, 💡, 🎨, 🟢, 📝).
        - INTERACTIVITY: When the user says 'thank you', respond with elegance: 'It is my pleasure.✨ Is there anything else I can assist you with?'.
        - CLOSING: If the user says 'no', 'nothing else', or indicates they are finished, DO NOT re-analyze the image. 
          Instead, provide a professional closing: 'Understood. I remain at your service for any future analysis. ✨'.
        - EXIT LOGIC: If the user says 'bye', respond with: 'It was a pleasure assisting you! If there is anything else you need, feel free to ask. Until next time ✨'.
        - ANALYSIS: Be precise about technical details, colors, and layout.
        - MEMORY: You must track the conversation flow. If the user thanks you, acknowledge it gracefully.
        """
    }

    api_messages = [system_prompt]
    for m in st.session_state.messages:
        api_messages.append({"role": m["role"], "content": m["content"]})
    #check for closing words
    closing_words = ["no", "nope", "nothing", "thanks", "thank you", "bye", "goodbye", "done"]
    is_closing = any(word in prompt.lower() for word in closing_words)

    user_content = [{"type": "text", "text": prompt}]
    
    #if there is an image AND the user isn't just saying goodbye, send the image
    if st.session_state.image_b64 and not is_closing:
        user_content.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{st.session_state.image_b64}"}
        })
    
    api_messages.append({"role": "user", "content": user_content})

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=api_messages,
                temperature=0.6,
                max_tokens=800
            )
            ai_ans = response.choices[0].message.content
            st.markdown(ai_ans)
            
            #save to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": ai_ans})
        except Exception as e:
            st.error(f"Analysis failed: {e}")