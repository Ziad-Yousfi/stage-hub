"""
Management command to seed the database with test data.
Run: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.core.models import UserRole, StageType, AcademicLevel
from apps.accounts.models import UserProfile, Etudiant, Entreprise, Enseignant
from apps.offres.models import Competence, Filiere, OffreStage
from apps.pfa.models import PFA, EtapePFA


class Command(BaseCommand):
    """
    Seeds the database with sample data for testing and development.
    
    Creates:
    - Sample users (students, companies, teachers)
    - Sample competencies and majors
    - Sample internship offers
    - Sample PFA projects
    """
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create competencies
        self.stdout.write('Creating competencies...')
        competencies = [
            {'nom': 'Python', 'categorie': 'Programming'},
            {'nom': 'Django', 'categorie': 'Web Development'},
            {'nom': 'JavaScript', 'categorie': 'Programming'},
            {'nom': 'React', 'categorie': 'Web Development'},
            {'nom': 'Data Analysis', 'categorie': 'Data Science'},
            {'nom': 'Machine Learning', 'categorie': 'AI'},
            {'nom': 'Project Management', 'categorie': 'Management'},
            {'nom': 'Communication', 'categorie': 'Soft Skills'},
        ]
        
        for comp_data in competencies:
            Competence.objects.get_or_create(**comp_data)
        
        # Create majors/filieres
        self.stdout.write('Creating majors...')
        filieres = [
            {'nom': 'Computer Science', 'description': 'Computing and software development'},
            {'nom': 'Information Systems', 'description': 'Business and technology integration'},
            {'nom': 'Data Science', 'description': 'Data analysis and machine learning'},
            {'nom': 'Cybersecurity', 'description': 'Information security'},
            {'nom': 'Software Engineering', 'description': 'Software development methodologies'},
        ]
        
        for filiere_data in filieres:
            Filiere.objects.get_or_create(**filiere_data)
        
        # Create sample users
        self.stdout.write('Creating sample users...')
        
        # Admin user
        admin, created = UserProfile.objects.get_or_create(
            email='admin@platform.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        
        # Student users
        student_emails = [
            ('student1@student.com', 'John', 'Doe', 'L3'),
            ('student2@student.com', 'Jane', 'Smith', 'M1'),
            ('student3@student.com', 'Bob', 'Johnson', 'M2'),
        ]
        
        students = []
        for email, first_name, last_name, niveau in student_emails:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': UserRole.ETUDIANT,
                }
            )
            if created:
                user.set_password('student123')
                user.save()
            
            etudiant, _ = Etudiant.objects.get_or_create(
                user=user,
                defaults={
                    'filiere': 'Computer Science',
                    'niveau': niveau,
                    'numero_etudiant': f'STU{email.split("@")[0].upper()}',
                    'annee_academique': '2024-2025',
                }
            )
            students.append(etudiant)
        
        # Company users
        company_data = [
            ('tech@company.com', 'TechCorp', 'Technology', 'Paris', 'www.techcorp.com'),
            ('innovate@company.com', 'InnovateLab', 'Research', 'Lyon', 'www.innovatelab.com'),
            ('data@company.com', 'DataSolutions', 'Data Science', 'Marseille', 'www.datasolutions.com'),
        ]
        
        companies = []
        for email, nom, secteur, ville, site in company_data:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': nom,
                    'last_name': 'Representative',
                    'role': UserRole.ENTREPRISE,
                }
            )
            if created:
                user.set_password('company123')
                user.save()
            
            entreprise, _ = Entreprise.objects.get_or_create(
                user=user,
                defaults={
                    'nom_entreprise': nom,
                    'secteur_activite': secteur,
                    'ville': ville,
                    'site_web': site,
                    'adresse': f'123 Business Street, {ville}',
                    'siret': f'SIRET{nom.upper()[:5]}123',
                }
            )
            companies.append(entreprise)
        
        # Teacher users
        teacher_data = [
            ('teacher1@university.com', 'Alice', 'Martin', 'Computer Science', 'Software Engineering', 'Professor'),
            ('teacher2@university.com', 'Pierre', 'Dubois', 'Information Systems', 'Database Systems', 'Associate Professor'),
        ]
        
        teachers = []
        for email, first_name, last_name, dept, specialite, grade in teacher_data:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': UserRole.ENSEIGNANT,
                }
            )
            if created:
                user.set_password('teacher123')
                user.save()
            
            enseignant, _ = Enseignant.objects.get_or_create(
                user=user,
                defaults={
                    'departement': dept,
                    'specialite': specialite,
                    'grade': grade,
                }
            )
            teachers.append(enseignant)
        
        # Create sample internship offers
        self.stdout.write('Creating sample internship offers...')
        offre_data = [
            {
                'titre': 'Full Stack Developer Intern',
                'description': 'Develop web applications using Django and React',
                'missions': 'Build features, fix bugs, write tests',
                'type_stage': StageType.PFA,
                'duree_semaines': 16,
                'date_debut': timezone.now().date() + timedelta(days=30),
                'date_fin_candidature': timezone.now().date() + timedelta(days=15),
                'niveau_requis': AcademicLevel.M1,
                'localisation': 'Paris, France',
                'teletravail': True,
                'gratification_montant': 800,
                'nombre_postes': 2,
                'statut': 'PUBLIEE',
            },
            {
                'titre': 'Data Science Intern',
                'description': 'Analyze data and build ML models',
                'missions': 'Data preprocessing, model training, visualization',
                'type_stage': StageType.PFE,
                'duree_semaines': 24,
                'date_debut': timezone.now().date() + timedelta(days=45),
                'date_fin_candidature': timezone.now().date() + timedelta(days=20),
                'niveau_requis': AcademicLevel.M2,
                'localisation': 'Lyon, France',
                'teletravail': False,
                'gratification_montant': 1000,
                'nombre_postes': 1,
                'statut': 'PUBLIEE',
            },
            {
                'titre': 'DevOps Intern',
                'description': 'Work on CI/CD pipelines and cloud infrastructure',
                'missions': 'Automate deployments, monitor systems',
                'type_stage': StageType.PERFECTIONNEMENT,
                'duree_semaines': 12,
                'date_debut': timezone.now().date() + timedelta(days=60),
                'date_fin_candidature': timezone.now().date() + timedelta(days=30),
                'niveau_requis': AcademicLevel.L3,
                'localisation': 'Marseille, France',
                'teletravail': True,
                'gratification_montant': 600,
                'nombre_postes': 1,
                'statut': 'PUBLIEE',
            },
        ]
        
        for i, data in enumerate(offre_data):
            offre, created = OffreStage.objects.get_or_create(
                titre=data['titre'],
                defaults=data
            )
            if created:
                offre.entreprise = companies[i % len(companies)]
                offre.save()
                
                # Add competencies
                competences = list(Competence.objects.all()[:3])
                offre.competences_requises.set(competences)
                
                # Add filieres
                filieres = list(Filiere.objects.all()[:2])
                offre.filieres_ciblees.set(filieres)
        
        # Create sample PFA projects
        self.stdout.write('Creating sample PFA projects...')
        pfa_data = [
            {
                'titre_pfa': 'E-commerce Platform Development',
                'description': 'Build a complete e-commerce solution',
                'domaine': 'Web Development',
                'mots_cles': 'Django, React, PostgreSQL',
                'semestre': 'S2',
            },
            {
                'titre_pfa': 'ML-based Recommendation System',
                'description': 'Develop a recommendation engine using machine learning',
                'domaine': 'Data Science',
                'mots_cles': 'Python, TensorFlow, Data Analysis',
                'semestre': 'S2',
            },
        ]
        
        for i, data in enumerate(pfa_data):
            pfa, created = PFA.objects.get_or_create(
                titre_pfa=data['titre_pfa'],
                defaults={
                    **data,
                    'annee_academique': '2024-2025',
                    'statut': 'EN_COURS',
                }
            )
            if created:
                # Add students
                pfa.etudiants.add(students[i % len(students)])
                
                # Add supervisor
                pfa.encadrant_academique = teachers[i % len(teachers)]
                pfa.save()
                
                # Add project steps
                steps = [
                    {'titre_etape': 'Requirements Analysis', 'ordre': 1},
                    {'titre_etape': 'System Design', 'ordre': 2},
                    {'titre_etape': 'Implementation', 'ordre': 3},
                    {'titre_etape': 'Testing', 'ordre': 4},
                    {'titre_etape': 'Documentation', 'ordre': 5},
                ]
                
                base_date = timezone.now().date()
                for step_data in steps:
                    EtapePFA.objects.create(
                        pfa=pfa,
                        date_debut_prevue=base_date + timedelta(weeks=step_data['ordre'] * 2),
                        date_fin_prevue=base_date + timedelta(weeks=(step_data['ordre'] + 1) * 2),
                        **step_data
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
        self.stdout.write('')
        self.stdout.write('Sample credentials:')
        self.stdout.write('  Admin: admin@platform.com / admin123')
        self.stdout.write('  Student: student1@student.com / student123')
        self.stdout.write('  Company: tech@company.com / company123')
        self.stdout.write('  Teacher: teacher1@university.com / teacher123')
