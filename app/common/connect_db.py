from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import base64
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base
from app.common.encrypt_decrypt import *
from sqlalchemy.orm import scoped_session, sessionmaker



Base = declarative_base()

def get_db():
    global engine, Session
    
    cwd = Path(__file__).parents[1]
    filename = cwd/'common'/'metadata_info.json'
    
    with open(filename) as fp:
        properties = json.load(fp)

    properties
    
    databaseType = properties["metadata_config"]["databaseType"]
    password = properties["metadata_config"]["psswrd"]
    hostname = properties["metadata_config"]["host"] 
    portnum = properties["metadata_config"]["port"]
    database_name = properties["metadata_config"]["databaseName"]
    username =  properties["metadata_config"]["username"]
    
    
    backToBytes = base64.b64decode(password)
    data = json_decrypt(backToBytes)
    
    SQLALCHEMY_DATABASE_URL = properties['metadata_config']['databaseType'].lower()+ "://" +properties['metadata_config']['username'].lower() + ":" + data + "@" + properties['metadata_config']['host'] + ":" + str(properties['metadata_config']['port']) + "/" + properties['metadata_config']['databaseName'].lower()
    engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
    session_factory = sessionmaker(bind=engine)

    Session = scoped_session(session_factory)

    db = Session()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()

    Session.remove()

    