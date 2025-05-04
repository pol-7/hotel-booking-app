from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from . import dto


class HotelDao(ABC):
    @abstractmethod
    async def get(self, hotel_id: UUID) -> dto.HotelWithID | None: ...

    @abstractmethod
    async def add(self, hotel: dto.Hotel) -> dto.HotelWithID: ...

    @abstractmethod
    async def update(self, hotel: dto.HotelWithID) -> dto.HotelWithID: ...

    @abstractmethod
    async def delete(self, hotel_id: UUID) -> None: ...

    @abstractmethod
    async def by_owner(self, owner_id: UUID) -> list[dto.HotelWithID]: ...


class HotelRoomDao(ABC):
    @abstractmethod
    async def get(self, room_id: UUID) -> dto.HotelRoomWithID | None: ...

    @abstractmethod
    async def add(self, room: dto.HotelRoom) -> dto.HotelRoomWithID: ...

    @abstractmethod
    async def update(self, room: dto.HotelRoomWithID) -> dto.HotelRoomWithID: ...

    @abstractmethod
    async def delete(self, room_id: UUID) -> None: ...

    @abstractmethod
    async def by_hotel(self, hotel_id: UUID) -> list[dto.HotelRoomWithID]: ...


class HotelReviewDao(ABC):
    @abstractmethod
    async def get(self, review_id: UUID) -> dto.HotelReviewWithID | None: ...

    @abstractmethod
    async def add(self, review: dto.HotelReview) -> dto.HotelReviewWithID: ...

    @abstractmethod
    async def update(self, review: dto.HotelReviewWithID) -> dto.HotelReviewWithID: ...

    @abstractmethod
    async def delete(self, review_id: UUID) -> None: ...

    @abstractmethod
    async def by_hotel(self, hotel_id: UUID) -> list[dto.HotelReviewWithID]: ...

    @abstractmethod
    async def by_author(self, author_id: UUID) -> list[dto.HotelReviewWithID]: ...


class UnitOfWork(ABC):
    hotel_dao: HotelDao
    hotel_room_dao: HotelRoomDao
    hotel_review_dao: HotelReviewDao

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork": ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
