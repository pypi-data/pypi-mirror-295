import requests
from io import BytesIO
from PIL import Image
import base64
import re
import json
import segmind_workflow
from importlib.resources import read_text

funcition_call_url = "https://api.segmind.com/v1"
function_call_sequence_url = "https://c670-194-68-245-76.ngrok-free.app"

class Workflow:
    def __init__(self, api_key):
        self.api_key = api_key
        self.context = ""
        self.query_sequence = []
        self.call_sequence = []
        self.results = None
        self.credits_left = None
        self.price_list = {
            "function1": 10,
            "function2": 20,
            "function3": 30
        }
        self.sequence_generated = False
        self.call_made = False
        # with open('slug_data.json') as f:
        #     self.slug_data = json.load(f)
        file_content = read_text(segmind_workflow, 'slug_data.json')
        self.slug_data = json.loads(file_content)

    def query(self, prompt):
        params = {
            "query": prompt,
            "prev_query": self.context,
            "sequence": self.call_sequence
        }
        response = requests.get(function_call_sequence_url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.call_sequence = data.get("result")
            self.context = data.get("next_query")
            self.query_sequence.append(prompt)
            self.sequence_generated = True
        else:
            raise Exception("Failed to query the API.")
    
    def get_sequence(self):
        if not self.sequence_generated:
            raise Exception("Error: No query sequence generated yet. Please call query() first.")
        return self.call_sequence

    def call(self, data):
        if not self.sequence_generated:
            raise Exception("Error: Call sequence not generated. Please call query() first.")
        
        self.results = []
        for function_call in self.call_sequence:
            for _ in range(function_call.count("INP")):
                idx = function_call.find("INP")
                d = data.pop(0)
                if isinstance(d, Image.Image):
                    buffered = BytesIO()
                    d.save(buffered, format="PNG")
                    d = base64.b64encode(buffered.getvalue()).decode('utf-8')
                elif isinstance(d, str):
                    d = d
                else:
                    raise Exception('Unknown type as input')
                
            for _ in range(function_call.count("OUT[")):
                match = re.search(r"OUT\[(\d+)\]", function_call)
                idx = match.group(1)
                d = self.results[idx]
                if isinstance(d, Image.Image):
                    buffered = BytesIO()
                    d.save(buffered, format="PNG")
                    d = base64.b64encode(buffered.getvalue()).decode('utf-8')
                elif isinstance(d, str):
                    d = d
                else:
                    raise Exception('Unknown type as input (in OUT of another function)')
                function_call = function_call[:idx] + d + function_call[idx+5+len(str(idx)):]
            result = self.make_function_call(function_call)
            self.results.append(result)
        self.call_made = True

    def make_function_call(self, function_call):
        function_name = function_call.split('(')[0]
        function_name = self.slug_data[function_name]
        params_string = function_call.split('(')[1].split(')')[0]
        params_list = params_string.split(',')
        input_data = {}
        for param in params_list:
            key, value = param.split('=')
            key = key.strip().strip("'\"")
            value = value.strip().strip("'\"")
            input_data[str(key)] = value
        # print(input_data)
        url = f"{funcition_call_url}/{function_name}"
        response = requests.post(url, json=input_data, headers={'x-api-key': self.api_key})
        if response.status_code == 200:
            self.credits_left = response.headers.get('x-remaining-credits')
            content_type = response.headers.get('Content-Type')
            if 'image' in content_type:
                return Image.open(BytesIO(response.content))
            elif 'json' in content_type:
                data = response.json()
                if 'choices' in data:
                    data = str(data['choices'][0]['message']['content'])
                elif 'content' in data:
                    data = str(data['content'])
                return str(data)
            elif 'octet-stream' in content_type:
                return Image.open(BytesIO(response.content))
            else:
                print(content_type)
                return response
        else:
            raise Exception(
                    f"Failed to call request for {function_name}\n"
                    f"Status Code: {response.status_code}\n"
                    f"Error Message: {response.text}"
                )
        
    def get_result(self):
        if not self.call_made:
            raise Exception("Error: No function call made yet. Please call the call() function first.")
        return self.results

    def w_of_cost(self):
        if not self.sequence_generated:
            raise Exception("Error: No function sequence available. Please call query() first.")
        
        # total_cost = sum(self.price_list.get(func, 0) for func in self.call_sequence)
        total_cost = 0
        print("Not implemented till now")
        return total_cost

    def w_of_credits_left(self):
        if self.credits_left is None:
            raise Exception("Error: No function call has been made yet. Please call the call() function first to know the credits left.")
        return f"Credits left: {self.credits_left}"

    def reset(self):
        self.context = ""
        self.query_sequence = []
        self.call_sequence = []
        self.results = None
        self.sequence_generated = False
        self.call_made = False

    def visualize(self):
        if not self.call_made:
            raise Exception("Error: No function call made yet. Please call the call() function first.")
        pass