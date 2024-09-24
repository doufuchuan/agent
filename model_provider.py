import dashscope
import os
from dashscope.api_entities.dashscope_response import Message
from prompt import user_msg
import json
class ModelProvider(object):
    def __init__(self) -> None:
        self.api_key = os.environ.get("API_KEY")
        self.model_name = os.environ.get("MODEL_NAME")
        self._client = dashscope.Generation()

        self.max_retry_time = 3
        pass

    def  chat(self, prompt, chat_history):
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_time:
            cur_retry_time+=1
            try:
                messages = [Message(role='system', content=prompt)]
                for his in chat_history:
                    messages.append(Message(role='user', content=his[0]))
                    messages.append(Message(role='assistant', content=his[1]))
                
                messages.append(Message(role='user', content=user_msg))
                response = self._client.call(
                    model = self.model_name,
                    api_key=self.api_key,
                    messages=messages
                )
                """
                {
                    "id":"chatcmpl-9b920f00-3cf4-9864-ac5f-b7309531ed5b",
                    "choices":[{"finish_reason":"stop",
                                "index":0,
                                "logprobs":null,
                                "message":{"content":"我是阿里云开发的一 款超大规模语言模型，我叫通义千问。",
                                            "refusal":null,
                                            "role":"assistant",
                                            "function_call":null,
                                            "tool_calls":null}
                                }],
                    "created":1727169959,
                    "model":"qwen-turbo",
                    "object":"chat.completion",
                    "service_tier":null,
                    "system_fingerprint":null,
                    "usage":{"completion_tokens":17,
                            "prompt_tokens":22,
                            "total_tokens":39,
                            "completion_tokens_details":null}
                }
                """
                # print(response)
                content = json.loads(response['output']['text'])
                return content
            except Exception as err:
                print("调用大模型出错：{}".format(err))
            return {}
