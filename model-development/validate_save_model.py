import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# reproduce data
df = pd.read_csv("data.csv")
X = df.drop(["id", "target"], axis="columns")
y = df["target"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, random_state=2000)

# load model
model_pipeline_load = joblib.load("model_pipeline.joblib")

# validate
load_train_pred = model_pipeline_load.predict(X_train)
load_valid_pred = model_pipeline_load.predict(X_valid)


load_train_acc = accuracy_score(y_true=y_train, y_pred=load_train_pred)
load_valid_acc = accuracy_score(y_true=y_valid, y_pred=load_valid_pred)

print("Load Model Train Accuracy :", load_train_acc)
print("Load Model Valid Accuracy :", load_valid_acc)

"""
Load Model Train Accuracy : 0.975
Load Model Valid Accuracy : 0.95
"""