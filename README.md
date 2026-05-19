# 🎓 Stage Hub — Plateforme de Gestion des Stages & PFA

> Projet de Fin d'Année (PFA) — EMSI, 3ème année IIR | 2024-2025

**Stage Hub** est une application web complète développée avec **Django** pour centraliser et automatiser la gestion des stages académiques et des Projets de Fin d'Année (PFA) au sein d'un établissement d'enseignement supérieur.

---

## 🧑‍💻 Auteur

| Nom | Filière | École |
|-----|---------|-------|
| **Ziad Yousfi** | Ingénierie Informatique et Réseaux (IIR) — 3ème année | EMSI |

---

## 🏗️ Stack Technique

| Couche | Technologie |
|--------|-------------|
| **Backend** | Django 4.2+, Django REST Framework |
| **Auth** | Django Allauth (email-based, multi-rôles) |
| **Base de données** | MySQL (prod) / SQLite (dev) |
| **Temps réel** | Firebase Firestore |
| **Frontend** | Django Templates, Bootstrap 5, Chart.js |
| **Formulaires** | django-crispy-forms + crispy-bootstrap5 |
| **PDF** | WeasyPrint |
| **IA** | OpenAI API (GPT-4o via Azure) |
| **Fichiers** | Pillow, PyPDF2, django-storages (AWS S3 opt.) |
| **Tâches async** | Celery + Redis |
| **Déploiement** | Gunicorn + WhiteNoise, Railway/Netlify ready |

---

## 📁 Structure du Projet

```
stage-hub-repo/
├── plateforme_stage/       # Application Django principale
│   ├── apps/
│   │   ├── accounts/       # Comptes & profils (Étudiant, Entreprise, Enseignant)
│   │   ├── offres/         # Offres de stage (CRUD, filtres, favoris)
│   │   ├── candidatures/   # Candidatures & suivi de statut
│   │   ├── stages/         # Stages en cours, rapports hebdomadaires
│   │   ├── pfa/            # Projets de Fin d'Année (Kanban, Gantt, docs)
│   │   ├── dashboard/      # Tableaux de bord par rôle
│   │   ├── notifications/  # Système de notifications
│   │   └── core/           # Mixins, enums, utilitaires partagés
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py     # Config commune
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   └── urls.py
│   ├── templates/
│   ├── static/
│   ├── media/
│   └── manage.py
├── requirements.txt
├── Procfile                # Config Railway/Heroku
├── start.sh
└── README.md
```

---

## ⚡ Installation Rapide

```bash
# 1. Cloner le repo
git clone <url-du-repo>
cd stage-hub-repo/plateforme_stage

# 2. Environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Dépendances
pip install -r requirements.txt

# 4. Variables d'environnement
copy .env.example .env
# Éditer .env avec vos valeurs

# 5. SQLite pour le dev (rapide)
# Ajouter USE_SQLITE=True dans .env

# 6. Migrations & lancement
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accès : [http://localhost:8000](http://localhost:8000)

---

## 📄 Licence

Projet académique — EMSI 2025-2026. Tous droits réservés.
