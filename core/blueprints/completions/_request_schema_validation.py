import flask
from functools import wraps
from jsonschema import validate

OPENAI_REQUEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
      "model": {
        "type": "string"
      },
      "messages": {
        "type": "array",
        "items": { "$ref": "#/$defs/message" }
      },
      "temperature": {
        "type": "number"
      },
      "top_p": {
        "type": "number"
      },
      "max_tokens": {
        "type": "integer"
      },
      "presence_penalty": {
        "type": "number"
      },
      "frequency_penalty": {
        "type": "number"
      },
      "stream":{
        "type": "boolean"
      },
      "response_format":{
        "type": "object",
        "properties": {
          "type":{
            "type":"string"
          }
        }
      }
    },
    "required": [
      "messages"
    ],
    "additionalProperties": False,
  "$defs": {
    "message": {
        "type": "object",
        "properties": {
          "role": {
            "type": "string"
          },
          "content": {
            "type": "string"
          }
        },
        "required": [
          "role",
          "content"
        ]
      }
  }

  }


def validate_json_body(f):
   @wraps(f)
   def decorator(*args, **kwargs):
    
    if not (flask.request.headers.get('Content-Type') == 'application/json'):
        return 'Content-Type not supported!'

    data = flask.request.json
    try:
        validate(instance=data, schema=OPENAI_REQUEST_SCHEMA)
    except:
        return "Request data does not match OpenAI request schema."
        
    return f(*args, **kwargs)
   
   return decorator