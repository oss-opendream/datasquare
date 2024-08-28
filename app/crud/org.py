from sqlalchemy.orm import Session

# from app.database import Base, engine
from app.models.database import datasquare_db, Base
from app.models.org import OrgDatabase, OrgDatabaseTable, OrgDatabaseTableColumn, DatabaseTag, DatabaseTagRelationship


class DBInterface():
    def __init__(self):
        # def __init__(self, db, org_metadata: list[tuple] = None):
        self.db = datasquare_db
        self.org_metadata = None

    def _insert_metadata_into_db(self):
        db_name_list = [d[0] for d in self.org_metadata]
        db_name_set = set(db_name_list)

        with next(self.db.get_db()) as db:
            for db_name in db_name_set:
                model = OrgDatabase(database_name=db_name)
                db.add(model)
            # db.add_all(models)
                db.commit()

    def _insert_metadata_into_table(self):
        db_table_pair_list = [(d[0], d[1]) for d in self.org_metadata]

        db_table_pair_set = set(db_table_pair_list)

        # Get the database_id for each database {database: database_id}
        db_id_dict = {}

        with next(self.db.get_db()) as db:
            # a = db.query(OrgDatabase).one()
            for model_instance in db.query(OrgDatabase):
                db_id_dict[model_instance.database_name] = model_instance.database_id
            models = []

            for pair in db_table_pair_set:
                model = OrgDatabaseTable(
                    table_name=pair[1],
                    within_db=db_id_dict[pair[0]],  # ID of the database
                )
                models.append(model)

            db.add_all(models)
            db.commit()

    def _insert_metadata_into_column(self):

        with next(self.db.get_db()) as db:
            for row in self.org_metadata:
                table = db.query(OrgDatabaseTable).join(OrgDatabase).filter(
                    OrgDatabase.database_name == row[0],
                    OrgDatabaseTable.table_name == row[1]
                ).first()

                model = OrgDatabaseTableColumn(
                    column_name=row[2],
                    ordinal_position=row[3],
                    data_type=row[4],
                    within_table=table.table_id
                )

                db.add(model)
            db.commit()

    def create_metadata(self, org_metadata: list[tuple] = None) -> bool:
        '''Metadata creation process.

        The metadata is inserted into the database in the following order:
        1. org_database
        2. org_database_table
        3. org_database_table_column

        If the metadata already exists, the tables are dropped and recreated.
        After the tables are recreated, the metadata is inserted into the tables.
        '''

        # OrgDatabaseTableColumn.__table__.drop(engine, checkfirst=True)
        # OrgDatabaseTable.__table__.drop(engine, checkfirst=True)
        # OrgDatabase.__table__.drop(engine, checkfirst=True)

        OrgDatabaseTableColumn.__table__.drop(
            datasquare_db.engine, checkfirst=True)
        OrgDatabaseTable.__table__.drop(datasquare_db.engine, checkfirst=True)
        OrgDatabase.__table__.drop(datasquare_db.engine, checkfirst=True)

        Base.metadata.create_all(
            bind=datasquare_db.engine,
            tables=[
                OrgDatabase.__table__,
                OrgDatabaseTable.__table__,
                OrgDatabaseTableColumn.__table__
            ]
        )

        try:
            # with next(self.db.get_db()) as db:
            self.org_metadata = org_metadata
            self._insert_metadata_into_db()
            self._insert_metadata_into_table()
            self._insert_metadata_into_column()
            # db.commit()
            # db.refresh()
        except Exception:
            with next(self.db.get_db()) as db:
                db.rollback()
            return False

        return True

    def read_databases(self):
        with next(self.db.get_db()) as db:
            databases = db.query(OrgDatabase, OrgDatabaseTable).all()

            database_list = []

            for databases, table in databases:
                col = db.query(OrgDatabaseTableColumn).filter(
                    OrgDatabaseTableColumn.within_table == table.table_id).all()
                col_name = [c.column_name for c in col]
                database_list.append(
                    [databases, table, len(col), ', '.join(col_name)])

        return database_list
