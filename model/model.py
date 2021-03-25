import os
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

Base = declarative_base()


class Portfolio(Base):
    """ Database model to store ticker, shares, and cost basis per share. """

    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    shares = Column(Float)
    cost_basis = Column(Float)


class DB:
    """ Interfacing database class to work with Portfolio model. """

    def __init__(self):
        engine = create_engine(
            "sqlite:///" + os.path.join(BASE_DIR, "portfolio.db") + "?check_same_thread=False",
            echo=False,
        )
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # perhaps add an update method and purge method

    def read_all(self):
        return self.session.query(Portfolio).all()

    def write(self, item):
        portfolio_db = Portfolio(
            symbol=item["symbol"], shares=item["shares"], cost_basis=item["cost_basis"],
        )
        self.session.add(portfolio_db)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # if someone tries to add the same ticker symbol twice
            print(f"symbol '{item['symbol']}' already exists.")
