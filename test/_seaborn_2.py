import matplotlib.pyplot as plt
import seaborn as sns


#导数数据集'titanic'
titanic=sns.load_dataset('titanic')

#查看数据集的随机10行数据，用sample方法
sam_10=titanic.sample(10)

age1=sam_10['age'].dropna()

# sns.distplot(age1)
sns.distplot(age1)