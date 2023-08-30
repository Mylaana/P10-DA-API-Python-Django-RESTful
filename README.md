# P10-DA-API-Python-Django-RESTful
Création d'une API sécurisée RESTful avec Django REST framework


- Seuls les contributeurs d’un projet peuvent accéder à ce dernier. Seuls les
contributeurs peuvent accéder aux ressources qui référencent un projet (l’issue
et le comment).


- Lors de la création de l’issue, le contributeur doit pouvoir la nommer et ajouter
une description. Il doit aussi pouvoir assigner l’issue à un autre contributeur s’il
le souhaite. Attention, seuls les contributeurs du projet correspondant à l’issue
sont sélectionnables.


- Enfin, un identifiant unique de type uuid est automatiquement généré. Ce
dernier permet de mieux référencer le comment.


-L’auteur d’une ressource peut modifier ou supprimer cette ressource. Les autres
utilisateurs ne peuvent que lire la ressource.

- Un système de pagination est implémenté pour le listage des ressources.


questions mentorat : 
comment capter l'id contributor dans la permission