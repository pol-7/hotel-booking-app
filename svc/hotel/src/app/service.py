import datetime
from uuid import UUID
from . import dto, interface as i, exception as exc


async def get_hotel(hotel_dao: i.HotelDao, hotel_id: UUID) -> dto.HotelWithID:
    hotel = await hotel_dao.get(hotel_id)

    if hotel is None:
        raise exc.ResourceNotFoundError("hotel", hotel_id)

    return hotel


async def get_hotels_by_owner(
    hotel_dao: i.HotelDao, owner_id: UUID
) -> list[dto.HotelWithID]:
    return await hotel_dao.by_owner(owner_id=owner_id)


async def create_hotel(hotel_dao: i.HotelDao, data: dto.HotelNew) -> dto.HotelWithID:
    hotel = dto.Hotel(
        owner_id=data.owner_id,
        name=data.name,
        description=data.description,
        location=data.location,
        rating=dto.Rating(average=0, num_votes=0),
    )

    return await hotel_dao.add(hotel)


async def update_hotel(hotel_dao: i.HotelDao, data: dto.HotelPatch) -> dto.HotelWithID:
    hotel = await get_hotel(hotel_dao, data.id)
    hotel = dto.HotelWithID.model_validate(hotel.__dict__ | data.__dict__)

    return await hotel_dao.update(hotel)


async def get_rooms_by_hotel(
    hotel_dao: i.HotelRoomDao, hotel_id: UUID
) -> list[dto.HotelRoomWithID]:
    return await hotel_dao.by_hotel(hotel_id)


async def get_reviews_by_hotel(
    hotel_dao: i.HotelReviewDao, hotel_id: UUID
) -> list[dto.HotelReviewWithID]:
    return await hotel_dao.by_hotel(hotel_id)


async def is_hotel_owner(hotel_dao: i.HotelDao, user_id: UUID, hotel_id: UUID) -> bool:
    hotel = await get_hotel(hotel_dao, hotel_id)

    return hotel.owner_id == user_id


async def create_hotel_review(
    hotel_dao: i.HotelDao,
    review_dao: i.HotelReviewDao,
    data: dto.HotelReviewNew,
) -> dto.HotelReviewWithID:
    hotel = await get_hotel(hotel_dao, data.hotel_id)

    review = dto.HotelReview(
        author_id=data.author_id,
        hotel_id=data.hotel_id,
        rating=data.rating,
        comment=data.comment,
        date_created=datetime.date.today(),
    )

    review = await review_dao.add(review)

    rating_sum = hotel.rating.average * hotel.rating.num_votes + review.rating
    hotel.rating.average = rating_sum / (hotel.rating.num_votes + 1)

    hotel.rating.num_votes += 1

    await hotel_dao.update(hotel)

    return review


async def get_hotel_review(
    review_dao: i.HotelReviewDao, review_id: UUID
) -> dto.HotelReviewWithID:
    review = await review_dao.get(review_id)

    if review is None:
        raise exc.ResourceNotFoundError("review", review_id)

    return review


async def delete_hotel_review(review_dao: i.HotelReviewDao, review_id: UUID) -> None:
    await review_dao.delete(review_id)


async def is_hotel_review_owner(
    review_dao: i.HotelReviewDao, user_id: UUID, review_id: UUID
):
    review = await get_hotel_review(review_dao, review_id)
    return review.author_id == user_id
