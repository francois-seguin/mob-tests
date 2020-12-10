# DISCUSSION

## qu'est-ce qu'on veut tester ?

* toutes les règles métier
* les branchements (interactions entre API et métier, métier et DB, etc...
  )
* routes de maj de modèles (création, édition, suppression)
* accès aux routes (permissions)
* dans l'idée d'une app déployée: écrire un test afin de reproduire un bug (comportement inattendu)
* ne pas oublier les cas limites
* efficacité (accès DB)
* ~~intégrité des données (rejoint la règle métier)~~


## qu'est-ce que je ne veux *pas* tester

* tester des comportements de modules/libs externes


### définissons des typologies de tests

* test unitaire
tester un comportement/une fonction, pas une route - en isolation de code externe ? (pas résolu: mocker la DB)
  
* test fonctionnel
vérifier un comportement métier qui utilise plusieurs fonctions

* test d'intégration
hors browser, faire une requête http (ex: ajout d'article de blog via POST)

* test end-to-end (comme un utilisateur)
depuis le browser (selenium etc) à la DB au browser


## comment ?

Exemple avec edit_post()
nous avons écrit des tests d'intégration !


## combien ?


