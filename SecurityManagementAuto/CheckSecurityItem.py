# -*- coding: UTF-8 -*-
import json
import subprocess
import ctypes
import sys

REG_QUERY = 'REG QUERY '
REG_ADD = 'REG ADD '

def getgroupPolicyListForJSON(file):
    """
    从JSON中读取待设定的组策略项目
    参数：file 文件路径Union[str, bytes, int]
    """
    with open(file, encoding='utf-8') as file:
        checkList = json.loads(file.read())

    return checkList['gp']

def getREGListForJSON(file):
    """
    从JSON中读取待设定的注册表项目
    参数：file 文件路径Union[str, bytes, int]
    """
    with open(file, encoding='utf-8') as file:
        checkList = json.loads(file.read())

    return checkList['reg']

def printREGCheckResultList(checkResultList):
    """
    打印注册表检查结果

    参数:
      checkResultList: [{
                    "Presentation":""
                    "checkResult":subprocess.CompletedProcess.class
                },...]
    """
    print("检查结果如下".center(40))
    print("========================================")
    i = 0
    for item in checkResultList:
        i = i+1
        print(str(i)+'. '+item['presentation'], end=":\t\t\t\t")
        # 检测是否符合默认值
        if item['checkResult'].returncode == 0:
            stdout = item['checkResult'].stdout
            index = stdout.rindex(item['valueName'])
            stdout = stdout[index:].splitlines()[0].split(" ")
            it = iter(stdout)
            keyType = next(it)
            keyType = next(it)
            while keyType is '':
                keyType = next(it)
            keyValue = next(it)
            while keyValue is '':
                keyValue = next(it)
            if item['keyType'] == keyType and item['keyValue'] == keyValue:
                item['checkResultCode'] = 0  # 成功
                print("设置成功")
            else:
                item['checkResultCode'] = 1  # 值错误
                print('\033[1;32;43m 未设置 \033[0m')

        else:
            item['checkResultCode'] = 1  # 值项为建立
            print('\033[1;32;43m 未设置 \033[0m')

def checkREG():
    '''
    检查注册表项目是否设置正确
    '''
    regList=getREGListForJSON('CheckItem.json')
    checkResultList = []
    for regItem in regList:
        # 将十进制数转换为十六进制的，方便于进行比较值。
        if regItem['keyType'] == 'REG_DWORD':
            regItem['keyValue'] = str(hex(int(regItem['keyValue'])))

        cmd = REG_QUERY+regItem['keyName']['fullKey'] + \
            ' /v '+regItem['valueName']
        result = regItem
        result['checkResult'] = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result['checkResult'].stdout = result['checkResult'].stdout.decode(
            'gbk')
        result['checkResult'].stderr = result['checkResult'].stderr.decode(
            'gbk')
        checkResultList.append(result)
    printCheckResultList(checkResultList)

def setAllREG():
    '''
    一键设置注册表项目
    '''

    regList=getREGListForJSON('CheckItem.json')
    setResultList = []
    for regItem in regList:
        # 将十进制数转换为十六进制的，方便于进行比较值。
        if regItem['keyType'] == 'REG_DWORD':
            regItem['keyValue'] = str(hex(int(regItem['keyValue'])))

        cmd = REG_ADD+regItem['keyName']['fullKey']+' /v '+regItem['valueName'] + \
            ' /t '+regItem['keyType']+' /d ' + regItem['keyValue']+' /f '
        result = regItem
        result['setResult'] = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result['setResult'].stdout = result['setResult'].stdout.decode('gbk')
        result['setResult'].stderr = result['setResult'].stderr.decode('gbk')
        setResultList.append(result)

    # print(setResultList)

def checkGP():
    '''
    检查组策略项目是否设置正确
    '''
    alterGPList = getgroupPolicyListForJSON('CheckItem.json')

    result = subprocess.run(
        'secedit /export /cfg policy.inf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("获取本地组策略状态失败!")
    policy=[]
    with open('policy.inf',encoding='UTF-16LE') as f:
        policy=f.read()

    currentGPList=[]
    for aletrGPItem in alterGPList:
        try:
            Name=aletrGPItem['name']
            index=policy.index(Name)
            index=index+len(Name)+3#过掉" = "三个符号
            Value=''
            while policy[index]!='\n':
                Value=Value+policy[index]
                index+=1
        except ValueError:
            Value=''
        finally:
            currentGPItem={}
            currentGPItem['name']=Name
            currentGPItem['value']=Value
            currentGPList.append(currentGPItem)
            print(aletrGPItem['presentation'], end=":\t\t\t\t\t")
            if aletrGPItem['defaultValue']==currentGPItem['value']:
                print("设置成功")
            else:
                print('\033[1;32;43m 未设置 \033[0m')

def setAllGP():
    alterGPList = getgroupPolicyListForJSON('CheckItem.json')

    result = subprocess.run(
        'secedit /export /cfg policy.inf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("获取本地组策略状态失败!")
    policy=''
    with open('policy.inf',encoding='UTF-16LE') as f:
        policy=f.read()

    newPolicy=policy
    for aletrGPItem in alterGPList:
        try:
            Name=aletrGPItem['name']
            index=newPolicy.index(Name)
            index=index+len(Name)+3#过掉" = "三个符号
            newPolicy=newPolicy[:index]+str(aletrGPItem['defaultValue']) 
            while newPolicy[index]!='\n':
                index+=1
            newPolicy+=newPolicy[index:]
        except ValueError:
            index=newPolicy.index(aletrGPItem['classify'])+1
            newPolicy=newPolicy[:index]+str(aletrGPItem['name']+' = '+aletrGPItem['defaultValue']) +newPolicy[index:]
    
    with open('policy.inf',mode='w',encoding='UTF-16LE') as f:
        f.write(newPolicy)

if __name__ == "__main__":
    # ctypes.windll.shell32.ShellExecuteW(
    #     None, "runas", sys.executable, __file__, None, 1)

    # checkGP()
    setAllGP()
    # checkREG()
    # setAllREG()
    # checkREG()

