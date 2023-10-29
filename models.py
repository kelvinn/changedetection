from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, DateTime
from sqlalchemy.orm import relationship, mapped_column

from database import Base


class Store(Base):
    __tablename__ = 'store'
    gid = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    start_urls = Column(String, unique=True)  # keep URLs separately?


class Price(Base):
    __tablename__ = 'prices'
    gid = Column(Integer, primary_key=True)
    amount = Column(Float)
    product_gid = mapped_column(ForeignKey("products.gid"))
    product = relationship("Product", back_populates="prices")
    created = Column(DateTime)


class Product(Base):
    __tablename__ = 'products'
    gid = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    url = Column(String, unique=True)
    prices = relationship("Price", back_populates="product", lazy=False)
    created = Column(DateTime)
    last_updated = Column(DateTime)
