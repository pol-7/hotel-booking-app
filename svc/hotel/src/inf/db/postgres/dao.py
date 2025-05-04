from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

import src.app.dto as dto
import src.app.interface as i
from src.app.enum import CountryCode, CurrencyCode

from .model import Hotel, HotelRoom, HotelReview


class HotelDao(i.HotelDao):
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def __to_dto(hotel: Hotel) -> dto.HotelWithID:
        return dto.HotelWithID(
            id=hotel.id,
            owner_id=hotel.owner_id,
            name=hotel.name,
            description=hotel.description,
            location=dto.Location(
                country_code=CountryCode(hotel.location_country_code),
                address=hotel.location_address,
            ),
            rating=dto.Rating(
                average=hotel.rating_average, num_votes=hotel.rating_num_votes
            ),
        )

    @staticmethod
    def __to_orm(hotel: dto.Hotel) -> Hotel:
        return Hotel(
            owner_id=hotel.owner_id,
            name=hotel.name,
            description=hotel.description,
            location_country_code=hotel.location.country_code.value,
            location_address=hotel.location.address,
            rating_average=hotel.rating.average,
            rating_num_votes=hotel.rating.num_votes,
        )

    async def get(self, hotel_id: UUID) -> dto.HotelWithID | None:
        stmt = select(Hotel).where(Hotel.id == hotel_id)
        hotel = (await self.db.execute(stmt)).scalar_one_or_none()

        if hotel is None:
            return None

        return self.__to_dto(hotel)

    async def add(self, hotel: dto.Hotel) -> dto.HotelWithID:
        orm_hotel = self.__to_orm(hotel)

        self.db.add(orm_hotel)
        await self.db.flush()

        return self.__to_dto(orm_hotel)

    async def update(self, hotel: dto.HotelWithID) -> dto.HotelWithID:
        orm_hotel = self.__to_orm(hotel)
        orm_hotel.id = hotel.id

        await self.db.merge(orm_hotel)

        return self.__to_dto(orm_hotel)

    async def delete(self, hotel_id: UUID) -> None:
        stmt = delete(Hotel).where(Hotel.id == hotel_id)
        await self.db.execute(stmt)

    async def by_owner(self, owner_id: UUID) -> list[dto.HotelWithID]:
        stmt = select(Hotel).where(Hotel.owner_id == owner_id)
        hotels = (await self.db.execute(stmt)).scalars().all()

        return [self.__to_dto(h) for h in hotels]


class HotelRoomDao(i.HotelRoomDao):
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def __to_dto(room: HotelRoom) -> dto.HotelRoomWithID:
        return dto.HotelRoomWithID(
            id=room.id,
            hotel_id=room.hotel_id,
            name=room.name,
            description=room.description,
            price_per_night=dto.Price(
                currency_code=CurrencyCode(room.price_per_night_currency_code),
                amount=room.price_per_night,
            ),
            numbers=room.numbers,
        )

    @staticmethod
    def __to_orm(room: dto.HotelRoom) -> HotelRoom:
        return HotelRoom(
            hotel_id=room.hotel_id,
            name=room.name,
            description=room.description,
            price_per_night_currency_code=room.price_per_night.currency_code.value,
            price_per_night=room.price_per_night.amount,
            numbers=room.numbers,
        )

    async def get(self, room_id: UUID) -> dto.HotelRoomWithID | None:
        stmt = select(HotelRoom).where(HotelRoom.id == room_id)
        room = (await self.db.execute(stmt)).scalar_one_or_none()

        if room is None:
            return None

        return self.__to_dto(room)

    async def add(self, room: dto.HotelRoom) -> dto.HotelRoomWithID:
        orm_room = self.__to_orm(room)

        self.db.add(orm_room)
        await self.db.flush()

        return self.__to_dto(orm_room)

    async def update(self, room: dto.HotelRoomWithID) -> dto.HotelRoomWithID:
        orm_room = self.__to_orm(room)
        orm_room.id = room.id

        await self.db.merge(orm_room)

        return self.__to_dto(orm_room)

    async def delete(self, room_id: UUID) -> None:
        stmt = delete(HotelRoom).where(HotelRoom.id == room_id)
        await self.db.execute(stmt)

    async def by_hotel(self, hotel_id: UUID) -> list[dto.HotelRoomWithID]:
        stmt = select(HotelRoom).where(HotelRoom.hotel_id == hotel_id)
        rooms = (await self.db.execute(stmt)).scalars().all()

        return [self.__to_dto(r) for r in rooms]


class HotelReviewDao(i.HotelReviewDao):
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def __to_dto(review: HotelReview) -> dto.HotelReviewWithID:
        return dto.HotelReviewWithID(
            id=review.id,
            author_id=review.author_id,
            hotel_id=review.hotel_id,
            rating=review.rating,
            comment=review.comment,
            date_created=review.date_created,
        )

    @staticmethod
    def __to_orm(rating: dto.HotelReview) -> HotelReview:
        return HotelReview(
            author_id=rating.author_id,
            hotel_id=rating.hotel_id,
            rating=rating.rating,
            comment=rating.comment,
            date_created=rating.date_created,
        )

    async def get(self, review_id: UUID) -> dto.HotelReviewWithID | None:
        stmt = select(HotelReview).where(HotelReview.id == review_id)
        review = (await self.db.execute(stmt)).scalar_one_or_none()

        if review is None:
            return None

        return self.__to_dto(review)

    async def add(self, review: dto.HotelReview) -> dto.HotelReviewWithID:
        orm_review = self.__to_orm(review)

        self.db.add(orm_review)
        await self.db.flush()

        return self.__to_dto(orm_review)

    async def update(self, review: dto.HotelReviewWithID) -> dto.HotelReviewWithID:
        orm_review = self.__to_orm(review)
        orm_review.id = review.id

        await self.db.merge(orm_review)

        return self.__to_dto(orm_review)

    async def delete(self, review_id: UUID) -> None:
        stmt = delete(HotelReview).where(HotelReview.id == review_id)
        await self.db.execute(stmt)

    async def by_hotel(self, hotel_id: UUID) -> list[dto.HotelReviewWithID]:
        stmt = select(HotelReview).where(HotelReview.hotel_id == hotel_id)
        reviews = (await self.db.execute(stmt)).scalars().all()

        return [self.__to_dto(r) for r in reviews]

    async def by_author(self, author_id: UUID) -> list[dto.HotelReviewWithID]:
        stmt = select(HotelReview).where(HotelReview.author_id == author_id)
        reviews = (await self.db.execute(stmt)).scalars().all()

        return [self.__to_dto(r) for r in reviews]
