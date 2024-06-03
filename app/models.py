from datetime import datetime

from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, DECIMAL, JSON
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from enum import Enum


Base = declarative_base()


class OrderStatus(Enum):
    IN_PROCESSING = 'IN_PROCESSING'
    CREATED = 'CREATED'
    DELIVERED = 'DELIVERED'
    ASSEMBLY = 'ASSEMBLY'
    SHIPPING = 'SHIPPING'
    CANCELLED = 'CANCELLED'
    RETURNED = 'RETURNED'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'))

    city: Mapped['City'] = relationship(back_populates='users')


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))

    categories: Mapped[list['Category']] = relationship(back_populates='group')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))

    group: Mapped['Group'] = relationship('Group', back_populates='categories')

    subcategories: Mapped[list['Subcategory']] = relationship(back_populates='category')


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship('Category', back_populates='subcategories')

    products: Mapped[list['Product']] = relationship(back_populates='subcategory')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    additional_fields: Mapped[JSON]
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategories.id'))

    subcategory = relationship('Subcategory', back_populates='products')
    orders: Mapped[list['OrderProducts']] = relationship(back_populates='product')


class Storehouse(Base):
    __tablename__ = 'storehouses'

    id: Mapped[int] = mapped_column(primary_key=True)
    adress: Mapped[str] = mapped_column(String(255), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=False)

    city: Mapped['City'] = relationship(back_populates='storehouses')


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    storehouses: Mapped[list['Storehouse']] = relationship(back_populates='city')
    users: Mapped[list['User']] = relationship(back_populates='city')


class ProductStorehouse(Base):
    __tablename__ = 'product_storehouse'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    storehouse_id: Mapped[int] = mapped_column(ForeignKey('storehouse.id'), nullable=False)

    product = relationship('Product', back_populates='storehouses')
    storehouse = relationship('Storehouse', back_populates='products')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    delivery_id: Mapped[int]

    user: Mapped['User'] = relationship(back_populates='orders')
    products: Mapped[list['OrderProducts']] = relationship(back_populates='order')


class OrderProducts(Base):
    __tablename__ = 'order_products'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)

    order: Mapped['Order'] = relationship(back_populates='products')
    product: Mapped['Product'] = relationship(back_populates='orders')
