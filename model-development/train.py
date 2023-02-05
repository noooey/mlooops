import joblib
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

# get data
db_connect = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="0429")
df = pd.read_sql("SELECT * FROM wisconsin_data ORDER BY id DESC LIMIT 100", db_connect)
X = df.drop(["id", "target"], axis="columns")
y = df["target"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, random_state=2000)

# model development and train
model_pipeline = Pipeline([("scaler", StandardScaler()), ("svc", SVC())])
model_pipeline.fit(X_train, y_train)

train_pred = model_pipeline.predict(X_train)
valid_pred = model_pipeline.predict(X_valid)

train_acc = accuracy_score(y_true=y_train, y_pred=train_pred)
valid_acc = accuracy_score(y_true=y_valid, y_pred=valid_pred)

print("Train Accuracy :", train_acc)
print("Valid Accuracy :", valid_acc)

# save model
joblib.dump(model_pipeline, "model_pipeline.joblib")

# save data
df.to_csv("data.csv", index=False)


"""
Train Accuracy : 0.975
Valid Accuracy : 0.95
"""