import pandas as pd, joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate

d = pd.read_csv("labels.csv")
X, y = d.wish.astype(str), d.label.astype(int)

model = make_pipeline(
    TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1, sublinear_tf=True),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
s = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "f1_macro"])
print(f"5-fold accuracy: {s['test_accuracy'].mean():.2f} (+/- {s['test_accuracy'].std():.2f})")
print(f"5-fold macro F1: {s['test_f1_macro'].mean():.2f}")

model.fit(X, y)
joblib.dump(model, "model.pkl")
for t in ["Ravi macha, sweets tinu ra, party cheddam 🪔", "May the luminous glow of Diwali fill your heart with timeless joy ✨"]:
    print(f"{model.predict_proba([t])[0][1]:.2f} natural-score | {t}")
print("model.pkl saved ✅")
