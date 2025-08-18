import streamlit as st
import pandas as pd
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="SDAIA Data Classification Tool",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .classification-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid;
        margin: 1rem 0;
    }
    .top-secret {
        background-color: #fee2e2;
        border-color: #ef4444;
        color: #991b1b;
    }
    .secret {
        background-color: #fed7aa;
        border-color: #f97316;
        color: #9a3412;
    }
    .restricted {
        background-color: #fef3c7;
        border-color: #eab308;
        color: #92400e;
    }
    .public {
        background-color: #dcfce7;
        border-color: #22c55e;
        color: #166534;
    }
    .impact-high { background-color: #fee2e2; color: #991b1b; }
    .impact-medium { background-color: #fed7aa; color: #9a3412; }
    .impact-low { background-color: #fef3c7; color: #92400e; }
    .impact-none { background-color: #dcfce7; color: #166534; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'impact_assessment' not in st.session_state:
    st.session_state.impact_assessment = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'selected_dataset' not in st.session_state:
    st.session_state.selected_dataset = None

# Example datasets
EXAMPLE_DATASETS = {
    'hr_employee': {
        'name': 'HR Employee Content Dataset',
        'description': 'Employee personal information, performance records, disciplinary actions',
        'examples': ['Employee ID', 'Full Name', 'National ID', 'Home Address', 'Phone Number', 'Performance Reviews', 'Disciplinary Records', 'Training Records'],
        'risk_factors': ['Personal identifiable information', 'Privacy concerns', 'Potential reputation damage']
    },
    'hr_payroll': {
        'name': 'HR Payroll Dataset',
        'description': 'Employee salary information, bank details, tax information',
        'examples': ['Employee ID', 'Salary Amount', 'Bank Account Number', 'Tax Information', 'Benefits Details', 'Bonuses', 'Deductions'],
        'risk_factors': ['Financial information', 'Privacy violations', 'Competitive intelligence']
    },
    'customer_data': {
        'name': 'Customer Database',
        'description': 'Customer contact information, purchase history, preferences',
        'examples': ['Customer ID', 'Contact Details', 'Purchase History', 'Preferences', 'Support Tickets', 'Feedback'],
        'risk_factors': ['Customer privacy', 'Business competitive advantage', 'GDPR compliance']
    },
    'financial_reports': {
        'name': 'Financial Reports',
        'description': 'Company financial statements, budget information, revenue data',
        'examples': ['Revenue Data', 'Profit/Loss Statements', 'Budget Allocations', 'Cost Centers', 'Investment Information'],
        'risk_factors': ['Market sensitive information', 'Competitive advantage', 'Investor relations']
    },
    'security_logs': {
        'name': 'Security System Logs',
        'description': 'Access logs, security incidents, system vulnerabilities',
        'examples': ['Access Logs', 'Login Records', 'Security Incidents', 'Vulnerability Reports', 'System Configurations'],
        'risk_factors': ['National security', 'Infrastructure protection', 'Operational security']
    },
    'research_data': {
        'name': 'Research & Development Data',
        'description': 'Product development, research findings, innovation plans',
        'examples': ['Research Results', 'Product Specifications', 'Innovation Plans', 'Patent Applications', 'Test Results'],
        'risk_factors': ['Competitive advantage', 'Intellectual property', 'Strategic planning']
    }
}

# Impact categories and questions
IMPACT_CATEGORIES = {
    'national_interest': {
        'name': 'National Interest',
        'icon': '🌍',
        'subcategories': {
            'reputation': {
                'name': "Kingdom's Reputation",
                'questions': [
                    'Would this information be subject to national or international media interest?',
                    'Would disclosure give a negative impression of the Kingdom?',
                    'Could this affect diplomatic relationships with other countries?'
                ]
            },
            'diplomatic': {
                'name': 'Diplomatic Relationships',
                'questions': [
                    'Would this information pose risk to relationships with friendly countries?',
                    'Could it raise international tension?',
                    'Could it lead to protests or sanctions from other countries?'
                ]
            },
            'security': {
                'name': 'National Security/Public Order',
                'questions': [
                    'Would this information help with terrorist or serious crimes if released?',
                    'Would it create public alarm?',
                    'Could it compromise security or military operations?'
                ]
            },
            'economy': {
                'name': 'National Economy',
                'questions': [
                    'Would disclosure cause economic losses at national level?',
                    'Could it affect GDP, employment, or market rates?',
                    'Would it impact multiple economic sectors?'
                ]
            },
            'infrastructure': {
                'name': 'National Infrastructure',
                'questions': [
                    'Could this cause interruption to critical national infrastructure?',
                    'Would it affect energy, transport, or health systems?',
                    'Could it compromise cyber security of critical services?'
                ]
            },
            'government': {
                'name': 'Government Functions',
                'questions': [
                    'Would this limit government entities ability to operate?',
                    'Could it affect delivery of government services?',
                    'Would it impact government decision-making processes?'
                ]
            }
        }
    },
    'entity_activities': {
        'name': 'Entity Activities',
        'icon': '🏢',
        'subcategories': {
            'private_profits': {
                'name': 'Profits of Private Entities',
                'questions': [
                    'Would disclosure lead to financial loss or bankruptcy?',
                    'Could it enable fraud or illegal transfers of funds?',
                    'Would it affect private entities operating public facilities?'
                ]
            },
            'private_functions': {
                'name': 'Functions of Private Entities',
                'questions': [
                    'Would this cause damage to private entities operating public facilities?',
                    'Could it lead to termination of significant employees?',
                    'Would it affect competitiveness of private entities?'
                ]
            }
        }
    },
    'individuals': {
        'name': 'Individuals',
        'icon': '👥',
        'subcategories': {
            'health_safety': {
                'name': 'Health/Safety of Individuals',
                'questions': [
                    'Would this lead to disclosure of names or locations of individuals?',
                    'Could it expose undercover agents or people under protection?',
                    'Would it cause physical harm or risk to individuals?'
                ]
            },
            'privacy': {
                'name': 'Privacy',
                'questions': [
                    'Would this violate privacy of individuals?',
                    'Would it infringe intellectual property rights?',
                    'Could it expose personal identifiable information?'
                ]
            }
        }
    },
    'environment': {
        'name': 'Environment',
        'icon': '🌿',
        'subcategories': {
            'resources': {
                'name': 'Environmental Resources',
                'questions': [
                    'Could this information be used to develop services/products that destroy environmental resources?',
                    'Would it cause long-term environmental damage?',
                    'Could it affect natural resources of the country?'
                ]
            }
        }
    }
}

CLASSIFICATION_LEVELS = {
    'top_secret': {
        'name': 'Top Secret',
        'css_class': 'top-secret',
        'impact': 'High',
        'description': 'Exceptionally serious and irreparable effect on national interests, security, or safety',
        'controls': [
            'Apply protective marking to all documents',
            'Restrict access to authorized personnel only',
            'Use only in specified secure locations',
            'Encrypt data using approved mechanisms',
            'No unattended storage permitted',
            'Secure disposal using electronic media disposal methods',
            'Maintain detailed access logs'
        ]
    },
    'secret': {
        'name': 'Secret',
        'css_class': 'secret',
        'impact': 'Medium',
        'description': 'Serious effect on national interests, security, or safety',
        'controls': [
            'Apply appropriate protective marking',
            'Implement access controls based on Need to Know',
            'Encrypt when stored or transmitted',
            'Restrict to authorized locations',
            'Regular access reviews required',
            'Secure disposal procedures',
            'Monitor and log access'
        ]
    },
    'restricted': {
        'name': 'Restricted',
        'css_class': 'restricted',
        'impact': 'Low',
        'description': 'Limited negative effect on entities, individuals, or environment',
        'controls': [
            'Apply protective marking as required',
            'Implement least privilege access',
            'Consider encryption for sensitive data',
            'Regular backup procedures',
            'Controlled sharing mechanisms',
            'Standard disposal procedures',
            'Access monitoring recommended'
        ]
    },
    'public': {
        'name': 'Public',
        'css_class': 'public',
        'impact': 'None',
        'description': 'No impact on national interests, activities, individuals, or environment',
        'controls': [
            'Standard information handling procedures',
            'Regular backup and maintenance',
            'Open sharing permitted after approval',
            'Standard retention policies apply',
            'Basic access logging',
            'Normal disposal procedures'
        ]
    }
}

def calculate_classification(assessment: Dict[str, Any]) -> str:
    """Calculate classification based on impact assessment responses."""
    all_responses = []
    for category in assessment.values():
        for subcategory in category.values():
            for response in subcategory.values():
                all_responses.append(response)
    
    high_count = all_responses.count('high')
    medium_count = all_responses.count('medium')
    low_count = all_responses.count('low')
    
    if high_count > 0:
        return 'top_secret'
    elif medium_count > 0:
        return 'secret'
    elif low_count > 0:
        return 'restricted'
    else:
        return 'public'

def get_impact_summary(assessment: Dict[str, Any]) -> Dict[str, int]:
    """Get summary of impact responses."""
    all_responses = []
    for category in assessment.values():
        for subcategory in category.values():
            for response in subcategory.values():
                all_responses.append(response)
    
    return {
        'high': all_responses.count('high'),
        'medium': all_responses.count('medium'),
        'low': all_responses.count('low'),
        'none': all_responses.count('none'),
        'total': len(all_responses)
    }

def has_complete_assessment(assessment: Dict[str, Any]) -> bool:
    """Check if assessment has at least some responses."""
    return bool(assessment and any(
        any(subcategory.values()) 
        for category in assessment.values() 
        for subcategory in category.values()
    ))

# Main App
def main():
    # Header
    st.title("🛡️ SDAIA Data Classification Tool")
    st.markdown("**Assess impact and classify your data according to Saudi Data & AI Authority guidelines**")
    
    if not st.session_state.show_results:
        # Dataset Selection Section
        st.header("📊 Select Dataset Example (Optional)")
        st.markdown("Choose an example dataset to help guide your impact assessment:")
        
        # Create columns for dataset cards
        cols = st.columns(3)
        for i, (key, dataset) in enumerate(EXAMPLE_DATASETS.items()):
            with cols[i % 3]:
                if st.button(
                    f"**{dataset['name']}**\n\n{dataset['description']}\n\n*Examples:* {', '.join(dataset['examples'][:3])}{'...' if len(dataset['examples']) > 3 else ''}",
                    key=f"dataset_{key}",
                    help=f"Risk Factors: {', '.join(dataset['risk_factors'])}"
                ):
                    st.session_state.selected_dataset = key
        
        if st.session_state.selected_dataset:
            dataset = EXAMPLE_DATASETS[st.session_state.selected_dataset]
            st.success(f"**Selected:** {dataset['name']}")
            st.info(f"**Key Risk Factors:** {', '.join(dataset['risk_factors'])}")
        
        # Impact Assessment Section
        st.header("🔍 Impact Assessment")
        st.markdown("Assess the potential impact of unauthorized access or disclosure in each category. Consider what would happen if this data was compromised or made public.")
        
        # Process each category
        for category_key, category in IMPACT_CATEGORIES.items():
            with st.expander(f"{category['icon']} {category['name']}", expanded=True):
                
                for subcat_key, subcategory in category['subcategories'].items():
                    st.subheader(subcategory['name'])
                    
                    for q_index, question in enumerate(subcategory['questions']):
                        st.markdown(f"**{question}**")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        response_key = f"{category_key}_{subcat_key}_{q_index}"
                        
                        with col1:
                            if st.button("🔴 High", key=f"{response_key}_high"):
                                if category_key not in st.session_state.impact_assessment:
                                    st.session_state.impact_assessment[category_key] = {}
                                if subcat_key not in st.session_state.impact_assessment[category_key]:
                                    st.session_state.impact_assessment[category_key][subcat_key] = {}
                                st.session_state.impact_assessment[category_key][subcat_key][q_index] = 'high'
                        
                        with col2:
                            if st.button("🟠 Medium", key=f"{response_key}_medium"):
                                if category_key not in st.session_state.impact_assessment:
                                    st.session_state.impact_assessment[category_key] = {}
                                if subcat_key not in st.session_state.impact_assessment[category_key]:
                                    st.session_state.impact_assessment[category_key][subcat_key] = {}
                                st.session_state.impact_assessment[category_key][subcat_key][q_index] = 'medium'
                        
                        with col3:
                            if st.button("🟡 Low", key=f"{response_key}_low"):
                                if category_key not in st.session_state.impact_assessment:
                                    st.session_state.impact_assessment[category_key] = {}
                                if subcat_key not in st.session_state.impact_assessment[category_key]:
                                    st.session_state.impact_assessment[category_key][subcat_key] = {}
                                st.session_state.impact_assessment[category_key][subcat_key][q_index] = 'low'
                        
                        with col4:
                            if st.button("🟢 None", key=f"{response_key}_none"):
                                if category_key not in st.session_state.impact_assessment:
                                    st.session_state.impact_assessment[category_key] = {}
                                if subcat_key not in st.session_state.impact_assessment[category_key]:
                                    st.session_state.impact_assessment[category_key][subcat_key] = {}
                                st.session_state.impact_assessment[category_key][subcat_key][q_index] = 'none'
                        
                        # Show current selection
                        if (category_key in st.session_state.impact_assessment and 
                            subcat_key in st.session_state.impact_assessment[category_key] and
                            q_index in st.session_state.impact_assessment[category_key][subcat_key]):
                            
                            current = st.session_state.impact_assessment[category_key][subcat_key][q_index]
                            color_class = f"impact-{current}"
                            st.markdown(f'<div class="{color_class}" style="padding: 0.25rem; border-radius: 0.25rem; text-align: center; margin: 0.5rem 0;">Selected: {current.title()}</div>', unsafe_allow_html=True)
                        
                        st.markdown("---")
        
        # Get Classification Button
        st.markdown("### Ready for Classification?")
        if st.button("🎯 Get Classification Result", type="primary", use_container_width=True):
            if has_complete_assessment(st.session_state.impact_assessment):
                st.session_state.show_results = True
                st.rerun()
            else:
                st.error("Please complete at least some of the impact assessment questions before getting results.")
    
    else:
        # Classification Results
        st.header("📋 Classification Result")
        
        classification = calculate_classification(st.session_state.impact_assessment)
        level = CLASSIFICATION_LEVELS[classification]
        summary = get_impact_summary(st.session_state.impact_assessment)
        
        # Main Classification Result
        st.markdown(f"""
        <div class="classification-card {level['css_class']}">
            <h2>🛡️ {level['name']}</h2>
            <h3>Impact Level: {level['impact']}</h3>
            <p>{level['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Two column layout for summary and controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Assessment Summary")
            
            if st.session_state.selected_dataset:
                dataset = EXAMPLE_DATASETS[st.session_state.selected_dataset]
                st.info(f"**Dataset:** {dataset['name']}\n\n{dataset['description']}")
            
            # Impact summary
            st.markdown("**Response Summary:**")
            st.markdown(f"""
            - 🔴 **High Impact:** {summary['high']} responses
            - 🟠 **Medium Impact:** {summary['medium']} responses  
            - 🟡 **Low Impact:** {summary['low']} responses
            - 🟢 **No Impact:** {summary['none']} responses
            """)
            
            # Classification logic explanation
            if summary['high'] > 0:
                st.warning("Classification: **Top Secret** (Any high impact response)")
            elif summary['medium'] > 0:
                st.warning("Classification: **Secret** (Medium impact responses, no high)")
            elif summary['low'] > 0:
                st.warning("Classification: **Restricted** (Low impact responses, no medium/high)")
            else:
                st.success("Classification: **Public** (No significant impact)")
        
        with col2:
            st.subheader("🔧 Required Controls")
            
            for control in level['controls']:
                st.markdown(f"• {control}")
        
        # Implementation Guidance
        st.info("""
        **Next Steps:** This classification should be reviewed by a Data Classification Reviewer within one month. 
        Implement the required controls and ensure all staff handling this data are trained on the appropriate procedures.
        """)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Start New Assessment", use_container_width=True):
                st.session_state.impact_assessment = {}
                st.session_state.show_results = False
                st.session_state.selected_dataset = None
                st.rerun()
        
        with col2:
            if st.button("✏️ Modify Assessment", use_container_width=True):
                st.session_state.show_results = False
                st.rerun()
        
        with col3:
            # Download results as text
            result_text = f"""SDAIA Data Classification Result
            
Dataset: {EXAMPLE_DATASETS[st.session_state.selected_dataset]['name'] if st.session_state.selected_dataset else 'Custom Dataset'}
Classification: {level['name']} ({level['impact']} Impact)
Description: {level['description']}

Assessment Summary:
- High Impact Responses: {summary['high']}
- Medium Impact Responses: {summary['medium']}
- Low Impact Responses: {summary['low']}
- No Impact Responses: {summary['none']}

Required Controls:
{chr(10).join([f"• {control}" for control in level['controls']])}

Generated by SDAIA Data Classification Tool
Based on SDAIA National Data Governance Policies v1.0 (5/5/2020)
"""
            st.download_button(
                "💾 Download Result",
                result_text,
                file_name=f"classification_result_{classification}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown("*Based on SDAIA National Data Governance Policies v1.0 (5/5/2020)*")

if __name__ == "__main__":
    main()
