import logging
import flask
import tiktoken
import uuid

from openai import OpenAI

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
    
        
    

# def chunk_completion(user, **kwargs):
#     model = kwargs["model"]
#     try:
#         client = OpenAI()
#         answer = client.chat.completions.create(**kwargs)
#         logging.error(answer)

#     except Exception as e:
#         return {"OpenAI Error": repr(e)}

#     try:
#         pass #save_num_tokens(model, answer.usage.total_tokens, user.id)
        
#         return answer.dict()
#     except Exception as e:
#         err_id = str(uuid.uuid4())
#         logging.error({"id": err_id, "exception": e, "location": "Saving number of tokens chunk"})
#         return {"Error": str(e) + " --- If reoccuring, contact TA with id " + err_id}
    
        




# def save_num_tokens(model, num, user):
#     logging.error("NUMBER OF TOKENS IN THIS STREAM:  " + str(num) + model)
#     price = get_price_per_token(model)

    
#     increase_used_budget(price, num, user)

    
    

def chunk_completion(**kwargs):
    # model = kwargs["model"]
    try:
        client = OpenAI()
        answer = client.chat.completions.create(**kwargs)
        logging.info(answer)

    except Exception as e:
        return {"OpenAI Error": repr(e)}

    try:
        #save_num_tokens(model, answer.usage.total_tokens, user.id)
        
        return answer.dict()
    except Exception as e:
        err_id = str(uuid.uuid4())
        logging.error({"id": err_id, "exception": e, "location": "Saving number of tokens chunk"})
        return {"Error": str(e) + " --- If reoccuring, contact TA with id " + err_id}


@completions.route("/chat/completions", methods=["GET", "POST"])
# @api_key_required
# @user_has_budget
# @validate_json_body
def chat_completion():
        data = flask.request.json
        logging.info(data)
        # if  data["model"] not in MODELS:
        #     return {"Error": "Please specify a supported model: " + str(MODELS)}

        if "stream" in data and data["stream"]:
            return stream_completion(**data)
        else:
            return chunk_completion(**data)
        

