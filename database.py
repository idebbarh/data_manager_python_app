from pymongo import MongoClient

class Stage:
    cnx = MongoClient(host="localhost",port=27017)
    db = cnx["DB_stage"]
    collection_stage = db['stage']

    def __init__(self,id="",intitule="",duree="",prix="",domaine="") :
        self.id = id
        self.intitule = intitule
        self.duree = duree
        self.prix = prix
        self.domaine = domaine

    def getAllStages(self) :
        return list(Stage.collection_stage.find())
        
    def getByComplexeSearch(self,myQuery) :
        return list(Stage.collection_stage.find(myQuery[0]))

    def prixTotalByDomaine(self,domaine):
        prixTotal = Stage.collection_stage.aggregate([{"$match":{"domaine":domaine}},{"$group":{"_id":None,"total price":{"$sum":"$prix"}}}])
        return list(prixTotal)

    def avgPriceBydomaine(self,domaine):
        avgPrice = Stage.collection_stage.aggregate([{"$match":{"domaine":domaine}},{"$group":{"_id":None,"average price":{"$avg":"$prix"}}}])
        return list(avgPrice)

    def minMaxPrice(self):
        minMax = Stage.collection_stage.aggregate([{"$group":{"_id":None,"min price":{"$min":"$prix"},"max price":{"$max":"$prix"}}}])
        return list(minMax)

    def stagesCount(self):
        stagesCount = Stage.collection_stage.aggregate([{"$group":{"_id":None,"totale stages":{"$sum":1}}}])
        return list(stagesCount)

    def getStageById(self,id) :
        return list(Stage.collection_stage.find({"id":id}))

    def getByDomaine(self,domaine):
        return list(Stage.collection_stage.find({"domaine":domaine}))

    def insertStage(self) :
        if not self.getStageById(self.id) :
            Stage.collection_stage.insert_one({"id":self.id,"intitule":self.intitule,"duree":self.duree,"prix":self.prix,"domaine":self.domaine})
    
    def updateStage(self):
        Stage.collection_stage.update_one({"id":self.id},{"$set":{"intitule":self.intitule,"duree":self.duree,"prix":self.prix,"domaine":self.domaine}})
    
    def deleteStage(self,id):
        Stage.collection_stage.delete_one({"id":id})