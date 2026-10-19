# AI Business Assistant

Analyse automatique de rapports d'intervention grâce à l'IA générative.

Un technicien colle son rapport en texte libre. L'application en extrait
une fiche structurée (client, ville, type, priorité, durée, problème,
action), la valide, l'enregistre en base et l'affiche dans un historique.

Le modèle d'IA tourne **en local avec Ollama** : les données ne quittent
pas l'infrastructure de l'entreprise.

## Fonctionnalités

- Analyse d'un rapport en texte libre par un LLM local (Ollama, `qwen3.5:4b`)
- Extraction d'une fiche d'intervention structurée en JSON
- Double validation de la réponse de l'IA : JSON valide, puis schéma
  Pydantic (priorité limitée à `normale` / `élevée` / `urgente`, durée ≥ 0)
- Contraintes répétées en base (`CHECK`) dans `init.sql`
- Enregistrement dans PostgreSQL avec des requêtes paramétrées
- Historique paginé et détail de chaque intervention
- Logs à chaque étape, route `/health`, erreurs HTTP explicites (404, 500)

## Architecture

```
React (Vite)  →  FastAPI  →  Ollama (qwen3.5:4b)
                    │
                    └──→  PostgreSQL
```

| Fichier | Rôle |
|---|---|
| `backend/api.py` | Routes FastAPI et construction du prompt |
| `backend/ai_service.py` | Appel au modèle via Ollama |
| `backend/utils.py` | Conversion JSON et validation de la réponse de l'IA |
| `backend/models.py` | Schémas Pydantic (entrée, sortie IA, réponse API) |
| `backend/repository.py` | Accès aux données (SQL paramétré) |
| `backend/database.py` | Connexion PostgreSQL (`DATABASE_URL`) |
| `backend/init.sql` | Création de la table au premier démarrage |
| `backend/import_json.py` | Import ponctuel d'interventions depuis un fichier JSON |
| `frontend/` | Interface React 19 + Vite |

## API

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | État de l'API |
| POST | `/analyser` | Analyse un rapport `{ "rapport": "..." }` |
| GET | `/historique` | Liste des interventions |
| GET | `/historique/{id}` | Détail d'une intervention (404 si absente) |

Documentation interactive (Swagger) : http://localhost:8000/docs

## Installation

### Prérequis

- Docker Desktop
- Ollama, avec le modèle : `ollama pull qwen3.5:4b`
- Node.js (pour le frontend)

### 1. Configuration

Copier `.env.example` en `.env`. Par défaut, l'API (dans Docker) joint
Ollama installé sur la machine hôte :

```
OLLAMA_HOST=http://host.docker.internal:11434
```

### 2. Backend et base de données

```bash
docker compose up --build
```

La table `interventions` est créée automatiquement au premier démarrage
(`backend/init.sql`).

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Application : http://localhost:5173

## Exemple

Rapport envoyé :

> Passage ce matin chez la mairie de Cavaillon suite à une baisse de
> pression signalée rue de la République. Détection acoustique : fuite
> sur canalisation fonte, réparée avec un collier. 1h30 sur place.
> À surveiller, risque de récidive.

Fiche obtenue : client, ville, type d'intervention, priorité, durée en
minutes, problème et action réalisée, enregistrés puis visibles dans
l'historique.

## Améliorations prévues

- Imposer le format JSON à Ollama (schéma Pydantic), ajouter un prompt
  système et une température à 0
- Timeout et nouvelles tentatives sur l'appel au modèle
- Code HTTP 502 pour les erreurs du service d'IA
- Identifiants de base dans le `.env`, healthcheck PostgreSQL
- Tests automatisés (pytest avec un LLM simulé)
- Validation humaine avant enregistrement et contrôle anti-hallucination
- Choix du modèle par variable d'environnement (local ou cloud)
