"""empty message

Revision ID: 55e687ca4033
Revises: 
Create Date: 2023-03-19 11:49:41.760501

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '55e687ca4033'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'moderators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('steamid', sa.BigInteger(), nullable=False),
        sa.Column('vk_id', sa.BigInteger(), nullable=False),
        sa.Column('avatar_url', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('steamid'),
        sa.UniqueConstraint('vk_id'),
    )
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_nickname', sa.String(), nullable=False),
        sa.Column('report_steamid', sa.BigInteger(), nullable=False),
        sa.Column('time', sa.DateTime(), nullable=False),
        sa.Column('server_number', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'checks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('steamid', sa.BigInteger(), nullable=False),
        sa.Column('moderator_id', sa.Integer(), nullable=False),
        sa.Column('start', sa.DateTime(), nullable=False),
        sa.Column('end', sa.DateTime(), nullable=True),
        sa.Column('server_number', sa.Integer(), nullable=True),
        sa.Column('is_ban', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['moderator_id'],
            ['moderators.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'moderator_settings',
        sa.Column('moderator_id', sa.Integer(), nullable=False),
        sa.Column('player_is_new', sa.Integer(), nullable=False),
        sa.Column('exclude_servers', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('exclude_reasons', postgresql.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(
            ['moderator_id'],
            ['moderators.id'],
        ),
        sa.PrimaryKeyConstraint('moderator_id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('moderator_settings')
    op.drop_table('checks')
    op.drop_table('reports')
    op.drop_table('moderators')
    # ### end Alembic commands ###
