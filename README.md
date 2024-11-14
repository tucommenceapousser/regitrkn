# Coach Minceur IA 🏋️‍♀️ | AI Weight Loss Coach

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/AI-GPT--4-orange.svg)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

Un assistant personnel de perte de poids alimenté par l'IA, offrant un suivi personnalisé et des conseils en temps réel.

[English](#english-version) | [Français](#coach-minceur-ia-)

## ✨ Fonctionnalités

- 🔐 **Authentification Sécurisée**
  - Système d'inscription et de connexion
  - Protection des données personnelles
  - Sessions sécurisées avec CSRF

- 📊 **Suivi des Mesures**
  - Enregistrement du poids
  - Mesure du tour de taille
  - Pourcentage de masse grasse
  - Visualisation graphique des progrès avec Chart.js

- 🍽️ **Plan de Repas Intelligent**
  - Suggestions de repas personnalisées par GPT-4
  - Calcul des calories
  - Suivi des macronutriments
  - Plans de repas hebdomadaires adaptatifs

- 💪 **Suivi des Exercices**
  - Enregistrement des activités physiques
  - Catégorisation des exercices (cardio, musculation, flexibilité)
  - Calcul des calories brûlées
  - Historique d'entraînement détaillé

- 📸 **Suivi Photo des Progrès**
  - Téléchargement sécurisé des photos
  - Traitement d'image avec Fabric.js
  - Visualisation de la progression
  - Organisation par type (face, profil, dos)

- 🤖 **Coach IA Interactif**
  - Conseils personnalisés via GPT-4
  - Réponses en temps réel
  - Historique des conversations
  - Support multilingue (Français/English)

- 📋 **Rapports de Progression**
  - Rapports détaillés imprimables
  - Graphiques de progression
  - Historique des exercices
  - Suivi photographique complet

## 🛠️ Stack Technique

### Backend
- **Python 3.11** - Langage de programmation
- **Flask** - Framework web léger et extensible
- **SQLAlchemy** - ORM pour la gestion de la base de données
- **OpenAI GPT-4** - Modèle d'IA pour le coaching personnalisé
- **PostgreSQL** - Base de données relationnelle

### Frontend
- **Bootstrap 5** - Framework CSS moderne et responsive
- **Chart.js** - Bibliothèque de visualisation de données
- **Fabric.js** - Manipulation et traitement d'images
- **CSRF Protection** - Sécurité des formulaires

## 📦 Installation sur Replit

1. Accédez au projet sur Replit :
```
https://replit.com/@trkn/regitrkn
```

2. Configurez les secrets dans l'onglet "Secrets" :
```
OPENAI_API_KEY=votre_clé_api_openai
FLASK_SECRET_KEY=votre_clé_secrète
```

3. L'installation des dépendances et le démarrage se font automatiquement sur Replit

### Résolution des Problèmes

1. Si la base de données ne se connecte pas :
   - Vérifiez que PostgreSQL est activé dans l'onglet "Tools"
   - Attendez quelques secondes que la base de données démarre
   - Vérifiez les logs dans l'onglet "Console"

2. Si l'API OpenAI ne répond pas :
   - Vérifiez que votre clé API est correctement configurée
   - Assurez-vous que votre clé a des crédits disponibles
   - Consultez les logs de réponse dans la console

3. Pour les problèmes de dépendances :
   - Utilisez l'onglet "Shell" pour vérifier les versions
   - Redémarrez le serveur si nécessaire
   - Consultez les logs d'erreur

## 🚀 Guide d'Utilisation

### 1. Inscription et Connexion
- Créez un compte avec votre email
- Connectez-vous de manière sécurisée
- Personnalisez votre profil

### 2. Dashboard
- Ajoutez vos mesures quotidiennes
- Visualisez vos progrès via les graphiques
- Accédez rapidement à toutes les fonctionnalités

### 3. Gestion des Repas
- Recevez des suggestions personnalisées
- Enregistrez vos repas quotidiens
- Suivez vos apports caloriques

### 4. Exercices
- Enregistrez vos séances d'entraînement
- Suivez votre progression
- Visualisez votre historique

### 5. Suivi Photo
- Importez vos photos de progression
- Organisez-les par catégorie
- Comparez votre évolution

### 6. Coaching IA
- Posez des questions en langage naturel
- Recevez des conseils personnalisés
- Consultez l'historique des échanges

## 🔧 API et Intégrations

### Configuration des Variables d'Environnement

Les variables suivantes doivent être configurées dans l'onglet "Secrets" de Replit :

```bash
# Requis
OPENAI_API_KEY=sk-...       # Clé API OpenAI
FLASK_SECRET_KEY=random     # Clé secrète Flask pour les sessions
DATABASE_URL=postgresql://  # URL de connexion PostgreSQL (auto-configurée)

# Optionnel
FLASK_ENV=development      # Environnement (development/production)
FLASK_DEBUG=1             # Mode debug (1/0)
```

### Endpoints Principaux

#### Authentification

```python
# POST /register
Request:
{
    "username": "utilisateur",
    "email": "utilisateur@email.com",
    "password": "motdepasse"
}
Response:
{
    "status": "success",
    "message": "Inscription réussie!"
}

# POST /login
Request:
{
    "username": "utilisateur",
    "password": "motdepasse"
}
Response:
{
    "status": "success",
    "message": "Connexion réussie!"
}
```

#### Mesures et Suivi

```python
# POST /add_measurement
Request:
{
    "weight": 75.5,
    "waist": 85,
    "body_fat": 20,
    "notes": "Après l'exercice"
}
Response:
{
    "status": "success",
    "message": "Mesure ajoutée!"
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet sur Replit
2. Créez votre branche (`feature/amélioration`)
3. Committez vos changements
4. Proposez vos améliorations via Pull Request

### Guide de Développement

1. Structure du Projet
```
/
├── app.py              # Configuration Flask
├── routes.py           # Routes et endpoints
├── models.py           # Modèles SQLAlchemy
├── chat_request.py     # Intégration OpenAI
├── templates/          # Templates HTML
├── static/            
│   ├── css/           # Styles CSS
│   └── js/            # Scripts JavaScript
└── README.md          # Documentation
```

2. Standards de Code
- Suivez PEP 8 pour Python
- Utilisez des docstrings pour la documentation
- Commentez le code complexe
- Testez avant de soumettre

## 🐛 Débogage

### Base de Données
- Utilisez l'interface PostgreSQL de Replit
- Vérifiez les logs dans l'onglet "Console"
- Consultez les erreurs dans "Shell"

### IA Coach
- Vérifiez la validité de votre clé API OpenAI
- Consultez les logs de réponse
- Testez les prompts dans l'interface de chat

---

# English Version

An AI-powered personal weight loss assistant providing personalized tracking and real-time advice.

## ✨ Features

- 🔐 **Secure Authentication**
  - Registration and login system
  - Personal data protection
  - CSRF-secured sessions

- 📊 **Measurement Tracking**
  - Weight recording
  - Waist measurement
  - Body fat percentage
  - Progress visualization with Chart.js

- 🍽️ **Smart Meal Planning**
  - GPT-4 powered meal suggestions
  - Calorie tracking
  - Macronutrient monitoring
  - Adaptive weekly meal plans

- 💪 **Exercise Tracking**
  - Physical activity logging
  - Exercise categorization (cardio, strength, flexibility)
  - Calorie burn calculation
  - Detailed training history

- 📸 **Progress Photo Tracking**
  - Secure photo uploads
  - Image processing with Fabric.js
  - Progress visualization
  - Type-based organization (front, side, back)

- 🤖 **Interactive AI Coach**
  - Personalized advice via GPT-4
  - Real-time responses
  - Conversation history
  - Multilingual support (French/English)

- 📋 **Progress Reports**
  - Detailed printable reports
  - Progress charts
  - Exercise history
  - Complete photo tracking

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Programming language
- **Flask** - Lightweight web framework
- **SQLAlchemy** - Database ORM
- **OpenAI GPT-4** - AI model for personalized coaching
- **PostgreSQL** - Relational database

### Frontend
- **Bootstrap 5** - Modern CSS framework
- **Chart.js** - Data visualization library
- **Fabric.js** - Image manipulation
- **CSRF Protection** - Form security

## 📦 Installation on Replit

1. Access the project on Replit:
```
https://replit.com/@trkn/regitrkn
```

2. Configure secrets in the "Secrets" tab:
```
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

3. Dependencies installation and startup happen automatically on Replit

### Troubleshooting

1. If the database doesn't connect:
   - Check if PostgreSQL is enabled in the "Tools" tab
   - Wait a few seconds for the database to start
   - Check logs in the "Console" tab

2. If the OpenAI API doesn't respond:
   - Verify your API key is correctly configured
   - Ensure your key has available credits
   - Check response logs in the console

3. For dependency issues:
   - Use the "Shell" tab to check versions
   - Restart the server if needed
   - Check error logs

## 🚀 Usage Guide

### 1. Registration and Login
- Create an account with your email
- Log in securely
- Customize your profile

### 2. Dashboard
- Add daily measurements
- View progress through charts
- Quick access to all features

### 3. Meal Management
- Receive personalized suggestions
- Log daily meals
- Track caloric intake

### 4. Exercises
- Record training sessions
- Track your progress
- View your history

### 5. Photo Tracking
- Import progress photos
- Organize by category
- Compare your evolution

### 6. AI Coaching
- Ask questions in natural language
- Receive personalized advice
- Review conversation history

## 🔧 API and Integrations

### Environment Variables Setup

The following variables must be configured in Replit's "Secrets" tab:

```bash
# Required
OPENAI_API_KEY=sk-...       # OpenAI API Key
FLASK_SECRET_KEY=random     # Flask secret key for sessions
DATABASE_URL=postgresql://  # PostgreSQL connection URL (auto-configured)

# Optional
FLASK_ENV=development      # Environment (development/production)
FLASK_DEBUG=1             # Debug mode (1/0)
```

### Main Endpoints

#### Authentication

```python
# POST /register
Request:
{
    "username": "user",
    "email": "user@email.com",
    "password": "password"
}
Response:
{
    "status": "success",
    "message": "Registration successful!"
}

# POST /login
Request:
{
    "username": "user",
    "password": "password"
}
Response:
{
    "status": "success",
    "message": "Login successful!"
}
```

#### Measurements and Tracking

```python
# POST /add_measurement
Request:
{
    "weight": 75.5,
    "waist": 85,
    "body_fat": 20,
    "notes": "After exercise"
}
Response:
{
    "status": "success",
    "message": "Measurement added!"
}
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project on Replit
2. Create your feature branch (`feature/improvement`)
3. Commit your changes
4. Submit your improvements via Pull Request

### Development Guide

1. Project Structure
```
/
├── app.py              # Flask configuration
├── routes.py           # Routes and endpoints
├── models.py           # SQLAlchemy models
├── chat_request.py     # OpenAI integration
├── templates/          # HTML templates
├── static/            
│   ├── css/           # CSS styles
│   └── js/            # JavaScript scripts
└── README.md          # Documentation
```

2. Code Standards
- Follow PEP 8 for Python
- Use docstrings for documentation
- Comment complex code
- Test before submitting

## 🐛 Debugging

### Database
- Use Replit's PostgreSQL interface
- Check logs in the "Console" tab
- Review errors in "Shell"

### AI Coach
- Verify OpenAI API key validity
- Check response logs
- Test prompts in the chat interface

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
