import numpy as np
import matplotlib.pyplot as plt

val_1=2
val_2=5
val_3=3
# 创建包含正负数的数组
arr = np.linspace(-3,10,14)

# 计算数组的绝对值
abs_reduce_1 = np.abs(arr-val_1)
abs_reduce_2 = np.abs(arr-val_2)
# abs_reduce_3 = np.abs(arr-val_3)
add=abs_reduce_2-abs_reduce_1

# 创建图表
# plt.figure(figsize=(8, 4))

# 绘制原始数组
# plt.plot(arr, arr, label='Original Values', marker='o', linestyle='-', color='b')

# 绘制绝对值数组
plt.plot(arr, abs_reduce_1, label='Absolute Values', marker='o', linestyle='--', color='r')
plt.plot(arr, abs_reduce_2,marker='o', linestyle='--', color='b')
plt.plot(arr, add,marker='o', linestyle='--', color='g')

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
