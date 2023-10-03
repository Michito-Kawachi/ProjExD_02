from random import randint
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    # こうかとん
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    move_dct = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5), 
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }
    
    clock = pg.time.Clock()

    # 爆弾
    bomb = pg.Surface((20, 20))
    bb_x: int = randint(0, WIDTH)
    bb_y: int = randint(0, HEIGHT)
    vx: int = +5
    vy: int = +5
    bb_rct = bomb.get_rect()
    bb_rct.center = bb_x, bb_y
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey("black")

    

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bomb, bb_rct)
        pg.display.update()
        tmr += 1

        """移動処理"""
        bb_rct.move_ip(vx, vy) # 爆弾移動

        # こうかとん移動
        key_lst = pg.key.get_pressed()
        kk_move = [0, 0]
        for key, mv in move_dct.items():
            if key_lst[key]:
                kk_move[0] += mv[0]
                kk_move[1] += mv[1]
        kk_rct.move_ip(kk_move)

        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()