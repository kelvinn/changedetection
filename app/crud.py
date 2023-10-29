from sqlalchemy.orm import Session

import models
from app import schemas


def get_product(db: Session, product_gid: int):
    product = db.query(models.Product).filter(models.Product.gid ==product_gid).first()

    return product
