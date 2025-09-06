# DMO-Classification Assistant
# Run this in Google Colab or local environment

# Install required packages

import streamlit as st
from google import genai
import time

# Configure page
st.set_page_config(
    page_title="DMO-Classification Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def toggle_theme():
    """Toggle between light and dark mode"""
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def get_css(theme):
    """Return CSS based on selected theme"""
    if theme == 'dark':
        return """
        <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .main-header {
                background: linear-gradient(90deg, #4A5568 0%, #2D3748 100%);
                padding: 2rem;
                border-radius: 10px;
                color: white;
                text-align: center;
                margin-bottom: 2rem;
            }
            .chat-container {
                background: #2D3748;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #4A5568;
                margin: 1rem 0;
                color: #E2E8F0;
            }
            .user-message {
                background: #2C5282;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                color: #E2E8F0;
            }
            .assistant-message {
                background: #553C9A;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                color: #E2E8F0;
            }
            .classification-result {
                background: #22543D;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 4px solid #38A169;
                margin: 1rem 0;
                color: #E2E8F0;
            }
            .error-message {
                background: #742A2A;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #E53E3E;
                margin: 1rem 0;
                color: #E2E8F0;
            }
            .guide-box {
                background: #2D3748;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                color: #E2E8F0;
            }
            .stButton button {
                background: #4A5568;
                color: white;
            }
            .stTextInput input {
                background: #2D3748;
                color: #E2E8F0;
            }
            .stTextArea textarea {
                background: #2D3748;
                color: #E2E8F0;
            }
        </style>
        """
    else:
        return """
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
            .guide-box {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
        </style>
        """

def get_messages(lang):
    """Get messages in selected language"""
    if lang == "arabic":
        return {
            "welcome": "مرحباً! اسمي DMO-Classification Assistant وأنا هنا لمساعدتك في التصنيف الصحيح! 🛡️",
            "chat_input": "اكتب رسالتك هنا...",
            "send": "إرسال",
            "clear": "مسح المحادثة",
            "english": "English",
            "arabic": "العربية",
            "no_api": "❌ لم يتم العثور على مفتاح API. يرجى التحقق من إعدادات الأسرار.",
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
            """,
            "theme_toggle": "تبديل الوضع الليلي/النهاري"
        }
    else:
        return {
            "welcome": "Hi! My name is DMO-Classification Assistant and I'm here to help you classify right! 🛡️",
            "chat_input": "Type your message here...",
            "send": "Send",
            "clear": "Clear Chat",
            "english": "English",
            "arabic": "العربية",
            "no_api": "❌ API key not found. Please check your secrets setup.",
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
            """,
            "theme_toggle": "Toggle Dark/Light Mode"
        }

def is_classification_related(text):
    """Check if the message is related to data classification"""
    classification_keywords = [
        'excel', 'file', 'document', 'database', 'sheet', 'data', 'information',
        'user', 'employee', 'customer', 'personal', 'financial', 'contract',
        'report', 'record', 'list', 'table', 'system', 'server', 'folder',
        'email', 'message', 'photo', 'video', 'backup', 'log', 'config',
        'classify', 'classification', 'secret', 'confidential', 'public', 'internal',
        'security', 'sensitive', 'private', 'restricted', 'open', 'protected',
        'ملف', 'بيانات', 'معلومات', 'مستخدم', 'موظف', 'عميل', 'شخصي', 'مالي',
        'تصنيف', 'سري', 'محدود', 'عام', 'داخلي', 'حساس', 'محمي'
    ]
    
    text_lower = text.lower()
    
    # If it contains any data-related keywords, it's probably about classification
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

def chat_with_assistant(user_input, lang):
    """Main chat function"""
    
    messages = get_messages(lang)
    
    # Check if question is about classification
    if not is_classification_related(user_input):
        return messages["out_of_scope"]
    
    try:
        # Get API key from secrets
        if 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
        else:
            return messages["no_api"]
        
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
    
    # Apply CSS based on theme
    st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ DMO-Classification Assistant</h1>
        <p>Your Smart Data Classification Helper</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        # Theme toggle
        messages = get_messages(st.session_state.language)
        if st.button(messages["theme_toggle"]):
            toggle_theme()
            time.sleep(0.1)  # Small delay to ensure theme changes
            st.rerun()
        
        # API status
        st.subheader("API Status")
        if 'GEMINI_API_KEY' in st.secrets:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ API Key Missing")
            st.info("Please set GEMINI_API_KEY in your Streamlit secrets")
        
        # Language selection
        st.subheader("Language")
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            if st.button("🇺🇸 English", use_container_width=True):
                st.session_state.language = 'english'
                st.rerun()
        with lang_col2:
            if st.button("🇸🇦 العربية", use_container_width=True):
                st.session_state.language = 'arabic'
                st.rerun()
        
        # Quick guide
        st.subheader(messages["guide_title"])
        st.markdown(f"""
        <div class="guide-box">
            {messages['guide']}
        </div>
        """, unsafe_allow_html=True)
        
        # Examples
        st.subheader("💡 Examples")
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
            if st.button(f"📄 {example}", use_container_width=True, key=f"ex_{hash(example)}"):
                st.session_state.user_input = example
    
    # Welcome message
    messages = get_messages(st.session_state.language)
    st.markdown(f"""
    <div class="chat-container">
        <h3>👋 {messages['welcome']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    col1, col2 = st.columns(2)
    with col1:
        send_btn = st.button(messages["send"], type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button(messages["clear"], use_container_width=True)
    
    # Process message
    if send_btn and user_input.strip():
        with st.spinner(messages["thinking"]):
            response = chat_with_assistant(user_input, st.session_state.language)
            
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
    
    # Footer
    st.markdown("---")
    st.info("""
    **Note**: This application uses the Gemini API for data classification. 
    Make sure you have set the `GEMINI_API_KEY` in your Streamlit secrets.
    """)

if __name__ == "__main__":
    main()
