# MLOPS_Final_Bilgnuer_Xuan_thu_Jiayin

## Auteur

* Bilgenur OZDEMIR
* Jiayin CHEN
* Xuan Thu NGUYEN

## Architecture du projet
Ce projet repose sur une architecture modulaire composée de plusieurs services interconnectés, qui facilitent le traitement des données, la surveillance et la visualisation des performances. Les principaux composants sont :

1. ***ml-app*** : Une application Flask utilisée pour le traitement et la prédiction de données via un modèle de machine learning (TensorFlow/Keras). Elle expose une API RESTful permettant aux utilisateurs de soumettre des données pour des prédictions en temps réel.
2. ***Prometheus*** : Utilisé pour surveiller les métriques des services. Prometheus collecte les métriques de performance des conteneurs et des services et les envoie vers Grafana pour une visualisation en temps réel.
3. ***Grafana*** : Utilisé pour la visualisation des métriques et la création de tableaux de bord interactifs. Grafana se connecte à Prometheus pour récupérer les données et fournir des graphiques et des alertes visuelles.
4. ***Terraform*** : Outil d'infrastructure en tant que code (IaC) utilisé pour provisionner et gérer les ressources cloud, notamment sur GCP.
5. ***MLflow*** : Outil de gestion des expériences en machine learning qui suit et organise les modèles, les paramètres, les métriques et les artefacts liés à chaque entraînement du modèle.
6. ***Docker et Docker Compose*** : Docker est utilisé pour containeriser les différents services de l'application, simplifiant ainsi le déploiement et la gestion des environnements. Docker Compose orchestre l'exécution de plusieurs services dans un même réseau.
7. ***Ansible*** : Utilisé pour la configuration des serveurs et l'automatisation des tâches répétitives, facilitant ainsi l'intégration continue et la gestion des environnements.

## Choix techniques

* ***Flask*** : Framework léger pour créer des API web en Python. Il est utilisé pour fournir une interface pour l'inférence du modèle de machine learning.
* ***TensorFlow/Keras*** : Bibliothèque de deep learning pour charger et exécuter le modèle de machine learning préalablement entraîné.
* ***Prometheus*** : Outil de collecte de métriques qui interroge les services pour récupérer des données relatives à leur performance.
* ***Grafana*** : Plateforme de visualisation de données qui permet de créer des dashboards interactifs pour surveiller les métriques collectées par Prometheus.
* ***Docker*** : Outil de virtualisation légère qui permet de créer, déployer et exécuter des applications dans des conteneurs isolés.
* ***MLflow*** : Outil de gestion des expériences en machine learning qui facilite le suivi des modèles, des hyperparamètres et des métriques.
* ***GCP*** : Plateforme cloud utilisée pour déployer des ressources et gérer l'infrastructure en tant que code via Terraform.

## Installation et guide d'exécution
### Prérequis
* Docker et Docker Compose installés sur votre machine.
* Compte Google Cloud Platform (GCP) avec les autorisations nécessaires pour provisionner des ressources.
* Terraform et Ansible configurés pour interagir avec GCP.

### Installation

1. Clonez le répertoire du projet :

```bash

git clone https://github.com/JYccccccc/MLOPS_Final_Bilgenur_Xuan_thu_Jiayin.git
cd MLOPS_Final_Bilgenur_Xuan_thu_Jiayin
```

2. Construisez les images Docker pour tous les services définis dans docker-compose.yml :

```bash

docker-compose build
```

3. Si vous prévoyez de déployer l'infrastructure sur GCP, initialisez Terraform et appliquez les configurations :

```bash

cd Iac
terraform init
terraform apply
```

### Exécution
1. Lancez les services avec Docker Compose :

```bash

docker-compose up -d
```
2.Accédez aux services via les URLs suivantes :

* ***ml-app (Flask)*** : http://localhost:5000 pour soumettre des prédictions via l'API.
* ***Prometheus*** : http://localhost:9090 pour surveiller les métriques collectées par Prometheus.
* ***Grafana*** : http://localhost:3000 pour visualiser les métriques dans des dashboards interactifs.
Vous pouvez également configurer l'accès à l'interface de Grafana en ajoutant un utilisateur dans grafana.ini si nécessaire.

## Utilisation de MLflow
* ***Suivi des expériences*** : MLflow est utilisé pour enregistrer les modèles, les paramètres et les métriques des entraînements. Vous pouvez consulter les résultats des entraînements dans le répertoire ```mlruns``` ou via l'interface Web de MLflow, en accédant à ```http://localhost:5000```.