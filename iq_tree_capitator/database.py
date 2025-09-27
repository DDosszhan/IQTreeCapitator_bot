import uuid
from sqlmodel import Field, SQLModel, create_engine


DATABASE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{DATABASE_NAME}"


class Tree(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    owner: str
    height: int
    lon: float
    lan: float


engine = create_engine(SQLITE_URL, echo=True)

SQLModel.metadata.create_all(engine)
