from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base_model import BaseModel

class MeasurementModel(BaseModel):
    __table_args__ = (
        UniqueConstraint(
            "timestamp", "channel_id", name="timestamp_on_channel_id_contstraint"
        ),
        PrimaryKeyConstraint("timestamp", "channel_id"),
        {},
    )
    timestamp: Mapped[float] = mapped_column(index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), index=True)
    value: Mapped[float] = mapped_column()
    accumulated: Mapped[float | None] = mapped_column()
