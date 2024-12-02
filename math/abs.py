import numpy as np
import matplotlib.pyplot as plt

# 创建包含正负数的数组
arr = np.array([-5, -2, 0, 3, 7])

# 计算数组的绝对值
abs_values = np.abs(arr)

# 创建图表
plt.figure(figsize=(8, 4))

# 绘制原始数组
plt.plot(arr, arr, label='Original Values', marker='o', linestyle='-', color='b')

# 绘制绝对值数组
plt.plot(arr, abs_values, label='Absolute Values', marker='o', linestyle='--', color='r')

# 设置x轴刻度为arr数组中的值
plt.xticks(arr)

# 添加图例
plt.legend()

# 添加标题和轴标签
plt.title('Original vs Absolute Values')
plt.xlabel('Original Array Values')
plt.ylabel('Value')

# 显示网格
plt.grid(True)

# 显示图形
plt.show()
