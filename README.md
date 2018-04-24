# 2018华为软件精英挑战赛

网址：http://codecraft.devcloud.huaweicloud.com/
初赛赛题：http://codecraft.devcloud.huaweicloud.com/home/detail

实现虚拟机预测，采用简单线性回归模型（$ y = w_0 + w_1 * x $）。

**运行说明**：

- 命令行运行只需要执行： python ecs.py /xxx/TrainData.txt /xxx/input.txt /xxx/output.txt
其中：TrainData.txt是历史数据文件，input.txt是其他参数输入文件，output.txt是输出文件。
- 若在PyCharm中运行ecs.py，需设置Run - Edit Configurations - Parameters如下：
data_2016_1.txt input.txt result.txt

编程语言：Python 2.7