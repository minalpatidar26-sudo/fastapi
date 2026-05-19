import os
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pandas as pd

app= FastAPI()
CSV_FILE="data.csv"
#Schema for adding new_data via POST
class Employee(BaseModel):
    id: int
    name: str
    role: str
    department: str



@app.get("/")
def read_root():
    return {"hello":"world"}


#1. GET Method :read and return csv data
@app.get("/csv-data")
def get_csv_data():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="csv file not found")
    #read csv and convert to a list of dictionaries
    df=pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")


@app.post("/csv-data")
def add_csv_data(employee:Employee):
    #prepare the new row
    new_data=pd.DataFrame([employee.model_dump()])

    #append to existing CSV or create a new one
    if os.path.exists(CSV_FILE):
        new_data.to_csv(CSV_FILE,mode="a",header=False,index=False)
    else:
        new_data.to_csv(CSV_FILE,mode="w",header=True,index=False)
    return{"message":"data added successfully","data":employee}



@app.get("/items/{item_id}")
def read_item(item_id:int,q:str | None=None):
    return{"item_id":item_id,"q":q}

