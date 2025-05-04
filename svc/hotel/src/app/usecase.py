from uuid import UUID
from . import dto, interface as i, service as svc, exception as exc

# common


class GetHotelUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, hotel_id: UUID) -> dto.HotelWithID:
        async with self.get_uow() as uow:
            return await svc.get_hotel(uow.hotel_dao, hotel_id)


class ListHotelRoomsUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, hotel_id: UUID) -> list[dto.HotelRoomWithID]:
        async with self.get_uow() as uow:
            return await svc.get_rooms_by_hotel(uow.hotel_room_dao, hotel_id)


class ListHotelReviewsUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, hotel_id: UUID) -> list[dto.HotelReviewWithID]:
        async with self.get_uow() as uow:
            return await svc.get_reviews_by_hotel(uow.hotel_review_dao, hotel_id)


# hotelier


class HotelierCreateHotelUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, hotelier_id: UUID, hotel: dto.HotelNew) -> dto.HotelWithID:
        async with self.get_uow() as uow:
            if not hotel.owner_id == hotelier_id:
                raise exc.NotOwnedError("hotel", hotelier_id)

            return await svc.create_hotel(uow.hotel_dao, hotel)


class HotelierUpdateHotelUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(
        self, hotelier_id: UUID, hotel: dto.HotelPatch
    ) -> dto.HotelWithID:
        async with self.get_uow() as uow:
            if not await svc.is_hotel_owner(uow.hotel_dao, hotelier_id, hotel.id):
                raise exc.NotOwnedError("hotel", hotelier_id)

            return await svc.update_hotel(uow.hotel_dao, hotel)


class HotelierListOwnedHotelsUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, hotelier_id: UUID) -> list[dto.HotelWithID]:
        async with self.get_uow() as uow:
            return await svc.get_hotels_by_owner(uow.hotel_dao, hotelier_id)


# user


class UserCreateReviewUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(
        self, user_id: UUID, review: dto.HotelReviewNew
    ) -> dto.HotelReviewWithID:
        async with self.get_uow() as uow:
            if not review.author_id == user_id:
                raise exc.NotOwnedError("review", user_id)

            return await svc.create_hotel_review(
                uow.hotel_dao, uow.hotel_review_dao, review
            )


class UserDeleteReviewUseCase:
    def __init__(self, get_uow: type[i.UnitOfWork]):
        self.get_uow = get_uow

    async def execute(self, user_id: UUID, review_id: UUID) -> None:
        async with self.get_uow() as uow:
            if not await svc.is_hotel_review_owner(
                uow.hotel_review_dao, user_id, review_id
            ):
                raise exc.NotOwnedError("review", user_id)

            await svc.delete_hotel_review(uow.hotel_review_dao, review_id)
