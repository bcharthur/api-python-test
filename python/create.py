import mysql.connector

def create_item(nom):
    """
    Crée un nouvel item dans la table.
    """
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Changez ces informations selon votre configuration MySQL
            password="",  # Mot de passe par défaut dans XAMPP est vide
            database="db_api_test"
        )

        # Créer un curseur
        cursor = connection.cursor()

        # Exécuter la requête
        cursor.execute("INSERT INTO item (nom) VALUES (%s)", (nom,))

        # Commit des modifications
        connection.commit()

        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        # Gestion des erreurs liées à MySQL
        raise Exception(f"Erreur MySQL : {err}")
    except Exception as e:
        # Gestion des autres erreurs
        raise Exception(f"Erreur lors de l'insertion dans la base : {e}")
