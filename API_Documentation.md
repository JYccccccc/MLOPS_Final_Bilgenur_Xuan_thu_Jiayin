# Documentation API

## Endpoints
1. POST /predict
* Description : Prédit une classe basée sur une image donnée. L'image est envoyée dans le corps de la requête et le modèle retourne une prédiction sous forme de classe et de probabilité.
* URL : ```/predict```
* Méthode HTTP : POST
* Content-Type : ```application/json```

### Exemple de requête

```json
{
  "image": "chemin/vers/image.png"
}
```
### Exemple de réponse

```json
{
  "prediction": 7,
  "probabilities": [0.1, 0.05, 0.0, 0.02, 0.03, 0.1, 0.1, 0.5, 0.05, 0.05]
}
```
2. GET /metrics
* Description : Retourne les métriques pour la surveillance avec Prometheus. Les métriques sont envoyées sous un format compatible avec Prometheus, permettant leur collecte et visualisation en temps réel.
* URL : ```/metrics```
* Méthode HTTP : GET

### Exemple de réponse
Les métriques sont renvoyées en texte brut, compatibles avec Prometheus.

3. GET /health
* Description : Vérifie si le service est opérationnel. Retourne un statut indiquant si le service est en ligne ou s'il rencontre des problèmes.
* URL : ```/health```
* Méthode HTTP : GET

### Exemple de réponse
```json
{
  "status": "OK"
}
```