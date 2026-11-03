# Diwali Wish Generator 🪔

A small web app that writes personalized Diwali wishes in Tanglish, Telugu, English or Hindi, then turns the best one into a downloadable greeting card.

## How it works

1. **Generation (LLM):** `wish.py` prompts `openai/gpt-oss-120b` via the Groq API. The prompt controls tone by relation (friend, amma, boss, teacher, ...), limits length, and uses a few examples to keep the style natural.
2. **Ranking (ML):** the app generates 3 candidate wishes. A scikit-learn classifier (character n-gram TF-IDF + logistic regression, `train.py`) scores each one as natural vs stiff, and the highest-scoring wish goes on the card.
3. **Card:** `card_html.py` renders an HTML/CSS card with an inline SVG diya, and a button downloads it as a PNG.
4. **UI:** Streamlit (`app.py`).

## Run locally

    pip install -r requirements.txt
    echo "GROQ_API_KEY=your_key" > .env
    streamlit run app.py

## Retrain the classifier

    python label.py    # label generated wishes: 1 = natural, 0 = stiff
    python train.py    # trains and saves model.pkl

## Known limitations

- The classifier is trained on only 49 wishes. Labels were assisted by rules (poetic-prompt outputs and wrong-script outputs marked as stiff), so the 1.00 cross-validation score mostly reflects that easy split. It is a working pipeline, not a validated quality metric.
- The classifier was trained on Roman-script text, so its scores are unreliable for Telugu script output.
- Casual Telugu in Telugu script is still weaker than Tanglish or English. Formal Telugu is fine.
- The public demo link runs from a laptop through a temporary tunnel, so it is not always online.

## Stack

Python, Streamlit, Groq API, scikit-learn, pandas, joblib.
