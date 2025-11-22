"""Insert data into products table

Revision ID: d659372d8e92
Revises: b121c6ac2132
Create Date: 2025-11-21 20:22:13.163201

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float, Text


revision = 'd659372d8e92'
down_revision = 'b121c6ac2132'
branch_labels = None
depends_on = None


def upgrade():
    products_table = table('products',
        column('name', String),
        column('price', Float),
        column('category_id', Integer)
    )

    op.bulk_insert(
        products_table,
        [
            {'name': 'Gaming Laptop', 'price': 1500.0, 'category_id': 1},
            
            {'name': 'Laptop', 'price': 1200.0, 'category_id': 1},
            
            {'name': 'Smartphone LG', 'price': 800.0, 'category_id': 1},
            
            {'name': 'Novel', 'price': 20.0, 'category_id': 2},
            
            {'name': 'T-Shirt', 'price': 25.0, 'category_id': 3},
        ]
    )

def downgrade():
    products_table = table('products', column('name', String))
    
    op.execute(
        products_table.delete().where(
            products_table.c.name.in_([
                'Gaming Laptop', 'Laptop', 'Smartphone LG', 'Novel', 'T-Shirt'
            ])
        )
    )