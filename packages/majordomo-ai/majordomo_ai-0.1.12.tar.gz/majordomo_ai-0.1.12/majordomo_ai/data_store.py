from enum import Enum, IntEnum
from pydantic import BaseModel, ValidationError
import os
import requests
import json

class DataStoreTypeEnum(IntEnum):
    VectorDB = 1
    UnifiedSQL = 2
    SQL = 3 
    MongoDB = 4
    UnifiedMongo = 5

class DataStore(BaseModel): 
    id : str
    group : str
    workspace : str
    user_name :  str
    type : DataStoreTypeEnum
    name : str

    vectordb_profile : str
    embedding_model : str
    shared :   bool

    db_url :  str
    db_name : str
    db_table : str

class DataStoreList(BaseModel):
    data_stores : list[DataStore]

class DataStoreMessage(BaseModel):
    md_api_key : str
    name : str
    type : DataStoreTypeEnum

    vectordb_profile : str
    embedding_model :  str

    db_url : str
    db_name : str
    db_table : str

    shared : bool

def CreateOrUpdateUnifiedDataStore(create,
                                    md_api_key, 
                                    name, 
                                    vectordb_profile,
                                    embedding_model,
                                    db_url, 
                                    db_name, 
                                    db_table, 
                                    shared):

    """Create or update an Unified Data Store. A unified store is a combination of a embedding 
    vector database and a structured database like SQL. This is typically used to store images
    extracted from documents because there needs to be additional storage option for the extractions.

    Parameters
    ----------
    md_api_key : Majordomo API Key.
    name : Name of the data store (This is also the name of the index in the vector database)
    vectordb_profile : The name of the Vector DB profile that will be used to retrieve the 
        connection parameters for the vector database.
    embedding_model : The model to use for creation of text or multi-modal embeddings.
    db_type : The database type. Valid values : 
        md.DataStoreTypeEnum.UnifiedSQL 
        md.DataStoreTypeEnum.UnifiedMongo 
    db_url : The URL of the database. 
    db_name : The name of the database, either in SQL or Mongo.
    db_table : The name of the table (or a collection or any sub-category) of the database.
    shared : Whether this data store can be used by other users for querying.

    Returns
    -------
    REST response with the following status codes. 
        200 : Success. 'response' contains the status of the add operation.
        400 : Parameters are valid but there was an error while executing the operations. 
                  'response' will provide the error message
        422 : Parameter Issue. Some parameters did not meet the API specification.
        404 : Method not found. API issue, please contact support.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = DataStoreTypeEnum.Unified
    json_input['vectordb_profile'] = vectordb_profile
    json_input['embedding_model'] = embedding_model
    json_input['db_type'] = db_type
    json_input['db_url'] = db_url
    json_input['db_name'] = db_name
    json_input['db_table'] = db_table
    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
            result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        else:
            result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def CreateVectorDBDataStore(md_api_key, 
                             name, 
                             vectordb_profile,
                             embedding_model,
                             shared):

    """Create a Vector Database. Once it is created with an embedding model, it cannot be changed as
    all documents will need to use the same model to get consistent results

    Parameters
    ----------
    md_api_key : Majordomo API Key.
    name : Name of the data store (This is also the name of the index in the vector database)
    vectordb_profile : The name of the Vector DB profile that will be used to retrieve the 
        connection parameters for the vector database.
    embedding_model : The model to use for creation of text or multi-modal embeddings.
    shared : Whether this data store can be used by other users for querying.

    Returns
    -------
    REST response with the following status codes. 
        200 : Success. 'response' contains the status of the add operation.
        400 : Parameters are valid but there was an error while executing the operations. 
                  'response' will provide the error message
        422 : Parameter Issue. Some parameters did not meet the API specification.
        404 : Method not found. API issue, please contact support.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = DataStoreTypeEnum.VectorDB
    json_input['embedding_model'] = embedding_model
    json_input['vectordb_profile'] = vectordb_profile
    json_input['db_type'] = DataStoreTypeEnum.VectorDB
    json_input['db_url'] = ''
    json_input['db_name'] = ''
    json_input['db_table'] = ''
    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def CreateOrUpdateStructDBDataStore(create,
                             md_api_key, 
                             name, 
                             type,
                             embedding_model,
                             db_url, 
                             db_name, 
                             db_table):

    """Create or update an Structered Data Store. A structured store is a placeholder for connecting
    to any database like an SQL or MongoDB that will server as the data source for a natural language
    to database query.

    Parameters
    ----------
    create : Create flag, set to True if creating data store for first time. 
    md_api_key : Majordomo API Key.
    name : Name of the data store (This is also the name of the index in the vector database)
    type : The database type. Valid values : 
        md.DataStoreTypeEnum.SQL 
        md.DataStoreTypeEnum.Mongo 
    db_url : The URL of the database. 
    db_name : The name of the database, either in SQL or Mongo.
    db_table : The name of the table (or a collection or any sub-category) of the database.
    shared : Whether this data store can be used by other users for querying.

    Returns
    -------
    REST response with the following status codes. 
        200 : Success. 'response' contains the status of the add operation.
        400 : Parameters are valid but there was an error while executing the operations. 
                  'response' will provide the error message
        422 : Parameter Issue. Some parameters did not meet the API specification.
        404 : Method not found. API issue, please contact support.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = type
    json_input['vectordb_profile'] = ''
    json_input['embedding_model'] = embedding_model
    json_input['db_type'] = type
    json_input['db_url'] = db_url
    json_input['db_name'] = db_name
    json_input['db_table'] = db_table
    json_input['shared'] = False

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
             result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        else:
             result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteDataStore(md_api_key, name):
       
    """Delete a Data Store. Incase of a vector database, this deletes the embedding vector database. Incase of 
    structured database type, this does not delete any customer owned database that was used for querying. In case
    of unified database also, this will only delete the vector database.

    Parameters
    ----------
    name : Name of the data store (This is also the name of the index in the vector database)

    Returns
    -------
    REST response with the following status codes. 
        200 : Success. 'response' contains the status of the add operation.
        400 : Parameters are valid but there was an error while executing the operations. 
                  'response' will provide the error message
        422 : Parameter Issue. Some parameters did not meet the API specification.
        404 : Method not found. API issue, please contact support.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

