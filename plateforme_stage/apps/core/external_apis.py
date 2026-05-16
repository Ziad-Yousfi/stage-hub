import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ExternalOffersService:
    @staticmethod
    def get_rapidapi_internships():
        """
        Récupère et normalise les offres depuis RapidAPI.
        """
        key = "6ecbfdd82fmsh74044df7cac8fd6p1f8637jsne7ae026db787"
        host = "internships-api.p.rapidapi.com"
        headers = {
            "x-rapidapi-key": key,
            "x-rapidapi-host": host,
            "Content-Type": "application/json"
        }
        
        raw_jobs = []
        endpoints = [
            "https://internships-api.p.rapidapi.com/active-jb-7d",
            "https://internships-api.p.rapidapi.com/active-ats-7d"
        ]
        
        for url in endpoints:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    jobs_list = data if isinstance(data, list) else data.get('data') or data.get('jobs') or []
                    if isinstance(jobs_list, list):
                        raw_jobs.extend(jobs_list)
            except Exception: pass
            
        # Normalisation
        normalized = []
        for j in raw_jobs:
            if not isinstance(j, dict): continue
            normalized.append({
                'title': j.get('job_title') or j.get('title'),
                'company': j.get('company_name') or j.get('organization') or j.get('employer_name') or 'Entreprise inconnue',
                'location': j.get('job_location') or (j.get('locations_derived')[0] if j.get('locations_derived') else 'International'),
                'url': j.get('job_apply_link') or j.get('url'),
                'description': j.get('job_description') or '',
                'source': 'RapidAPI'
            })
        return normalized

    @staticmethod
    def get_openwebninja_internships(query="internship"):
        """
        Récupère et normalise les offres depuis Open Web Ninja (JSearch).
        """
        api_key = "ak_ehf097fnl217k23shpmgawumdhmrnusu4wk017i4nzoyuj4"
        url = "https://api.openwebninja.com/jsearch/search" 
        headers = {"x-api-key": api_key}
        params = {
            "query": query,
            "employment_types": "INTERN",
            "page": 1,
            "num_pages": 1
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                raw_jobs = data.get('data', [])
                
                normalized = []
                for j in raw_jobs:
                    if not isinstance(j, dict): continue
                    normalized.append({
                        'title': j.get('job_title') or j.get('title'),
                        'company': j.get('employer_name') or j.get('organization') or j.get('company_name') or 'Entreprise inconnue',
                        'location': f"{j.get('job_city', '')} {j.get('job_country', '')}".strip() or 'International',
                        'url': j.get('job_apply_link') or j.get('url'),
                        'description': j.get('job_description') or '',
                        'source': 'Ninja'
                    })
                return normalized
            return []
        except Exception:
            return []
