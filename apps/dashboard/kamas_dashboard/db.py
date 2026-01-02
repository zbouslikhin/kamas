from sqlmodel import create_engine

engine = create_engine(
    "sqlite:///kamastrainer.db",
    echo=False,
)