from typing import Optional
from typing import List
from pydantic import AnyUrl, BaseModel, Field


class MetadataTable_PostgreSQL(BaseModel):
    databaseType : str = Field(example="databaseType",min_length=1)
    host: str = Field(example="host",min_length=2)
    port : int = Field(example="port", ge=0, le=65535)
    username : str = Field(example="username",min_length=1)
    psswrd : str = Field(example="psswrd",min_length=1)
    databaseName : str = Field(example="databaseName",min_length=1)