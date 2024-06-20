from unicodedata import name
import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
    Uuid
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
import uuid

BaseModel = declarative_base()
###

def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#

class FacilityModel(BaseModel):
    """Spravuje data spojena s objektem daneho typu"""

    __tablename__ = "facilities"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    label = Column(String)
    address = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    capacity = Column(Integer)
    geometry = Column(String)
    geolocation = Column(String)

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)
    facilitytype_id = Column(ForeignKey("facilitytypes.id"), index=True)
    master_facility_id = Column(ForeignKey("facilities.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class FacilityTypeModel(BaseModel):
    """Urcuje typ objektu (areal, budova, patro, mistnost)"""

    __tablename__ = "facilitytypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    #facilities = relationship("FacilityModel", back_populates="facilitytype")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class EventFacilityModel(BaseModel):
    __tablename__ = "facilities_events"

    id = UUIDColumn()
    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True)
    facility_id = Column(ForeignKey("facilities.id"), index=True)
    state_id = Column(ForeignKey("facilityeventstatetypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class EventFacilityStateType(BaseModel):
    __tablename__ = "facilityeventstatetypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    # rozvrh, naplánováno, žádost, schváleno, zrušeno, ...
    # planned, requested, accepted, canceled, priority0, priority1, ...

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

# class FacilityManagement(BaseModel):
#     __tablename__ = "facilitymanagementgroups"

#     id = UUIDColumn()
#     facility_id = Column(ForeignKey("facilities.id"), index=True)
#     group_id = UUIDFKey(nullable=False)#Column(ForeignKey("groups.id"), index=True)

#     created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
#     lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
#     createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
#     changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

###########################################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5435")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring
