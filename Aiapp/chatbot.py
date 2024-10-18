import requests

api_endpoint = 'http://localhost:11434/api/chat'

messages = []

while True:
    user_input = input()
    messages.append({'role': 'user', 'content': user_input})
    data = {'model': 'llama2','stream': False,'messages': messages}
    response = requests.post(api_endpoint, json=data)

    if response.status_code == 200:
        response_data = response.json()
        assistant_response = response_data['message']['content']
        messages.append({'role': 'chatbot', 'content': 'assistant_reply'})
        print(f'Assistant: {assistant_response}')
    else:
        print('Failed to get response from Ollama API')

