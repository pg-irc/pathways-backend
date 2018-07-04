def get_explore_taxonomy_id():
    return 'explore'


def get_system_taxonomies():
    return {
        'explore':
        {
            'settling_in': {'icon': 'sign-text'},
            'education': {'icon': 'book-open-variant'},
            'healthCare': {'icon': 'medical-bag'},
            'money': {'icon': 'currency-usd'},
            'housing': {'icon': 'home'},
            'employment': {'icon': 'briefcase'},
            'legal': {'icon': 'gavel'},
            'driving': {'icon': 'car'},
            'helpForIndividualsAndFamilies': {'icon': 'account'}
        },
        'time_in_canada':
        {
            'not_yet_arrived': {},
            'under_1_month': {},
            'under_6_months': {},
            'under_1_year': {},
            'under_2_years': {},
            'over_2_years': {},
        },
        'user': {
            'alone': {},
            'with_family': {}
        },
        'age': {
            'under_13': {},
            '13_to_18': {},
            '18_to_64': {},
            'over_65': {},
        },
        'immigrant_type': {
            'refugee_claimant': {},
            'temporary_resident': {},
            'permanent_resident': {},
            'unknown': {},
        },
        'refugee_claim_stage': {
            'claim_at_border': {},
            'not_started': {},
            'claim_at_cic_office': {},
            'hearing': {},
            'positive_decision': {},
            'negative_decision': {},
        },
        'english_level': {
            'none': {},
            'beginner': {},
            'intermediate': {},
            'fluent': {},
        },
        'group': {
            'women': {},
            'disability': {},
            'lgbtq2': {},
            'services_in_french': {},
            'low_income': {},
        }
    }
