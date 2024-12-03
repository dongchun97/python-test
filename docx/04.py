import os
import requests
from docx import Document

 
def read_outline_from_docx(docx_path):
    """
    从 docx 文件中读取目录大纲
    返回：包含章节标题及其级别的列表
    """
    document = Document(docx_path)
    outline = []
    for paragraph in document.paragraphs:
        if paragraph.style.name.startswith("Heading"):  # 检测标题样式
            level = int(paragraph.style.name.split(" ")[1])  # 获取标题级别
            outline.append((level, paragraph.text.strip())) 
    return outline

def read_and_analyze_requirements(req_docx_path):
    """
    读取并分析需求文件的内容
    返回：需求关键内容（以段落为基础）
    """
    document = Document(req_docx_path)
    requirements = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:  # 仅保留非空段落
            requirements.append(text)
    return requirements

if __name__ == "__main__":
    # 固定文件路径
    docx_path = "./docx/index.docx"  # 包含目录大纲的文件路径
    # req_docx_path = "./docx/tender.doc"  # 需求文件路径
    # output_path = "./docx/out/file.docx"  # 生成的文档保存路径

    # Ollama 使用的模型名称
    # ollama_model = "llama3.2"  # 可根据本地模型调整，例如 "llama2" 或其他模型

    # 运行主程序
    read=read_outline_from_docx(docx_path)
    print(read)