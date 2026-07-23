# XComic — Personal Email Marketer

An advanced, premium cold email marketing and visual email campaign automation application. It features a FastAPI backend, SQLAlchemy database schema, and a self-contained modern HTML5/JS single-page frontend.

---

## Technical Stack
- **Frontend**: HTML5, Vanilla JS, CSS Custom Variables (Premium Dark/Glassmorphism design).
- **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy (SQLite database by default).
- **Deployment**: cPanel hosting compatibility via Passenger WSGI (`passenger_wsgi.py`) and FTP uploads.
- **AI Integrations**: Gemini API and Groq API.

---

## Getting Started

### 1. Prerequisites
Make sure you have Python 3.8+ installed on your computer.

### 2. Setup Local Environment
1. Clone the repository to your local computer.
2. Install the Python dependencies:
   ```bash
   pip install -r xcomic_backend/requirements.txt
   ```
3. Set up the local `.env` configuration file in the `xcomic_backend/` folder (you can copy `.env.example` as a starting point).

---

## Project Control & Deployment

This project includes a unified control script `deploy.py` located at the root of the repository. It streamlines running the application locally, committing/syncing changes to Git, and uploading files directly to your live FTP server.

### Run Local Development Server
To launch the FastAPI server locally on port 8000:
```bash
python deploy.py --run
```
The server will start at `http://127.0.0.1:8000`.

### Sync Changes with Git
To automatically stage all your local changes, commit them with a message, and push to GitHub:
```bash
python deploy.py --git -m "Description of changes"
```

### Deploy to Live Server (FTP)
To upload your files to the live cPanel hosting server via FTP:
- **Deploy Frontend only** (index.html, auth.html, assets/*):
  ```bash
  python deploy.py --deploy frontend
  ```
- **Deploy Backend only** (Python APIs, excluding databases/credentials) and trigger an automatic application restart:
  ```bash
  python deploy.py --deploy backend
  ```
- **Deploy Both (Frontend & Backend)**:
  ```bash
  python deploy.py --deploy all
  ```

---

## Directory Structure
- 📁 `xcomic.xyz/` — Frontend source files (HTML, CSS, JS, assets).
- 📁 `xcomic_backend/` — FastAPI backend endpoints, models, mail service integrations, and WSGI entry point.
- 📄 `deploy.py` — Unified automation manager.
