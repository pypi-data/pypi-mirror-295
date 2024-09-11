from enum import Enum, IntEnum
from pydantic import BaseModel

import requests
import json
import os

from .utils import create_user_response

class IndexTypeEnum(str, Enum):
    vector_db = "vector_db" 
    simple_list = "simple_list" 

class VectorDB(BaseModel):
    name : str
    provider : str

    def retrieve_nodes(self, user_token, query_str, top_k):
        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = VectorDBRetrieve(
                user_token=user_token,
                query_str=query_str,
                top_k=top_k,
                vector_db=self
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/vector_db_retrieve', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

    def summarize_document(self, user_token, summary_eataset, llm_model, summary_instruction):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = SummarizeDocument(
                user_token=user_token,
                vector_db=self,
                summary_vector_db=summary_vector_db,
                llm_model=llm_model,
                summary_instruction=summary_instruction,
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/summarize_document', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

    def delete(self, user_token):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = VectorDBDelete(
                user_token=user_token,
                vector_db=self
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/vector_db_delete', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

class VectorDBDelete(BaseModel):

    user_token : str
    vector_db : VectorDB

class VectorDBRetrieve(BaseModel):

    user_token : str

    vector_db : VectorDB
    query_str : str
    top_k : int | None = 2
    
class SummarizeDocument(BaseModel):
    user_token : str

    vector_db : VectorDB
    llm_model: str
    summary_vector_db : VectorDB
    summary_instruction : str
