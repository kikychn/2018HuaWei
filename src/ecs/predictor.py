# coding: utf-8
from sklearn import linear_model
from datetime import datetime, timedelta
from simple_linear_regression import predict_target_value, cal_simple_linear_regression_coefficients
import math
import matplotlib.pyplot as plt
import ecs

def predict_vm(ecs_lines, input_lines):
    result = []

    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    # 处理input文本内容，输出需要预测的虚拟机型号及预测的时间段
    flavors, preStart, preEnd, predays = processInput(input_lines)
    intervalData = 1

    sum = 0
    sum_preError = 0
    testData_actY = []
    testData_preY = []
    for i in range(len(flavors)):
        targetFlavor = flavors[i]
        targetFlavorNum, testData_sumY, testPreData_sumY = singleVM(ecs_lines, targetFlavor, predays, intervalData, preStart)
        sum += targetFlavorNum
        result.append(targetFlavor + ' ' + str(targetFlavorNum))
        testData_actY.append(testData_sumY)
        testData_preY.append(testPreData_sumY)
    result.insert(0, sum)
    return result


# 预测单台虚拟机数量
def singleVM(ecs_lines, targetFlavor, predays, intervalData, preStart):
    trainData_X, trainData_Y, firstTrainRecord = processHistoryData(ecs_lines, targetFlavor, intervalData)
    print '训练集中型号为', targetFlavor, '的虚拟机，最早的一条历史数据日期为：', firstTrainRecord
    print '该型号训练集数据为：', trainData_X, trainData_Y

    if trainData_X == []:
        print '---------------------------------------------------'
        return 0
    # 训练数据，线性回归建模
    preTrainData(trainData_X, trainData_Y)
    print '剔除异常点后的训练数据为：：', trainData_X, trainData_Y
    # reg = linear_model.LinearRegression()
    # reg.fit(trainData_X, trainData_Y)
    w0, w1 = cal_simple_linear_regression_coefficients(trainData_X, trainData_Y)
    print 'w1：', w1

    # 通过构造好的模型，预测未来一段时间的虚拟机申请数
    timedel = (preStart - firstTrainRecord).days
    preFuture_X = futureDate_X(timedel, predays, intervalData)
    # preFuture_Y = reg.predict(preFuture_X)
    preFuture_Y = []
    for x in preFuture_X:
        preFuture_Y.append(predict_target_value(x, w0, w1))
    preFuture_sumY = int(math.ceil(sum(preFuture_Y)))
    if preFuture_sumY < 0:
        preFuture_sumY = 0
    print '预测未来', predays, '天的数据为：', preFuture_X, preFuture_Y, preFuture_sumY

    testPreData_Y = []
    for x in trainData_X:
        testPreData_Y.append(predict_target_value(x, w0, w1))
    testData_Y, testPreData_Y = get_testData(trainData_Y, testPreData_Y)
    testData_sumY = int(math.ceil(sum(testData_Y)))
    testPreData_sumY = int(math.ceil(sum(testPreData_Y)))
    print '---------------------------------------------------'

    # 可视化
    newTrainData_X = []
    newPreFuture_X = []
    for x in trainData_X:
        newTrainData_X.append([x])
    for x in preFuture_X:
        newPreFuture_X.append([x])
    plt.scatter(newTrainData_X, trainData_Y)
    plt.plot(newTrainData_X, trainData_Y)
    plt.scatter(newPreFuture_X, preFuture_Y)
    plt.plot(newPreFuture_X, preFuture_Y)
    plt.show()

    return preFuture_sumY, testData_sumY, testPreData_sumY


# 将从txt文本中读取的虚拟机申请数据转换成标准格式
# eg:规格为flavor5的虚拟机对应数据:trainDdata_X=[日期,日期,日期...],trainData_Y=[数量,数量,数量,...]
def processHistoryData(data_lines, flavor, intervalData):
    data = {}
    firstRecordData = None
    for index, item in enumerate(data_lines):
        values = item.split("\t")
        uuid = values[0]
        flavorName = values[1]
        createTime = values[2]
        createDate = datetime.strptime(createTime.split(" ")[0], '%Y-%m-%d')
        # print str(index), uuid, flavorName, createTime, createDate, '\n'

        # 统计每天每种类型虚拟机的申请数量
        if flavorName == flavor:
            if data == {}:
                firstRecordData = createDate
            keyDate = (createDate - firstRecordData).days
            if data.has_key(keyDate):
                data[keyDate] += 1
            else:
                data[keyDate] = 1
        # print data
    # 将训练数据转换为模型输入需要的格式,intervalData
    dataWithInterval = {}
    for key, value in data.items():
        if dataWithInterval.has_key(key / intervalData) is False:
            dataWithInterval[key / intervalData] = value
        else:
            dataWithInterval[key / intervalData] += value

    data_X = []
    data_Y = []
    for key, value in dataWithInterval.items():
        data_X.append(key)
        data_Y.append(value)
    size = len(data_X);
    lastNum = min(size / 4, 5)
    for i in range(size - lastNum, size):
        data_X.append(data_X[i])
        data_Y.append(data_Y[i])
    return data_X, data_Y, firstRecordData

# 剔除异常数据
def preTrainData(trainData_X, trainData_Y):
    # average = float(sum(trainData_Y))/len(trainData_Y)
    average = sum(trainData_Y) / len(trainData_Y)
    print '训练数据的平均值为：', average
    for index, y in enumerate(trainData_Y):
        if y > average * 6:
            trainData_Y[index] = average
        elif y > average * 4:
            trainData_Y[index] = average * 4
        if y < average / 2:
            trainData_Y[index] = average


# 需要预测的未来一段时间
def futureDate_X(timedel, predays, intervalData):
    future_X = []
    for i in range(predays / intervalData):
        future_X.append(timedel / intervalData + i)
    return future_X


# 处理input文本内容，输出需要预测的虚拟机型号及预测的时间段
def processInput(input_lines):
    countVM = int(input_lines[2])
    vm = []
    for i in range(3, 3 + countVM):
        vm.append(input_lines[i].split(" ")[0])
    # print vm
    preStart = datetime.strptime(input_lines[6 + countVM].split(" ")[0], '%Y-%m-%d')
    preEnd = datetime.strptime(input_lines[7 + countVM].split(" ")[0], '%Y-%m-%d')
    days = (preEnd - preStart).days + 1
    # print preStart, preEnd, days
    return vm, preStart, preEnd, days

def get_testData(data_Y, pre_data_Y):
    testData_Y = data_Y[:]
    test_preData_Y = pre_data_Y[:]
    return testData_Y, test_preData_Y
