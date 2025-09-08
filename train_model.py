import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
df=pd.read_csv("spam.csv",encoding="cp1251")
print(df)

if "v1" in df.columns and "v2" in df.columns:
    df=df[["v1","v2"]]
    df.columns=["label","text"]

X= df["text"]
y=df["label"]

train_X,val_X,train_y,val_y=train_test_split(X,y,random_state=42)

vectorizer = CountVectorizer()
train_X_vectorized = vectorizer.fit_transform(train_X)
val_X_vectorized = vectorizer.transform(val_X)

model = MultinomialNB()
model.fit(train_X_vectorized,train_y)

y_prediction = model.predict(val_X_vectorized)
print("accuracy is ",accuracy_score(val_y,y_prediction))

joblib.dump(model,"model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")