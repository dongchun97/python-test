import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

iris=sns.load_dataset('iris')
# print(iris)
iris_10=iris.sample(10)
sns.scatterplot(x='sepal_length',y='sepal_width',data=iris_10)
plt.show()

sns.boxplot(x="sepal_length", y="sepal_length", data=iris_10)
plt.show()

# print(pd.value_counts(iris_10['species']))

