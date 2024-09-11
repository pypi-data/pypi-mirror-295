import os
import json
import requests
from pydantic import BaseModel, ValidationError
from enum import Enum, IntEnum
import majordomo_ai as md

from pathlib import Path

class TextIngestType(IntEnum):
    Base = 1 
    Summary = 2

class PDFExtractorTypeEnum(IntEnum):
    LlamaParse = 1
    PyMuPDF = 2
    PDF2Image = 3

class IngestTypeEnum(IntEnum):
    Text = 1
    Image = 2
    Custom = 3

class DocStoreTypeEnum(IntEnum):
    AWSS3 = 1
    AzureBlob = 2
    Webpage = 3
    Local = 4
    SQL = 5

class IngestPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    data_store : str
    doc_store_type : DocStoreTypeEnum
    doc_store_info : str
    ingest_type : IngestTypeEnum
    ingest_params : str
    timer_interval : int
    timer_on : int

class IngestPipelineMessage(BaseModel):
    md_api_key : str
    name : str
    data_store : str
    doc_store_type : DocStoreTypeEnum
    doc_store_info : str
    ingest_type : IngestTypeEnum
    ingest_params : str
    timer_interval : int
    timer_on : int

class IngestPipelineRunMessage(BaseModel):
    md_api_key : str
    data_store : str
    name : str

def CreateIngestPipeline(md_api_key,
                       data_store,
                       name,
                       doc_store_type,
                       doc_store_info,
                       ingest_type,
                       ingest_params,
                       timer_interval,
                       timer_on):
       

    #embedding_model : str
    #ingest_type : TextIngestType | None = "Base"
    #output_store : DataStore | None = DataStore(location='local', info=LocalDataStore(file_name=''))
    #pdf_extractor: PDFExtractorTypeEnum | None = "PyMuPDF"
    #chunking_type : str | None = 'normal'
    #chunk_size : int | None = 1024
    #llm_model : str | None = ''

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['data_store'] = data_store
    json_input['name'] = name
    json_input['doc_store_type'] = doc_store_type
    json_input['doc_store_info'] = doc_store_info
    json_input['ingest_type'] = ingest_type
    json_input['ingest_params'] = ingest_params
    json_input['timer_interval'] = timer_interval
    json_input['timer_on'] = timer_on

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def UpdateIngestPipeline(md_api_key,
                         data_store,
                         name,
                         doc_store_info,
                         ingest_params,
                         timer_interval,
                         timer_on):
       

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['data_store'] = data_store 
    json_input['name'] = name
    json_input['doc_store_type'] = 0
    json_input['doc_store_info'] = doc_store_info
    json_input['ingest_type'] = 0
    json_input['ingest_params'] = ingest_params
    json_input['timer_interval'] = timer_interval
    json_input['timer_on'] = timer_on

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteIngestPipeline(md_api_key, name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def IngestPipelineRun(md_api_key, data_store, ingest_pipeline):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['data_store'] = data_store
    json_input['name'] = ingest_pipeline

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/ingest_pipeline_run', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DataStoreIngest(md_api_key, 
                    data_store, 
                    doc_store_type, 
                    doc_store_info, 
                    ingest_type, 
                    ingest_params):

    """Add a document to the Data Store as a one time activity.

    Parameters
    ----------
    md_api_key : Majordomo API Key.
    data_store : Name of the data store.
    doc_store_type : This is the source of the document. Valid values are,
        md.DocStoreTypeEnum.AWSS3
        md.DocStoreTypeEnum.AzureBlob
        md.DocStoreTypeEnum.Webpage
        md.DocStoreTypeEnum.Local
    doc_store_info : A JSON describing the location of the file. Examples for 
         different types are below.
         {"files" : "abcd.pdf", "region": "us-east-1", "bucket": "demo"}
         {"url" : "http://abcd.pdf"}
    ingest_type : The type of ingestion to be performed. Valid values are,
        md.IngestTypeEnum.Text
        md.IngestTypeEnum.Image
    ingest_params : A JSON describing any special ingestion parameters.

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
    json_input['name'] = ''
    json_input['doc_store_type'] = doc_store_type
    json_input['doc_store_info'] = doc_store_info
    json_input['data_store'] = data_store
    json_input['ingest_type'] = ingest_type
    json_input['ingest_params'] = ingest_params

    try:
        infoMap = json.loads(doc_store_info)
    except Exception as e: raise

    try:
        "files" in infoMap
    except Exception as e: raise

    if doc_store_type == md.DocStoreTypeEnum.Local:
        files = {'file': open(infoMap["files"],'rb')}
        values = {'md_api_key': md_api_key}

        try:
            result = requests.post(director_url + '/file_upload', files=files, data=values)
        except Exception as e: raise

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store_ingest', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise
