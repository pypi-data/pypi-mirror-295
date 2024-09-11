import os
import json
import requests
from pydantic import BaseModel, ValidationError
from enum import Enum, IntEnum

from pathlib import Path

class QueryTypeEnum(IntEnum):
    Text = 1
    Image = 2
    SQL = 3

class QueryModeEnum(IntEnum):
    Refine = 1
    Compact = 2
    Accumulate = 3

class QueryPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    data_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str

class QueryPipelineMessage(BaseModel):
    user_token : str
    name : str
    data_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str

def CreateOrUpdateQueryPipeline(create,
                                md_api_key,
                                name,
                                query_type,
                                data_store,
                                llm_model,
                                query_params):
       

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_type'] = query_type
    json_input['data_store'] = data_store
    json_input['llm_model'] = llm_model
    json_input['query_params'] = query_params

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
            result = requests.post(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        else:
            result = requests.put(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteQueryPipeline(md_api_key, name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def RunQueryPipeline(md_api_key, name, query_str):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_pipeline_run', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DataStoreQuery(md_api_key, 
                   data_store, 
                   query_type,
                   llm_model,
                   query_params,
                   query_str):

    """Query a document using the Data Store as a one time activity.

    Parameters
    ----------
    md_api_key : Majordomo API Key.
    data_store : Name of the data store.
    query_type : This is the type of query to be executed. Valid values are:
        md.QueryTypeEnum.Text
        md.QueryTypeEnum.Image
        md.QueryTypeEnum.SQL
    llm_model : Specify the LLM model to be used for the query. This should be
        permitted for this user in model profile.
    query_params : A JSON describing any special ingestion parameters.
    query_str : The actual query string. As of now, variable expansion within the string
        is not supported. Please do that operation outside this call and supply the final
        query string. Query string may contain indications to the model about the format of
        the output. But honoring that accurately will be the purview of the LLM model.

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
    json_input['data_store'] = data_store
    json_input['query_type'] = query_type
    json_input['llm_model'] = llm_model
    json_input['query_params'] = query_params
    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store_query', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise
