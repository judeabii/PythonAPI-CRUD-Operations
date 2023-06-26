import sqlite3
from typing import Optional

from fastapi import FastAPI, Body,Response,status,HTTPException
from pydantic import BaseModel

app = FastAPI()


class Students(BaseModel):
    name: str
    grade: str
    email: str
    lastname: Optional[str] = None


@app.get("/student/{std_id}")
def get_student(std_id,response : Response):
    conn = sqlite3.connect("sample.db")
    conn.row_factory = sqlite3.Row
    values = conn.execute("SELECT * FROM Student where id =?", [std_id]).fetchall()
    print(values)
    if len(values) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The student with the id: {std_id} was not found')
    return values


@app.get("/")
def read_root():
    conn = sqlite3.connect("sample.db")
    conn.row_factory = sqlite3.Row
    values = conn.execute("SELECT * FROM Student").fetchall()
    print(values)
    return values

    '''list_accumulator = []
    for item in values:
        list_accumulator.append({k: item[k] for k in item.keys()})
    return list_accumulator
    '''


'''@app.post("/student")
def write(payload: dict = Body(...)):   # Can use a list here too
    name = payload['Name']
    grade = payload['Grade']
    email = payload['Email']
    print(f"{name} {grade} {email}")
    conn = sqlite3.connect("sample.db")

    conn.execute("insert into Student (Name,Grade,Email) Values(?,?,?)", (name, grade, email))
    conn.commit()

    conn.close()
    return "Succesfully created"
'''


@app.post("/student", status_code=status.HTTP_201_CREATED)
def write(post: Students):
    data = post.dict()
    name = data['name']
    grade = post.grade
    email = post.email
    conn = sqlite3.connect("sample.db")

    conn.execute("insert into Student (Name,Grade,Email) Values(?,?,?)", (name, grade, email))
    conn.commit()

    conn.close()
    return data


@app.delete('/remove/{st_id}')
def remove_student(st_id):
    conn = sqlite3.connect("sample.db")
    values = conn.execute("SELECT * FROM Student where ID = ?", [st_id]).fetchall()
    if len(values) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The student with the id: {st_id} was not found')
    else:
        conn.execute("delete from Student where ID = ?", [st_id])
        conn.commit()
        conn.close()

        return {'message': f'Student with ID: {st_id} was deleted successfully'}

