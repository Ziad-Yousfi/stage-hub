# 🎓 Plateforme Stage — Gestion des Stages & PFA

Application web Django complète pour la gestion des stages académiques et des Projets de Fin d'Année (PFA) à l'EMSI.

---

## 🎯 Fonctionnalités par Rôle

### 👨‍🎓 Étudiant
- Parcourir et filtrer les offres de stage
- Postuler (limite configurable, défaut : 5 candidatures)
- Suivre le statut de ses candidatures en temps réel
- Soumettre des rapports hebdomadaires d'avancement
- Gérer son PFA via un tableau Kanban + vue Gantt
- Sauvegarder des offres en favoris

### 🏢 Entreprise
- Publier et gérer des offres de stage (CRUD complet)
- Consulter et traiter les candidatures reçues
- Communiquer avec les étudiants et enseignants via messagerie interne
- Gérer les stagiaires accueillis

### 👨‍🏫 Enseignant
- Superviser les stages de ses étudiants
- Valider les rapports hebdomadaires avec commentaires
- Suivre l'avancement des PFA
- Gérer les soutenances et les jurys

### 🛡️ Administrateur
- Gestion complète de la plateforme
- Gestion des utilisateurs et des rôles
- Statistiques et reporting
- Export des données (CSV/Excel via django-import-export)
- Accès au panneau Django Admin

---

## 🏗️ Stack Technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Framework | Django | ≥ 4.2 |
| API REST | Django REST Framework | ≥ 3.14 |
| Auth | Django Allauth | ≥ 0.54 |
| Base de données | MySQL (prod) / SQLite (dev) | — |
| Temps réel | Firebase Firestore | — |
| Frontend | Bootstrap 5 + Chart.js | — |
| Formulaires | django-crispy-forms | ≥ 2.0 |
| PDF | WeasyPrint | ≥ 59.0 |
| IA | OpenAI API (GPT-4o / Azure) | ≥ 1.3.0 |
| Tâches async | Celery + Redis | ≥ 5.3 / ≥ 4.6 |
| Déploiement | Gunicorn + WhiteNoise | — |
| Stockage | Django Storages (AWS S3 opt.) | ≥ 1.13 |

---

## 📁 Architecture du Projet

```
plateforme_stage/
├── config/                     # Configuration du projet
│   ├── settings/
│   │   ├── base.py             # Paramètres communs (Firebase, DB, Auth...)
│   │   ├── development.py      # Paramètres de développement
│   │   └── production.py       # Paramètres de production
│   ├── urls.py                 # Routage principal
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                       # Applications Django
│   ├── core/                   # Utilitaires partagés
│   │   └── models.py           # Enums : UserRole, StageType, CandidatureStatus...
│   │   └── mixins              # RoleRequiredMixin, RBAC
│   │
│   ├── accounts/               # Gestion des utilisateurs
│   │   └── models.py           # UserProfile, Etudiant, Entreprise, Enseignant
│   │
│   ├── offres/                 # Offres de stage
│   │   └── models.py           # OffreStage, Competence, Filiere, Favori
│   │
│   ├── candidatures/           # Candidatures
│   │   └── models.py           # Candidature + workflow de statut
│   │
│   ├── stages/                 # Stages en cours
│   │   └── models.py           # StageEnCours, VisiteTerrainRapport, MessageInterne
│   │
│   ├── pfa/                    # Projets de Fin d'Année
│   │   └── models.py           # PFA, EtapePFA, ReunionSuivi, DocumentPFA, MessagePFA
│   │
│   ├── dashboard/              # Tableaux de bord (par rôle)
│   └── notifications/          # Système de notifications in-app
│
├── templates/                  # Templates HTML
├── static/                     # CSS, JS, images
├── media/                      # Fichiers uploadés
├── firebase-key.json           # Clé Firebase (ne pas commiter en prod !)
├── requirements.txt
├── manage.py
└── .env.example
```

---

## 👥 Rôles Utilisateurs

| Rôle | Code | Description |
|------|------|-------------|
| Étudiant | `ETUDIANT` | Parcourir les offres, postuler, suivre son stage/PFA |
| Entreprise | `ENTREPRISE` | Publier des offres, gérer les candidatures |
| Enseignant | `ENSEIGNANT` | Encadrer, valider rapports, gérer jurys |
| Administrateur | `ADMIN` | Accès complet à la plateforme |

---

## 🔑 Variables d'Environnement

Copier `.env.example` vers `.env` et renseigner :

```env
# Django
SECRET_KEY=votre_cle_secrete_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données (MySQL par défaut)
DATABASE_USER=root
DATABASE_PASSWORD=votre_mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=plateforme_stage_db

# SQLite (développement uniquement)
USE_SQLITE=True

# IA — GitHub/Azure OpenAI
GITHUB_TOKEN=votre_token_github
AI_MODEL=gpt-4o
AI_ENDPOINT=https://models.inference.ai.azure.com

# APIs externes
RAPIDAPI_KEY=votre_cle_rapidapi
RAPIDAPI_HOST=internships-api.p.rapidapi.com
OPEN_WEB_NINJA_KEY=votre_cle_ninja

# Firebase (si Firestore utilisé)
FIREBASE_PROJECT_ID=...
FIREBASE_PRIVATE_KEY=...
FIREBASE_CLIENT_EMAIL=...

# Email SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre@email.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app

# AWS S3 (optionnel)
USE_S3=False
```

---

## 📋 Installation

### Prérequis
- Python 3.9+
- MySQL 8+ (ou SQLite pour le développement)
- Redis (optionnel, pour Celery)

### Étape par étape

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd stage-hub-repo/plateforme_stage

# 2. Créer l'environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
# Éditer .env selon votre environnement

# 5. Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Lancer le serveur de développement
python manage.py runserver
```

Accès : **[http://localhost:8000](http://localhost:8000)**
Admin : **[http://localhost:8000/admin/](http://localhost:8000/admin/)**

---

## 🔐 Authentification

La plateforme utilise **Django Allauth** avec authentification par email.

| URL | Description |
|-----|-------------|
| `/accounts/signup/` | Inscription (choix du rôle) |
| `/accounts/login/` | Connexion |
| `/accounts/logout/` | Déconnexion |
| `/accounts/profile/` | Profil utilisateur |

---

## 📊 Modules Détaillés

### 📋 Offres de Stage (`/offres/`)
- CRUD complet pour les entreprises
- Filtrage avancé : type de stage, durée, localisation, niveau, compétences
- Recherche plein texte
- Sauvegarde en favoris avec notes personnelles
- Statuts : Brouillon → Publiée → Expirée / Pourvue

### 📨 Candidatures (`/candidatures/`)
- Candidature en un clic (si profil complet)
- Limite paramétrable (défaut : **5 candidatures actives**)
- Workflow de statut : En attente → Vue → Retenue → Acceptée / Refusée
- Notifications email automatiques

### 🗂️ Stages en Cours (`/stages/`)
- Suivi visuel avec timeline
- Rapports hebdomadaires structurés (tâches, difficultés, avancement %)
- Validation par l'enseignant encadrant avec commentaires
- Messagerie interne entre étudiant, enseignant et entreprise
- Génération de PDF (convention, rapport final)

### 🎓 PFA (`/pfa/`)
- Tableau Kanban pour les étapes du projet
- Vue Gantt (dates prévues vs réelles)
- Versioning des documents (rapports, présentations)
- Suivi des réunions avec compte-rendus et actions
- Calcul automatique de la note finale : `40% encadrant + 60% jury`
- Lien vers le code source GitHub

---

## 🔒 Sécurité

- **RBAC** : Mixins de contrôle d'accès par rôle (`EtudiantRequiredMixin`, `EntrepriseRequiredMixin`...)
- Protection **CSRF** sur tous les formulaires
- Validation des fichiers uploadés (types, taille)
- Hashage sécurisé des mots de passe (Django default)
- Variables sensibles via `python-decouple`

---

## 🚀 Déploiement (Production)

### Railway / Heroku

```bash
# Le Procfile est déjà configuré
web: gunicorn config.wsgi --log-file -
```

### Checklist production

```env
DEBUG=False
SECRET_KEY=<cle-forte-aleatoire>
ALLOWED_HOSTS=votre-domaine.com
USE_SQLITE=False  # Utiliser MySQL
```

```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### AWS S3 (stockage fichiers)
```env
USE_S3=True
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

---

## 🧪 Tests

```bash
python manage.py test
```

---

## 📦 Dépendances Principales

```
Django>=4.2
djangorestframework>=3.14
django-allauth>=0.54
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
django-import-export>=3.2
Pillow>=10.0
python-decouple>=3.8
psycopg2-binary>=2.9
mysqlclient>=2.2.0
WeasyPrint>=59.0
django-storages>=1.13
celery>=5.3
redis>=4.6
gunicorn>=21.2.0
whitenoise>=6.5.0
openai>=1.3.0
PyPDF2>=3.0.0
firebase-admin>=6.5.0
dj-database-url>=2.1.0
```

---

## 📄 Licence

Projet académique — EMSI 2024-2025 — Tous droits réservés.

---

**Développé avec Django ❤️ par Ziad Yousfi — EMSI IIR 3ème année**
