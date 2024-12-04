# +---------------------------------------------+
# |                   DocProcessor              |
# +---------------------------------------------+
# | - doc_path: str                              |
# | - outline: dict                              |
# | - references: dict[str, DocReference]       |
# ｜ - document: Document（）                       |
# | - api_caller: ApiCaller                      |
# +---------------------------------------------+
# | + load_document(): None                      |
# | + extract_outline(): dict                    |
# | + fill_content(): None                        |
# | + save_document(): None                      |
# | + process_outline(): None                    |
# | + add_reference(name: str, reference: DocReference): None |
# | + generate_content(level: int, text: str): str |
# | + adjust_content(section: str, feedback: str): None |
# +---------------------------------------------+

# +---------------------------------------------+
# |                   ApiCaller                 |
# +---------------------------------------------+
# | - api_type: str                              |
# | - api_key: str                               |
# | - endpoint: str                              |
# +---------------------------------------------+
# | + call_api(prompt: str) -> str               |
# +---------------------------------------------+

# +---------------------------------------------+
# |                DocReference                 |
# +---------------------------------------------+
# | - doc_path: str                              |
# +---------------------------------------------+
# | + extract_content(outline_section: str) -> str |
# +---------------------------------------------+


# 1-DocProcessor
# 主控制类，负责处理长文档（docA），读取大纲、分级处理内容，并调用API生成文档内容。

# 属性：

# doc_path：文档路径。
# outline：存储文档大纲的字典，每个级别对应其子级内容。
# references：字典，用于存储参考文档（如docB、docC等）。
# api_caller：一个ApiCaller实例，用于和AI接口交互。
# 主要方法：

# load_document()：加载长文档并提取大纲。
# extract_outline()：提取文档大纲为字典。
# process_outline()：按层级逐级处理大纲内容，生成并填充文档内容。
# add_reference(name, reference)：增加参考文档对象。
# generate_content(level, text)：调用API生成内容，自动处理字数要求。
# adjust_content(section, feedback)：接收反馈并修改特定部分内容。


# 2-ApiCaller
# 负责与AI API交互，支持扩展至不同API类型（如OpenAI API、Ollama API等）。

# 属性：

# api_type：API类型（如"OpenAI"、"Ollama"等）。
# api_key：API密钥。
# endpoint：API端点。
# 方法：

# call_api(prompt)：调用指定API，发送prompt并返回生成结果。


# 3-DocReference
# 用于处理参考文档（docB、docC等），可以提取特定大纲部分的内容，用于辅助生成。

# 属性：

# doc_path：参考文档路径。
# 方法：

# extract_content(outline_section)：从参考文档中提取特定大纲部分的内容。


from docx import Document
import os


# 加载大纲并处理
class DocProcessor:
    def __init__(self, doc_path, api_caller):
        self.doc_path = doc_path
        self.api_caller = api_caller
        self.outline = {}
        self.document=Document()
        self.references = {}

    def load_document(self):
        """加载文档"""
        doc = Document(self.doc_path)
        self.extract_outline(doc)

    def extract_outline(self, doc):
        """提取文档大纲构建一个嵌套字典结构"""
        self.outline = {"title": "Document Title", "content": "", "subsections": {}}
        current_section = None

        for paragraph in doc.paragraphs:
            if paragraph.style.name.startswith('Heading'):
                level = int(paragraph.style.name[-1])
                title = paragraph.text.strip()

                if level == 1:  # 一级标题
                    current_section = {"content": "", "subsections": {}}
                    self.outline['subsections'][title] = current_section
                elif level == 2 and current_section:  # 二级标题
                    current_section['subsections'][title] = {"content": "", "subsections": {}}
                elif level == 3 and current_section:  # 三级标题
                    current_section['subsections'][title] = {"content": "", "subsections": {}}
        print(self.outline)

    def fill_content(self, section, level=1):
        """填充大纲内容，递归调用AI生成内容"""
        # 创建内容段落
        section_title = section.get('title', 'Untitled Section')
        self.document.add_heading(section_title, level)

        # 调用API生成内容
        section['content'] = self.api_caller.call_api(f"请生成{level}级标题的内容：{section_title}")
        self.document.add_paragraph(section['content'])

        # 递归处理子级
        for subsection in section['subsections'].values():
            self.fill_content(subsection, level + 1)

    def save_document(self, file_path):
        """保存填充后的文档"""
        self.document.save(file_path)
        print(f"文档已保存到 {file_path}")

    def process_outline(self, outline=None, level=1):
        """递归处理大纲，生成内容"""
        if outline is None:
            outline = self.outline

        for section, sub_sections in outline.items():
            # 检查字数要求
            if "(" in section:
                section_title, word_count = section.split("(")
                word_count = int(word_count.strip(")"))
                if word_count > 2000:
                    # 调用AI生成子目录
                    sub_sections = self.generate_sub_outline(section_title)
            
            # 调用API生成内容
            content = self.generate_content(level, section)
            print(f"填充内容：{content}")
            
            # 递归处理子级大纲
            if sub_sections:
                self.process_outline(sub_sections, level + 1)

    def _add_to_outline(self, outline, level, content):
        """递归存储大纲层级内容"""
        # 实现逻辑：递归生成嵌套字典
        pass

    def add_reference(self, name, reference):
        """增加参考文档对象，将一个外部文档引用添加到当前文档中"""
        self.references[name] = reference

    #  生成大纲级别的内容
    def generate_content(self, level, text):
        """根据输入的文本生成对应级别的内容，调用 API 生成内容"""
        # 根据字数要求生成内容
        prompt = f"请根据以下内容生成约{level}字：\n{text}"
        content = self.api_caller.call_api(prompt)
        return content

    # 拆分大纲并处理长内容


# 调用AI API生成内容
class ApiCaller:
    def __init__(self, api_type, api_key, endpoint):
        self.api_type = api_type
        self.api_key = api_key
        self.endpoint = endpoint

    def call_api(self, prompt):
        """调用AI生成内容"""
        # 处理API调用，返回生成的内容
        pass


if __name__ == "__main__":
    # 示例用法
    doc_path = "./files/input/a_things.docx"
    api_caller = ApiCaller("OpenAI", "OPENAI_API_KEY", "https://api.openai.com/v1/completions")
    doc_processor = DocProcessor(doc_path, api_caller)
    doc_processor.load_document()

    # # 填充内容
    # doc_processor.fill_content(doc_processor.outline)
    
    # # 保存填充后的文档
    # doc_processor.save_document("./files/output/a_things.docx")
    doc_processor.extract_outline(doc_processor.document)