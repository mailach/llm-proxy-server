import tiktoken

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



def change_user_budget(model, input_tokens, output_tokens, user):
    
    input_price = input_tokens * (model.price_input_token/1_000_000)
    output_price = output_tokens * (model.price_output_token/1_000_000)
    
    user.used_budget += input_price + output_price
    user.save()