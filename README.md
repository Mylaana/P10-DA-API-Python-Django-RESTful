# P10-DA-API-Python-Django-RESTful

Ce README explique comment installer et configurer l'API Django REST.

## Table des matières
**Prérequis**  
**Installation**  
**Exécution**  
**Utilisation**  
**Tests**  

## Prérequis
Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

Python : Vous pouvez le télécharger sur python.org.  
pip : Le gestionnaire de paquets Python.

## Installation
**Clonez ce dépôt sur votre machine locale en utilisant la commande suivante :**
```
git clone https://github.com/Mylaana/P10-DA-API-Python-Django-RESTful.git
```
**Accédez au répertoire du projet :**
```
cd repertoire-de-l'API
```

**Créez un environnement virtuel pour isoler les dépendances du projet :**
```
python -m venv venv
```

**Activez l'environnement virtuel :**

Sur macOS et Linux :
```
source venv/bin/activate
```
  
Sur Windows (PowerShell) :
```
.\venv\Scripts\Activate.ps1
```
  
**Installez les dépendances du projet :**
```
pip install -r requirements.txt
```

## Exécution
Appliquez les migrations de base de données :
```
python manage.py migrate
```
Créez un superutilisateur Django (administrateur) :
```
python manage.py createsuperuser
```
Lancez le serveur de développement Django :
```
python manage.py runserver
```

## Utilisation
L'application est maintenant accessible à l'adresse http://localhost:8000/.
Vous pouvez également vous connecter à l'interface d'administration http://localhost:8000/admin avec le superutilisateur que vous avez créé et manager les différentes tables.

**Endpoints de l'API ne nécessitant pas d'authentification:**
- API ROOT (method GET) : http://localhost:8000/
  c'est le rooter de l'API.

- Obtain Token (method POST) : http://127.0.0.1:8000/api/token/
  permet d'obtenir un token d'authentification, à condition de fournir un [username] et un [password] valides.

**Endpoints de l'API nécessitant une authentification:**
- Profile : http://127.0.0.1:8000/profile/
  methode GET : permet de lister les utilisateurs de la base de donnée
  methode POST : permet de créer un utilisateur
    (pour limiter la création de compte, seul un admin ou un utilisateur authentifié peuvent créer de nouveaux profils)

-Profile + profileID : http://127.0.0.1:8000/profile/[profileID]
  **acces au endpoint restraint soit à l'utilisateur du profil soit à un admin**
  methode GET : permet de lister les informations de l'utilisateur
  methode PUT : permet de mettre à jour toutes les informations de l'utilisateur (owner/admin seulement)
  methode PATCH : permet de mettre à jour certaines informations de l'utilisateur (owner/admin seulement)
  methode DELETE : permet de supprimer l'utilisateur (owner/admin seulement)

- Project (method GET): http://127.0.0.1:8000/project/
- project-contribution (method GET): http://127.0.0.1:8000/project-contribution/
