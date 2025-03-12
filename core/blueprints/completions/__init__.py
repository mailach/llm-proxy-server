import logging
import traceback
import flask
import uuid


from core.models import LanguageModel
from core.blueprints.auth import api_key_and_budget_required

from ._request_schema_validation import validate_json_body
from ._openai_provider import OpenAICompletionProvider


completions = flask.Blueprint("completion", __name__)


# currently only openai provider is integrated. Add other proivders by using the provider base class in _abstract_provider.py
providers = {"openai": OpenAICompletionProvider}


@completions.route("/chat/completions", methods=["GET", "POST"])
@validate_json_body
@api_key_and_budget_required
def chat_completion(user):
        data = flask.request.json
        lm = LanguageModel.query.get(data["model"])
        
        if not lm:
             return {"Error": "Chosen model not supported"}
         
        try: 
            app = flask.current_app._get_current_object()
            provider = providers[lm.provider](app)
            
            if "stream" in data and data["stream"]:
                return provider.stream_completion(user, lm, **data)
            else:
                return provider.chunk_completion(user, lm, **data)
        
        except Exception as e:
            err_id = str(uuid.uuid4())
            tb = traceback.extract_tb(e.__traceback__)[-1]
            logging.error({"id": err_id, "exception": e, "location": f"{tb.filename}:{tb.lineno} in {tb.name}"})
            return {"Error": str(e) + " --- If reoccuring, contact TA with id " + err_id}
        

