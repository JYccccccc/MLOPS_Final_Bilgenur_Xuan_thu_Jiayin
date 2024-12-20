# MLOPS_Final_Bilgnuer_Xuan_thu_Jiayin
Ce projet met en place un pipeline MLOps complet intégrant des pratiques DevOps et des outils spécifiquement conçus pour le machine learning. Il utilise des technologies telles que Docker, Terraform, Ansible, GCP, MLflow, GitHub Actions pour l'automatisation, et Prometheus + Grafana pour la surveillance.
## Auteur

* Bilgenur OZDEMIR
* Jiayin CHEN
* Xuan Thu NGUYEN

## Table des matières
1. [Prérequis](#jump1)
2. [Architecture du projet](#jump2)
3. [Présentation projet ML](#jump3)
4. [Installation](#jump4)
5. [Utilisation](#jump5)
6. [API Documentation](#jump6)
7. [CI/CD avec GitHub Actions](#jump7)
8. [Surveillance avec Prometheus et Grafana](#jump8)
9. [Gestion des erreurs](#jump9)
10. [Sécurité](#jump10)
11. [Contribution](#jump11)
12. [Licence](#jump12)

## <span id="jump1">Prérequis</span>
Avant de démarrer avec ce projet, vous devez vous assurer que les éléments suivants sont installés sur votre machine ou dans votre environnement cloud :

* Docker : Pour la containerisation des applications et des services.
* Terraform : Pour la gestion de l'infrastructure comme code.
* Ansible : Pour la configuration et la gestion des serveurs.
* GCP (Google Cloud Platform) : Pour déployer l'infrastructure dans le cloud (alternative à AWS ou Azure).
* MLflow : Pour la gestion des modèles de machine learning.
* GitHub Actions : Pour la CI/CD.
* Prometheus et Grafana : Pour la collecte et la visualisation des métriques.
### Versions recommandées :
* Docker : 20.x ou supérieur
* Terraform : 1.0 ou supérieur
* Ansible : 2.9 ou supérieur
* GCP SDK : dernière version
* Python : 3.8 ou supérieur
* MLflow : 1.20 ou supérieur
  

## <span id="jump2">Architecture du projet</span>
Le projet est structuré autour de plusieurs composants clés qui interagissent pour assurer un flux MLOps fluide et automatisé :

### 1. ***Docker*** :
Tous les services sont encapsulés dans des conteneurs Docker pour assurer la portabilité et la reproductibilité des environnements.

* ***ml-app*** : Application Flask pour exposer un API de prédiction ML.
* ***Prometheus*** : Service de surveillance qui collecte des métriques de l'infrastructure.
* ***Grafana*** : Interface de visualisation des métriques collectées par Prometheus.
* ***MLflow Tracking Server*** : Serveur de suivi pour enregistrer les métadonnées des modèles et des expériences de machine learning.
* ***Model Server*** : Serveur qui héberge le modèle de machine learning pour les prédictions.
### 2. ***Terraform & Ansible*** :
* ***Terraform*** est utilisé pour déployer l'infrastructure sur GCP, y compris les ressources comme les machines virtuelles, le stockage, etc.
* ***Ansible*** est utilisé pour la configuration des serveurs, l'installation des dépendances, et la gestion des déploiements des applications.
### 3. ***CI/CD avec GitHub Actions*** :
Les workflows GitHub Actions automatisent les processus suivants :

* ***Test unitaire*** : Lancer des tests sur le code source.
* ***Build Docker images*** : Créer et pousser des images Docker vers un registre.
* ***Déploiement automatique*** : Déployer les images Docker sur l'infrastructure cloud (GCP).
### 4. ***Surveillance avec Prometheus et Grafana*** :
* ***Prometheus*** est configuré pour collecter des métriques comme les requêtes API, les erreurs, la latence, l'utilisation des ressources, etc.
* ***Grafana*** est utilisé pour créer des tableaux de bord interactifs permettant de visualiser ces métriques en temps réel.
## <span id="jump3">Présentation projet ML</span>
Pour plus de détails sur l'API de prédiction, veuillez consulter le ficher [Mnist.ipynb](./Mnist.ipynb).
## <span id="jump4">Installation</span>
### Cloner le repository
```bash
git clone https://github.com/JYccccccc/MLOPS_Final_Bilgenur_Xuan_thu_Jiayin.git
cd MLOPS_Final_Bilgenur_Xuan_thu_Jiayin
```
### Prérequis d'environnement
1. Installez [Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/).
2. Installez [Terraform](https://developer.hashicorp.com/terraform/install).
3. Installez [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible).
4. Configurez un compte GCP et installez [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk?hl=fr).
5. Configurez [MLflow](https://mlflow.org/docs/latest/getting-started/index.html).
6. Configurez [Prometheus](https://prometheus.io/docs/prometheus/latest/getting_started/) et [Grafana](https://grafana.com/) pour la surveillance.
### Déploiement de l'infrastructure
1. Configurer Terraform : Personnalisez votre fichier terraform.tfvars avec vos identifiants GCP.

2. Appliquer Terraform : Exécutez les commandes suivantes pour déployer l'infrastructure :

```bash

terraform init
terraform apply
```
3. Configurer Ansible : Assurez-vous que les hôtes et les configurations Ansible sont correctement définis dans ansible/hosts et ansible/config.yml.

4. Exécuter Ansible : Déployez les configurations sur les machines virtuelles déployées par Terraform :

```bash

ansible-playbook -i ansible/hosts ansible/setup.yml
```
### Démarrer les services Docker
1. Lancer les conteneurs Docker :
```bash

docker-compose up --build
```
Cela va démarrer les services définis dans votre fichier ```docker-compose.yml```.

## <span id="jump5">Utilisation</span>
### Lancer l'API de prédiction
Une fois le service déployé, vous pouvez tester l'API de prédiction en envoyant une image via une requête ```POST``` à l'endpoint ```/predict```.

#### Exemple de requête via ```curl``` :

```bash

curl -X POST "http://localhost:5000/predict" -H "Content-Type: application/json" -d '{"image": "chemin/vers/limage.png"}'
```
### Accéder à MLflow
Le serveur MLflow est accessible à l'adresse suivante : ```http://localhost:5001```. Vous pouvez y consulter les expériences et les modèles.

## <span id="jump6">Documentation de l'API</span>
Pour plus de détails sur l'API de prédiction, veuillez consulter l'[API Documentation](./API_Documentation.md).

## <span id="jump7">CI/CD avec GitHub Actions</span>
Le projet utilise des ***workflows GitHub Actions*** pour automatiser le processus de développement et de déploiement.

### Structure des workflows
1.***CI - Tests et Build Docker*** : Le workflow CI s'exécute à chaque push sur la branche principale et effectue les étapes suivantes :

* Exécute les tests unitaires.
* Construit et publie les images Docker.
2. ***CD - Déploiement Automatique :*** Après le passage des tests, le workflow CD déploie automatiquement les images Docker dans l'infrastructure cloud (GCP).

Exemple de fichier de workflow GitHub Actions (```.github/workflows/main.yml```) :

```yaml

name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest

    - name: Build Docker image
      run: |
        docker build -t ml-api .
```
## <span id="jump8">Surveillance avec Prometheus et Grafana</span>
### Prometheus
Prometheus est utilisé pour collecter des métriques depuis l'API, le serveur MLflow, et les autres services.

### Grafana
Grafana est configuré pour afficher ces métriques dans des tableaux de bord interactifs et utiles.

Accédez à Grafana via ```http://localhost:3000```.
Utilisez le tableau de bord par défaut pour surveiller les métriques.
## <span id="jump9">Gestion des erreurs</span>
L'API et les services sont conçus pour gérer les erreurs de manière robuste. En cas d'erreur, une réponse détaillée est renvoyée, comprenant un message d'erreur et un code d'état HTTP.

## <span id="jump10">Sécurité</span>
### Authentification
L'API utilise ***JWT (JSON Web Tokens)*** pour l'authentification et la gestion des utilisateurs.

### Sécurisation des Secrets
Les secrets et clés sont gérés via ***AWS Secrets Manager*** ou un service équivalent sur GCP.

## <span id="jump11">Contribution</span>
Nous accueillons les contributions de la communauté ! Pour contribuer :

1. Fork ce repository.
2. Crée une branche pour ta fonctionnalité (```git checkout -b feature/ma-nouvelle-fonctionnalité```).
3. Commit tes changements (```git commit -am 'Ajoute une nouvelle fonctionnalité'```).
4. Push à ta branche (```git push origin feature/ma-nouvelle-fonctionnalité```).
5. Ouvre une Pull Request.
## <span id="jump12">Licence</span>
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.