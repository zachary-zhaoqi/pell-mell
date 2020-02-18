# -*- coding: UTF-8 -*-
import ctypes
import json
import os
import subprocess
import sys

REG_QUERY = 'REG QUERY '
REG_ADD = 'REG ADD '

current_file_path = os.path.dirname(os.path.abspath(__file__))
JSONFILE = current_file_path+'\\CheckItem.json'
# todo: 这个在打包生产时需要改为相对路径


def getgroupPolicyListForJSON():
    """
    从JSON中读取待设定的组策略项目
    参数：file 文件路径Union[str, bytes, int]
    """
    with open(JSONFILE, encoding='utf-8') as file:
        checkList = json.loads(file.read())

    return checkList['gp']


def get_REG_list_for_JSON():
    """
    从JSON中读取待设定的注册表项目
    参数：file 文件路径Union[str, bytes, int]
    """
    with open(JSONFILE, encoding='utf-8') as file:
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
            while keyType == '':
                keyType = next(it)
            keyValue = next(it)
            while keyValue == '':
                keyValue = next(it)
            if item['keyType'] == keyType and item['keyValue'] == keyValue:
                item['checkResultCode'] = 0  # 成功
                print("设置成功")
            else:
                item['checkResultCode'] = 1  # 值错误
                print('\033[1;32;43m 未设置 \033[0m')

        else:
            item['checkResultCode'] = 1  # 值项未建立
            print('\033[1;32;43m 未设置 \033[0m')


def read_REG_current_settings():
    '''
    检查注册表项目是否设置正确
    '''
    check_list_REG = get_REG_list_for_JSON()
    check_result_list = []
    for regItem in check_list_REG:
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
        check_result_list.append(result)
    # printREGCheckResultList(checkResultList)
    for item in check_result_list:
        item['checkResult'] = item['checkResult'].__dict__

    return check_result_list


def contrast(REGcurrentSettingsList):
    '''对照当前注册表设置与期望是否一致，并返回差异'''

    contrast_result = []
    for item in REGcurrentSettingsList:
        # 检测是否符合默认值
        if item['checkResult']['returncode'] != 0:
            fail = item['presentation']+'：当前未设置'
            contrast_result.append(fail)
        else:
            stdout = item['checkResult']['stdout']
            index = stdout.rindex(item['valueName'])
            stdout = stdout[index:].splitlines()[0].split(" ")
            it = iter(stdout)
            keyType = next(it)
            keyType = next(it)
            while keyType == '':
                keyType = next(it)
            keyValue = next(it)
            while keyValue == '':
                keyValue = next(it)
            if item['keyType'] != keyType or item['keyValue'] != keyValue:
                fail = item['presentation']+'：当前设置不符合要求'
                contrast_result.append(fail)
    return contrast_result


def set_all_REG():
    '''
    一键设置注册表项目
    '''

    check_list_REG = get_REG_list_for_JSON()
    set_REG_result_list = []
    for regItem in check_list_REG:
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
        set_REG_result_list.append(result)
    
    for item in set_REG_result_list:
        item['setResult'] = item['setResult'].__dict__
    return set_REG_result_list

def get_set_REG_fail_results(set_REG_result_list):
    """通过设置结果返回设置失败项"""
    set_REG_fail_results = []
    for item in set_REG_result_list:
        # 检测是否符合默认值
        if item['setResult']['returncode'] != 0:
            fail = item['presentation']+'：当前未设置'
            set_REG_fail_results.append(fail)
    return set_REG_fail_results

def checkGP():
    '''
    检查组策略项目是否设置正确
    '''
    alterGPList = getgroupPolicyListForJSON()

    result = subprocess.run(
        'secedit /export /cfg policy.inf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("获取本地组策略状态失败!")
    policy = []
    with open('policy.inf', encoding='UTF-16LE') as f:
        policy = f.read()

    currentGPList = []
    for aletrGPItem in alterGPList:
        try:
            Name = aletrGPItem['name']
            index = policy.index(Name)
            index = index+len(Name)+3  # 过掉" = "三个符号
            Value = ''
            while policy[index] != '\n':
                Value = Value+policy[index]
                index += 1
        except ValueError:
            Value = ''
        finally:
            currentGPItem = {}
            currentGPItem['name'] = Name
            currentGPItem['value'] = Value
            currentGPList.append(currentGPItem)
            print(aletrGPItem['presentation'], end=":")
            if str(aletrGPItem['defaultValue']) == currentGPItem['value']:
                print("设置成功")
            else:
                print('\033[1;32;43m 未设置 \033[0m')
                print("\033[1;32;43m test \033[0m")


def setAllGP():
    alterGPList = getgroupPolicyListForJSON()

    result = subprocess.run(
        'secedit /export /cfg policy.inf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("获取本地组策略状态失败!")
    policy = ''
    with open('policy.inf', encoding='UTF-16LE') as f:
        policy = f.read()

    newPolicy = policy
    for aletrGPItem in alterGPList:
        try:
            Name = aletrGPItem['name']
            index = policy.index(Name)
            index = index+len(Name)+3  # 过掉" = "三个符号
            newPolicy = policy[:index]+str(aletrGPItem['defaultValue'])
            while policy[index] != '\n':
                index += 1
            newPolicy += policy[index:]
        except ValueError:
            index = policy.index(
                aletrGPItem['classify'])+len(aletrGPItem['classify'])+1
            newPolicy = policy[:index]+aletrGPItem['name'] + \
                ' = '+str(aletrGPItem['defaultValue']) + '\n' + policy[index:]
        finally:
            policy = newPolicy

    with open('policy.inf', mode='w', encoding='UTF-16LE') as f:
        f.write(newPolicy)

    result = subprocess.run(
        'secedit /configure /db temp.sdb /cfg policy.inf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("设置成功！")
    else:
        print("设置失败，请联系作者")

if __name__ == "__main__":
    # ctypes.windll.shell32.ShellExecuteW(
    #     None, "runas", sys.executable, __file__, None, 1)

    # current_REG_settings_list=read_REG_current_settings()
    # a=json.dumps(current_REG_settings_list),ensure_ascii=False)
    # print(a)
    # contrast_result=contrast(current_REG_settings_list)
    # print(contrast_result)
    # checkGP()
    # setAllGP()
    # readREGCurrentSettings()
    set_all_REG()
    # readREGCurrentSettings()
