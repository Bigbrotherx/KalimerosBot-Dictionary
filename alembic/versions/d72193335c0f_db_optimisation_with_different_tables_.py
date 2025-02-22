"""DB_optimisation with different tables for users and for words

Revision ID: d72193335c0f
Revises: 2e4affa662ab
Create Date: 2025-02-22 15:03:35.877709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd72193335c0f'
down_revision: Union[str, None] = '2e4affa662ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_words',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'word_id')
    )
    op.create_index(op.f('ix_user_words_user_id'), 'user_words', ['user_id'], unique=False)
    op.drop_index('ix_words_user_id', table_name='words')
    op.create_unique_constraint(None, 'words', ['word', 'translation'])
    op.drop_column('words', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'words', type_='unique')
    op.create_index('ix_words_user_id', 'words', ['user_id'], unique=False)
    op.drop_index(op.f('ix_user_words_user_id'), table_name='user_words')
    op.drop_table('user_words')
    # ### end Alembic commands ###
