from fastapi import FastAPI
import pyrebase as pb
import json
from pydantic import BaseModel
import uvicorn

class Data(BaseModel):
    pet_name : str
    owner_name : str
    type : str
    gender : str


with open('config.json') as data:
    config = json.load(data)

app = FastAPI(title="PetStore-api")

class CloudStorage:
    def __init__(self, cred):
        self.apiKey = cred['apiKey']
        self.authDomain = cred['authDomain']
        self.projectId = cred['projectId']
        self.storageBucket = cred['storageBucket']
        self.messagingSenderId = cred['messagingSenderId']
        self.appId = cred['appId']
        self.measurementId = cred['measurementId']
        self.databaseURL = cred['databaseURL']
        self.firebase = pb.initialize_app(cred)
    
    def initializeFirebaseStorage(self):
        self.database = self.firebase.database()

    def create(self):
        @app.post('/create-user')
        def create(data: Data):
            data = dict(data)
            id = len(self.database.child("User").get().val())
            self.database.child("User").child(id).set(data)
            return f"Successfully Updated; your id is {id}"
        
    def read(self):
        @app.get('/get-data')
        def read(id: int):
            return self.database.child("User").child(id).get().val()
        
    def update(self):
        @app.put('/update-data')
        def update(id:int, key: str, val: str):
            self.database.child('User').child(id).update({key:val})
            return f"Successfully Updated; {self.database.child('User').child(id).get().val()}"

    def delete(self):
        @app.delete('/delete-data')
        def delete(id:int):
            self.database.child("User").child(id).remove()
            return "Successfully Deleted"
        
c1 = CloudStorage(config)
c1.initializeFirebaseStorage()


c1.create()
c1.read()
c1.update()
c1.delete()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

