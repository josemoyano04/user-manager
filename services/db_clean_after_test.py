#TODO Pendiente de integracion.

from services.db_client_conection import create_client
from libsql_client import ResultSet


#================================Client================================
CLIENT = create_client

#================================Service================================

async def get_sqlite_sequence() -> list:
    """
    Obtiene la secuencia de la tabla sqlite_sequence de la base de datos.

    Este método asíncrono crea un cliente de base de datos, ejecuta una consulta para seleccionar todos los registros
    de la tabla sqlite_sequence y devuelve los resultados.

    Returns:
        list: Una lista de filas que representan la secuencia de la tabla sqlite_sequence.
    """
    client = await CLIENT()
    query = "SELECT * FROM sqlite_sequence"
    data = await client.execute(query)
    await client.close()

    return data.rows

async def restore_sqlite_sequence(backup_data: list) -> None:
    """
    Restaura la secuencia de la tabla sqlite_sequence utilizando datos de respaldo.

    Este método asíncrono crea un cliente de base de datos y actualiza la tabla sqlite_sequence con los datos
    proporcionados en la lista backup_data. Cada fila de backup_data debe contener el nombre de la tabla y el
    valor de la secuencia correspondiente.

    Args:
        backup_data (list): Una lista de listas/tuplas, donde cada sublista contiene el nombre de la tabla y el valor
                            de la secuencia a restaurar. Vea el metodo get_sqlite_sequence() el cual obtiene los datos
                            en el formato admitido por este metodo.
    """
    client = await CLIENT()
    for row in backup_data:
        query = f"""
                UPDATE sqlite_sequence
                SET seq = ?
                WHERE name = ?
                """
        await client.execute(query, [row[1], row[0]])
    await client.close()
