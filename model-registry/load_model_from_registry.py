import os
from argparse import ArgumentParser

import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# set envirion variables
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "qwer1234"

# load model from mlflow
parser = ArgumentParser()
parser.add_argument("--model-name", dest="model_name", type=str, default="sk_model")
parser.add_argument("--run-id", dest="run_id", type=str)
args = parser.parse_args()

model_pipeline = mlflow.sklearn.load_model(f"runs:/{args.run_id}/{args.model_name}")

# get data
df = pd.read_csv("data.csv")

X = df.drop(["id", "target"], axis="columns")
y = df["target"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, random_state=2000)

# validate
load_train_pred = model_pipeline.predict(X_train)
load_valid_pred = model_pipeline.predict(X_valid)


load_train_acc = accuracy_score(y_true=y_train, y_pred=load_train_pred)
load_valid_acc = accuracy_score(y_true=y_valid, y_pred=load_valid_pred)

print("Train Accuracy :", load_train_acc)
print("Valid Accuracy :", load_valid_acc)

"""
Load Model Train Accuracy : 0.975
Load Model Valid Accuracy : 0.95
"""