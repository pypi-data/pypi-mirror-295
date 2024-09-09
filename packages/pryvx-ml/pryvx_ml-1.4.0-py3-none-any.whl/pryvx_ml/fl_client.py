from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error, mean_squared_error
import requests
import pickle
import json
import base64

class Client:

    @staticmethod
    def preprocess_data(df, input_columns, target_column):

        X = df[input_columns]
        y = df[target_column]

        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_columns),
                ('cat', categorical_transformer, categorical_columns)
            ])

        pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

        X_preprocessed = pipeline.fit_transform(X)

        return X_preprocessed, y

    @staticmethod
    def split_train_test(X, y, test_sample_size=0.2):
        return train_test_split(X, y, test_size=test_sample_size)


    @staticmethod
    def train_logistic_regression(X_train, X_test, y_train, y_test):
        model = LogisticRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        clf_report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)

        extracted_metrics = {}
        extracted_metrics["accuracy"] = clf_report["accuracy"]

        extracted_metrics["table"] = {}
        for class_name in clf_report.keys():
            if class_name not in ["accuracy", "macro avg", "weighted avg"]:
                extracted_metrics["table"][class_name] = clf_report[class_name]

        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            fpr = fp / (fp + tn)
            extracted_metrics["false_positive_rate"] = fpr

        return model, extracted_metrics
    

    @staticmethod
    def train_linear_regression(X_train, X_test, y_train, y_test):
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return model, { "mae": mean_absolute_error(y_test, y_pred), "mse": mean_squared_error(y_test, y_pred) }
    

    @staticmethod
    def send_model_to_server(trained_model, metrics_dict, PROJECT_ID, COLLABORATOR_ID, CLIENT_SECRET_KEY):

        serialized_params = pickle.dumps(trained_model)
        encoded_params = base64.b64encode(serialized_params).decode('utf-8')
    
        payload = {
            "model_params": encoded_params,
            "metrics": json.dumps(metrics_dict),
        }

        headers = {
            "projectId": PROJECT_ID,
            "collaboratorId": COLLABORATOR_ID,
            "clientSecretKey": CLIENT_SECRET_KEY,
            "Content-Type": "application/json"
        }

        url = "https://api.pryvx.com/send-params"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return "Error:", response.text
        
    
    @staticmethod
    def send_model_to_server_test(trained_model, metrics_dict, PROJECT_ID, COLLABORATOR_ID, CLIENT_SECRET_KEY):

        serialized_params = pickle.dumps(trained_model)
        encoded_params = base64.b64encode(serialized_params).decode('utf-8')
    
        payload = {
            "model_params": encoded_params,
            "metrics": json.dumps(metrics_dict),
        }

        headers = {
            "projectId": PROJECT_ID,
            "collaboratorId": COLLABORATOR_ID,
            "clientSecretKey": CLIENT_SECRET_KEY,
            "Content-Type": "application/json"
        }

        url = "https://middleware-app-siuquavhfa-lz.a.run.app/send-params"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return "Error:", response.text

