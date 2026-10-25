from merge.domain.board import Board
from merge.kaiten.api.board import BoardAPI


class BoardGateway:
    def __init__(self, api: BoardAPI):
        self.api = api

    async def get_boards(self, space_id: int) -> list[Board]:
        boards = await self.api.get_boards(space_id)
        return [Board(**board) for board in boards]

    async def get_board(self, space_id: int, board_id: int) -> Board:
        board = await self.api.get_board(space_id, board_id)
        return Board(**board)

    async def post_board(self, space_id: int, title: str, unique_board_lane_name):
        data = await self.api.post_board(
            space_id=space_id,
            title=title,
            unique_board_lane_name=unique_board_lane_name,
        )

        return Board(**data)