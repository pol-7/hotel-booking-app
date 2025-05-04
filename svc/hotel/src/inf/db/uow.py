from typing import Any
import src.app.interface as i

from .postgres.dao import HotelDao, HotelRoomDao, HotelReviewDao
from .postgres.engine import smaker as pg_session_factory


class UnitOfWork(i.UnitOfWork):
    async def __aenter__(self) -> "UnitOfWork":
        self.__pg_session = pg_session_factory()

        self.hotel_dao = HotelDao(self.__pg_session)
        self.hotel_room_dao = HotelRoomDao(self.__pg_session)
        self.hotel_review_dao = HotelReviewDao(self.__pg_session)

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.__pg_session.close()
        pass

    async def commit(self):
        await self.__pg_session.commit()
        pass

    async def rollback(self):
        await self.__pg_session.rollback()
        pass
