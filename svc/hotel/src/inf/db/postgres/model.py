from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import ARRAY, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .engine import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID]

    name: Mapped[str]
    description: Mapped[str]

    location_country_code: Mapped[str]
    location_address: Mapped[str]

    rating_average: Mapped[float]
    rating_num_votes: Mapped[int]


class HotelRoom(Base):
    __tablename__ = "hotel_room"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    hotel_id: Mapped[UUID] = mapped_column(ForeignKey("hotel.id"))

    name: Mapped[str]
    description: Mapped[str]

    price_per_night_currency_code: Mapped[str]
    price_per_night: Mapped[float]

    numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer))


class HotelReview(Base):
    __tablename__ = "hotel_review"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    author_id: Mapped[UUID]

    hotel_id: Mapped[UUID] = mapped_column(ForeignKey("hotel.id"))

    rating: Mapped[int]
    comment: Mapped[str]

    date_created: Mapped[date]
