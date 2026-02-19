from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import Literal
import pandas as pd
import numpy as np
import pickle 
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI(title="Loan Approval Prediction API")

# Add these if not already imported (you have most, but add if missing)
from fastapi.staticfiles import StaticFiles

# Mount static folder at root with auto-serving of index.html / for.html
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
with open("app/rf_model.pkl", "rb") as f:
    model = pickle.load(f)

from fastapi.responses import FileResponse

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    return FileResponse("static/for.html")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanInput(BaseModel):
    Gender: Literal['Male','Female']
    Married: Literal['Yes','No']
    Dependents: int
    Education: Literal['Graduate','Not Graduate']
    Self_Employed: Literal['Yes','No']
    ApplicantIncome: int
    CoapplicantIncome: int
    LoanAmount: int
    Loan_Amount_Term: int
    Credit_History: int
    Property_Area: Literal['Urban','Semiurban','Rural']

@app.post("/predict")
def predict_loan(input_data: LoanInput):

    df = pd.DataFrame([input_data.model_dump()])

    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    df['Married'] = df['Married'].map({'Yes': 1, 'No': 0})
    df['Education'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
    df['Self_Employed'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})
    df['Property_Area'] = df['Property_Area'].map({
        'Urban': 2, 'Semiurban': 1, 'Rural': 0
    })

    df['EMI'] = df['LoanAmount'] / df['Loan_Amount_Term']
    df['LoanAmount_log'] = np.log1p(df['LoanAmount'])
    df['Total_Income_log'] = np.log1p(df['ApplicantIncome'] + df['CoapplicantIncome'])

    df.drop(columns=['LoanAmount'], inplace=True)

    if hasattr(model, "feature_names_in_"):
        df = df[model.feature_names_in_]

    pred_class = int(model.predict(df)[0])
    pred_proba = float(model.predict_proba(df)[:, 1][0])

    return {
        "prediction": pred_class,
        "probability": round(pred_proba, 4)
    }



