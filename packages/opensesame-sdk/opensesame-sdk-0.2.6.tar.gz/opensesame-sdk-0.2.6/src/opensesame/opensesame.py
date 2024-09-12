import openai
import google.generativeai as genai
import anthropic
import requests
import json
from groq import Groq 
import threading
from typing import Dict, Any, List, Union
import cohere
from langchain_openai import AzureOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.schema import LLMResult
from langchain.schema import AIMessage, HumanMessage, SystemMessage

class OpenSesame:
    def __init__(self, open_sesame_key, project_name):
        self._open_sesame_key = open_sesame_key
        self._project_name = project_name
        self._prompt = None
        self._answer = None
        print("OpenSesame constructor called")
    
    #def AddVectorStore(self, index_name, embedding_model, api_key) :
    #    self.index_name = index_name
     #   self.embedding_model = embedding_model
      #  self.api_key = api_key
        # Make an API call to add the vector store info


    def _send_evaluate_request(self) :
        prompt = self._prompt
        answer = self._answer
        try:
                        print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
                        print('Request body:', json.dumps({
                            'openSesameKey': self._open_sesame_key,
                            'prompt': prompt,
                            'answer': answer,
                            'projectName': self._project_name
                            
                        }))

                        response = requests.post(
                            'https://app.opensesame.dev/api/newEvaluate',
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': self._open_sesame_key
                            },
                            json={
                                'prompt': prompt,
                                'answer': answer,
                                'projectName': self._project_name,
                            }
                        )

                        response.raise_for_status()
                        data = response.json()
                        return data
        except requests.RequestException as error:
                        print('Error in API call:', error)
                        if error.response:
                            print('Error response:', error.response.text)

    def evaluate(self, prompt, answer) :
        self._prompt = prompt
        self._answer = answer
        evaluate_thread = threading.Thread(target=self._send_evaluate_request)
        evaluate_thread.start()
                



class OpenSesame_openai(openai.OpenAI):
    def __init__(self, config: Dict[str, Any]):
        openai_config = {k: v for k, v in config.items() if k in ['api_key', 'organization']}
        super().__init__(**openai_config)
        self._api_key = config['api_key']
        self._open_sesame_key = config['open_sesame_key']
        self._project_name = config['project_name']
        print("OpenSesame_openai constructor called")
        self._monkey_patch_methods()

    def _monkey_patch_methods(self):
        print("monkey_patch_methods called")
        original_create = self.chat.completions.create
        
        def new_create(messages: List[Dict[str, str]], **kwargs):
            print("chat.completions.create called")
            self._log_chat_completion_query(messages, **kwargs)

            result = original_create(messages=messages, **kwargs)
            
            if isinstance(result, openai.types.chat.ChatCompletion):
                self._log_chat_completion_answer(result)
                prompt = next((msg['content'] for msg in messages if msg['role'] == 'user'), None)
                system = next((msg['content'] for msg in messages if msg['role'] == 'system'), None)
                prompt = f"""
                        {system}
                        {prompt}
                        """
                answer = result.choices[0].message.content

                print('Prompt:', prompt)
                print('Answer:', answer)
                def _send_evaluation_request() :
                    try:
                        print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
                        print('Request body:', json.dumps({
                            'openSesameKey': self._open_sesame_key,
                            'prompt': prompt,
                            'answer': answer,
                            'projectName': self._project_name
                            
                        }))

                        response = requests.post(
                            'https://app.opensesame.dev/api/newEvaluate',
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': self._open_sesame_key
                            },
                            json={
                                'prompt': prompt,
                                'answer': answer,
                                'projectName': self._project_name,
                            }
                        )

                        response.raise_for_status()
                        data = response.json()
                        print('Evaluation:', data)
                    except requests.RequestException as error:
                        print('Error in API call:', error)
                        if error.response:
                            print('Error response:', error.response.text)
                
                evaluate_thread = threading.Thread(target=_send_evaluation_request)
                evaluate_thread.start()

            return result

        self.chat.completions.create = new_create

    def _log_chat_completion_query(self, messages: List[Dict[str, str]], **kwargs):
        print('OpenAI Query:')
        print('Model:', kwargs.get('model', 'Not specified'))
        print('Messages:')
        last_user_message = next((msg for msg in reversed(messages) if msg['role'] == 'user'), None)

        if last_user_message:
            print('Last User Query:')
            print(f"  {last_user_message['content']}")
        else:
            print('No user query found in the messages.')

        if 'temperature' in kwargs:
            print('Temperature:', kwargs['temperature'])
        if 'max_tokens' in kwargs:
            print('Max Tokens:', kwargs['max_tokens'])
        print('---')

    def _log_chat_completion_answer(self, result: openai.types.chat.ChatCompletion):
        print('LLM Answer:')
        for i, choice in enumerate(result.choices, 1):
            print(f"Choice {i}:")
            print(f"  Role: {choice.message.role}")
            print(f"  Content: {choice.message.content}")
        print('---')

#*****************************************************************************************************

class OpenSesame_gemini:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        genai.configure(api_key=config['api_key'])
        print("OpenSesame constructor called")

    def GenerativeModel(self, model_name: str):
        return self.GenerativeModelImpl(f"models/{model_name}", self._config)

    class GenerativeModelImpl(genai.GenerativeModel):
        def __init__(self, model_name: str, config: Dict[str, Any]):
            super().__init__(model_name)
            self._model_name = model_name
            self._config = config

        def generate_content(self, prompt: str, **kwargs):
            print("generate_content called")
            self._log_generation_query(prompt, **kwargs)

            result = super().generate_content(prompt, **kwargs)
            
            def _send_evaluation_request() :
                    self._log_generation_answer(result)
                    answer = result.text

                    print('Prompt:', prompt)
                    print('Answer:', answer)
                    
                    try:
                        print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
                        request_body = {
                            'openSesameKey': self._config['open_sesame_key'],
                            'prompt': prompt,
                            'answer': answer,
                            'projectName': self._config['project_name']
                        }
                        print('Request body:', json.dumps(request_body))

                        response = requests.post(
                            'https://app.opensesame.dev/api/newEvaluate',
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': self._config['open_sesame_key']
                            },
                            json=request_body
                        )

                        response.raise_for_status()
                        data = response.json()
                        print('Evaluation:', data)
                    except requests.RequestException as error:
                        print('Error in API call:', error)
                        if error.response:
                            print('Error response:', error.response.text)

            if result.text :
                evaluate_thread = threading.Thread(target=_send_evaluation_request)
                evaluate_thread.start()  
            
            return result

        def _log_generation_query(self, prompt: str, **kwargs):
            print('Gemini Query:')
            print('Model:', self._model_name)
            print('Prompt:', prompt)

            if 'temperature' in kwargs:
                print('Temperature:', kwargs['temperature'])
            if 'max_output_tokens' in kwargs:
                print('Max Output Tokens:', kwargs['max_output_tokens'])
            print('---')

        def _log_generation_answer(self, result):
            print('Gemini Answer:')
            print(f"Content: {result.text}")
            print('---')

# ********************************************************************************************************************

class OpenSesame_anthropic:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config["api_key"]
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
        self.anthropic_url = "https://api.anthropic.com/v1/messages"
        self.anthropic_version = "2023-06-01"

    class Messages:
        def __init__(self, parent):
            self.parent = parent
        
        def create(self, model: str, messages: List[Dict[str, str]], **kwargs):
            headers = {
                "x-api-key": self.parent.api_key,
                "anthropic-version": self.parent.anthropic_version,
                "content-type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": messages,
                **kwargs
            }
            
            # Call Anthropic API
            response = requests.post(self.parent.anthropic_url, json=data, headers=headers)
            prompt = next((msg['content'] for msg in messages if msg['role'] == 'user'), '')
            if kwargs["system"] :
                prompt = f"""
                        {kwargs["system"]},
                        {prompt}
                """
            
            if response.status_code != 200:
                raise Exception(f"Anthropic API error: {response.status_code} {response.text}")
            
            result = response.json()
            content = result["content"]
            completion = content[0]["text"]
            
            # Immediately send the result to OpenSesame API
            evaluate_thread = threading.Thread(target=self._send_evaluation_request,args=(prompt, completion))
            evaluate_thread.start()
            
            return result
        
        def _send_evaluation_request(self, prompt, answer: str):
            
            print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
            print('Request body:', json.dumps({
                'openSesameKey': self.parent.open_sesame_key,
                'prompt': prompt,
                'answer': answer
            }))
            
            try:
                response = requests.post(
                    'https://app.opensesame.dev/api/newEvaluate',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': self.parent.open_sesame_key
                    },
                    json={
                        'prompt': prompt,
                        'answer': answer,
                        'projectName': self.parent.project_name
                    }
                )
                response.raise_for_status()
                data = response.json()
                print('Evaluation:', data)
                print("OpenSesame API called succsefully")
            except requests.RequestException as error:
                print('Error in API call:', error)
                if error.response:
                    print('Error response:', error.response.text)

        def _wrap_response(self, content: str):
            # Wrap the content in a simple object to mimic the Anthropic API's return structure
            class Response:
                def __init__(self, content):
                    self.content = content
            
            return Response(content)

# *******************************************************************
        

class OpenSesame_groq:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config["api_key"]
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
        self.client = Groq(api_key=config["api_key"])

    class ChatCompletions:
        def __init__(self, parent):
            self.parent = parent
        
        def create(self, model: str, messages: List[Dict[str, str]], **kwargs):
            chat_completion = self.parent.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            print("groq called successfully")
            completion_text = chat_completion.choices[0].message.content
            
            evaluate_thread = threading.Thread(target=self._send_evaluation_request,args=(messages, completion_text))
            evaluate_thread.start() 
            
            return chat_completion
        
        def _send_evaluation_request(self, messages: List[Dict[str, str]], answer: str):
            prompt = next((msg['content'] for msg in messages if msg['role'] == 'user'), '')
            system = next((msg['content'] for msg in messages if msg['role'] == 'system'), '')
            prompt = f"""
                        {system}
                        {prompt}
                     """
            print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
            request_body = {
                'openSesameKey': self.parent.open_sesame_key,
                'prompt': prompt,
                'answer': answer,
                'projectName': self.parent.project_name
            }
            print('Request body:', request_body)
            
            try:
                response = requests.post(
                    'https://app.opensesame.dev/api/newEvaluate',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': self.parent.open_sesame_key
                    },
                    json=request_body
                )
                response.raise_for_status()
                data = response.json()
                print('Evaluation:', data)
                print("OpenSesame API called succesfully")
                return data
            except requests.RequestException as error:
                print('Error in API call:', error)
                if error.response:
                    print('Error response:', error.response.text)
                return None
            
# ********************************************************************************************
            
class OpenSesame_huggingface:
    def __init__(self, config: Dict[str, Any]):
        self.hf_api_token = config["hf_api_token"]
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
        self.hf_api_url = "https://api-inference.huggingface.co/models"

    def generate_text(self, model_name: str, prompt: str, **kwargs):
        headers = {"Authorization": f"Bearer {self.hf_api_token}"}
        payload = {"inputs": prompt, **kwargs}

        # Call Hugging Face API
        response =  requests.post(f"{self.hf_api_url}/{model_name}", headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Hugging Face API error: {response.status_code} {response.text}")

        result = response.json()

        # Extract the generated text
        generated_text = result[0]['generated_text'] if isinstance(result, list) else result

        # Send the result to OpenSesame API for evaluation
        evaluate_thread = threading.Thread(target=self._send_evaluation_request,args=(prompt,generated_text))
        evaluate_thread.start()

        return result

    def _send_evaluation_request(self, prompt: str, answer: str):
        print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
        request_body = {
            'openSesameKey': self.open_sesame_key,
            'prompt': prompt,
            'answer': answer,
            'projectName': self.project_name
        }
        print('Request body:', request_body)
        
        try:
            response = requests.post(
                    'https://app.opensesame.dev/api/newEvaluate',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': self.open_sesame_key
                    },
                    json=request_body
                )
            response.raise_for_status()
            data = response.json()
            print('Evaluation:', data)
            print("OpenSesame API called successfully")
            return data
        except requests.RequestException as error:
            print('Error in API call:', error)
            if error.response:
                print('Error response:', error.response.text)
            return None
        
#***************************************************************************************************
        
class OpenSesame_cohere:
    def __init__(self, config: Dict[str, Any]):
        self.cohere_api_key = config["api_key"]
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
        self.client = cohere.Client(config["api_key"])

    def chat(self, message: str, **kwargs):
        # Call Cohere's Chat API with all provided parameters

        response = self.client.chat(
            message=message,
            **kwargs
        )

        # Extract the chatbot's response
        answer = response.text if hasattr(response, 'text') else response.generations[0].text

        if kwargs["preamble"] :
            message = kwargs["preamble"] + " " +message

        # Send the result to OpenSesame API for evaluation
        evaluate_thread = threading.Thread(target=self._send_evaluation_request,args=(message, answer))
        evaluate_thread.start()

        return response

    def _send_evaluation_request(self, user_message: str, answer: str):
        prompt = user_message

        print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
        request_body = {
            'openSesameKey': self.open_sesame_key,
            'prompt': prompt,
            'answer': answer,
            'projectName': self.project_name
        }
        print('Request body:', request_body)
        
        try:
            response = requests.post(
                'https://app.opensesame.dev/api/newEvaluate',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': self.open_sesame_key
                },
                json=request_body
            )
            response.raise_for_status()
            data = response.json()
            print('Evaluation:', data)
            return data
        except requests.RequestException as error:
            print('Error in API call:', error)
            if error.response:
                print('Error response:', error.response.text)
            return None
        


class OpenSesame_azure_openai:
    def __init__(self, config: Dict[str, Any]):
        self.llm = AzureOpenAI(
            api_key=config["api_key"],
            azure_endpoint=config["azure_endpoint"],
            deployment_name=config["deployment"],
            api_version=config["api_version"]
        )

        self._open_sesame_key = config['open_sesame_key']
        self._project_name = config['project_name']

        print("OpenSesame_azure_openai constructor called")

    def call(self, prompt: str, **kwargs):
        print("call method invoked")
        self._log_prompt(prompt, **kwargs)

        response = self.llm.invoke(prompt, **kwargs)
        
        if response:
            self._log_response(response)

            def _send_evaluation_request():
                try:
                    print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
                    print('Request body:', {
                        'openSesameKey': self._open_sesame_key,
                        'prompt': prompt,
                        'answer': response,
                        'projectName': self._project_name
                    })

                    response_eval = requests.post(
                        'https://app.opensesame.dev/api/newEvaluate',
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': self._open_sesame_key
                        },
                        json={
                            'openSesameKey': self._open_sesame_key,
                            'prompt': prompt,
                            'answer': response,
                            'projectName': self._project_name
                        }
                    )

                    response_eval.raise_for_status()
                    data = response_eval.json()
                    print('Evaluation:', data)
                except requests.RequestException as error:
                    print('Error in API call:', error)
                    if error.response:
                        print('Error response:', error.response.text)
                
            evaluate_thread = threading.Thread(target=_send_evaluation_request)
            evaluate_thread.start()

        return response

    def _log_prompt(self, prompt: str, **kwargs):
        print('LangChain Azure OpenAI Query:')
        print(f'Prompt: {prompt}')

        if 'max_tokens' in kwargs:
            print('Max Tokens:', kwargs['max_tokens'])
        if 'temperature' in kwargs:
            print('Temperature:', kwargs['temperature'])
        print('---')

    def _log_response(self, response: str):
        print('LLM Response:')
        print(response)
        print('---')


class OpenSesame_RAG_callback(BaseCallbackHandler):
    def __init__(self, config):
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
        self.current_prompt = None
        self.current_answer = None
        self.chain_inputs = {}
        self.chain_outputs = {}
        self.sent_request = False

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        self.current_prompt = prompts[0] if prompts else None
        print(f"LLM started. Prompt: {self.current_prompt}")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        self.current_answer = response.generations[0][0].text if response.generations else None
        print(f"LLM ended. Answer: {self.current_answer}")
        if self.sent_request == False :
            evaluate_thread = threading.Thread(target=self._send_evaluation_request)
            evaluate_thread.start()
            self.sent_request=True

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        self.chain_inputs = inputs
        self.current_prompt = self._extract_prompt(inputs)
        print(f"Chain started.")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        self.chain_outputs = outputs
        print(f"Chain ended.")
        self.current_answer = self._extract_answer(self.chain_outputs)
        if self.sent_request == False :
            evaluate_thread = threading.Thread(target=self._send_evaluation_request)
            evaluate_thread.start()
        self.sent_request=True
        

    def _extract_prompt(self, inputs: Union[Dict[str, Any], str, HumanMessage, AIMessage, SystemMessage]) -> str:
        if isinstance(inputs, (str,HumanMessage,SystemMessage)):
            return inputs.content if hasattr(inputs, 'content') else str(inputs)
        if isinstance(inputs, dict):
            for key in ['query', 'question', 'input', 'prompt']:
                if key in inputs:
                    value = inputs[key]
                    return value.content if hasattr(value, 'content') else str(value)
            return str(next(iter(inputs.values()), ''))
        return str(inputs)

    def _extract_answer(self, outputs: Union[Dict[str, Any], AIMessage, str]) -> str:
        if isinstance(outputs, (AIMessage)):
            return outputs.content
        if isinstance(outputs, str):
            return outputs
        if isinstance(outputs, dict):
            for key in ['output', 'answer', 'result', 'response', 'text']:
                if key in outputs:
                    value = outputs[key]
                    return value.content if hasattr(value, 'content') else str(value)
            return str(next(iter(outputs.values()), ''))
        return str(outputs)

    def _send_evaluation_request(self):
        if not self.current_prompt or not self.current_answer:
            print(f"Prompt or answer is missing. Prompt: {self.current_prompt}, Answer: {self.current_answer}")
            return

        try:
            print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
            request_body = {
                'openSesameKey': self.open_sesame_key,
                'prompt': self.current_prompt,
                'answer': self.current_answer,
                'projectName': self.project_name
            }
            print('Request body:', json.dumps(request_body))

            response = requests.post(
                'https://app.opensesame.dev/api/newEvaluate',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': self.open_sesame_key
                },
                json=request_body
            )

            response.raise_for_status()
            data = response.json()
            print('Evaluation:', data)
        except requests.RequestException as error:
            print('Error in API call:', error)
            if error.response:
                print('Error response:', error.response.text)

class OpenSesame_langchain:
    def __init__(self, config: Dict[str, Any]):
        self.open_sesame_key = config["open_sesame_key"]
        self.project_name = config["project_name"]
    def rag_callback_manager(self):
        config = {"open_sesame_key": self.open_sesame_key, "project_name": self.project_name}
        os_callback =OpenSesame_RAG_callback(config)
        callback_manager = CallbackManager([os_callback])
        return callback_manager







