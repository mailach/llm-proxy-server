import logging
import traceback
import flask
import tiktoken
import uuid

from openai import OpenAI
from core.blueprints.auth import api_key_and_budget_required
from core.models import User, LanguageModel

completions = flask.Blueprint("completion", __name__)
ENCODER = tiktoken.get_encoding("cl100k_base")



# taken from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb and adapted
def count_tokens(messages):
    tokens_per_message = 4
    tokens_per_name = -1
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(ENCODER.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def stream_completion(**kwargs):
    # num_tokens = count_tokens(kwargs["messages"])
    # model = kwargs["model"]
    try:
        client = OpenAI()
        completion_generator = client.chat.completions.create(**kwargs)
    except Exception as e:
        yield str({"OpenAI Error": repr(e)})
        return

    try:
        for event in completion_generator:

            if event.choices[0].finish_reason:
                pass# save_num_tokens(model, num_tokens, user.id)
            # num_tokens +=1
            yield str(event.dict())
    except Exception as e:
        err_id = str(uuid.uuid4())
        logging.error({"id": err_id, "exception": e, "location": "Saving number of tokens chunk"})
        yield str({"Error": str(e) + " --- If reoccuring, contact TA with id " + err_id})
    


def _change_user_budget(model, input_tokens, output_tokens, user):
    
    input_price = input_tokens * (model.price_input_token/1_000_000)
    output_price = output_tokens * (model.price_output_token/1_000_000)
    
    user.used_budget += input_price + output_price
    user.save()
    

    
    

def chunk_completion(user, lm, **kwargs):
    try:
        client = OpenAI()
        answer = client.chat.completions.create(**kwargs)
        logging.info(answer)

    except Exception as e:
        
        return {"OpenAI Error": repr(e)}

    _change_user_budget(lm, answer.usage.prompt_tokens, answer.usage.completion_tokens, user)
    return answer.dict()
    


@completions.route("/chat/completions", methods=["GET", "POST"])
@api_key_and_budget_required
# @validate_json_body
def chat_completion(user):
        data = flask.request.json
        
        lm = LanguageModel.query.get(data["model"])
        if not lm:
             return {"Error": "Chosen model not supported"}
         
        try: 
            if "stream" in data and data["stream"]:
                return stream_completion(**data)
            else:
                return chunk_completion(user, lm, **data)
        
        except Exception as e:
            err_id = str(uuid.uuid4())
            tb = traceback.extract_tb(e.__traceback__)[-1]
            logging.error({"id": err_id, "exception": e, "location": f"{tb.filename}:{tb.lineno} in {tb.name}"})
            return {"Error": str(e) + " --- If reoccuring, contact TA with id " + err_id}
        

