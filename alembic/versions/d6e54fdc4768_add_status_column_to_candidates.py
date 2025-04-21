"""Add status column to candidates

Revision ID: d6e54fdc4768
Revises: 30d479680b50
Create Date: 2025-04-19 21:47:43.495584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6e54fdc4768'
down_revision: Union[str, None] = '30d479680b50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Сначала создаем ENUM тип
    candidatestatus = sa.Enum('new', 'approved', 'rejected', name='candidatestatus')
    candidatestatus.create(op.get_bind())
    
    # Затем добавляем колонку с этим типом
    op.add_column('candidates', sa.Column('status', 
                 sa.Enum('new', 'approved', 'rejected', name='candidatestatus'), 
                 server_default='new',  # Установка значения по умолчанию
                 nullable=False))

def downgrade():
    # Удаляем колонку
    op.drop_column('candidates', 'status')
    
    # Удаляем ENUM тип
    candidatestatus = sa.Enum('new', 'approved', 'rejected', name='candidatestatus')
    candidatestatus.drop(op.get_bind())
