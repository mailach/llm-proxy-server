
from openai import OpenAI
from ._count_tokens import count_tokens, change_user_budget
from ._abstract_provider import CompletionProvider


class OpenAICompletionProvider(CompletionProvider): 
    
    def __init__(self, app):
        super().__init__(app)
        self._client = OpenAI()
    
    def stream_completion(self, user, lm, **kwargs):
        input_tokens = count_tokens(kwargs["messages"])
        output_tokens = 0
        

        with self._app.app_context(): 
            try:
                completion_generator = self._client.chat.completions.create(**kwargs)
                
            except Exception as e:
                yield str({"OpenAI Error": repr(e)})
                return    

            for event in completion_generator:

                if event.choices[0].finish_reason:    
                    change_user_budget(lm, input_tokens, output_tokens, user)
                    
                output_tokens +=1
                yield str(event.dict())
        
        
    def chunk_completion(self, user, lm, **kwargs):
        try:
            answer = self._client.chat.completions.create(**kwargs)

        except Exception as e:
            return {"OpenAI Error": repr(e)}

        change_user_budget(lm, answer.usage.prompt_tokens, answer.usage.completion_tokens, user)
        return answer.dict()