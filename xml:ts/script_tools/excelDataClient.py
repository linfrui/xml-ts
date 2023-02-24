#!/usr/bin/python
# coding=utf-8

import xlrd,struct,os,traceback                    #导入xlrd模块
import csv
import xml.dom.minidom as XmlDom

########################################################################
def GetFileName(strFile):
    path,_,_=strFile.rpartition('.')
    _,_,filename=path.rpartition('/')
    return filename

def getCsvAllData(csvFile):
    csvfile = open(csvFile, 'rt')
    reader = csv.reader(csvfile)
    
    allData=[]
    for line in reader:
        allData.append(line)
    
    csvfile.close()
    
    return allData,GetFileName(csvFile)

def convertToInt(val):
    return int(round(float(val)))

def getXmlAllData(xmlFile):
    dom=XmlDom.parse(xmlFile)
    sheet=dom.getElementsByTagName("Worksheet")[0]
    sheet_name=sheet.getAttribute("ss:Name")
    table=sheet.getElementsByTagName("Table")[0]
    
    allData=[]
    nRow=0
    for row in table.childNodes:
        if row.nodeType!= XmlDom.Node.ELEMENT_NODE or row.tagName!="Row":
            continue
        rowData=[]
        nRow+=1
        cellIndex=1
        for cell in row.childNodes:
            if cell.nodeType!= XmlDom.Node.ELEMENT_NODE or cell.tagName!="Cell":
                continue
            curIndex=cellIndex
            if cell.hasAttribute("ss:Index"):
                curIndex=convertToInt(cell.getAttribute("ss:Index"))
            for i in range(cellIndex,curIndex):
                rowData.append("")
            #
            cellIndex=curIndex+1
            #
            dataList=cell.getElementsByTagName("Data")
            if len(dataList)==0:
                dataList=cell.getElementsByTagName("ss:Data")
            if len(dataList)>0:
                data=dataList[0].childNodes[0]
                rowData.append(data.nodeValue)
            else:
                rowData.append("")
        #
        allData.append(rowData)
    
    return allData,sheet_name

def getXlsAllData(xlsFile):
    book = xlrd.open_workbook(xlsFile)     #获得excel的book对象
    
    #获取sheet对象，方法有2种：
    sheet_name=book.sheet_names()[0]          #获得指定索引的sheet名字
    sheet=book.sheet_by_index(0)     #通过sheet索引获得sheet对象

    #获取行数和列数：
    nrows = sheet.nrows    #行总数
    ncols = sheet.ncols   #列总数
    
    #通过cell的位置坐标获得指定cell的值
    allData=[]
    for y in range(nrows):
        rowData=[]
        for x in range(ncols):
            val=sheet.cell_value(y,x)
            if type(val)=='unicode':
                val=val.encode("utf-8") 
            rowData.append(val)
        #
        allData.append(rowData)
    #
    
    return allData,sheet_name.encode("utf-8") 

def getCellVal(srcAllData,row,col):
    ret=""
    if row<len(srcAllData) and col<len(srcAllData[row]):
        ret=srcAllData[row][col]
    #
    if ret==None:
        ret=""
    return ret

def suportExt(file):
    print ('44444')
    print (file)
    return file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".csv") or file.endswith(".xml")

def getExcelData(xlsFile):
    print(xlsFile)
    if xlsFile.endswith(".csv"):
        srcAllData,sheet_name=getCsvAllData(xlsFile)
    elif xlsFile.endswith(".xml"):
        srcAllData,sheet_name=getXmlAllData(xlsFile)
    else:
        srcAllData,sheet_name=getXlsAllData(xlsFile)
        
    return srcAllData,sheet_name


########################################################################
cfgFieldKey=1
cfgFieldNoClient=2
cfgFieldNoServer=4
#
cfgFieldType_Int=1
cfgFieldType_String=2
cfgFieldType_List=4

class cfgField:
    def __init__(self):
        self.cLen = 0
        self.sName = ""
        self.nType = cfgFieldType_Int
        self.nProperty = 0
        self.colIndex=0
        self.listStruct=[]
    

##################################################################
def buildFieldList(row_data,isServer):
    fieldList=[]
    print (row_data)
    for fieldIndex in range(len(row_data)):
        colTitle=row_data[fieldIndex]
        print ('@@@@@')
        print (colTitle)
        # if type(colTitle)!= 'str' or len(colTitle.strip())==0:
        #     break
        print ('！！！！！')
        print (colTitle)
        nameList=colTitle.split(":")
        field=cfgField()
        field.sName=nameList[0]
        field.cLen=len(field.sName)
        field.nProperty=0
        if "string" in nameList:
            field.nType=cfgFieldType_String
        elif "list" in nameList:
            # field.nType=cfgFieldType_List
            field.nType=cfgFieldType_String
        else:
            field.nType=cfgFieldType_Int
            
        if "key" in nameList:
            field.nProperty|=cfgFieldKey
        if "client" in nameList and isServer==True:
            continue
        if "server" in nameList and isServer==False:
            continue
        if "none" in nameList:
            continue
        #

        for name in nameList:
            name=name.strip()
            if "(" == name[0] and ")" == name[-1]:
                tempList=name[1:-1].split(",")
                field.listStruct=[]
                for temp in tempList:
                    temp=temp.strip()
                    if temp == "int":
                        field.listStruct.append(0)
                    else:
                        field.listStruct.append("")
        field.colIndex=fieldIndex
        fieldList.append(field)
        
    #

    return fieldList

def getListData(cell_value,field,y):
    listData=[]
    cell_value=cell_value.strip(";")
    cell_value=cell_value.strip()
    if len(cell_value)>0:
        strRow=cell_value.split(";")
        for item in strRow:
            if len(item)==0:
                continue
            listVal=item.split(",")
            colValList=[]
            valIndex=0
            for strVal in listVal:
                realVal=strVal
                if valIndex<len(field.listStruct):
                    testVal=field.listStruct[valIndex]
                    if type(testVal)!=str:
                        try:
                            realVal=convertToInt(strVal)
                        except:
                            print("erro list val 2",colValList,"pos:%d,%d" % (y,field.colIndex))
                            os.system('pause')
                else:
                    try:
                        realVal=convertToInt(strVal)
                    except:
                        realVal=strVal
                colValList.append(realVal)
                valIndex+=1
            #
            if len(colValList)>len(field.listStruct):
                field.listStruct=colValList
            #
            listData.append(colValList)
    #
    return listData

def buildAllData(srcAllData,fieldList):
    print ('---------')
    print (fieldList)
    print (srcAllData)
    nrows = len(srcAllData)    #行总数
    allData=[]
    for y in range(1,nrows):
        rowData=[]
        for field in fieldList:
            cell_value = getCellVal(srcAllData,y,field.colIndex)
            if field.nType==cfgFieldType_String:
                if type(cell_value)!=str:
                    cell_value="%d" % convertToInt(cell_value)
                #
                if cell_value=="null":
                    cell_value=""
                rowData.append(cell_value)
            elif field.nType==cfgFieldType_List:
                if type(cell_value)!=str:
                    cell_value="%d" % convertToInt(cell_value)
                #
                if cell_value=="null":
                    cell_value=""
                rowData.append(getListData(cell_value,field,y))
            else:
                if type(cell_value)==str:
                    if field.colIndex==0 and len(cell_value)==0:#无效行
                        break
                    try:
                        cell_value=convertToInt(cell_value)
                    except:
                        cell_value=0
                else:
                    cell_value=convertToInt(cell_value)
                #
                rowData.append(cell_value)
            #
        #
        if len(rowData)==len(fieldList):
            allData.append(rowData)
    #
    return allData