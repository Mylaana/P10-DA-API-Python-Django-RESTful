# P10-DA-API-Python-Django-RESTful

Ce README explique comment installer et configurer l'API Django REST.

## Table des matières
**Prérequis**  
**Installation**  
**Exécution**  
**Utilisation**  

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

- Profile/[profileID] : http://127.0.0.1:8000/profile/[profileID]  
  methode GET : permet de lister les informations de l'utilisateur  
  methode PUT : permet de mettre à jour toutes les informations de l'utilisateur (owner/admin seulement)  
  methode PATCH : permet de mettre à jour certaines informations de l'utilisateur (owner/admin seulement)  
  methode DELETE : permet de supprimer l'utilisateur (owner/admin seulement)  

- Project : http://127.0.0.1:8000/project/  
  methode GET : permet d'accéder à la liste des projets (admin/contributor seulement)  
  methode POST : permet de créer un projet et d'en devenir contributeur.  

- Projet/[projetID] : http://127.0.0.1:8000/project/[projetID]  
  methode GET : permet de voir les informations de l'instance [projetID] ainsi que les informations y étant attachées (admin/contributor seulement)  
  methode PUT : permet de mettre à jour toutes les informations de l'instance projet [projetID] (owner/admin seulement)  
  methode PATCH : permet de mettre à jour certaines informations de l'instance projet [projetID] (owner/admin seulement)  
  methode DELETE : permet de supprimer l'instance projet [projetID] (owner/admin seulement)  

- Projet/[projetID]/issue : http://127.0.0.1:8000/project/[projetID]/issue  
  methode GET : permet de lister les issues attachées à l'instance du projet [projetID] (contributor/admin seulement)  
  methode POST : permet de créer une nouvelle issue attachée à l'instance du projet [projetID] (contributor/admin seulement)  

- Projet/[projetID]/issue/[issueID] : http://127.0.0.1:8000/project/[projetID]/issue/issue[ID]  
  methode PUT : permet de mettre à jour toutes les informations de l'instance issue [issueID] (owner/admin seulement)  
  methode PATCH : permet de mettre à jour certaines informations de l'instance issue [issueID] (owner/admin seulement)  
  methode DELETE : permet de supprimer l'instance de l'issue [issueID] (owner/admin seulement)  

- Projet/[projetID]/issue/[issueID]/comment : http://127.0.0.1:8000/project/[projetID]/issue/[issueID]/comment  
  methode GET : permet de lister les comments attachées à l'instance de l'issue [issueID] (contributor/admin seulement)  
  methode POST : permet de créer une nouvelle issue attachée à l'instance du projet [projetID] (contributor/admin seulement)  

- Projet/[projetID]/Issue/[issueID]/comment/[commentUUID] : http://127.0.0.1:8000/project/[projetID]/Issue/issue[ID]/comment/[commentUUID]  
  methode PUT : permet de mettre à jour toutes les informations de l'instance comment [commentUUID] (owner/admin seulement)  
  methode PATCH : permet de mettre à jour certaines informations de l'instance comment [commentUUID] (owner/admin seulement)  
  methode DELETE : permet de supprimer l'instance de l'issue [commentUUID] (owner/admin seulement)  
  
- project-contribution: http://127.0.0.1:8000/project-contribution/  
  methode GET : permet d'accéder à la liste des projets et de voir si on y contribue déja ou non.  
  methode POST : permet de contribuer à un projet.

- project-contribution/[contributionID] http://127.0.0.1:8000/project-contribution/[contributionID]  
  methode DELETE : permet de supprimer sa contribution au projet.
