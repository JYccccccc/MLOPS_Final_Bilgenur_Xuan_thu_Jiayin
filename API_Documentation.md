# Documentation API

Cette API permet de prédire des valeurs en utilisant un modèle de machine learning, de gérer l'état du modèle, et de fournir des données de suivi via des métriques collectées par Prometheus. Elle permet également de gérer l'entraînement du modèle.

## Table des Matières
1. [POST /predict](#jump1)
2. [GET /metrics](#jump2)
3. [GET /health](#jump3)
4. [GET /model/info](#jump4)
5. [POST /train](#jump5)
6. [GET /logs](#jump6)
7. [Gestion des erreurs](#jump7)
8. [POST /user](#jump8)
9. [POST /model/deploy](#jump9)
10. [Gestion des erreurs](#jump10)
11. [Sécurité et authentification](#jump11)

## Endpoints
### <span id="jump1">1.POST /predict<span>
* Description : Ce point de terminaison permet d'envoyer une image et de recevoir une prédiction basée sur un modèle de machine learning pré-entraîné. Le modèle effectuera la classification de l'image et renverra les catégories probables et leurs probabilités respectives.
* URL : ```/predict```
* Méthode HTTP : ```POST```
* Content-Type : ```application/json```
* Paramètres de la requête :
    * ```image``` : Chemin relatif ou URL de l'image à prédire. L'image peut être une image locale ou une URL pointant vers une image disponible en ligne.

#### Exemple de requête

```json
{
  "image": "chemin/vers/image.png"
}
```
#### Exemple de réponse

```json
{
  "prediction": 7,
  "probabilities": [0.1, 0.05, 0.0, 0.02, 0.03, 0.1, 0.1, 0.5, 0.05, 0.05]
}
```
* ***prediction*** : Le label (ou classe) prédite pour l'image (par exemple, le chiffre 7).
* ***probabilities*** : Un tableau contenant les probabilités associées à chaque classe possible (par exemple, de ```0``` à ```9``` pour un modèle de classification de chiffres manuscrits).

#### Réponse d'erreur (si l'image n'est pas valide) :
```json
{
  "error": "Chemin d'image invalide",
  "message": "Le fichier ou l'URL de l'image fourni est incorrect ou inaccessible."
}
```
* ***error*** : Type d'erreur (par exemple, "Chemin d'image invalide").
* ***message*** : Description détaillée de l'erreur, utile pour diagnostiquer le problème.
----

### <span id="jump2">2. GET /metrics<span>
* ***Description*** : Ce point de terminaison fournit les données de métriques collectées par Prometheus, permettant de suivre l'état de l'infrastructure, des requêtes API et des performances du modèle.
* ***URL*** : ```/metrics```
* ***Méthode HTTP*** : ```GET```
* ***Format de réponse***: Le contenu est renvoyé au format texte brut, comme attendu par Prometheus.

#### Exemple de réponse
```bash
# HELP api_requests_total Nombre total de requêtes API
# TYPE api_requests_total counter
api_requests_total{method="GET"} 1027
api_requests_total{method="POST"} 735
# HELP api_request_duration_seconds Durée de la requête API en secondes
# TYPE histogramme api_request_duration_seconds
api_request_duration_seconds_bucket{le="0.1"} 532
api_request_duration_seconds_bucket{le="0.2"} 902
api_request_duration_seconds_bucket{le="0.5"} 1047
api_request_duration_seconds_bucket{le="1.0"} 1049
api_request_duration_seconds_bucket{le="+Inf"} 1049
api_request_duration_seconds_sum 45.7
api_request_duration_seconds_count 1049
```
Les métriques incluent :

* ***api_requests_total*** : Nombre total de requêtes, détaillant le nombre de requêtes GET et POST.
* ***api_request_duration_seconds*** : Distribution des durées de réponse des requêtes API, par intervalles de temps.
---

### <span id="jump3">3. GET /health<span>
* Description :  Vérifie si l'API est en état de fonctionnement. Ce point de terminaison renvoie un statut ```OK``` si l'API est opérationnelle, sinon un message d'erreur.
* URL : ```/health```
* Méthode HTTP : ```GET```

#### Exemple de réponse (si l'API fonctionne normalement):
```json
{
  "status": "OK"
}
```
* ***status*** : "OK" indique que le service est opérationnel.

#### Réponse d'erreur (si l'API est hors ligne) :
```json
{
  "status": "ERROR",
  "message": "Le service est actuellement hors ligne"
}
```
* ***status*** : "ERROR" indique que le service n'est pas disponible.
* ***message*** ： Fournit des détails sur la panne ou l'indisponibilité du service.
------
### <span id="jump4">4. GET /model/info<span>
* ***Description*** : Retourne des informations détaillées sur le modèle de machine learning actuellement déployé, y compris sa version, ses performances et les paramètres utilisés pour son entraînement.

* ***URL*** : ```/model/info```

* ***Méthode*** : ```GET```

#### Exemple de réponse :
```json
{
  "model_name": "modelMnist1",
  "version": "v1.0",
  "accuracy": 0.98,
  "loss": 0.02,
  "training_params": {
    "batch_size": 32,
    "epochs": 10,
    "optimizer": "adam"
  }
}
```
* ***model_name*** : Nom du modèle (exemple : modelMnist1).
* ***version*** : Version du modèle (exemple : v1.0).
* ***accuracy*** : Précision du modèle (0.98 signifie que 98% des prédictions sont correctes).
* ***loss*** : Valeur de la fonction de perte, mesurant l'erreur du modèle pendant l'entraînement.
* ***training_params*** : Paramètres d'entraînement utilisés pour *entraîner le modèle, comme la taille du lot (batch_size), le nombre d'époques (epochs), et l'optimiseur (optimizer).
---
### <span id='jump5'>5.POST /train</span>
* ***Description*** : Démarre un nouvel entraînement pour le modèle de machine learning. Cette requête permet de redémarrer l'entraînement avec de nouveaux paramètres.

* ***URL*** : ```/train```

* ***Méthode*** : ```POST```

* ***Paramètres de la requête*** :

 * ```batch_size``` : Taille du lot pour l'entraînement (par défaut : 32).
 * ```epochs``` : Nombre d'époques d'entraînement (par défaut : 10).
 * ```optimizer``` : Algorithme d'optimisation utilisé (par défaut : "adam").

#### Exemple de requête :
```json
{
  "batch_size": 64,
  "epochs": 20,
  "optimizer": "sgd"
}
```
#### Exemple de réponse :
```json
{
  "status": "Entraînement démarré",
  "message": "L'entraînement a démarré avec batch_size=64, epochs=20, optimizer='sgd'."
}
```
---
### <span id='jump6'>6. GET /logs<span>
* ***Description*** : Récupère les journaux des entraînements, permettant de suivre la progression de l'entraînement et les performances du modèle.

* ***URL*** : ```/logs```

* ***Méthode*** : ```GET```

#### Exemple de réponse :
```json

{
  "logs": [
    "Epoch 1/10 - Loss: 0.25, Accuracy: 0.89",
    "Epoch 2/10 - Loss: 0.20, Accuracy: 0.91",
    "Epoch 3/10 - Loss: 0.15, Accuracy: 0.92"
  ]
}
```
---

### <span id='jump7'>7. GET /user<span>
* ***Description*** : Récupère les informations de l'utilisateur actuellement connecté.

* ***URL*** : ```/user```

* ***Méthode*** : ```GET```

#### Exemple de réponse :
```json
{
  "user_id": "12345",
  "username": "john_doe",
  "role": "admin",
  "last_login": "2024-12-20T10:00:00Z"
}
```
* ***user_id*** : ID unique de l'utilisateur.
* ***username*** : Nom d'utilisateur.
* ***role*** : Rôle de l'utilisateur (par exemple, "admin", "user").
* ***last_login*** : Dernière date de connexion de l'utilisateur.
---
### <span id="jump8">8. POST /user</span>
* ***Description*** : Permet de créer ou de mettre à jour un utilisateur dans le système.

* ***URL*** : ```/user```

* ***Méthode*** : ```POST```

* ***Content-Type*** : ```application/json```

* ***Paramètres de la requête*** :

    * ```username``` : Nom d'utilisateur (obligatoire).
    * ```password``` : Mot de passe (obligatoire).
    * ```role``` : Rôle de l'utilisateur ("user", "admin").
#### Exemple de requête :
```json

{
  "username": "new_user",
  "password": "securepassword123",
  "role": "user"
}
```
#### Exemple de réponse :
```json

{
  "status": "Utilisateur créé",
  "message": "L'utilisateur 'new_user' a été créé avec succès."
}
```
---
### <span id="jump9">9. POST /model/deploy<span>
* ***Description*** : Permet de déployer une nouvelle version du modèle de machine learning dans l'environnement de production.

* ***URL*** : ```/model/deploy```

* ***Méthode*** : ```POST```

#### Exemple de réponse :
```json
{
  "status": "Déploiement réussi",
  "message": "Le modèle version v2.0 a été déployé avec succès."
}
```
---
### <span id="jump10">Gestion des erreurs<span>
Les erreurs sont renvoyées dans un format JSON standard avec un code d'erreur et un message détaillé pour faciliter le diagnostic.

#### Exemple d'erreur générique :
```json
{
  "error": "BadRequest",
  "message": "Les paramètres fournis ne sont pas valides."
}
```
---
### <span id="jump11">Sécurité et authentification</span>
* Méthode d'authentification : L'authentification est gérée via des tokens JWT (JSON Web Tokens).
* Protection des points de terminaison : Les points de terminaison nécessitant des privilèges (par exemple, ```/train```, ```/user```, ```/model/deploy```) sont protégés par des contrôles d'accès basés sur les rôles (RBAC).
#### Exemple d'en-tête d'authentification :
```text
Authorization: Bearer <votre_token_jwt>
```