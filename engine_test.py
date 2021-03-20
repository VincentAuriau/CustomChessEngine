import engine
import importlib
importlib.reload(engine)


def test_castling():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)
    game.move_from_coordinates(game.player1, 0, 5, 3, 2)
    game.move_from_coordinates(game.player2, 7, 3, 4, 6)
    game.move_from_coordinates(game.player1, 0, 6, 2, 5)
    game.move_from_coordinates(game.player2, 7, 1, 5, 2)

    # small castling move
    game.move_from_coordinates(game.player1, 0, 4, 0, 6)

    game.move_from_coordinates(game.player2, 6, 3, 5, 3)
    game.move_from_coordinates(game.player1, 0, 1, 2, 2)
    game.move_from_coordinates(game.player2, 7, 2, 6, 3)
    game.move_from_coordinates(game.player1, 0, 3, 1, 4)

    # big castling move
    game.move_from_coordinates(game.player2, 7, 4, 7, 2)


if __name__ == '__main__':
    test_castling()