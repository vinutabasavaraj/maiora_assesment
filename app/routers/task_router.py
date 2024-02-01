from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.websocket.chat_manager import manager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime
from pathlib import Path
import base64

from app.services.task_service import create_task, get_task, update_task, delete_task
from app.schemas.user_schema import Users
from app.schemas.task_schema import Task
from app.schemas.message_schema import Message
from app.models.task_models import User


from app.schemas.metadata_schema import MetadataTable_PostgreSQL
from app.models.task_models import Base
from app.common.encrypt_decrypt import *
from app.common.connect_db import get_db
from app.common.authentication import Auth

auth_handler = Auth()


security = HTTPBearer()
auth_handler = Auth()
router = APIRouter()

@router.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(task_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



@router.post("/tasks/", tags=["Task"],response_model=Task)
def create_task_api(taskinfo: Task, credentials: HTTPAuthorizationCredentials = Security(security),db: Session = Depends(get_db)):
    """
    API to add the task
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        return create_task(db, taskinfo)

@router.get("/tasks/{task_id}", response_model=Task, tags=["Task"])
def read_task_api(task_id: int, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    API to fetch the partcular task based on task id
    """
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        task = get_task(db, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@router.put("/tasks/{task_id}", response_model=Task, tags=["Task"])
def update_task_api(task_id: int, updated_task: Task, credentials: HTTPAuthorizationCredentials = Security(security),db: Session = Depends(get_db)):
    """
    API to update the tasks
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        existing_task = update_task(db, task_id, updated_task)
        return existing_task

@router.delete("/tasks/{task_id}", response_model=Task, tags=["Task"])
def delete_task_api(task_id: int, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    API to remove the tasks
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        task = delete_task(db, task_id)
        return task


cwd = Path(__file__).parents[1]
filepath = cwd/'common'/'metadata_info.json'

async def metadata_configuration(new_data):
    with open(filepath,'r+',encoding='utf-8') as file:
        file_data = json.load(file)
        file_data["metadata_config"]=new_data
        file.seek(0)
        file.truncate()
        json.dump(file_data, file,ensure_ascii = False, indent = 4)




@router.post('/create_table', tags=["Metadata"])
async def create_tables(db_details:MetadataTable_PostgreSQL):
    """API to Create the Tables:
    Request Body:

    - DatabaseType : Database type should be Postgresql. 
    - Host : Host/IP address of the database server. Example: hostname.domain.com/192.168.0.1
    - Port : Port number of the database server. Example: 5432
    - Username : Database username.
    - Psswrd : Database psswrd.
    - DatabaseName : Database name.
    """
    
    try:
        SQLALCHEMY_DATABASE_URL = db_details.databaseType.lower() + "://" + db_details.username.lower() + ":" + db_details.psswrd + "@" + db_details.host.lower() + ":" + str(db_details.port) + "/" + db_details.databaseName.lower()
        
        engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
        engine.connect()
        
        Base.metadata.create_all(engine)
        
        enc_data = json_encrypt(str(db_details.psswrd))
        enc_data = base64.b64encode(enc_data).decode('utf-8')
        metadata_config = {
                            "databaseType": db_details.databaseType,
                            "host": db_details.host,
                            "port": db_details.port,
                            "username": db_details.username,
                            "psswrd":enc_data,
                            "databaseName": db_details.databaseName
                        }
                    
        await metadata_configuration(metadata_config)
        return {"detail": {"message": "Tables created successfully.", "statusCode": 201, "errorCode": None}} 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": f"Creation of tables failed: {str(e)}", "statusCode": 503, "errorCode": "errorcode"}
        )
    
@router.post('/user', tags=["Users"])
async def register_user(userinfo : Users ,db: Session = Depends(get_db)):
    """
    API to register the users
    This endpoint allows users to register by providing their username and password.
    """
    
    hashed_password = bcrypt.hash(userinfo.password)

    timestamp = datetime.utcnow()
    
    user_details = User(username = userinfo.username, password = hashed_password,created_date = timestamp,last_updated = timestamp)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
                
    return {"detail": {"message": "User details added successfully.", "statusCode": 201, "errorCode": None}} 

@router.post('/Login', tags=["Users"])
async def login(userinfo : Users ,db: Session = Depends(get_db)):
    """
    API to Login the users
    This endpoint allows users to login by providing their username and password
    """

    user_id = db.query(User).filter(User.username == userinfo.username).first()
    if user_id is not None:
        access_token = auth_handler.encode_token(str(user_id))
        return {"detail": {"data": {'access_token': access_token}, "message": "Logged in successfully", "statusCode": 200, "errorCode": None}}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Username/Password Incorrect", "statusCode": 401}
        )

       