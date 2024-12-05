import os
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from docx import Document

# 1. 定义读取大纲文件的函数，增加层级的支持
def read_outline_from_docx(file_path):
    document = Document(file_path)
    outline = []
    current_level = 1  # 初始层级为 1
    
    for para in document.paragraphs:
        # 判断层级
        if para.style.name.startswith('Heading'):
            level = int(para.style.name.replace('Heading ', ''))
            title = para.text.strip()
            if level > current_level:
                current_level = level  # 更新层级
            elif level < current_level:
                current_level = level  # 如果返回上一层级，更新层级
            outline.append({"title": title, "word_count": None, "level": current_level})
        else:
            # 其他段落不作为标题处理
            continue

    return outline

# 2. 定义保存文档的函数，支持多层级的标题
def save_document_to_docx(content, output_file_path, outline):
    doc = Document()
    
    for section in outline:
        title = section["title"]
        level = section["level"]
        
        # 根据层级设置标题样式
        doc.add_heading(title, level=level)  # 根据层级自动选择 Heading 1, Heading 2, ..., Heading n

        # 添加章节内容
        doc.add_paragraph(content.get(section["title"], "无内容"))
    
    doc.save(output_file_path)

# 3. 设置大纲模板
prompt_template = PromptTemplate(
    input_variables=["title", "word_count", "references"],
    template="请用中文写一篇关于 '{title}' 字数约 {word_count}。参考以下资料：{references}"
)

# 4. 初始化 Ollama LLM
llm = OllamaLLM(model="llama3.2")

# 5. 参考资料模块
class ReferenceModule:
    def __init__(self):
        self.references = {}

    def load_main_reference(self, main_reference_file):
        """加载主参考资料文件"""
        if os.path.exists(main_reference_file):
            with open(main_reference_file, "r", encoding="utf-8") as file:
                content = file.read().splitlines()
            self.references["main_file"] = content
        else:
            print(f"警告：主参考文件 {main_reference_file} 未找到。")

    def load_auxiliary_references(self, reference_folder):
        """加载辅助参考资料文件夹中的所有文件"""
        if os.path.exists(reference_folder):
            for file_name in os.listdir(reference_folder):
                file_path = os.path.join(reference_folder, file_name)
                if os.path.isfile(file_path) and file_name.endswith(".txt"):  # 只加载 .txt 文件
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read().splitlines()
                    self.references[file_name] = content
        else:
            print(f"警告：参考资料文件夹 {reference_folder} 未找到。")

    def get_references_for_section(self, section_title):
        """根据章节标题提取相关的参考资料"""
        references = []
        # 先从主参考文件中查找
        if "main_file" in self.references:
            for line in self.references["main_file"]:
                if section_title.lower() in line.lower():
                    references.append(line)
        
        # 从辅助参考文件中查找
        for ref_file, ref_content in self.references.items():
            if ref_file != "main_file":  # 排除主文件
                for line in ref_content:
                    if section_title.lower() in line.lower():
                        references.append(line)
        return references

    def format_references(self, references):
        """将参考资料格式化为字符串"""
        return "\n".join(references) if references else "无参考资料"

def main():
    # 6. 配置文件路径（在这里修改路径）
    outline_file_path = "files/input/input.docx"  # 大纲文件路径
    main_reference_file_path = "files/references/tender.docx"  # 主参考资料文件路径
    auxiliary_reference_folder = ""  # 辅助参考资料文件夹路径
    output_file_path = "files/output/file.docx"  # 输出文件路径

    # 7. 读取本地大纲文件
    outline = read_outline_from_docx(outline_file_path)

    # 8. 参考资料模块（加载主参考文件和辅助参考文件夹）
    reference_module = ReferenceModule()

    # 加载主参考文件
    if main_reference_file_path:
        reference_module.load_main_reference(main_reference_file_path)

    # 加载辅助参考文件夹
    if auxiliary_reference_folder:
        reference_module.load_auxiliary_references(auxiliary_reference_folder)

    # 9. 生成每个章节内容并合成文档
    content = {}
    for section in outline:
        # 如果参考资料存在，则添加参考资料；如果没有，则不加入参考资料
        references = reference_module.get_references_for_section(section["title"])
        formatted_references = reference_module.format_references(references)
        
        # 如果没有字数，AI自动决定字数
        if section["word_count"] is None:
            prompt = prompt_template.format(title=section["title"], word_count=1000, references=formatted_references)  # 默认1000字
            section_content = llm(prompt)  # 直接调用模型
            content[section["title"]] = section_content
        else:
            prompt = prompt_template.format(title=section["title"], word_count=section["word_count"], references=formatted_references)
            section_content = llm(prompt)  # 直接调用模型
            content[section["title"]] = section_content

    # 10. 保存生成的文档
    save_document_to_docx(content, output_file_path, outline)

    print(f"文档已保存到 {output_file_path}")

if __name__ == "__main__":
    main()
