from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    from app.models import User  # noqa: F401

    Base.metadata.create_all(bind=engine)


init_db()
