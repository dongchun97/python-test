import requests
import json
import gradio as gr

def generate_chat_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.2",
        "prompt": prompt
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        final_response = data.get("completion", "无回答")
        return final_response
    else:
        print("Error:", response.status_code, response.text)
        return "无法获得回答"

demo = gr.Interface(
    fn=generate_chat_response,
    inputs=gr.Textbox(label="问题"),
    outputs=gr.Textbox(lines=2, placeholder="回答")
)

demo.launch(share=True)

