import argparse
import logging
import typing as t
from pathlib import Path

from cratedb_toolkit.io.mongodb.cdc import MongoDBCDCRelayCrateDB
from cratedb_toolkit.io.mongodb.copy import MongoDBFullLoad
from cratedb_toolkit.io.mongodb.core import export, extract, translate
from cratedb_toolkit.io.mongodb.transform import TransformationManager
from cratedb_toolkit.model import DatabaseAddress
from cratedb_toolkit.util.cr8 import cr8_insert_json
from cratedb_toolkit.util.database import DatabaseAdapter

logger = logging.getLogger(__name__)


def mongodb_copy_migr8(source_url, target_url, transformation: Path = None, limit: int = 0, progress: bool = False):
    """
    Transfer MongoDB collection using migr8.

    Synopsis
    --------
    export CRATEDB_SQLALCHEMY_URL=crate://crate@localhost:4200/testdrive/demo
    ctk load table mongodb://localhost:27017/testdrive/demo

    Backlog
    -------
    TODO: Run on multiple collections.
    TODO: Run on the whole database.
    TODO: Accept parameters like `if_exists="append,replace"`.
    TODO: Propagate parameters like `scan="full"`.
    TODO: Handle timestamp precision(s)?
    """
    logger.info("Running MongoDB copy")

    # Decode database URL.
    mongodb_address = DatabaseAddress.from_string(source_url)
    mongodb_uri, mongodb_collection_address = mongodb_address.decode()
    mongodb_database = mongodb_collection_address.schema
    mongodb_collection = mongodb_collection_address.table

    # 1. Extract schema from MongoDB collection.
    logger.info(f"Extracting schema from MongoDB: {mongodb_database}.{mongodb_collection}")
    extract_args = argparse.Namespace(
        url=str(mongodb_uri) + f"&limit={limit}",
        database=mongodb_database,
        collection=mongodb_collection,
        scan="partial",
        transformation=transformation,
    )
    mongodb_schema = extract(extract_args)
    count = mongodb_schema[mongodb_collection]["count"]
    if not count > 0:
        logger.error(f"No results when extracting schema from MongoDB: {mongodb_database}.{mongodb_collection}")
        return False

    # 2. Translate schema to SQL DDL.
    cratedb_address = DatabaseAddress.from_string(target_url)
    cratedb_uri, cratedb_table_address = cratedb_address.decode()
    ddl = translate(mongodb_schema, schemaname=cratedb_table_address.schema)

    # 3. Load schema SQL DDL into CrateDB.
    cratedb = DatabaseAdapter(dburi=str(cratedb_uri))
    for collection, query in ddl.items():
        logger.info(f"Creating table for collection '{collection}': {query}")
        cratedb.run_sql(query)

    # 4. Transfer data to CrateDB.
    """
    migr8 export --host localhost --port 27017 --database test_db --collection test | \
        cr8 insert-json --hosts localhost:4200 --table test
    """
    logger.info(
        f"Transferring data from MongoDB to CrateDB: "
        f"source={mongodb_collection_address.fullname}, target={cratedb_table_address.fullname}"
    )
    export_args = argparse.Namespace(
        url=str(mongodb_uri) + f"&limit={limit}",
        database=mongodb_database,
        collection=mongodb_collection,
        transformation=transformation,
    )
    buffer = export(export_args)
    cr8_insert_json(infile=buffer, hosts=cratedb_address.httpuri, table=cratedb_table_address.fullname)

    return True


def mongodb_copy(source_url, target_url, transformation: t.Union[Path, None] = None, progress: bool = False):
    """
    Transfer MongoDB collection using translator component.

    Synopsis
    --------
    export CRATEDB_SQLALCHEMY_URL=crate://crate@localhost:4200/testdrive/demo
    ctk load table mongodb://localhost:27017/testdrive/demo
    """

    logger.info(f"Invoking MongoDBFullLoad. source_url={source_url}")

    # Optionally configure transformations.
    tm = None
    if transformation:
        tm = TransformationManager(path=transformation)

    # Invoke `full-load` procedure.
    mdb_full = MongoDBFullLoad(
        mongodb_url=source_url,
        cratedb_url=target_url,
        tm=tm,
        progress=progress,
    )
    mdb_full.start()
    return True


def mongodb_relay_cdc(source_url, target_url, progress: bool = False):
    """
    Synopsis
    --------
    export CRATEDB_SQLALCHEMY_URL=crate://crate@localhost:4200/testdrive/demo-cdc
    ctk load table mongodb+cdc://localhost:27017/testdrive/demo

    Backlog
    -------
    TODO: Run on multiple collections.
    TODO: Run on the whole database.
    TODO: Accept parameters like `if_exists="append,replace"`.
    TODO: Propagate parameters like `scan="full"`.
    """
    logger.info("Running MongoDB CDC relay")

    # Decode database URL.
    mongodb_address = DatabaseAddress.from_string(source_url)
    mongodb_uri, mongodb_collection_address = mongodb_address.decode()
    mongodb_database = mongodb_collection_address.schema
    mongodb_collection = mongodb_collection_address.table

    cratedb_address = DatabaseAddress.from_string(target_url)
    cratedb_uri, cratedb_table_address = cratedb_address.decode()

    # Configure machinery.
    relay = MongoDBCDCRelayCrateDB(
        mongodb_url=str(mongodb_uri),
        mongodb_database=mongodb_database,
        mongodb_collection=mongodb_collection,
        cratedb_sqlalchemy_url=str(cratedb_uri),
        cratedb_table=cratedb_table_address.fullname,
    )

    # Invoke machinery.
    relay.start()
