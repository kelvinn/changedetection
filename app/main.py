from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/{product_gid}/", response_model=schemas.Product)
def read_product(product_gid: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_gid=product_gid)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=List[schemas.ProductSummary])
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products
