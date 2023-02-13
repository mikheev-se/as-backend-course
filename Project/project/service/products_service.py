from fastapi import Depends
from sqlalchemy.orm import Session

from project.db.db import get_session
from project.models.dto.products_dto import CreateProductDto, UpdateProductDto
from project.models.product import Product


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> list[Product]:
        products = (
            self.session
            .query(Product)
            .order_by(
                Product.id.desc()
            )
            .all()
        )

        return products

    def get(self, product_id: int) -> Product:
        product = (
            self.session
            .query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        return product

    def add(self, user_id: int, dto: CreateProductDto) -> Product:
        product = Product(**dto.dict())
        product.created_by = user_id
        product.modified_by = user_id
        self.session.add(product)
        self.session.commit()
        return product

    def update(self, product_id: int, user_id: int, dto: UpdateProductDto) -> Product:
        product = self.get(product_id)
        for field, value in dto:
            if value:
                setattr(product, field, value)

        product.modified_by = user_id
        self.session.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
