# [Projet flask](https://github.com/LucasTHOMAS18/Projet-Flask)
Groupe: Lucas THOMAS, Yasin KESKIN

## Guide d'utilisation :
Installation des dépendances :
```bash
pip install -r requirements.txt 
```

Chargement de la base de données :
```bash
flask load_db src/data/data.yml
```

Création d'un utilisateur :
```bash
flask new_user <speudo> <mdp>
```

## Fonctionalités :
* Consultation des livres depuis la page d'accueil
* Consultation des auteurs
* Connexion à un compte
  * Les redirections lors de la connexion/déconnexion sont prises en compte
* Ajout de livres à une liste de favoris
* Recherche avancée
  * Par titre
  * Par auteur
  * Tri par ordre alphabétique
  * Tri par prix
* Système de notation
* Système de commentaires
* Intégration complète de Bootstrap
* Édition des auteurs
