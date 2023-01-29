from stage import database
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
# tkinter setup

fen = Tk()
msg = StringVar()
fen.title("Gestion Stage")
# main obj
objStage = Stage()

def showMsg(message, color):
    label_title = Label(inputFrame, textvariable=msg, text="", fg=color)
    label_title.grid(column=0,row=6)
    msg.set(message)
#type of sort when user sort stages in treeView heading
sortDescendingOrder = [False]
def showStages(stages):
    if stages:
        treeFrame = Frame(fen,name='treeFrame')
        treeFrame.grid(column=0, row=2)
        #sort stage when user click to treeView Heading
        def getClickedHeading(e,tree):
            columnToIndex = {'id':1,'intitule':2,'duree':3,'prix':4,'domaine':5}
            item = tree.identify_column(e.x)
            if tree.heading(item)['state'] == 'active pressed' :
                column = tree.heading(item)['text']
                index = columnToIndex[column]
                sortStages(index)
                sortDescendingOrder[0] = not sortDescendingOrder[0]
        # define columns
        columns = [key for key, _ in stages[0].items() if key != "_id"]
        tree = ttk.Treeview(treeFrame, columns=columns, show='headings',name='mainTreeView')
        #heading event
        tree.bind('<ButtonRelease-1>',lambda event,curTree=tree:getClickedHeading(event,curTree))
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col,width=150)
        stageData = []
        for stage in stages:
            stageData.append([stage['id'], stage['intitule'],
                             stage['duree'], stage['prix'], stage['domaine']])

        for stage in stageData:
            tree.insert('', END, values=stage)

        tree.grid(column=0, row=0)
        #add scroll bar to treeView
        scrollbar = ttk.Scrollbar(treeFrame,orient=VERTICAL,command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky='ns')
        
    else:
        complexeSearchShowMsg("not found", "red")


def allStages():
    stages = objStage.getAllStages()
    showStages(stages)

allStages()

def getMinMax():
    minMax = objStage.minMaxPrice()
    if minMax:
        showMsg('min price is :'+str(minMax[0]['min price']) +
                ', and max price is :'+str(minMax[0]['max price']), 'green')

def getStagesCount():
    stagesCount = objStage.stagesCount()
    if stagesCount:
        showMsg('totale stages is :' +
                str(stagesCount[0]['totale stages']), 'green')
#by get by functions domaine 
def getAveragePriceByDomaine():
    domaine = curDomaine.get()
    if len(domaine) == 0:
        showMsgInComboBox(f'please select domaine', 'red')
    else:
        totalPrice = objStage.avgPriceBydomaine(domaine)
        showMsgInComboBox(f'average price in {domaine} is : '+str(totalPrice[0]['average price']), 'green')

def getTotalPiceByDomaine():
    domaine = curDomaine.get()
    if len(domaine) == 0:
        showMsgInComboBox(f'please select domaine', 'red')
    else:
        totalPrice = objStage.prixTotalByDomaine(domaine)
        showMsgInComboBox(f'total price in {domaine} is : '+str(totalPrice[0]['total price']), 'green')

def getStagesByDomaine():
    domaine = curDomaine.get()
    if len(domaine) == 0:
        showMsgInComboBox(f'please select domaine', 'red')
    else:
        stages = objStage.getByDomaine(domaine)
        showStages(stages)

def insertStage():
    try:
        id = int(idInput.get())
        intitule = intituleInput.get()
        duree = float(dureeInput.get())
        prix = float(prixInput.get())
        domaine = domaineInput.get()
        objStage = Stage(id, intitule, duree, prix, domaine)
        if not objStage.getStageById(id):
            objStage.insertStage()
            clearInputes()
            showMsg("add successfully", "green")
            idInput.delete(0, END)
            allStages()
            combo1['values'] = ['None',*setToComboBox('domaine')]
            domainesChoosen['values'] = setToComboBox('domaine')
        else:
            idInput.delete(0, END)
            showMsg("id is already in collection", "red")
    except:
        showMsg("invalid input", "red")

def getByStageById():
    try:
        clearInputes()
        id = int(idInput.get())
        if objStage.getStageById(id):
            st = objStage.getStageById(id)[0]
            intituleInput.insert(0, st["intitule"])
            dureeInput.insert(0, st["duree"])
            prixInput.insert(0, st["prix"])
            domaineInput.insert(0, st["domaine"])
            msg.set("")
        else:
            showMsg("id not found", "red")
    except:
        showMsg("invalid id", "red")

def clearInputes():
    intituleInput.delete(0, END)
    dureeInput.delete(0, END)
    prixInput.delete(0, END)
    domaineInput.delete(0, END)

def comfirm(someThing):
    return askyesno(title='confirmation',message=f'Are you sure that you want to {someThing}')

def deleteStage():
    if comfirm('delete'):
        try:
            id = int(idInput.get())
            objStage.deleteStage(id)
            clearInputes()
            showMsg("delete successfully", "green")
            idInput.delete(0, END)
            allStages()
            combo1['values'] = ['None',*setToComboBox('domaine')]
            domainesChoosen['values'] = setToComboBox('domaine')
        except:
            showMsg("invalid input", "red")

def updateStage():
    if comfirm('update'):
        try:
            id = int(idInput.get())
            intitule = intituleInput.get()
            duree = float(dureeInput.get())
            prix = float(prixInput.get())
            domaine = domaineInput.get()
            objStage = Stage(id, intitule, duree, prix, domaine)
            objStage.updateStage()
            clearInputes()
            showMsg("update successfully", "green")
            idInput.delete(0, END)
            allStages()
            combo1['values'] = ['None',*setToComboBox('domaine')]
            domainesChoosen['values'] = setToComboBox('domaine')
        except:
            showMsg("invalid input", "red")

# inputes Fame
inputFrame = Frame(fen)
inputFrame.grid(column=0, row=0)
# labels
label_title = Label(inputFrame, text="Id :")
label_title.grid(column=0, row=0)
label_title = Label(inputFrame, text="Nom Stage :")
label_title.grid(column=0, row=1)
label_title = Label(inputFrame, text="Duree Stage :")
label_title.grid(column=0, row=2)
label_title = Label(inputFrame, text="Prix Stage :")
label_title.grid(column=0, row=3)
label_title = Label(inputFrame, text="Domaine Stage :")
label_title.grid(column=0, row=4)
# zone de text
idInput = Entry(inputFrame)
idInput.grid(column=1, row=0)
intituleInput = Entry(inputFrame)
intituleInput.grid(column=1, row=1)
dureeInput = Entry(inputFrame)
dureeInput.grid(column=1, row=2)
prixInput = Entry(inputFrame)
prixInput.grid(column=1, row=3)
domaineInput = Entry(inputFrame)
domaineInput.grid(column=1, row=4)
# button Frame
# Buttons
btnInsert = Button(inputFrame, text="insert", command=insertStage)
btnInsert.grid(column=0, row=5)
btnEdite = Button(inputFrame, text="Edite", command=getByStageById)
btnEdite.grid(column=1, row=5)
btnDelete = Button(inputFrame, text="delete", command=deleteStage)
btnDelete.grid(column=2, row=5)
btnUpdate = Button(inputFrame, text="update", command=updateStage)
btnUpdate.grid(column=3, row=5)
btnGetAll = Button(inputFrame, text="get all stages", command=allStages)
btnGetAll.grid(column=4, row=5)
btnMinMax = Button(inputFrame, text="min max price", command=getMinMax)
btnMinMax.grid(column=7, row=5)
btnCount = Button(inputFrame, text="total stages", command=getStagesCount)
btnCount.grid(column=8, row=5)
# combo Frame
comboFrame = Frame(fen)
comboFrame.grid(column=1, row=0)
comboMsg = StringVar()
# Combobox creation
curDomaine = StringVar()
comboLabel = Label(comboFrame, text="Selected Domaine")
comboLabel.grid(column=0, row=0)
domainesChoosen = ttk.Combobox(comboFrame, textvariable=curDomaine)
domainesChoosen.grid(column=1, row=0)
btnTotalPriceByDomain = Button(
    comboFrame, text="total price", command=getTotalPiceByDomaine)
btnTotalPriceByDomain.grid(column=0, row=2)
btnAveragePriceByDomain = Button(
    comboFrame, text="average price", command=getAveragePriceByDomaine)
btnAveragePriceByDomain.grid(column=0, row=3)
# Adding combobox drop down list
def setToComboBox(key):
    stages = objStage.getAllStages()
    domaines = set()
    for stage in stages:
        domaines.add(stage[key])
    return list(domaines)
#combo msg function
def showMsgInComboBox(message,color):
    label_title = Label(comboFrame, textvariable=comboMsg, text="", fg=color)
    label_title.grid(column=0,row=5)
    comboMsg.set(message)
domainesChoosen['values'] = setToComboBox('domaine')
######################################complexe search######################################
#set up the frame
complexSerachFrame = Frame(fen)
complexSerachFrame.grid(column=1,row=1)
complexSerachFrameTitle = Label(complexSerachFrame, text="Complexe Search")
complexSerachFrameTitle.grid(column=0,row=0)
searchList = [0 for i in range(4)]
comlexeSearchMsg = StringVar()
# combo box creation function (this function take column,row of comboBox and label text of comboBox and values of comboBox)
def createCombo(col,rw,labelText,values):
    #create comboBox
    combo = ttk.Combobox(complexSerachFrame)
    #place in grid
    combo.grid(column=col, row=rw)
    #label
    complexSerachDomainesChoosenLabel = Label(complexSerachFrame, text=labelText)
    #place in grid
    complexSerachDomainesChoosenLabel.grid(column=col-1, row=rw)
    #values of comboBox
    combo['values'] = values
    #default value of comboBox
    combo.current(0)
    #return comboBox
    return combo
#add search to list every change of combobox value
hashMap = {"greater than":'$gt','little than':'$lt','equal':'$eq'}
def addSearch(event,index,combo,rw,key):
    #get the value from comboBox
    selected = combo.get()
    #check if comboBox is Domaine, because the form of search by domaine query is defferent
    if index != 0 :
        #add selected value to searchList
        if selected in hashMap :
            searchList[index] = 0 if selected == 'None' else {key:{hashMap[selected]:''}}
        else :
            searchList[index] = 0 if selected == 'None' else {key:{selected:''}}
    else :
        searchList[index] = 0 if selected == 'None' else {key:selected}
    #creacte input
    if index != 0 :
        curInput = Entry(complexSerachFrame,name=f'{index}')
        curInput.grid(column=2,row=rw)
        #if combo value is None destroy it.
        if selected == "None" :
            complexSerachFrame.nametowidget(f'{index}').destroy()
#show msg function
def complexeSearchShowMsg(message,color):
    label_title = Label(complexSerachFrame, textvariable=comlexeSearchMsg, text="", fg=color)
    label_title.grid(column=0,row=6)
    comlexeSearchMsg.set(message)
#this function run when i click to search button
def complexeSearch():
    #here where i put my search querys
    myQuery = [{}]
    #to check if search valid or not
    isValid = True
    #add input values to searchList
    try :
        for i,search in enumerate(searchList) :
            if search == 0 or i == 0: continue
            #get the value from Entry by name
            value = complexSerachFrame.nametowidget(f'{i}').get()
            key1 = list(searchList[i].keys())[0] #{key1:{key2:''}} =>{prix:{'like': '1500'}}
            key2 = list(list(searchList[i].values())[0].keys())[0]
            #if Entry value is empty
            if len(value) == 0 :
                #throw an error
                raise Exception()
            #else add Entry value to search list,after convert the duree and prix values to int
            searchList[i] = {key1:{key2:int(value) if key1 in ['duree','prix'] else value}}
    except :
        #if an error isValid bacome False,this mean search is invalid (one of Entrys is empty or duree or prix not number)
        isValid = False
        #show error msg
        complexeSearchShowMsg('invalid search !!','red')
    #if search is valid
    if isValid :
        #loop for searchList and create myQuery, dont include the last value bacause the form of query is defferent.
        for s in searchList[0:len(searchList)-1] :
            if s == 0 : continue
            #spread object in another one.
            #example : {**{key1:value},**{key2:{"key3":value}}} = {key1:value,key2:{"key3":value}}
            myQuery[0] = {**myQuery[0],**s}

        #set the query of last value (intitule)
        if searchList[-1] :
            key1 = list(searchList[-1].keys())[0]
            key2 = list(list(searchList[-1].values())[0].keys())[0]
            key2Value = list(list(searchList[-1].values())[0].values())[0]
            if key2 == 'start with' : #{key1:{key2:key2Value}} =>{prix:{'like': '1500'}}
                myQuery[0] = {**myQuery[0],**{key1: { "$regex": f"^{key2Value}" }} }
            if key2 == 'end with' :
                myQuery[0] = {**myQuery[0],**{key1: { "$regex": f"{key2Value}$" }}}
            if key2 == 'have' :
                myQuery[0] = {**myQuery[0],**{key1: { "$regex": f"{key2Value}" }} }

        #after create a valid query search i call getByComplexeSearch
        stages = objStage.getByComplexeSearch(myQuery)
        #and i show result to the table (treeview)
        showStages(stages)
        #show success msg
        if stages :
            complexeSearchShowMsg('successful search','green')

#creation of the 4 search comboBox (domaine,prix,duree,intitule) 
combo1 = createCombo(1,1,'domaine',['None',*setToComboBox('domaine')])
combo2 = createCombo(1,2,'prix',['None','greater than','little than','equal'])
combo3 = createCombo(1,3,'duree',['None','greater than','little than','equal'])
combo4 = createCombo(1,4,'intitule',['None','start with','end with','have'])
#add events listeners for every change in comboboxes
combo1.bind('<<ComboboxSelected>>', lambda event,combo=combo1,index=0,row=1,key='domaine':addSearch(event,index,combo,row,key))
combo2.bind('<<ComboboxSelected>>', lambda event,combo=combo2,index=1,row=2,key='prix':addSearch(event,index,combo,row,key)) 
combo3.bind('<<ComboboxSelected>>', lambda event,combo=combo3,index=2,row=3,key='duree':addSearch(event,index,combo,row,key)) 
combo4.bind('<<ComboboxSelected>>', lambda event,combo=combo4,index=3,row=4,key='intitule':addSearch(event,index,combo,row,key)) 
#add button to submit
searchBtn = Button(
    complexSerachFrame, text="Search", command=complexeSearch)
searchBtn.grid(column=0,row=5)
######################################complexe search######################################
######################sorting#############################################################
sortFrame = Frame(fen)
sortFrame.grid(column=1,row=2)
sortLabel = Label(sortFrame, text="sort result")
sortLabel.grid(column=0,row=0)
sortMsg = StringVar()
sortCombo = ttk.Combobox(sortFrame)
sortCombo.grid(column=1,row=1)
sortComboLabel = Label(sortFrame,text="Sorting By")
sortComboLabel.grid(column=0,row=1)
sortCombo['values'] = ['None','id','intitule','duree','prix','domaine']
sortType = StringVar()
sortType.set('ascen')
ascenRadio = ttk.Radiobutton(sortFrame, text='ascending order', value='ascen', variable=sortType)
ascenRadio.grid(column=0,row=2)
descenRadio = ttk.Radiobutton(sortFrame, text='descending order', value='descen', variable=sortType)
descenRadio.grid(column=1,row=2)
def sortStages(index=None):
    #get stages from treeview
    tree = fen.nametowidget('treeFrame').nametowidget('mainTreeView')
    stages = []
    for line in tree.get_children() :
        stages.append(tree.item(line)['values'])
        tree.delete(line)
    #sort Stages using bubble sort
    sortStagesUsingBubbleSort(stages,index)
    if index == None :
        if sortType.get() == 'descen' :
            stages = stages[::-1]
    else :
        if sortDescendingOrder[0] :
            stages = stages[::-1]
    #insert sorted stages to treeview
    for stage in stages:
        tree.insert('', END, values=stage)

def sortStagesUsingBubbleSort(stages,index):
    if index == None :
        comparingIndex = sortCombo.current()-1
    else :
        comparingIndex = index-1
    if comparingIndex != -1 :
        for i in range(len(stages)) :
            tmp = 0
            for j in range(len(stages)-i-1) :
                if comparingIndex in [0,2,3] :
                    if float(stages[j][comparingIndex]) > float(stages[j+1][comparingIndex]) :
                        tmp = stages[j]
                        stages[j] = stages[j+1]
                        stages[j+1] = tmp
                else :
                    if stages[j][comparingIndex] > stages[j+1][comparingIndex] :
                        tmp = stages[j]
                        stages[j] = stages[j+1]
                        stages[j+1] = tmp

sortBtn = Button(
    sortFrame, text="Sort", command=sortStages)
sortBtn.grid(column=0,row=3)
sortCombo.current(0)
######################sorting###########################################
#add some padding
# for frame in fen.winfo_children() :
#     for widget in frame.winfo_children():
#         widget.grid(padx=5, pady=5)
fen.mainloop()
