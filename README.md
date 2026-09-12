# Briefly

**Read less. Know more.**

AI-powered news article summarization platform built on a fine-tuned T5-small model trained on CNN-DailyMail.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Framer Motion, Zustand |
| **Backend** | FastAPI, Python 3.11, PyTorch, HuggingFace Transformers |
| **Database** | SQLite (dev) / PostgreSQL (prod) via SQLAlchemy async |
| **Model** | Fine-tuned T5-small (60M params), CNN/DailyMail dataset |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- The `fine_tuned_t5_small.zip` model file (already extracted to `backend/model/`)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. API docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

### Docker

```bash
docker-compose up --build
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # REST endpoints (summarize, auth, history)
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Business logic (model, NLP, auth, extraction)
│   │   ├── config.py     # App settings
│   │   ├── database.py   # Async SQLAlchemy setup
│   │   └── main.py       # FastAPI app entry point
│   └── model/            # Extracted T5 model files
├── frontend/
│   └── src/
│       ├── app/          # Next.js App Router pages
│       ├── components/   # React components
│       ├── lib/          # API client, utilities
│       └── store/        # Zustand state stores
├── docker-compose.yml
└── README.md
```

## Features

- **Multiple input methods**: Paste text, URL, or upload PDF/DOCX/TXT
- **Configurable summaries**: Short, medium, or detailed length
- **Smart analytics**: Sentiment, keywords, readability, confidence scores
- **Key points extraction**: Auto-extracted bullet points
- **History dashboard**: Search, favorite, and export past summaries
- **Authentication**: Email/password signup and login
- **Dark/light mode**: Elegant theme switching
- **Responsive**: Fully mobile-optimized

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/summarize/text` | Summarize raw text |
| `POST` | `/api/summarize/url` | Extract + summarize from URL |
| `POST` | `/api/summarize/file` | Upload file + summarize |
| `POST` | `/api/auth/signup` | Create account |
| `POST` | `/api/auth/login` | Login |
| `GET` | `/api/history` | List past summaries |
| `GET` | `/api/health` | Health check |


