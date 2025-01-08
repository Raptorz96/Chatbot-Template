# Insurance categories with subcategories
INSURANCE_CATEGORIES = {
    "auto": {
        "name": "Auto Insurance",
        "subcategories": ["RC Auto", "Kasko", "Furto e Incendio"]
    },
    "casa": {
        "name": "Home Insurance",
        "subcategories": ["Responsabilità Civile", "Danni", "Catastrofi Naturali"]
    },
    "vita": {
        "name": "Life Insurance",
        "subcategories": ["Temporanea", "Vita Intera", "Mista"]
    },
    "sinistri": {
        "name": "Claims",
        "subcategories": ["Denuncia", "Gestione", "Rimborsi"]
    },
    "polizze": {
        "name": "Policy",
        "subcategories": ["Nuova Polizza", "Rinnovo", "Modifica"]
    }
}

# Document types
DOCUMENT_TYPES = {
    "faq": "Frequently Asked Questions",
    "policy": "Policy Document",
    "procedure": "Procedure Document",
    "info": "General Information"
}

# Priority levels for documents
PRIORITY_LEVELS = {
    1: "Low",
    2: "Medium-Low",
    3: "Medium",
    4: "Medium-High",
    5: "High"
}

# Default metadata structure
DEFAULT_METADATA = {
    "categoria": None,
    "subcategoria": None,
    "tipo": "faq",
    "priority": 3,
    "language": "it"
}