# translations.py

def get_translation(lang_key):
    translations = {
        "English": {
            "title": "🧠 Learn About Stroke",
            "desc": "A stroke happens when the blood supply to part of your brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients.",
            "warning": "Warning Signs of Stroke",
            "warning_list": [
                "Sudden numbness or weakness in the face, arm, or leg—especially on one side of the body",
                "Sudden confusion, trouble speaking, or understanding speech",
                "Sudden trouble seeing in one or both eyes",
                "Sudden trouble walking, dizziness, loss of balance or coordination",
                "Sudden severe headache with no known cause"
            ],
            "cta": "📝 Go to Stroke Risk Assessment",
            "lang_code": "en"
        },
        "French": {
            "title": "🧠 Apprenez à propos des AVC",
            "desc": "Un AVC se produit lorsque l'approvisionnement en sang d'une partie de votre cerveau est interrompu ou réduit.",
            "warning": "Signes d'alerte d'un AVC",
            "warning_list": [
                "Engourdissement soudain ou faiblesse du visage, d’un bras ou d’une jambe",
                "Confusion soudaine, troubles de la parole",
                "Problèmes de vision soudains",
                "Vertiges, problèmes de coordination",
                "Forte migraine sans cause connue"
            ],
            "cta": "📝 Passer à l'évaluation des risques",
            "lang_code": "fr"
        }
        # Add more languages here
    }
    return translations.get(lang_key, translations["English"])
