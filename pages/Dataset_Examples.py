"""Dataset definitions for SDAIA Data Classification Tool."""

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
