from datasets import load_dataset
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load GoEmotions dataset
dataset = load_dataset("go_emotions", split="train")

# Filter for single-label examples
filtered = dataset.filter(lambda x: len(x['labels']) == 1)

# Map emotion indices to names
label_map = dataset.features['labels'].feature.names
texts = filtered['text']
labels = [label_map[l[0]] for l in filtered['labels']]

# Use a few key emotions for now
target_emotions = ['joy', 'sadness', 'anger', 'fear', 'neutral']
df = pd.DataFrame({'text': texts, 'label': labels})
df = df[df['label'].isin(target_emotions)]

# Vectorize and train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save model and vectorizer
joblib.dump(model, '../model/emotion_model.pkl')
joblib.dump(vectorizer, '../model/vectorizer.pkl')

print("✅ Model trained and saved.")
