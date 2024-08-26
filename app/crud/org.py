from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models.org import OrgDatabase, OrgDatabaseTable, OrgDatabaseTableColumn


class DBInterface:
    def __init__(self, db: Session, org_metadata: list[tuple] = None):
        self.db = db
        self.org_metadata = org_metadata

    def _insert_metadata_into_db(self):
        db_name_list = [d[0] for d in self.org_metadata]
        db_name_set = set(db_name_list)
        models = [OrgDatabase(database_name=db_name)
                  for db_name in db_name_set]

        self.db.add_all(models)
        self.db.flush()

    def _insert_metadata_into_table(self):
        db_table_pair_list = [(d[0], d[1]) for d in self.org_metadata]
        db_table_pair_set = set(db_table_pair_list)

        # Get the database_id for each database {database: database_id}
        db_id_dict = {}
        for model_instance in self.db.query(OrgDatabase):
            db_id_dict[model_instance.database_name] = model_instance.database_id

        models = []

        for pair in db_table_pair_set:
            model = OrgDatabaseTable(
                table_name=pair[1],
                within_db=db_id_dict[pair[0]],  # ID of the database
            )
            models.append(model)

        self.db.add_all(models)
        self.db.flush()

    def _insert_metadata_into_column(self):
        for row in self.org_metadata:
            table = self.db.query(OrgDatabaseTable).join(OrgDatabase).filter(
                OrgDatabase.database_name == row[0],
                OrgDatabaseTable.table_name == row[1]
            ).first()

            model = OrgDatabaseTableColumn(
                column_name=row[2],
                ordinal_position=row[3],
                data_type=row[4],
                within_table=table.table_id
            )

            self.db.add(model)

        self.db.flush()

    def create_metadata(self) -> bool:
        '''Metadata creation process.

        The metadata is inserted into the database in the following order:
        1. org_database
        2. org_database_table
        3. org_database_table_column

        If the metadata already exists, the tables are dropped and recreated.
        After the tables are recreated, the metadata is inserted into the tables.
        '''

        OrgDatabaseTableColumn.__table__.drop(engine, checkfirst=True)
        OrgDatabaseTable.__table__.drop(engine, checkfirst=True)
        OrgDatabase.__table__.drop(engine, checkfirst=True)

        Base.metadata.create_all(
            bind=engine,
            tables=[
                OrgDatabase.__table__,
                OrgDatabaseTable.__table__,
                OrgDatabaseTableColumn.__table__
            ]
        )

        try:
            self._insert_metadata_into_db()
            self._insert_metadata_into_table()
            self._insert_metadata_into_column()
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False

        return True
