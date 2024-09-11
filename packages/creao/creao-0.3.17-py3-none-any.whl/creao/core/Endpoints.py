from openai import OpenAI
import time
import requests
import os


class Embed:
    def __init__(self):
        self.client = OpenAI()

    def invoke(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding


class CreaoLLM:
    def __init__(self, bot_name="assistant", bot_content="assistant") -> None:
        self.bot_name = bot_name
        self.bot_content = bot_content

    def invoke(self, prompt, schema, component_id="default", pipeline_id="default"):
        """
        Invoke the Creao LLM API
        """
        start_time = time.time()
        # The API Gateway endpoint URL
        url = "https://drk3mkqa6b.execute-api.us-west-2.amazonaws.com/default/minimaxserver"
        api_key = os.environ["CREAO_API_KEY"]
        headers = {"Content-Type": "application/json", "x-api-key": api_key}
        # Payload to be sent to the Lambda function via API Gateway
        payload = {
            "prompt": prompt,
            "schema": schema,
            "bot_name": self.bot_name,
            "bot_content": self.bot_content,
            "component_id": component_id,
            "pipeline_id": pipeline_id,
        }
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        response_josn = response.json()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("response_josn:", response_josn)
        print(f"CreaoLLM API call took total {elapsed_time} seconds")
        if "elapsed_time" in response_josn:
            minimax_elapsed_time = response_josn["elapsed_time"]
            print(f"Minimax server took {minimax_elapsed_time} seconds")
        # print("reponse:", response.content)
        try:
            return response_josn
        except Exception as e:
            print(f"CreaoLLM json decode error:{e}, with response:{response.text}")
            return {"reply": ""}


class OpenAILLM:
    def __init__(self, model_id="gpt-4o-mini"):
        self.client = OpenAI()
        self.model_id = model_id

    def invoke(self, prompt, schema=None):
        messages = [{"role": "user", "content": prompt}]
        try:
            if schema is None:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                )
                return response.choices[0].message.content
            else:
                response = self.client.beta.chat.completions.parse(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                    response_format=schema,
                )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return None


# creaoLM = CreaoLLM()
# r = creaoLM.invoke("hello", {"name":"world"})
# print(r)
