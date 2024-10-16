from flask import Flask, request, jsonify
import mysql.connector
from db import Database

app = Flask(__name__)

db = Database("127.0.0.1","root","","ciel2025") 

@app.route('/v3/etudiants/', methods=['GET'])
def getAllEtudiant():
    try:
        # Check if the request is authorized
        if not db.authorized(request):
            return jsonify({"message": "Accès non autorisé"}), 401
        
        #if 'required_param' not in request.args:
            # 400 Bad Request: Missing or invalid parameter
            #return jsonify({"message": "Commande SQL incorrecte"}), 400
        # Fetch all students from the database
        etudiants = []
        result = db.readAll()

        # Parse the result and build the response                                                                           
        for row in result:                                                                          
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }
            etudiants.append(etudiant)

        # Return the list of students as a JSON response
        return jsonify(etudiants), 200

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({"message": f"Erreur interne du serveur: {err}"}), 500
    
    except Exception as e:
        # Catch all other errors (if any)
        return jsonify({"message": f"Erreur: {str(e)}"}), 500

@app.route('/v3/etudiant/<int:id>', methods=['GET'])
def getEtudiant(id):
    try:
        if not db.authorized(request):
            return jsonify("Message : Accès non autorisé"), 401

        #if 'required_param' not in request.args:
            # 400 Bad Request: Missing or invalid parameter
            #return jsonify({"message": "Commande SQL incorrecte"}), 400
        result = db.readOne(id)

        if not result:
            return jsonify({"message": "Aucun étudiant trouvé"}), 404
    
        if result: 
            etudiant = {
                "idetudiant": result[0],
                "nom": result[1],
                "prenom": result[2],
                "email": result[3],
                "telephone": result[4]
            }     
        return jsonify(etudiant), 200
    
    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({"message": f"Erreur interne du serveur: {err}"}), 500
    
    except Exception as e:
        # Catch all other errors (if any)
        return jsonify({"message": f"Erreur: {str(e)}"}), 500

@app.route('/v3/etudiants/', methods=['POST'])
def createEtudiant():
    try:
        
        if not db.authorized(request):
            return jsonify("Message : Accès non autorisé"), 401

        data = request.json
        nom = data['nom']
        prenom = data['prenom']
        email = data['email']
        telephone = data['telephone']

        result = db.create(nom, prenom, email, telephone)

        return jsonify({"message": "Étudiant créé avec succès"}), 201

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({"message": f"Erreur interne du serveur: {err}"}), 500
    
    except Exception as e:
        # Catch all other errors (if any)
        return jsonify({"message": f"Erreur: {str(e)}"}), 500

@app.route('/v3/etudiant/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    try:
        if not db.authorized(request):
            return jsonify("Message : Accès non autorisé"), 401
    
        result = db.delete(id)
        if result > 0:
            return jsonify({"message": "Étudiant supprimé avec succès"}), 200
        else:
            return jsonify({"message": "Étudiant non trouvé ou déjà supprimé"}), 404

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({"message": f"Erreur interne du serveur: {err}"}), 500
    
    except Exception as e:
        # Catch all other errors (if any)
        return jsonify({"message": f"Erreur: {str(e)}"}), 500
    
@app.route('/v3/etudiant/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    try:
        if not db.authorized(request):
            return jsonify("Message : Accès non autorisé"), 401
    
        data = request.json
        nom = data['nom']
        prenom = data['prenom']
        email = data['email']
        telephone = data['telephone']

        result = db.update(nom, prenom, email, telephone, id)
        if result > 0:
            return jsonify({"message": "Étudiant mis a jour avec succès"}), 200
        else:
            return jsonify({"message": "Étudiant non trouvé ou déjà supprimé"}), 404

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({"message": f"Erreur interne du serveur: {err}"}), 500
    
    except Exception as e:
        # Catch all other errors (if any)
        return jsonify({"message": f"Erreur: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)