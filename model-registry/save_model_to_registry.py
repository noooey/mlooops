import os
from argparse import ArgumentParser

import mlflow
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


# set mlflow environments
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "qwer1234"

# get data
db_connect = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="0429"
    )
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
parser = ArgumentParser()
parser.add_argument("--model-name", dest="model_name", type=str, default="sk_model")
args = parser.parse_args()

# 'experiment에 new-exp 폴더 생성하여 정보 저장
mlflow.set_experiment("new-exp")

# 잘못 된 인풋 들어오지 않도록 예시 샘플들 넣어줌
signature = mlflow.models.signature.infer_signature(model_input=X_train, model_output=train_pred)
input_sample = X_train.iloc[:10]

# mlflow 실행
with mlflow.start_run():
    mlflow.log_metrics({"train_acc": train_acc, "valid_acc": valid_acc})
    mlflow.sklearn.log_model(
        sk_model=model_pipeline,
        artifact_path=args.model_name,
        signature=signature,
        input_example=input_sample,
    )

# save data
df.to_csv("data.csv", index=False)


"""
Train Accuracy : 0.975
Valid Accuracy : 0.95
"""