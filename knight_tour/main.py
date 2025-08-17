import pygame as p
from Knight_Engine import GameState, load_images

Width = Height = 520
Dimension = 8
SQ_Size = Height // Dimension
MAX_FPS = 15


def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    p.display.set_caption("Knight's Tour")
    clock = p.time.Clock()
    game_state = GameState()
    load_images()
    running = True
    sq_selected = ()
    knight_placed = False

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN and not knight_placed:
                location = p.mouse.get_pos()
                col = location[0] // SQ_Size
                row = location[1] // SQ_Size

                if sq_selected == (row, col):
                    sq_selected = ()
                else:
                    sq_selected = (row, col)

                if sq_selected and game_state.Board[row][col] == '--':
                    game_state.Board[row][col] = 'wN'
                    knight_placed = True
                    sq_selected = ()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_RIGHT and knight_placed:
                    x, y = game_state.get_knight_location()
                    game_state.knight_tour(screen, x, y)
                elif event.key == p.K_f and knight_placed:
                    x, y = game_state.get_knight_location()
                    game_state.knight_tour_finisher(screen, x, y)

        game_state.draw_game_state(screen)
        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()


if __name__ == '__main__':
    main()
