import mysql.connector

def delete_item(item_id):
    """
    Supprime un item de la table.
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

        # Exécuter la requête de suppression
        cursor.execute("DELETE FROM item WHERE id = %s", (item_id,))

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
        raise Exception(f"Erreur lors de la suppression de l'item : {e}")
