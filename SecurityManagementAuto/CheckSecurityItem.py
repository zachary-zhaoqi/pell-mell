# -*- coding: UTF-8 -*-
import json
import subprocess


def printCheckResultList(checkResultList):
    """
    打印检查结果

    参数:
      checkResultList: [{
                    "Presentation":""
                    "runResult":subprocess.CompletedProcess.class
                },...]
    """
    print("检查结果如下".center(40))
    print("========================================")
    i = 0
    for item in checkResultList:
        i = i+1
        print(str(i)+'. '+item['presentation'], end=":\t\t\t\t")
        # 检测是否符合默认值
        if item['runResult'].returncode == 0:
            stdout = item['runResult'].stdout
            index = stdout.rindex(item['ValueName'])
            stdout = stdout[index:].splitlines()[0].split(" ")
            it = iter(stdout)
            next(it)
            # while True:
            #     if not next(it).isspace():
            #         break
            keyType = next(it)
            # while True:
            #     if not next(it).isspace() :
            #         break
            keyValue=next(it)
            print("设置成功")
        else:
            print('\033[1;32;43m 未设置 \033[0m')


REG_QUERY = 'REG QUERY '

with open('CheckItem.json', encoding='utf-8') as file:
    checkList = json.loads(file.read())

regList = checkList['reg']
gpList = checkList['gp']

checkResultList = []

# 检查注册表项目
for regItem in regList:
    cmd = REG_QUERY+regItem['KeyName']['FullKey']+' /v '+regItem['ValueName']
    result = regItem
    result['runResult'] = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result['runResult'].stdout = result['runResult'].stdout.decode('gbk')
    result['runResult'].stderr = result['runResult'].stderr.decode('gbk')

    # print(result.stdout.decode('gbk'))
    # print(result.stderr.decode('gbk'))
    checkResultList.append(result)

printCheckResultList(checkResultList)
# print(checkResultList)
