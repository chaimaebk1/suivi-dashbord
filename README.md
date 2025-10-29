# Suivi Dashboard Job

Ce projet fournit un script Python léger permettant de télécharger un fichier Excel de suivi depuis OneDrive, de transformer les données en table linéaire, puis de générer un tableau de bord HTML statique et une exportation Excel nettoyée. Le job est conçu pour tourner sur un serveur (ou localement) et être planifié via `cron`. Aucune application web ou base de données n'est nécessaire : tout se résume à un script qui lit, transforme et écrit des fichiers.

## Installation et exécution locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.yaml config.local.yaml  # ou modifier config.yaml directement
python src/main.py
```

## Lien OneDrive direct-download

1. Depuis OneDrive/SharePoint, créer un lien de partage en lecture seule.
2. Copier le lien généré.
3. Ajouter `?download=1` à la fin de l'URL pour forcer le téléchargement direct.
4. Mettre cette URL dans `config.yaml` sous `source.onedrive_direct_url`.

## Déploiement sur VPS

Assurez-vous que le répertoire `/var/www/suivi` est servi par Nginx (ou un autre serveur web). Le script y écrira :

- `dashboard.html` : tableau de bord Plotly statique.
- `export_clean.xlsx` : table linéaire nettoyée.

## Planification via cron

Exemple d'entrée cron pour lancer le job tous les jours à 6h :

```
0 6 * * * /usr/bin/python3 /path/to/repo/src/main.py >> /var/log/suivi.log 2>&1
```

## Portée

Ce dépôt n'inclut **pas** d'application Dash/Flask, de base de données ni de mécanisme d'authentification. Le script est autonome et pensé pour être simple à maintenir.