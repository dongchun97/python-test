import os
import requests
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def ensure_style_exists(doc, style_name, style_type=WD_STYLE_TYPE.PARAGRAPH, left_indent=Inches(0.5)):
    if style_name not in doc.styles:
        style = doc.styles.add_style(style_name, style_type)
        style.paragraph_format.left_indent = left_indent
        style.font.name = '宋体'
    return doc.styles[style_name]

def answer_question(question):
    # 调用Ollama来生成回答
    url = "http://localhost:11434/api/completion"  # 假设 Ollama 运行在本地
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.2",  # 假设你使用的是模型名称
        "prompt": question,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 如果失败会抛出异常
        result = response.json()
        return result.get('completion', '无回答')
    except requests.exceptions.RequestException as e:
        print(f"请求 Ollama 时出错: {e}")
        return "无法获得回答"

def process_document(doc):
    indent_style = ensure_style_exists(doc, '正文缩进')
    
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            question = para.text
            answer = answer_question(question)
            
            # 添加回答段落
            new_para = doc.add_paragraph(answer)
            new_para.style = indent_style

if __name__ == "__main__":
    input_doc = './docx/index.docx'
    output_doc = './docx/out/index_updated.docx'
    
    if not os.path.exists(input_doc):
        print(f"文件 {input_doc} 不存在")
    else:
        doc = Document(input_doc)
        
        # 确保输出目录存在
        if not os.path.exists(os.path.dirname(output_doc)):
            os.makedirs(os.path.dirname(output_doc))
        
        process_document(doc)
        doc.save(output_doc)
        print(f"文档已处理并保存为 {output_doc}")
