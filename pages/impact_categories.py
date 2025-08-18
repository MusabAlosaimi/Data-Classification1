"""Impact categories and questions for SDAIA Data Classification."""

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
