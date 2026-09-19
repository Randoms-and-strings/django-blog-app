#### Project overview
Django blog application with user accounts, post creation/editing, and full‑text search powered by **Elasticsearch**. Includes user profile management, image handling for profile pictures, and basic test coverage for user flows. The project is containerized and includes Dockerfiles for the Django app, Elasticsearch, and an Nginx webserver.

---

#### Tech stack
- **Backend:** Python, Django  
- **Search:** Elasticsearch (7.x client compatibility)  
- **Database:** PostgreSQL (used in compose snippet)  
- **Webserver / Reverse proxy:** Nginx  
- **Containerization:** Docker, docker‑compose  
- **Testing:** Django `TestCase` (pytest optional)  
- **Other:** Django auth, Django forms, Django signals

---

#### Quickstart (local, repo root or inside this folder)
Use the included `compose.yml` to build and run the blog stack (Postgres, Elasticsearch, Django, Nginx).

1. Copy or create an `.env` file in the repo root with required variables (example below).  
2. Build and start services:
```bash
docker compose -f compose.yml up --build
```
3. Access the site:
- Django app: `http://localhost:8000`  
- Nginx (if configured): `http://localhost:8080`  
- Elasticsearch: `http://localhost:9200`

Stop services:
```bash
docker compose -f compose.yml down
```

---

#### Required environment variables (example)
Create a `.env` file and set these values (do not commit secrets):
```env
POSTGRES_USER=<postgres-user>
POSTGRES_PASSWORD=<postgres-password>
POSTGRES_DB=testing-db

ELASTIC_PORT=9200
ELASTIC_URL=http://elasticsearch:9200
ELASTIC_PASSWORD=<elastic-password>

DJANGO_SECRET_KEY=<django-secret-key>
DJANGO_DEBUG=1
```
Adjust names/values to match your deployment and `compose.yml` settings.

---

#### Important endpoints and routes
- **Home / posts listing:** `/`  
- **Post detail:** `/<post_id>`  
- **Create post:** `/create_post/` (login required)  
- **Edit post:** `/edit_post/<post_id>/` (author only)  
- **Delete post:** `/delete_post/<post_id>/` (author only)  
- **Search:** `/search_blogs/` (POST form with `keyword` and `search_by`)  
- **User routes:** register, login, logout, profile, edit profile (see `users_details` urls)

Healthcheck example (container internal): the compose uses a `user/create_new` style check for other services; for this app you can use a simple GET to `/` or a custom health endpoint if you add one.

---

#### Elasticsearch integration notes
- The app uses the Python Elasticsearch client and expects an `ELASTIC_URL` environment variable.  
- Index name used in code: `blog_posts`. The app creates the index if it does not exist and indexes documents on post creation.  
- Search queries use `match` and `multi_match` across `title`, `author`, and `content`. Consider adding explicit mappings and analyzers for better relevance and language handling.  
- The Dockerfile pins `elasticsearch==7.17.13` compatibility; ensure the running Elasticsearch version matches the client.

---

#### Running tests
The repo includes Django `TestCase` tests for user registration, login, profile, and basic flows. Run tests inside the Django container or locally with the project virtualenv:
```bash
# inside container or virtualenv
python manage.py test
```
Add `pytest` and test fixtures if you prefer a pytest workflow.

---

#### Docker / deployment notes
- **Django Dockerfile** runs migrations on container start (`makemigrations` and `migrate`) and starts the development server. For production, replace `runserver` with a WSGI server (Gunicorn/Uvicorn) behind Nginx.  
- **Nginx** is provided to serve static files and proxy to the Django app; `nginx.conf` is included.  
- **Elasticsearch** container is configured as single‑node with `xpack.security.enabled: 'true'` in the compose snippet; set `ELASTIC_PASSWORD` and other envs accordingly.  
- **Volumes**: Postgres and Elasticsearch volumes are declared in `compose.yml` to persist data.

---

#### Contributing & license
- Fork → branch → tests → PR.  
- Add `CONTRIBUTING.md` and a `LICENSE` file (MIT recommended for personal projects).

---
