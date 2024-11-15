import mysql.connector
import logging

def list_items():
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Changez ces informations selon votre configuration MySQL
            password="",  # Mot de passe par défaut dans XAMPP est vide
            database="db_api_test"
        )

        cursor = connection.cursor(dictionary=True)  # `dictionary=True` pour retourner les résultats sous forme de dictionnaires
        cursor.execute("SELECT * FROM item")
        items = cursor.fetchall()

        # Fermez les connexions
        cursor.close()
        connection.close()

        # Retournez les données sous format liste (pas de jsonify ici)
        return {"status": "success", "data": items}

    except mysql.connector.Error as e:
        logging.error(f"[LIST] Erreur MySQL: {e}")
        return {"status": "error", "message": f"MySQL Error: {str(e)}"}

    except Exception as e:
        logging.error(f"[LIST] Erreur générale: {e}")
        return {"status": "error", "message": str(e)}
