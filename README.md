# GenAI RAG Assistant (Google Gemini)

A PDF question-answering assistant. Upload a PDF, ask questions, get
answers grounded in that document. Uses Google Gemini for both embeddings
and chat — no local model server needed.

## Files in this project
```
rag_assistant.py               # the app
requirements.txt               # dependencies
.gitignore                     # keeps secrets/junk out of git
.streamlit/secrets.toml.example  # template for your API key (local use)
README.md                      # this file
```

---

## PART 1 — Run it locally

### Step 1: Install Python
You need Python 3.9 or newer. Check with:
```
python --version
```

### Step 2: Create a project folder and put these files in it
Put `rag_assistant.py`, `requirements.txt`, `.gitignore`, and the
`.streamlit/` folder all in the same directory.

### Step 3: (Recommended) Create a virtual environment
```
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### Step 4: Install dependencies
```
pip install -r requirements.txt
```

### Step 5: Get a Google API key
1. Go to https://aistudio.google.com/apikey
2. Sign in, click "Create API Key", copy it

### Step 6: Give the app your key (pick ONE)
**Option A — quick, no file needed:**
Just run the app (Step 7) and paste the key into the sidebar box each time.

**Option B — don't want to paste it every time:**
Inside `.streamlit/`, rename `secrets.toml.example` to `secrets.toml`, then
open it and replace `paste_your_key_here` with your real key:
```toml
GOOGLE_API_KEY = "AIza...your real key..."
```
The app will now load it automatically — no sidebar typing needed.
This file is already in `.gitignore` so it won't be accidentally uploaded.

### Step 7: Run the app
```
streamlit run rag_assistant.py
```
It opens automatically at `http://localhost:8501`.

### Step 8: Use it
1. Upload a PDF
2. Wait for "Indexed X chunks..." to appear
3. Type a question in the chat box at the bottom

---

## PART 2 — Deploy it publicly (Streamlit Community Cloud, free)

### Step 1: Push your project to GitHub
```
git init
git add .
git commit -m "GenAI RAG Assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
**Important:** because `secrets.toml` is in `.gitignore`, your real API key
will NOT be pushed to GitHub. That's intentional — never commit real keys.

### Step 2: Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch `main`, and set the main file path to
   `rag_assistant.py`
5. Click "Advanced settings" → "Secrets" and paste:
   ```toml
   GOOGLE_API_KEY = "AIza...your real key..."
   ```
6. Click "Deploy"

Streamlit builds the app from `requirements.txt` and starts it. You'll get
a public URL like `https://your-app-name.streamlit.app`.

### Step 3: Update the deployed app later
Any time you `git push` new changes to `main`, Streamlit Cloud
auto-redeploys. No manual redeploy step needed.

---

## How it works
1. PDF is split into ~1000-character chunks.
2. Each chunk is converted to a vector using Google's `gemini-embedding-001` model.
3. Your question is also converted to a vector; the most similar chunks are
   retrieved via semantic search.
4. Those chunks + your question go to Gemini (`gemini-flash-latest` or
   `gemini-pro-latest` — Google's aliases that always point to their current
   stable model), which must answer using only that context.

## Limitations to know before you demo this
- Gemini's free tier has rate limits — heavy/rapid use will hit them.
- The vector store is in-memory: restarting the app clears the index, and
  every user session on the deployed app gets a fresh, separate index (no
  shared memory between visitors).
- Large PDFs (100+ pages) are slow to index on the free tier due to
  embedding rate limits.
- On Streamlit Community Cloud, the app sleeps after inactivity and takes
  a few seconds to wake up on the next visit — normal for the free tier.
- The assistant only answers using text found in the uploaded PDF. It will
  correctly say "I don't know" to opinion questions (e.g. "is this a good
  resume?") — that's expected behavior, not a bug.
- **Google renames/retires model names often.** This project has already
  been updated twice for exactly that reason (old embedding and chat model
  names stopped working). If you get a `404` or `models/... is not found`
  error in the future, the model name changed again — check
  https://ai.google.dev/gemini-api/docs/models for the current name and
  swap it into `rag_assistant.py`.
