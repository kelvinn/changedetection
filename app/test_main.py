from fastapi.testclient import TestClient
import models
from database import SessionLocal, engine
from .main import app
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_read_main():

    name = "Sample Shirt"
    url = "https://www.outdoorstore.com"
    amount = 123.45

    db = SessionLocal()

    product = db.query(models.Product).filter_by(name=name).one_or_none()
    if not product:
        # Add a test product
        product = models.Product(name=name, url=url, created=datetime.now(), last_updated=datetime.now())
        db.add(product)
        db.commit()
        db.refresh(product)

    # Add a test price
    price = models.Price(amount=amount, product=product, created=datetime.now())
    db.add(price)
    db.commit()
    
    response = client.get(f'/products/{product.gid}/')
    assert response.status_code == 200
    data = response.json()

    assert data['name'] == name
    assert data['url'] == url
    assert data['prices'][0]['amount'] == amount

    product = db.query(models.Product).filter_by(name=name).one_or_none()

    # Cleanup
    db.query(models.Price).filter(models.Price.product_gid == product.gid).delete(synchronize_session=False)  # noqa
    db.query(models.Product).filter(models.Product.name == product.name).delete(synchronize_session=False)  # noqa
    db.commit()
