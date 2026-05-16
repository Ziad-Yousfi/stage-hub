import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.endpoint = os.getenv("AI_ENDPOINT", "https://models.inference.ai.azure.com")
        self.model = os.getenv("AI_MODEL", "gpt-4o")
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in environment variables.")
            
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file object."""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""

    def match_cv_to_offers(self, cv_text, offers_list):
        """
        Ask the AI to rank and filter the best offers for a given CV.
        offers_list should be a list of dictionaries with offer details.
        """
        offers_context = "\n".join([
            f"ID: {o['id']} | Titre: {o['titre']} | Entreprise: {o['entreprise']} | Missions: {o['missions']}"
            for o in offers_list
        ])
        
        prompt = f"""
        Tu es un expert en recrutement international. Analyse le CV de l'étudiant et sélectionne les 3 meilleures offres de stage parmi la liste fournie.
        
        CV DE L'ÉTUDIANT:
        ---
        {cv_text}
        ---
        
        LISTE DES OFFRES (Contient des offres Locales et Internationales):
        ---
        {offers_context}
        ---
        
        CONSIGNES:
        1. Compare les langages, frameworks et outils du CV avec les missions des offres.
        2. Sélectionne EXACTEMENT 3 IDs (ou moins s'il n'y a vraiment aucune correspondance).
        3. Réponds uniquement au format JSON:
        {{"best_matches": ["ID1", "ID2", "ID3"], "explanation": "Une explication personnalisée de 2-3 phrases en français sur pourquoi ces offres correspondent au profil de l'étudiant."}}
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Tu es un assistant spécialisé dans le matching de stages."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI Match Error: {e}")
            return None

    def get_pfa_tutor_response(self, pfa_context, student_message, chat_history):
        """
        Act as an expert professor guiding the student on their PFA.
        """
        messages = [
            {"role": "system", "content": f"""
                Tu es le Professeur IA, Tuteur Expert à l'EMSI (École Marocaine des Sciences de l'Ingénieur).
                Ton rôle est d'encadrer l'étudiant dans son Projet de Fin d'Année (PFA).
                
                TON STYLE:
                - Professionnel, académique, mais encourageant.
                - Utilise le "Nous" pour montrer que tu accompagnes l'étudiant.
                - Sois précis techniquement (si l'étudiant parle de code ou d'architecture).
                - Ne donne pas la solution toute faite immédiatement, guide l'étudiant par des questions ou des pistes de réflexion.
                
                CONTEXTE DU PROJET:
                Titre: {pfa_context['titre']}
                Description: {pfa_context['description']}
                Domaine: {pfa_context['domaine']}
                Jalons prévus: {pfa_context['etapes']}
                
                STRUCTURE DE TES RÉPONSES:
                1. Analyse rapide de la demande de l'étudiant.
                2. Conseils ou corrections spécifiques.
                3. Proposition de la prochaine étape ou d'un point de vigilance.
            """}
        ]
        
        # Add history
        for msg in chat_history:
            messages.append({"role": "user" if msg['is_user'] else "assistant", "content": msg['text']})
            
        # Add current message
        messages.append({"role": "user", "content": student_message})
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI PFA Error: {e}")
            return "Désolé, j'ai rencontré une erreur technique en analysant votre message. Réessayez dans un instant."
