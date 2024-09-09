# 扩展库介绍

这是中国传媒大学胡凤国老师上课分享的自定义函数库，其中包含几个常用的文本处理函数。发布本扩展库主要是方便上课学生练习Python程序，顺便分享给其他需要的Pythoner。

刚学会发布扩展库，PyPI很多东西还不熟，如有问题，请多提宝贵意见。

# 安装说明

pip install hufengguo

# 用法说明

具体用法见胡凤国老师的上课教材：《Python程序设计（基于计算思维和新文科建设）》，ISBN：9787121435577，胡凤国，电子工业出版社，2022年6月。

这里举一个简单的例子：

```
from hufengguo import isprime
x = [i for i in range(101) if isprime(i)]
print(x)
```