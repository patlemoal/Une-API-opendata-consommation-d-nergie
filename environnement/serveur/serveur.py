from flask import Flask, render_template, request, jsonify
from data import DataAccess as da

app = Flask(__name__)

#Données d'une région
@app.route("/region_data/<int:region>", methods=['GET'])
def get_region(region):
    da.connexion()
    data = da.get_region_data(region)
    da.deconnexion()
    for instance in data:
        instance["_id"] = str(instance["_id"])

    return jsonify(data), 200


#Données d'une filière pour une région
@app.route("/region_sector_data/<sector>/<int:region>", methods=['GET'])
def get_region_sector_data(sector, region):
    da.connexion()
    data = da.get_region_sector_data(sector, region)
    da.deconnexion()
    for instance in data:
        instance["_id"] = str(instance["_id"])

    return jsonify(data), 200

#Données d'une filière
@app.route("/sector_data/<sector>/<int:position>", methods=['GET'])
def get_sector_data(sector, position):
    da.connexion()
    data = da.get_sector_data(sector, position)
    da.deconnexion()
    for instance in data:
        instance["_id"] = str(instance["_id"])

    return jsonify(data), 200


#Consommation totale d'une filière
@app.route("/sector_conso/<sector>", methods=['GET'])
def get_sector_conso(sector):
    da.connexion()
    data = da.get_sector_conso(sector)
    da.deconnexion()

    return jsonify(data), 200


#Consommation totale d'une filière sur un département
@app.route("/dept_sector_conso/<dept>/<sector>", methods=['GET'])
def get_dept_sector_conso(dept, sector):
    da.connexion()
    try:
        data = da.get_dept_sector_conso(dept, sector)
    except IndexError:
        data = 0
    da.deconnexion()
    return jsonify(data), 200


#route pour supprimer un document
@app.route("/env/<id>", methods=['DELETE'])
def delete_doc(cls, id):
    da.connexion()
    da.delete_doc(id)
    da.deconnexion()

    return jsonify({"message":"document supprimé avec succès"}), 200

#récupère les valeurs correspondats à l'id du document
@app.route("/document/<id>", methods=['GET'])
def get_fields(id):
    da.connexion()
    data = da.get_document(id)
    da.deconnexion()
    data["_id"] = str(data["_id"])

    return jsonify(data), 200

@app.route("/document/update/<id>", methods=['PUT'])
def update_document(id):
    #on récupère les données du formulaire pour les envoyer à la bdd
    donne_front = request.form.to_dict()
    print(donne_front)
    da.connexion()
    da.update_doc(id, donne_front)
    da.deconnexion()

    return jsonify("Le document a bien été modifié"), 200


@app.route("/document/delete/<id>", methods=['DELETE'])
def delete_document(id):
    #on récupère les données du formulaire pour les envoyer à la bdd
    da.connexion()
    da.delete_doc(id)
    da.deconnexion()

    return jsonify("Le document à été supprimé avec succès"), 200

#gestion d'erreurs
@app.errorhandler(404)
def page_not_found(e):

    return "erreur", 404


#lancement de l'app
if __name__ == "__main__" :
    app.run(debug=True, port=5001)