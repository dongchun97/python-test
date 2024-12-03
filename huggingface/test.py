from transformers import pipeline

# 加载预训练的文本生成模型
generator = pipeline('text-generation', model='gpt2')

# 使用模型生成文本
print(generator("你好"))
