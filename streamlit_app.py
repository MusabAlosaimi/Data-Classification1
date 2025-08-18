import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum

# Page config
st.set_page_config(
    page_title="SDAIA Data Classification Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .quick-assess-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        cursor: pointer;
        transition: transform 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .quick-assess-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .classification-result {
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .level-top-secret {
        background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%);
        color: white;
    }
    
    .level-secret {
        background: linear-gradient(135deg, #ff922b 0%, #e8590c 100%);
        color: white;
    }
    
    .level-restricted {
        background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%);
        color: #333;
    }
    
    .level-public {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-left: 4px solid;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateX(5px);
    }
    
    .metric-high { border-left-color: #ff6b6b; }
    .metric-medium { border-left-color: #ff922b; }
    .metric-low { border-left-color: #ffd43b; }
    .metric-none { border-left-color: #51cf66; }
    
    .smart-suggestion {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.9; }
        50% { opacity: 1; }
        100% { opacity: 0.9; }
    }
    
    .dataset-preview {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .control-item {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Data classes for better structure
class ImpactLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

class ClassificationLevel(Enum):
    TOP_SECRET = "top_secret"
    SECRET = "secret"
    RESTRICTED = "restricted"
    PUBLIC = "public"

@dataclass
class DatasetProfile:
    name: str
    category: str
    sensitivity_indicators: List[str]
    risk_score: float
    suggested_level: ClassificationLevel

@dataclass
class AssessmentResult:
    classification: ClassificationLevel
    confidence: float
    impact_scores: Dict[str, int]
    recommendations: List[str]
    timestamp: datetime

# Enhanced session state management
class SessionManager:
    @staticmethod
    def init():
        defaults = {
            'assessment_mode': 'smart',  # 'smart', 'quick', 'detailed'
            'current_assessment': {},
            'assessment_history': [],
            'selected_dataset': None,
            'show_results': False,
            'ai_suggestions': True,
            'batch_datasets': []
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def reset():
        st.session_state.current_assessment = {}
        st.session_state.show_results = False
        st.session_state.selected_dataset = None

# Smart classification engine
class SmartClassifier:
    """AI-powered classification suggestions"""
    
    SENSITIVITY_PATTERNS = {
        'personal_id': ['national id', 'ssn', 'passport', 'driver license', 'id number'],
        'financial': ['bank account', 'credit card', 'salary', 'payment', 'iban'],
        'health': ['medical', 'health', 'diagnosis', 'treatment', 'patient'],
        'security': ['password', 'token', 'secret', 'key', 'credential'],
        'strategic': ['strategy', 'plan', 'forecast', 'projection', 'confidential']
    }
    
    @classmethod
    def analyze_dataset(cls, dataset_info: Dict) -> DatasetProfile:
        """Analyze dataset and provide smart recommendations"""
        name = dataset_info.get('name', '')
        description = dataset_info.get('description', '')
        fields = dataset_info.get('fields', [])
        
        # Calculate sensitivity score
        sensitivity_score = 0
        indicators = []
        
        combined_text = f"{name} {description} {' '.join(fields)}".lower()
        
        for category, patterns in cls.SENSITIVITY_PATTERNS.items():
            for pattern in patterns:
                if pattern in combined_text:
                    sensitivity_score += 1
                    indicators.append(f"{category}: {pattern}")
        
        # Determine suggested classification
        if sensitivity_score >= 5:
            suggested = ClassificationLevel.TOP_SECRET
        elif sensitivity_score >= 3:
            suggested = ClassificationLevel.SECRET
        elif sensitivity_score >= 1:
            suggested = ClassificationLevel.RESTRICTED
        else:
            suggested = ClassificationLevel.PUBLIC
        
        return DatasetProfile(
            name=name,
            category=cls._determine_category(combined_text),
            sensitivity_indicators=indicators[:5],  # Top 5 indicators
            risk_score=min(sensitivity_score / 10, 1.0),
            suggested_level=suggested
        )
    
    @staticmethod
    def _determine_category(text: str) -> str:
        categories = {
            'HR & Personnel': ['employee', 'hr', 'payroll', 'staff'],
            'Financial': ['financial', 'revenue', 'budget', 'cost'],
            'Customer': ['customer', 'client', 'user', 'subscriber'],
            'Operations': ['operation', 'process', 'system', 'infrastructure'],
            'Strategic': ['strategy', 'plan', 'research', 'development']
        }
        
        for cat, keywords in categories.items():
            if any(kw in text.lower() for kw in keywords):
                return cat
        return 'General'

# Quick assessment templates
QUICK_TEMPLATES = {
    'hr_sensitive': {
        'name': 'HR Sensitive Data',
        'icon': '👥',
        'description': 'Personal employee information, performance, disciplinary records',
        'preset_impacts': {
            'national_interest': ImpactLevel.LOW,
            'entity_activities': ImpactLevel.MEDIUM,
            'individuals': ImpactLevel.HIGH,
            'environment': ImpactLevel.NONE
        }
    },
    'financial_critical': {
        'name': 'Financial Records',
        'icon': '💰',
        'description': 'Financial statements, transactions, sensitive business data',
        'preset_impacts': {
            'national_interest': ImpactLevel.MEDIUM,
            'entity_activities': ImpactLevel.HIGH,
            'individuals': ImpactLevel.MEDIUM,
            'environment': ImpactLevel.NONE
        }
    },
    'public_info': {
        'name': 'Public Information',
        'icon': '📢',
        'description': 'Marketing materials, public reports, general information',
        'preset_impacts': {
            'national_interest': ImpactLevel.NONE,
            'entity_activities': ImpactLevel.NONE,
            'individuals': ImpactLevel.NONE,
            'environment': ImpactLevel.NONE
        }
    },
    'security_critical': {
        'name': 'Security Data',
        'icon': '🔐',
        'description': 'Security logs, vulnerabilities, access credentials',
        'preset_impacts': {
            'national_interest': ImpactLevel.HIGH,
            'entity_activities': ImpactLevel.HIGH,
            'individuals': ImpactLevel.MEDIUM,
            'environment': ImpactLevel.NONE
        }
    }
}

# Visualization functions
def create_impact_radar(impact_scores: Dict[str, int]) -> go.Figure:
    """Create radar chart for impact visualization"""
    categories = list(impact_scores.keys())
    values = list(impact_scores.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker=dict(color='rgba(102, 126, 234, 0.8)'),
        line=dict(color='rgba(102, 126, 234, 1)', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

def create_classification_gauge(level: ClassificationLevel) -> go.Figure:
    """Create gauge chart for classification level"""
    level_values = {
        ClassificationLevel.PUBLIC: 1,
        ClassificationLevel.RESTRICTED: 2,
        ClassificationLevel.SECRET: 3,
        ClassificationLevel.TOP_SECRET: 4
    }
    
    colors = {
        ClassificationLevel.PUBLIC: '#51cf66',
        ClassificationLevel.RESTRICTED: '#ffd43b',
        ClassificationLevel.SECRET: '#ff922b',
        ClassificationLevel.TOP_SECRET: '#ff6b6b'
    }
    
    value = level_values[level]
    color = colors[level]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': "Classification Level"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 4], 'tickwidth': 1},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 1], 'color': '#e8f5e9'},
                {'range': [1, 2], 'color': '#fff9c4'},
                {'range': [2, 3], 'color': '#ffe0b2'},
                {'range': [3, 4], 'color': '#ffebee'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# Main application functions
def render_header():
    """Render application header"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🛡️ SDAIA Data Classification Tool</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
            Advanced AI-Powered Data Classification & Impact Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_smart_assessment():
    """Render smart assessment mode"""
    st.header("🤖 Smart Assessment Mode")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Dataset Information")
        
        # Quick input form
        with st.form("smart_assessment_form"):
            dataset_name = st.text_input("Dataset Name", placeholder="e.g., Employee Database")
            dataset_desc = st.text_area("Description", placeholder="Brief description of the data...", height=100)
            
            # Multi-select for data fields
            common_fields = ['Name', 'Email', 'Phone', 'Address', 'ID Number', 'Financial Data', 
                           'Health Records', 'Passwords', 'Personal Photos', 'Location Data']
            selected_fields = st.multiselect("Select Data Fields Present", common_fields)
            
            custom_fields = st.text_input("Additional Fields (comma-separated)")
            
            submitted = st.form_submit_button("🔍 Analyze Dataset", type="primary", use_container_width=True)
        
        if submitted and dataset_name:
            # Combine fields
            all_fields = selected_fields + [f.strip() for f in custom_fields.split(',') if f.strip()]
            
            # Analyze with smart classifier
            dataset_info = {
                'name': dataset_name,
                'description': dataset_desc,
                'fields': all_fields
            }
            
            profile = SmartClassifier.analyze_dataset(dataset_info)
            
            # Store in session
            st.session_state.selected_dataset = dataset_info
            st.session_state.dataset_profile = profile
            
            # Show analysis results
            st.success("✅ Dataset analyzed successfully!")
            
            with st.expander("📊 Analysis Results", expanded=True):
                st.markdown(f"**Category:** {profile.category}")
                st.markdown(f"**Risk Score:** {profile.risk_score:.1%}")
                
                if profile.sensitivity_indicators:
                    st.markdown("**Sensitivity Indicators Found:**")
                    for indicator in profile.sensitivity_indicators:
                        st.markdown(f"• {indicator}")
                
                # Classification suggestion
                level_names = {
                    ClassificationLevel.TOP_SECRET: "🔴 Top Secret",
                    ClassificationLevel.SECRET: "🟠 Secret",
                    ClassificationLevel.RESTRICTED: "🟡 Restricted",
                    ClassificationLevel.PUBLIC: "🟢 Public"
                }
                
                st.markdown(f"""
                <div class="smart-suggestion">
                    <h4 style="margin: 0;">💡 AI Recommendation</h4>
                    <p style="margin: 0.5rem 0;">Based on the analysis, we recommend: 
                    <strong>{level_names[profile.suggested_level]}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Accept Recommendation", use_container_width=True):
                        st.session_state.final_classification = profile.suggested_level
                        st.session_state.show_results = True
                        st.rerun()
                
                with col2:
                    if st.button("🔧 Customize Assessment", use_container_width=True):
                        st.session_state.assessment_mode = 'detailed'
                        st.rerun()
    
    with col2:
        st.markdown("### Quick Templates")
        
        for template_key, template in QUICK_TEMPLATES.items():
            if st.button(f"{template['icon']} {template['name']}", key=f"template_{template_key}", 
                        use_container_width=True, help=template['description']):
                
                # Apply template
                st.session_state.current_assessment = template['preset_impacts']
                st.session_state.selected_dataset = {
                    'name': template['name'],
                    'description': template['description']
                }
                
                # Calculate classification
                high_count = sum(1 for v in template['preset_impacts'].values() if v == ImpactLevel.HIGH)
                medium_count = sum(1 for v in template['preset_impacts'].values() if v == ImpactLevel.MEDIUM)
                
                if high_count > 0:
                    st.session_state.final_classification = ClassificationLevel.TOP_SECRET
                elif medium_count > 0:
                    st.session_state.final_classification = ClassificationLevel.SECRET
                else:
                    st.session_state.final_classification = ClassificationLevel.PUBLIC
                
                st.session_state.show_results = True
                st.rerun()

def render_results():
    """Render classification results"""
    st.header("📋 Classification Results")
    
    # Get classification
    classification = st.session_state.get('final_classification', ClassificationLevel.PUBLIC)
    
    # Classification card
    level_display = {
        ClassificationLevel.TOP_SECRET: ("Top Secret", "level-top-secret", "🔴"),
        ClassificationLevel.SECRET: ("Secret", "level-secret", "🟠"),
        ClassificationLevel.RESTRICTED: ("Restricted", "level-restricted", "🟡"),
        ClassificationLevel.PUBLIC: ("Public", "level-public", "🟢")
    }
    
    name, css_class, icon = level_display[classification]
    
    st.markdown(f"""
    <div class="classification-result {css_class}">
        <h2 style="margin: 0; font-size: 2rem;">{icon} {name}</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.1rem;">
            Your data has been classified as <strong>{name}</strong> based on the impact assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Classification Level")
        fig = create_classification_gauge(classification)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Impact Analysis")
        # Create sample impact scores
        impact_scores = {
            'National Interest': 2 if classification == ClassificationLevel.TOP_SECRET else 1,
            'Entity Activities': 2 if classification in [ClassificationLevel.SECRET, ClassificationLevel.TOP_SECRET] else 1,
            'Individuals': 3 if classification != ClassificationLevel.PUBLIC else 0,
            'Environment': 0
        }
        fig = create_impact_radar(impact_scores)
        st.plotly_chart(fig, use_container_width=True)
    
    # Required Controls
    st.subheader("🔒 Required Security Controls")
    
    controls = {
        ClassificationLevel.TOP_SECRET: [
            "Implement end-to-end encryption with quantum-resistant algorithms",
            "Deploy multi-factor authentication with biometric verification",
            "Establish 24/7 security monitoring and incident response",
            "Conduct quarterly security audits and penetration testing",
            "Implement data loss prevention (DLP) solutions",
            "Maintain detailed access logs with immutable audit trail"
        ],
        ClassificationLevel.SECRET: [
            "Apply AES-256 encryption for data at rest and in transit",
            "Implement role-based access control (RBAC)",
            "Conduct bi-annual security assessments",
            "Deploy intrusion detection systems",
            "Regular security awareness training for staff"
        ],
        ClassificationLevel.RESTRICTED: [
            "Standard encryption protocols",
            "Access control lists and user authentication",
            "Annual security reviews",
            "Regular backup procedures",
            "Basic security monitoring"
        ],
        ClassificationLevel.PUBLIC: [
            "Standard information security practices",
            "Regular maintenance and updates",
            "Basic access logging",
            "Standard backup procedures"
        ]
    }
    
    for i, control in enumerate(controls[classification], 1):
        st.markdown(f"""
        <div class="control-item">
            <strong>{i}.</strong> {control}
        </div>
        """, unsafe_allow_html=True)
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Generate report
        report_data = {
            'classification': name,
            'date': datetime.now().isoformat(),
            'dataset': st.session_state.get('selected_dataset', {}).get('name', 'Unknown'),
            'controls': controls[classification]
        }
        
        st.download_button(
            "📄 Download Report (JSON)",
            json.dumps(report_data, indent=2),
            file_name=f"classification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email functionality would be integrated here")
    
    with col3:
        if st.button("🔄 New Assessment", use_container_width=True):
            SessionManager.reset()
            st.rerun()

def main():
    # Initialize session
    SessionManager.init()
    
    # Render header
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Assessment Mode")
        
        mode_options = {
            'smart': '🤖 Smart (AI-Powered)',
            'quick': '⚡ Quick Templates',
            'detailed': '📋 Detailed Manual'
        }
        
        selected_mode = st.radio(
            "Choose assessment mode:",
            options=list(mode_options.keys()),
            format_func=lambda x: mode_options[x],
            key='assessment_mode'
        )
        
        st.divider()
        
        st.markdown("### 📊 Statistics")
        if 'assessment_history' in st.session_state:
            st.metric("Assessments Completed", len(st.session_state.assessment_history))
        
        st.divider()
        
        st.markdown("### ℹ️ About")
        st.info("""
        **Version 2.0**
        
        Enhanced SDAIA Data Classification Tool with AI-powered recommendations and smart assessment modes.
        
        Based on SDAIA National Data Governance Policies v1.0
        """)
        
        if st.button("🔄 Reset All", use_container_width=True):
            SessionManager.reset()
            st.rerun()
    
    # Main content
    if not st.session_state.show_results:
        if st.session_state.assessment_mode == 'smart':
            render_smart_assessment()
        elif st.session_state.assessment_mode == 'quick':
            st.header("⚡ Quick Assessment")
            st.info("Select a template from the sidebar to quickly classify your data.")
            
            # Show template cards
            cols = st.columns(2)
            for i, (key, template) in enumerate(QUICK_TEMPLATES.items()):
                with cols[i % 2]:
                    if st.button(
                        f"{template['icon']} {template['name']}\n{template['description']}", 
                        key=f"main_template_{key}",
                        use_container_width=True
                    ):
                        st.session_state.current_assessment = template['preset_impacts']
                        st.session_state.show_results = True
                        st.rerun()
        else:
            st.header("📋 Detailed Manual Assessment")
            st.info("Detailed manual assessment mode - Full questionnaire would be implemented here")
    else:
        render_results()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; color: #6c757d; padding: 1rem;">
            <p>🛡️ SDAIA Data Classification Tool v2.0 | © 2024 | Based on SDAIA National Data Governance Policies</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
