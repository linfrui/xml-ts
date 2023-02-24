#!/usr/bin/python
# coding=utf-8

#  python buildXlsJs.py
import sys
reload(sys)
sys.setdefaultencoding('utf8')

client_path = '../1/'
xls_path = '../2'
exclude_files = \
    ['activity_collect_box.xlsx','activity_collect.xlsx','broadcast.xlsx','bigwincontrol.xlsx','br_ps_ai.xlsx',
     'br_randomHead.xlsx','chat.xls','chat_robot.xlsx','client_actions.xlsx','ddz_bomb_num.xlsx','ddz_plan_poker_group.xlsx',
     'ddz_plan_poker.xlsx','ddz_plan_poker_group_player.xlsx','ddz_policy.xlsx','game_poker_lib.xlsx','game_room_drop_reward.xlsx',
     'game_room_num.xlsx','gateoutlist.xlsx','goldMarket.xlsx','itemMarket.xlsx','lotteryTime.xls','lotteryTimeLongHu.xls',
     'lotteryTimeLongHuCoin.xls','mailText.xlsx','match.xlsx','matchReward.xlsx','matchRewardMap.xlsx','matchRobot.xls',
     'matchRound.xlsx','matchSignNumMap.xlsx','match_horseRaceLampName.xlsx','randomHead.xls','randomName_en.xls',
     'randomName.xls','robotroom.xlsx','robotnumber.xlsx','robottime.xlsx','sevenReward.xls','sh_ai.xlsx','sh_blood_ai.xlsx'
     ]
import os, traceback, shutil, sys, copy
import excelDataClient as excelData


# import packConfig_multi

def getFileContent(fileName):
    all_the_text = ""
    try:
        file_object = open(fileName, 'rt')
        all_the_text = file_object.read()
        file_object.close()
    except:
        pass
    return all_the_text


def writeFileContent(fileName, strContent):
    output = open(fileName, 'wt')
    output.write(strContent)
    output.close()
    return


def CreateDir(strDir):
    try:
        os.makedirs(strDir)
    except:
        pass
    return


########################################################################
def GetFileName(strFile):
    path, _, _ = strFile.rpartition('.')
    _, _, filename = path.rpartition('/')
    return filename


########################################################################
def encodeJsStr(strValue):
    #strValue = strValue.replace("\\", "\\\\")
    #strValue = strValue.replace("\"", "\\\"")
    #strValue = strValue.replace("\'", "\\'")
    #strValue = strValue.replace("\n", "\\n")
    return "\"%s\"" % strValue


def buildJsField(cfgField, cell_value):
    jsField = ""
    if type(cell_value) == 'str':
        jsField = encodeJsStr(cell_value)
    elif type(cell_value) == 'list':
        jsField = buildJsList(cfgField, cell_value)
    else:
        jsField = "%d" % cell_value
    #
    return jsField


def buildJsList(cfgField, listData):
    erlData = []
    for rowVal in listData:
        rowErl = []
        for index in range(len(cfgField.listStruct)):
            val = cfgField.listStruct[index]
            if index < len(rowVal):
                if type(val) != type(rowVal[index]):
                    print("erro")
                    os.system('pause')
                val = rowVal[index]
            else:
                if type(val) == 'str':
                    val = ""
                else:
                    val = 0
            #
            if type(val) == 'str':
                rowErl.append(encodeJsStr(val))
            else:
                rowErl.append("%d" % val)
        #
        erlData.append("{%s}" % (",".join(rowErl)))

    return "{%s}" % (",".join(erlData))


def tabDataToJs(tableData, jsDir, module_name):
    #
    print ('tabDatatojs')
    print (module_name)
    print (tableData)
    dataFile = jsDir + "/" + module_name + ".ts"
    #
    jsRowList = []
    for rowTable in tableData:
        rowData = rowTable[1]
        print ('88888')
        print (rowData)
        key = rowTable[0]
        jsRow = []
        for index in range(0, len(rowData)):
            cfgField = rowData[index][1]
            cell_value = rowData[index][2]
            jsField = buildJsField(cfgField, cell_value)
            jsRow.append("%s:%s" % (cfgField.sName, jsField))
        #
        if type(key) == 'str':
            key = encodeJsStr(key)
            jsRowList.append("      { key:%s,%s }" % (key, ",".join(jsRow)))
        else:
            jsRowList.append("      { key:%d,%s }" % (key, ",".join(jsRow)))

    print (999999)
    print (jsRowList)
    jsFileTemp = """var data_%s =
{
    items:
    [
%s
    ],

    /**
     * 查找第一个符合filter的item
     * @param filter
     * @returns {*}
     */
    getItem: function(filter){
        var result = null;
        for(var i=0; i<this.items.length; ++i){
            if(filter(this.items[i])){
                result = this.items[i];
                return result;
            }
        }
        return result;
    },

    /**
     * 查找第一个符合filter的list
     * @param filter
     * @returns {*}
     */
    getItemList: function(filter){
        var list = new Array();
        this.items.forEach(function (item) {
            if(filter(item)){
                list.push(item);
            }
        });
        return list;
    },
};

module.exports=data_%s;"""

    strData = jsFileTemp % (module_name, ",\n".join(jsRowList), module_name)
    writeFileContent(dataFile, strData)
    return  # parse excel file


def xlsToTable(xlsFile):
    srcAllData, sheet_name = excelData.getExcelData(xlsFile)

    # 获取行数和列数：
    print (srcAllData)
    nrows = len(srcAllData)  # 行总数
    ncols = len(srcAllData[0])  # 列总数
    print(sheet_name, "row:", nrows, "col:", ncols)

    # 获得指定行、列的值，返回对象为一个值列表
    row_data = srcAllData[0]  # 获得第1行的数据列表
    fieldList = excelData.buildFieldList(row_data, False)
    # 通过cell的位置坐标获得指定cell的值
    allData = excelData.buildAllData(srcAllData, fieldList)
    # support the xls file named with task.xls task#ch.xls(for ch)
    module_name = sheet_name[0].lower() + sheet_name[1:]
    index = module_name.find("#")
    if index != -1:
        module_name = module_name[0:index]

    return module_name, allData, fieldList


def getArrKeyIndex(arr, key):
    for index in range(len(arr)):
        if arr[index][0] == key:
            return index
    return -1


# parse the excel files in dir to tabAllData
def xlsDirToTable(xlsDir, tabAllData):
    #
    for file in os.listdir(xlsDir):
        print(xlsDir)
        strFile = xlsDir + "/" + file
        print(strFile)
        if os.path.isdir(strFile) == False:
            if (file in exclude_files) == False:
                print ('33333 :'+file)
                if excelData.suportExt(file):
                    # parse the file
                    module_name, allData, fieldList = xlsToTable(strFile)
                    print (module_name)
                    print (tabAllData)
                    # if exist the same module name in tabAllData,get the data, else just append this module to tabAllData
                    xlsTab = []
                    xlsTabIndex = getArrKeyIndex(tabAllData, module_name)
                    print (77777)
                    print (xlsTabIndex)
                    if xlsTabIndex != -1:
                        xlsTab = tabAllData[xlsTabIndex][1]
                    else:
                        tabAllData.append([module_name, xlsTab])

                    # visit all row
                    print (66666)
                    print (allData)
                    print (len(allData))
                    for y in range(len(allData)):
                        # if exist the row with same key,get the rowArr,else just appect this row to xlsTab
                        rowArr = []
                        print (y)
                        key = allData[y][0]
                        keyIndex = getArrKeyIndex(xlsTab, key)
                        if keyIndex != -1:
                            rowArr = xlsTab[keyIndex][1]
                        else:
                            xlsTab.append([key, rowArr])

                        # vist all cell,if already exist the cell,use the new value,else append the cell to rowArr
                        for x in range(1, len(fieldList)):
                            cfgField = fieldList[x]
                            cell_value = allData[y][x]
                            nameIndex = getArrKeyIndex(rowArr, cfgField.sName)
                            if nameIndex == -1:
                                rowArr.append([cfgField.sName, cfgField, cell_value])
                            else:

                                rowArr[nameIndex] = [cfgField.sName, cfgField, cell_value]
    print ('55555555')
    print (tabAllData)
    return tabAllData


def tabAllDataToJs(tabAllData):
    print (66666)
    print (tabAllData)
    shutil.rmtree(client_path)
    os.mkdir(client_path)
    for keyTableData in tabAllData:
        print ("22222")
        module_name = keyTableData[0]
        print (module_name)
        tableData = keyTableData[1]
        print (tabAllData)
        tabDataToJs(tableData, client_path, module_name)
    return

def xlsDirToJs():
    tabAllData = []
    xlsDirToTable(xls_path, tabAllData)
    tabAllDataToJs(tabAllData)


if __name__ == "__main__":
    try:
        xlsDirToJs()
    except:
        print(traceback.format_exc())
