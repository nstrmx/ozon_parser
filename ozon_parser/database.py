import typing
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func


log = logging.getLogger("default")


link = "sqlite:///data.db"
engine = create_engine(link)

DB_SESSIONS = {
    "default": sessionmaker(),
}

@contextmanager
def connect(using: str = "default") -> typing.Generator[Session, None, None]:
    Session = DB_SESSIONS[using]
    Session.configure(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    old_price = Column(Integer, nullable=False)
    new_price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Database:
    def generate(self, data_itr):
        products = []
        for item in data_itr:
            product = Product(
                title=item.title,
                old_price=item.old_price,
                new_price=item.new_price,
                discount=item.discount
            )
            products.append(product)
            yield item
        log.debug(products)
        if len(products) == 0:
            return
        with connect() as session:
            session.bulk_save_objects(products)
            session.commit()