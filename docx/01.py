import os
import requests
from docx import Document
from tqdm import tqdm


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


def ask_ollama(question, model="llama2"):
    """
    调用本地 Ollama 接口回答问题
    参数:
        question: 提问内容
        model: Ollama 使用的模型名称
    返回:
        Ollama 的回答文本
    """
    url = "http://localhost:11434/api/completion"  # Ollama 本地 API 地址
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": question,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        return result.get("completion", "（Ollama 未返回内容）")
    except Exception as e:
        print(f"调用 Ollama 接口失败：{e}")
        return "（无法生成内容，请检查 Ollama 配置）"


def match_and_fill_outline_with_ollama(outline, requirements, model="llama2"):
    """
    根据目录大纲和需求内容，调用 Ollama 自动生成回答
    返回：填充后的目录内容
    """
    content = []
    for level, title in tqdm(outline, desc="自动生成目录内容", unit="标题"):
        # 将需求内容合并为上下文
        context = "\n".join(requirements)
        question = f"根据以下需求内容，回答与标题 '{title}' 相关的内容：\n{context}"
        
        # 调用 Ollama 获取回答
        answer = ask_ollama(question, model)
        if not answer.strip():  # 如果 Ollama 没有回答内容，留空等待人工填写
            answer = "（无匹配内容，请后续手动补充）"

        content.append((level, title, answer))
    return content


def write_to_new_docx(output_path, content):
    """
    将生成的内容写入新的 docx 文件
    """
    document = Document()
    for level, title, answer in tqdm(content, desc="写入文档", unit="章节"):
        # 添加标题
        document.add_heading(title, level=level)
        # 添加内容
        document.add_paragraph(answer)
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # 保存文档
    document.save(output_path)
    print(f"文档已保存到：{output_path}")


def main(docx_path, req_docx_path, output_path, model="llama2"):
    """
    主程序
    """
    if not os.path.exists(docx_path):
        print(f"目录文件路径无效：{docx_path}")
        return

    outline = read_outline_from_docx(docx_path)
    if not outline:
        print("未在文档中检测到目录大纲，请检查文件内容！")
        return

    if not os.path.exists(req_docx_path):
        print(f"需求文件路径无效：{req_docx_path}")
        return

    requirements = read_and_analyze_requirements(req_docx_path)
    if not requirements:
        print("需求文件为空或未能提取有效内容，请检查文件！")
        return

    print("\n正在根据需求文件生成内容，请稍候...\n")
    auto_filled_content = match_and_fill_outline_with_ollama(outline, requirements, model)

    print("\n正在写入文档，请稍候...\n")
    write_to_new_docx(output_path, auto_filled_content)


if __name__ == "__main__":
    # 固定文件路径
    docx_path = "./docx/index.docx"  # 包含目录大纲的文件路径
    req_docx_path = "./docx/tender.doc"  # 需求文件路径
    output_path = "./docx/out/file.docx"  # 生成的文档保存路径

    # Ollama 使用的模型名称
    ollama_model = "llama3.2"  # 可根据本地模型调整，例如 "llama2" 或其他模型

    # 运行主程序
    main(docx_path, req_docx_path, output_path, model=ollama_model)
