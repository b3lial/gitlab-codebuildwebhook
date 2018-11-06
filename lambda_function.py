import json
from http import HTTPStatus
from json import dumps as json_dump

import boto3

def lambda_handler(event, context):
  req_context = event["requestContext"]
  
  # POST
  if req_context["httpMethod"] == "POST":
    print("Event: {}".format(event['body']))
    body = json.loads(event['body'])
    
    if body['project']['name'] is not None:
      print('Starting a new build ...')
      target = body['project']['name']
      cb = boto3.client('codebuild')
      build = {
        'projectName': target
      }
      print('Starting build for project {0}'.format(build['projectName']))
      try:
        build = cb.start_build(**build)
        print('Successfully launched a new CodeBuild project build!')
        print('Codebuild returned: {}'.format(build))
      except Exception as e:
        print('Codebuild Error: {}'.format(e));
    else:
      print('project parameter is missing')
      return missing_param_error()
  
    return create_default_rest_reply(HTTPStatus.OK, create_no_meta_body(
      {'message' : 'Ok'}))
      
  # GET, PUT, DELETE etc.
  else:
    print("Unsupported HTTP Method: {} at {}".format(req_context["httpMethod"], req_context["resourcePath"]))                                                                                  
    return method_not_allowed_error()
  
# --------------------------------------------------------------------
  
def create_rest_reply(status_code, headers, body):                                                                                                                                                        
  return{                    
    "statusCode": status_code,      
    "headers": headers,
    "body": body
  }


def create_default_rest_reply(status_code, body):
  return create_rest_reply(status_code, create_header(), body)                                                                                                                                          


def create_header():
  return {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Origin": "*",
    "Cache-control": "no-cache, no-store",
    "Pragma": "no-cache",
    "Expires": "0",
    "Content-type": "application/json",                                                                                                                                                               
  }
  
def create_body(meta, data):
  return '{{"meta": {}, "data": {}}}'.format(json_dump(meta), json_dump(data))


def create_no_meta_body(data):
  return create_body({}, data)

# --------------------------------------------------------------------

def missing_param_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.BAD_REQUEST))

  return create_default_rest_reply(
    HTTPStatus.BAD_REQUEST,
    create_no_meta_body({"error": "Missing parameters"})
  )

def not_implemented_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.NOT_IMPLEMENTED))

  return create_default_rest_reply(
    HTTPStatus.NOT_IMPLEMENTED,     
    create_no_meta_body({"error": "Not implemented."})
  )
    
def service_unavailable_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.SERVICE_UNAVAILABLE))

  return create_default_rest_reply(
    HTTPStatus.SERVICE_UNAVAILABLE, 
    create_no_meta_body({"error": "Resource not available."})
  )

def resource_not_found_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.NOT_FOUND))

  return create_default_rest_reply(
    HTTPStatus.NOT_FOUND,
    create_no_meta_body({"error": "Resource not found."})
  )

def method_not_allowed_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.METHOD_NOT_ALLOWED))

  return create_default_rest_reply(
    HTTPStatus.METHOD_NOT_ALLOWED,
    create_no_meta_body({"error": "Method not allowed."})
  )

def internal_server_error():
  print("Returning HTTPStatus {}.".format(HTTPStatus.INTERNAL_SERVER_ERROR))

  return create_default_rest_reply(
    HTTPStatus.INTERNAL_SERVER_ERROR,
    create_no_meta_body({"error": "Internal Server Error."})
  )
