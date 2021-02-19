from pymongo import MongoClient
from bson import ObjectId
import pprint

class DataAccess :
    size = 0

    @classmethod
    def connexion(cls) :
        cls.client = MongoClient()
        cls.db = cls.client['agence_ore']

    @classmethod
    def deconnexion(cls) :
        cls.client.close()

    #méthode pour récupérer les données par secteur
    @classmethod
    def get_sector_data(cls, sector, position):
        data = cls.db.conso.find({"fields.filiere":sector})
        data = list(data)
        start = max(0, position*10)
        end = min(((position+1) * 10), len(data))
        return data[start:end]

    #méthode pour récupérer les données par région
    @classmethod
    def get_region_data(cls, region):
        data = cls.db.conso.find({"fields.code_region":region})
        return list(data)

    #méthode pour récupérer les données par région et par secteur
    @classmethod
    def get_region_sector_data(cls, sector, region):
        pipe = [{"$match": {"$and": [{"fields.filiere": sector}, {"fields.code_region": region}]}}]
        data = cls.db.conso.aggregate(pipeline = pipe)
        data = list(data)
        return data

    #méthode qui récupère les données de consommation par secteur et par département
    @classmethod
    def get_dept_sector_conso(cls, dept, sector):
        pipe = [{"$match": {"$and": [{"fields.filiere": sector},{"fields.libelle_departement": str(dept)}]}}, {'$group': {'_id': None, 'total': {'$sum': '$fields.conso'}}}]
        data = cls.db.conso.aggregate(pipeline=pipe)
        data = list(data)[0]
        return data["total"]

    # méthode qui récupère la consommation par secteur
    @classmethod
    def get_sector_conso(cls, sector):
        pipe = [{"$match": {"fields.filiere": sector}}, {'$group': {'_id': None, 'total': {'$sum': '$fields.conso'}}}]
        data = cls.db.conso.aggregate(pipeline=pipe)
        data = list(data)[0]
        return data["total"]

    #suppression d'un document précis
    @classmethod
    def delete_doc(cls, id):
        cls.db.conso.delete_one({'_id': ObjectId(id)})
    
    #création d'une fonction qui recherche les éléments pour la mise à jour des champs
    @classmethod
    def get_document(cls, id):
        data = cls.db.conso.find_one({"_id":ObjectId(id)})
        return data

    # modifier un document précis
    @classmethod
    def update_doc(cls, id, list_info):
        #data = {"fields.libelle_epci" : list_info[0], "fields.libelle_region" : list_info[1], "fields.filiere" : list_info[2], "fields.code_region" :list_info[3], "fields.libelle_iris" : list_info[4], "fields.partr" : list_info[5], "fields.libelle_grand_secteur" : list_info[6], "fields.operateur" : list_info[7], "fields.code_naf" : list_info[8], "fields.conso" : list_info[9], "fields.code_epci" : list_info[10], "fields.code_grand_secteur" : list_info[11], "fields.code_commune" : list_info[12], "fields.libelle_commune" : list_info[13], "fields.annee" : list_info[14], "fields.thermor" : list_info[15], "fields.libelle_departement" : list_info[16], "fields.indqual" : list_info[17], "fields.pdl" : list_info[18], "fields.code_departement" : list_info[19], "fields.code_iris" : list_info[20], "fields.nombre_mailles_secretisees" : list_info[21]}
        cls.db.conso.update_one({"_id":ObjectId(id)}, {'$set': list_info})


#DataAccess.connexion()
#print(DataAccess.get_region_sector_data("Electricité", 84))