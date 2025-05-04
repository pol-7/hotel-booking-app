from pydantic import BaseModel, UUID4
from datetime import date
from . import enum

# misc


class Location(BaseModel):
    country_code: enum.CountryCode
    address: str


class Price(BaseModel):
    currency_code: enum.CurrencyCode
    amount: float


class Rating(BaseModel):
    average: float
    num_votes: int


# hotel


class Hotel(BaseModel):
    owner_id: UUID4

    name: str
    description: str

    location: Location
    rating: Rating


class HotelWithID(Hotel):
    id: UUID4


class HotelNew(BaseModel):
    owner_id: UUID4

    name: str
    description: str

    location: Location


class HotelPatch(BaseModel):
    id: UUID4

    name: str | None
    description: str | None

    location: Location | None


# hotel room


class HotelRoom(BaseModel):
    hotel_id: UUID4

    name: str
    description: str
    price_per_night: Price

    numbers: list[int]


class HotelRoomWithID(HotelRoom):
    id: UUID4


class HotelRoomNew(BaseModel):
    hotel_id: UUID4

    name: str
    description: str
    price_per_night: Price

    numbers: list[int]


class HotelRoomPatch(BaseModel):
    id: UUID4

    name: str | None
    description: str | None
    price_per_night: Price | None

    numbers: list[int] | None


# hotel review


class HotelReview(BaseModel):
    author_id: UUID4

    hotel_id: UUID4

    rating: int
    comment: str

    date_created: date


class HotelReviewWithID(HotelReview):
    id: UUID4


class HotelReviewNew(BaseModel):
    author_id: UUID4

    hotel_id: UUID4

    rating: int
    comment: str
