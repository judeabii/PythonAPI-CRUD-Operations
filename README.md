# PythonAPI-CRUD-Operations
This project showcases a comprehensive Python API project built using FastAPI. The project focuses on performing CRUD operations on a SQLite database, implementing schema validations, authentication, and various other functionalities. With a clean and efficient framework like FastAPI, this project demonstrates the power and flexibility of building robust APIs in Python.

## Pre-requisites
Use the package manager pip to install fastapi with all the dependencies
```commandline
pip install fastapi[all]
```
## Code walkthrough
### CRUD operations
#### Create
```commandline
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
```
#### Read
```commandline
@app.get("/")
def read_root():
    conn = sqlite3.connect("sample.db")
    conn.row_factory = sqlite3.Row
    values = conn.execute("SELECT * FROM Student").fetchall()
    print(values)
    return values
```
#### Update
```commandline
@app.put('/update/{st_id}',status_code=status.HTTP_200_OK)
def update_student(st_id, post: Students):
    name = post.name
    grade = post.grade
    email = post.email
    conn = sqlite3.connect("sample.db")

    values = conn.execute("SELECT * FROM Student where ID = ?", [st_id]).fetchall()
    if len(values) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The student with the id: {st_id} was not found')
    conn.execute("UPDATE Student Set Name = ?,Grade =?,Email= ? where ID = ?",
                 (name, grade, email, st_id))
    conn.commit()
    conn.close()
    return {'message': 'successfully updated'}
```
#### Delete
```commandline
@app.delete('/remove/{st_id}', status_code=status.HTTP_204_NO_CONTENT)
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

        return Response(status_code=status.HTTP_204_NO_CONTENT)
```