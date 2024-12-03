from langchain_ollama import OllamaLLM

# 创建 OllamaLLM 实例
ollama = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")

# 调用 generate 方法，传入列表作为 prompts 参数
response = ollama.generate(prompts=["写一个关于清华大学集成电路学院展厅设计方案的大纲？,写200字"])

# 提取返回的回答文本
if response.generations:
    print(response.generations[0][0].text)  # 确保正确访问嵌套结构
else:
    print("未收到生成结果")