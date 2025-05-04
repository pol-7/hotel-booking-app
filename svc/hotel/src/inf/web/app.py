from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, HTTPException, Header, status

from src.app import dto, usecase, exception as exc
from src.inf.db.uow import UnitOfWork

app = FastAPI()


@app.get("/hotels/{hotel_id}")
async def get_hotel(hotel_id: UUID) -> dto.HotelWithID:
    return await usecase.GetHotelUseCase(UnitOfWork).execute(hotel_id)


@app.get("/hotels/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: UUID) -> list[dto.HotelRoomWithID]:
    return await usecase.ListHotelRoomsUseCase(UnitOfWork).execute(hotel_id)


@app.get("/hotels/{hotel_id}/reviews")
async def get_hotel_reviews(hotel_id: UUID) -> list[dto.HotelReviewWithID]:
    return await usecase.ListHotelReviewsUseCase(UnitOfWork).execute(hotel_id)


@app.post("/my_hotels")
async def create_owned_hotel(
    x_auth_request_user: Annotated[UUID, Header()], hotel: dto.HotelNew
) -> dto.HotelWithID:
    return await usecase.HotelierCreateHotelUseCase(UnitOfWork).execute(
        x_auth_request_user, hotel
    )


@app.patch("/my_hotels")
async def update_owned_hotel(
    x_auth_request_user: Annotated[UUID, Header()], hotel: dto.HotelPatch
) -> dto.HotelWithID:
    return await usecase.HotelierUpdateHotelUseCase(UnitOfWork).execute(
        x_auth_request_user, hotel
    )


@app.get("/my_hotels")
async def get_owned_hotels(
    x_auth_request_user: Annotated[UUID, Header()],
) -> list[dto.HotelWithID]:
    return await usecase.HotelierListOwnedHotelsUseCase(UnitOfWork).execute(
        x_auth_request_user
    )


@app.post("/reviews")
async def create_review(
    x_auth_request_user: Annotated[UUID, Header()], review: dto.HotelReviewNew
) -> dto.HotelReviewWithID:
    return await usecase.UserCreateReviewUseCase(UnitOfWork).execute(
        x_auth_request_user, review
    )


@app.delete("/reviews")
async def delete_review(
    x_auth_request_user: Annotated[UUID, Header()], review_id: UUID
) -> None:
    return await usecase.UserDeleteReviewUseCase(UnitOfWork).execute(
        x_auth_request_user, review_id
    )


@app.exception_handler(exc.ResourceNotFoundError)
async def not_found_handler(req, exc):
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.exception_handler(exc.NotOwnedError)
async def not_owned_handler(req, exc):
    raise HTTPException(status.HTTP_403_FORBIDDEN)
