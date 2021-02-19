from flask import Flask, render_template, jsonify, redirect, url_for, request
import json

import requests

URL_API = "http://127.0.0.1:5001"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# Affichage des données d'une région
@app.route("/region_data/<int:code_region>")
def region_data(code_region):
    url = URL_API + "/region_data/" + str(code_region)
    reponse = requests.get(url)
    nom_region = json.loads(reponse.content.decode("utf-8"))

    #filière
    filiere = ('Gaz', 'Electricité')

    #nom de la région
    region_name = nom_region[0]['fields']['libelle_region']

    #données region par filière
    #gaz
    url = URL_API + "/region_sector_data/Gaz/" + str(code_region)
    reponse = requests.get(url)
    conso_gaz = json.loads(reponse.content.decode("utf-8"))
    conso_region_gaz = 0
    for i in range(len(conso_gaz)):
        conso_region_gaz = conso_region_gaz + conso_gaz[i]['fields']['conso']
    conso_region_gaz = round(conso_region_gaz, 2)

    #Electricité
    url = URL_API + "/region_sector_data/Electricité/" + str(code_region)
    reponse = requests.get(url)
    conso_elec = json.loads(reponse.content.decode("utf-8"))
    conso_region_elec = 0
    for i in range(len(conso_elec)):
        conso_region_elec = conso_region_elec + conso_elec[i]['fields']['conso']
    conso_region_elec = round(conso_region_elec, 2)    

    #nom des départements
    departement = {}
    departement = set()
    for i in range(len(nom_region)):
        departement.add(nom_region[i]['fields']['libelle_departement'])


    return render_template("region.html",
                            region_name = region_name,
                            departement = departement,
                            filiere = filiere,
                            conso_region_gaz = conso_region_gaz,
                            conso_region_elec = conso_region_elec)


@app.route("/region/<code_region>/<int:position>")
def get_region(code_region, position):
    code_region = str(code_region)
    region_gas = requests.get(f"{URL_API}/region_sector_conso/{code_region}/Gaz")
    region_gas = json.loads(region_gas.content.decode("utf-8"))

    region_electricity = requests.get(f"{URL_API}/region_sector_conso/{code_region}/Electricité")
    region_electricity = json.loads(region_electricity.content.decode("utf-8"))

    region_data = requests.get(f"{URL_API}/region_data/{code_region}/{position}")
    region_data = json.loads(region_data.content.decode("utf-8"))

    dict_region = {'84':"Auvergne-Rhône-Alpes", '27':"Bourgogne-Franche-Comté", '53':"Bretagne", '24':"Centre-Val de Loire", '94':"Corse", '44':"Grand Est", '32':"Hauts-de-France", '11':"Île-de-France", '28':"Normandie", '75':"Nouvelle-Aquitaine", '76':"Occitanie", '52':"Pays de la Loire", '93':"Provence-Alpes-Côte d'Azur", '1':"Guadeloupe", '2':"Martinique", '3':"Guyane", '4':"La Réunion", '6':"Mayotte"}

    region_name = dict_region[code_region]
    
    return render_template("regionbaptiste.html", code_region=code_region, region_name=region_name, region_data=region_data, region_gas=region_gas, region_electricity=region_electricity, position=position)

#conso département par secteur
@app.route("/dep_data/<string:sector>/<string:departement>")
def dep_conso(departement, sector):
    url = URL_API + "/dept_sector_conso/" + str(departement) + "/" + str(sector)
    reponse = requests.get(url)
    dep_conso = json.loads(reponse.content.decode("utf-8"))
    unite = 'MWh'
    dep_conso = round(dep_conso, 2)
    dep_conso = "{:,}".format(dep_conso).replace(","," ")
    return render_template("departement.html", dep_conso = dep_conso, dep = departement, sector = sector, unite = unite)


@app.route("/sector/<sector>/<int:position>")
def get_sector(sector, position):

    url_conso = f"{URL_API}/sector_conso/{sector}"
    url_data = f"{URL_API}/sector_data/{sector}/{position}"

    sector_conso = requests.get(url_conso)
    sector_conso = json.loads(sector_conso.content.decode("utf-8"))

    sector_data = requests.get(url_data)
    sector_data = json.loads(sector_data.content.decode("utf-8"))
    
    return render_template("sector.html", sector=sector, sector_conso=sector_conso, sector_data=sector_data, position=position)


# Route qui propose la modification du document
@app.route("/document")
def document_choix():

    return render_template("choix_modification.html")


# Route qui crée un formulaire qui modifie un document
@app.route("/document/formulaire", methods=['POST'])
def document_formulaire():
    id = request.form.to_dict()

    url = URL_API + "/document/" + str(id['id'])
    reponse = requests.get(url)
    dataPy = json.loads(reponse.content.decode("utf-8"))
  
    return render_template("formulaire_modification.html", data = dataPy)



#Route qui récupère et envoie à l'api les valeurs
@app.route("/document/traitement", methods=['POST'])
def document_traitement():
    data = request.form.to_dict()

    url = URL_API + "/document/update/" + str(data['id'])
    del data["id"]
    #la fonction put  requete http qui envoie vers le serveur et à forcément l'url et la data
    reponse = requests.put(url, data=data)
    print(reponse)

    dataPy = json.loads(reponse.content.decode("utf-8"))
    return render_template("etudiant.html", donnee = dataPy)



# Route qui propose la suppression du document
@app.route("/suppression_choix")
def suppression_choix():

    return render_template("suppression.html")


#Suppression d'un document
@app.route("/suppression", methods=["POST"])
def supp_doc():
    data = request.form.to_dict()

    url = URL_API + "/document/delete/" + str(data['id'])
    reponse = requests.delete(url)
    dataPy = json.loads(reponse.content.decode("utf-8"))
    return render_template("etudiant.html", donnee = dataPy)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__" :
    app.run(debug=True, port=5000)