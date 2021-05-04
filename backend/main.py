from typing import Optional
from fastapi import FastAPI , Request
import mysql.connector
import json
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
   
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/addarticle")
async def add(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"INSERT INTO `article` (`name`, `description`,`image`,`catname`) VALUES ('{body['name']}', '{body['description']}','{body['image']}','{body['catname']}');")
    mydb.commit()
    return "done"

@app.get("/article")
def gets():
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM article")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    if json_data:
        resutls = []
        for res in json_data:
            arid = res["arid"]
            mycursor.execute(f"SELECT * FROM commentaire where articleid={arid}")
            row_headers=[x[0] for x in mycursor.description]
            comments = [dict(zip(row_headers,el)) for el in mycursor.fetchall()]
            res["comments"] = comments
            resutls.append(res)
        return resutls
    return json_data




@app.delete("/article/delete/{_id}")
def delete_article(_id:int):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    mycursor.execute(f"delete FROM article where arid={_id}")
    mydb.commit()
    return "deleted"

@app.put("/article/modify/{_id}")
async def update_article(_id:int,request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"update article set name='{body['name']}' where arid={_id}")
    mydb.commit()
    return "modified"
@app.get("/commentaire")
def get_comment(id:int):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM commentaire where articleid = '{id}'")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return  json_data

@app.delete("/del_commentaire")
def delete_comment(id:int):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "database")
    mycursor = mydb.cursor()
    mycursor.execute(f"DELETE FROM commentaire where comid={id}")
    mydb.commit()
    return "deleted"