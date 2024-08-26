import psycopg

from app.schemas.org import DBConnectionForm


METADATA_EXTRACTION_QUERY = '''
SELECT table_catalog AS database, table_name, column_name, ordinal_position, data_type
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY database, table_name, ordinal_position
;
'''


def get_org_metadata(form_data: DBConnectionForm) -> list[tuple]:
    org_database_url = f'postgresql://{form_data.user}:\
{form_data.password}@{form_data.host}:{form_data.port}/{form_data.db_name}'

    try:
        with psycopg.connect(org_database_url) as conn:  # pylint: disable=not-context-manager
            with conn.cursor() as cur:
                cur.execute(METADATA_EXTRACTION_QUERY)
                metadata = cur.fetchall()
    except Exception:
        return []

    return metadata
