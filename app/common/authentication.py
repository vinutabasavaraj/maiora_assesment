from fastapi import HTTPException, status
import os
import hashlib
import secrets

from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timedelta



# Class to authorize user.
class Auth():
    hasher= CryptContext(schemes=['bcrypt'])
    secretval = secrets.token_hex(32)
    
    os.environ['value'] = secretval

    secret = os.getenv("value")
    
    # Method to encode psswrd using sha512 algorithm.
    def encode_psswrd(self, psswrd):

        encoded_psswrd = psswrd.encode()
        digest = hashlib.pbkdf2_hmac('sha512', encoded_psswrd,  10000)
        hex_hash = digest.hex()
        hashedpsswrd = hex_hash
        return hashedpsswrd

    # Method to encode token.
    def encode_token(self, userid):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'scope': 'access_token',
            'sub' : str(userid)
        }

        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )


    
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Scope for The Token is Invalid", "statusCode": 401}
        )
        except ExpiredSignatureError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token Expired", "statusCode": 401}
        )
        except JWTError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid Token", "statusCode": 401}
        )

