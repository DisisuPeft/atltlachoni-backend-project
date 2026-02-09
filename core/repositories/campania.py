from django.db import connection
from core.helpers import fetch_all_parser

class CampaniaRepositoryService:
    @staticmethod
    def get_campania():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, pe.nombre as nombre 
                FROM control_escolar_campania c
                INNER JOIN control_escolar_programaeducativo pe on c.programa_id = pe.id
                WHERE c.status = 1
                AND pe.status = 1
            """)
            return fetch_all_parser(cursor)
