from sqlmodel import Field, SQLModel, create_engine, Session


DATABASE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{DATABASE_NAME}"

class Tree(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tree_id: str
    lon: str
    lan: str
    height: int
    owner: str


engine = create_engine(SQLITE_URL, echo=True)

SQLModel.metadata.create_all(engine)
session = Session(engine)
