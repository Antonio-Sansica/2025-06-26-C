from database.DB_connect import DBConnect
from model.constructor import Constructor
from model.result import Result


class DAO():
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT DISTINCT r.`year` AS year
        FROM races r 
        ORDER BY r.`year` ASC 
                """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodi():
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)
        # Sostituito qualifying con results (almeno 1 gran premio)
        query = """
            SELECT DISTINCT c.* FROM constructors c 
            JOIN results r ON c.constructorId = r.constructorId 
            """
        cursor.execute(query)
        for row in cursor:
            constructor = Constructor(
                constructorId=row['constructorId'],
                name=row['name'],
                nationality=row['nationality'],
                url=row['url']
            )
            result.append(constructor)  # ERA FUORI DAL CICLO FOR NEL TUO CODICE!

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getRisultati(anno1, anno2, idC):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        # Tolti gli hardcode (4 e 1980) e messi i %s!
        query = """
                SELECT r2.`year`, r.raceId, r.driverId, r.position
                FROM results r 
                JOIN races r2 ON r.raceId = r2.raceId 
                WHERE r2.`year` BETWEEN %s AND %s AND r.constructorId = %s
                """
        cursor.execute(query, (anno1, anno2, idC))

        res = []
        for row in cursor:
            res.append(row)  # Restituisco la riga grezza, la gestiamo nel Model

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi_grafo_pesato(anno1, anno2, anno11, anno22):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT t1.id1 AS id_1, t2.id2 AS id_2, t1.peso1 + t2.peso2 AS peso_arco 
FROM
(SELECT DISTINCT r2.constructorId AS id1, COUNT(*) AS peso1
FROM races r
JOIN results r2 ON r.raceId = r2.raceId 
WHERE r.`year` BETWEEN %s AND %s AND r2.`position`  IS NOT NULL
GROUP BY r2.constructorId ) t1,
(SELECT DISTINCT r2.constructorId AS id2, COUNT(*) AS peso2
FROM races r
JOIN results r2 ON r.raceId = r2.raceId 
WHERE r.`year` BETWEEN %s AND %s AND r2.`position`  IS NOT NULL
GROUP BY r2.constructorId ) t2
WHERE t1.id1 < t2.id2
GROUP BY t1.id1, t2.id2
            
            """

            cursor.execute(query, (anno1, anno2, anno11, anno22))

            for row in cursor:
                # Appendo una TUPLA con i tre dati fondamentali per tracciare l'arco pesato
                result.append((row['id_1'], row['id_2'], row['peso_arco']))

            return result

        except Exception as e:
            print(f"Errore DAO estrazione archi: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()
