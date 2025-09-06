# DMO-Classification Assistant
# Run this in Google Colab or local environment

# Install required packages

import streamlit as st
from google import genai

# Configure page
st.set_page_config(
    page_title="DMO-Classification Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .classification-result {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .error-message {
        background: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 1rem 0;
    }
    .lang-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def get_messages(lang):
    """Get messages in selected language"""
    if lang == "arabic":
        return {
            "welcome": "مرحباً! اسمي DMO-Classification Assistant وأنا هنا لمساعدتك في التصنيف الصحيح! 🛡️",
            "api_key": "🔑 أدخل مفتاح Gemini API الخاص بك",
            "chat_input": "اكتب رسالتك هنا...",
            "send": "إرسال",
            "clear": "مسح المحادثة",
            "english": "English",
            "arabic": "العربية",
            "no_api": "❌ يرجى إدخال مفتاح API أولاً",
            "thinking": "🤔 جاري التفكير...",
            "guide_title": "📋 دليل التصنيف السريع",
            "out_of_scope": "آسف، أنا DMO-Classification Assistant متخصص في تصنيف البيانات فقط. يرجى سؤالي عن تصنيف البيانات.",
            "ask_classification": "ما رأيك في تصنيف هذه البيانات؟",
            "wrong_classification": "❌ للأسف، تصنيفك خاطئ هذه المرة!",
            "guide": """
            **🔴 سري للغاية**: أمن قومي، عسكري، مفاتيح التشفير
            **🟠 سري**: اقتصادي، دبلوماسي، منشآت حيوية
            **🟡 محدود**: بيانات شخصية، أسرار تجارية
            **🔵 داخلي**: سياسات الشركة، مذكرات داخلية
            **🟢 عام**: إعلانات، مواد تسويقية
            """
        }
    else:
        return {
            "welcome": "Hi! My name is DMO-Classification Assistant and I'm here to help you classify right! 🛡️",
            "api_key": "🔑 Enter your Gemini API Key",
            "chat_input": "Type your message here...",
            "send": "Send",
            "clear": "Clear Chat",
            "english": "English",
            "arabic": "العربية",
            "no_api": "❌ Please enter your API key first",
            "thinking": "🤔 Thinking...",
            "guide_title": "📋 Quick Classification Guide",
            "out_of_scope": "Sorry, I'm DMO-Classification Assistant specialized in data classification only. Please ask me about data classification.",
            "ask_classification": "What do you think the classification should be?",
            "wrong_classification": "❌ You got it wrong this time!",
            "guide": """
            **🔴 TOP SECRET**: National security, military, encryption keys
            **🟠 SECRET**: Economic, diplomatic, vital installations
            **🟡 CONFIDENTIAL**: Personal data, business secrets
            **🔵 INTERNAL**: Company policies, internal memos
            **🟢 PUBLIC**: Press releases, marketing materials
            """
        }

def is_classification_related(text):
    """Check if the message is related to data classification"""
    classification_keywords = [
        'classify', 'classification', 'data', 'secret', 'confidential', 'public', 'internal',
        'تصنيف', 'بيانات', 'سري', 'محدود', 'عام', 'داخلي'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in classification_keywords)

def create_classification_prompt(user_data, user_guess, lang):
    """Create classification prompt with user guess validation"""
    
    levels = """
TOP SECRET: National security, military operations, encryption keys, terrorism intelligence
SECRET: Economic storage, diplomatic agreements, vital installations  
CONFIDENTIAL: Personal data, business secrets, financial records
INTERNAL: Company policies, internal documents, employee directories
PUBLIC: Press releases, marketing materials, public announcements
"""
    
    if lang == "arabic":
        if user_guess:
            return f"""
أنت DMO-Classification Assistant. المستخدم يعتقد أن البيانات "{user_data}" يجب تصنيفها كـ "{user_guess}".

المستويات: {levels}

إذا كان تصنيف المستخدم صحيحاً:
- أكد له: "✅ ممتاز! تصنيفك صحيح"
- السبب: [سبب مختصر]

إذا كان تصنيف المستخدم خاطئاً:
- قل: "❌ للأسف، تصنيفك خاطئ هذه المرة!"
- التصنيف الصحيح: [المستوى الصحيح]
- السبب: [لماذا هو خاطئ]
- المخاطر: [مخاطر التصنيف الخاطئ]
"""
        else:
            return f"""
أنت DMO-Classification Assistant. صنف البيانات: "{user_data}"

المستويات: {levels}

أعط:
- التصنيف: [المستوى]
- السبب: [سبب مختصر]
- ثم اسأل: "ما رأيك في تصنيف هذه البيانات؟"
"""
    else:
        if user_guess:
            return f"""
You are DMO-Classification Assistant. User thinks data "{user_data}" should be classified as "{user_guess}".

Levels: {levels}

If user is correct:
- Confirm: "✅ Excellent! Your classification is correct"
- Reason: [brief reason]

If user is wrong:
- Say: "❌ You got it wrong this time!"
- Correct classification: [correct level]
- Reason: [why it's wrong]
- Risk: [risks of wrong classification]
"""
        else:
            return f"""
You are DMO-Classification Assistant. Classify data: "{user_data}"

Levels: {levels}

Give:
- CLASSIFICATION: [level]
- REASON: [brief reason]
- Then ask: "What do you think the classification should be?"
"""

def chat_with_assistant(api_key, user_input, lang):
    """Main chat function"""
    
    messages = get_messages(lang)
    
    # Check if question is about classification
    if not is_classification_related(user_input):
        return messages["out_of_scope"]
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Check if user is providing their classification guess
        user_guess = None
        guess_keywords = ['i think', 'should be', 'أعتقد', 'يجب أن يكون']
        
        for keyword in guess_keywords:
            if keyword in user_input.lower():
                # Extract the classification level from user input
                levels = ['top secret', 'secret', 'confidential', 'internal', 'public',
                         'سري للغاية', 'سري', 'محدود', 'داخلي', 'عام']
                for level in levels:
                    if level in user_input.lower():
                        user_guess = level
                        break
        
        # Create appropriate prompt
        if user_guess:
            # Get the original data from chat history
            original_data = ""
            for chat in reversed(st.session_state.chat_history):
                if "What do you think" in chat.get('assistant', '') or "ما رأيك" in chat.get('assistant', ''):
                    original_data = chat.get('user', '')
                    break
            
            if original_data:
                prompt = create_classification_prompt(original_data, user_guess, lang)
            else:
                prompt = create_classification_prompt(user_input, user_guess, lang)
        else:
            prompt = create_classification_prompt(user_input, None, lang)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ DMO-Classification Assistant</h1>
        <p>Your Smart Data Classification Helper</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🇺🇸 English", key="en_btn"):
            st.session_state.language = 'english'
            st.rerun()
    with col2:
        if st.button("🇸🇦 العربية", key="ar_btn"):
            st.session_state.language = 'arabic'
            st.rerun()
    
    messages = get_messages(st.session_state.language)
    
    # Welcome message
    st.markdown(f"""
    <div class="chat-container">
        <h3>👋 {messages['welcome']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # API Key
        api_key = st.text_input(
            messages["api_key"],
            type="password",
            key="api_key"
        )
        
        # Chat interface
        st.markdown("### 💬 Chat")
        
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {chat['user']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="assistant-message">
                <strong>DMO-Assistant:</strong> {chat['assistant']}
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_area(
            messages["chat_input"],
            height=100,
            key="user_input"
        )
        
        # Buttons
        send_col, clear_col = st.columns([1, 1])
        with send_col:
            send_btn = st.button(messages["send"], type="primary")
        with clear_col:
            clear_btn = st.button(messages["clear"])
        
        # Process message
        if send_btn and user_input.strip():
            if not api_key:
                st.markdown(f"""
                <div class="error-message">
                    {messages['no_api']}
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner(messages["thinking"]):
                    response = chat_with_assistant(api_key, user_input, st.session_state.language)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_input,
                        "assistant": response
                    })
                    st.rerun()
        
        # Clear chat
        if clear_btn:
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        # Quick guide
        st.markdown(f"### {messages['guide_title']}")
        st.markdown(messages['guide'])
        
        # Examples
        st.markdown("### 💡 Examples")
        if st.session_state.language == 'arabic':
            examples = [
                "ملف إكسل بيانات الموظفين",
                "قاعدة بيانات العملاء",
                "وثائق عقود حكومية",
                "مواد تسويقية للشركة"
            ]
        else:
            examples = [
                "Excel file with employee data",
                "Customer database",
                "Government contract documents", 
                "Company marketing materials"
            ]
        
        for example in examples:
            if st.button(f"📄 {example}", key=f"ex_{example}"):
                st.session_state.user_input = example

    # Footer
  
if __name__ == "__main__":
    main()

# SECRETS SETUP INSTRUCTIONS:
# 
# Method 1: Local Development
# Create file: .streamlit/secrets.toml
# Add: GEMINI_API_KEY = "your_api_key_here"
#
# Method 2: Streamlit Cloud
# 1. Go to app dashboard
# 2. Settings → Secrets
# 3. Add: GEMINI_API_KEY = "your_api_key_here"

if __name__ == "__main__":
    main()

# To run in Colab:
# !streamlit run app.py --server.port 8501 --server.address 0.0.0.0
