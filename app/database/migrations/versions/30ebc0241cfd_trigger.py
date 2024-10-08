"""trigger

Revision ID: 30ebc0241cfd
Revises: 436d73d23db9
Create Date: 2023-07-19 13:41:03.575163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ebc0241cfd'
down_revision = '436d73d23db9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_accumulated_delivery()
        RETURNS TRIGGER AS $$
        DECLARE
            recent_accumulated_value FLOAT;
        BEGIN
            EXECUTE format('
                SELECT COALESCE((
                    SELECT accumulated FROM measurement
                    WHERE channel_id = %s
                    AND timestamp < %L
                    ORDER BY timestamp DESC
                    LIMIT 1
                ), 0)', NEW.channel_id, NEW.timestamp) INTO recent_accumulated_value;

            NEW.accumulated := recent_accumulated_value + NEW.value;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER cumulative_sum_trigger
        BEFORE INSERT ON measurement
        FOR EACH ROW
        EXECUTE FUNCTION update_accumulated_delivery();
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
