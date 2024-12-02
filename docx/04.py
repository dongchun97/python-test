from langchain_ollama import OllamaLLM

# 创建 OllamaLLM 实例
ollama = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")

# 调用 generate 方法，传入列表作为 prompts 参数
response = ollama.generate(prompts=["请用中文解释为什么天空是蓝色的？,写200字"])

# 提取返回的回答文本
if response.generations:
    print(response.generations[0][0].text)  # 确保正确访问嵌套结构
else:
    print("未收到生成结果")
