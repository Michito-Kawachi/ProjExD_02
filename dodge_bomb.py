from random import randint
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def CheckBound(obj_rct: pg.Rect):
    """
    引数: こうかとんRect or 爆弾Rect
    戻り値: タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate


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
        
        """接触判定"""
        if kk_rct.colliderect(bb_rct): # 衝突: True
            print("ゲームオーバー")
            return

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bomb, bb_rct)
        pg.display.update()
        tmr += 1

        """移動処理"""
        # こうかとん移動
        key_lst = pg.key.get_pressed()
        kk_move = [0, 0]
        for key, mv in move_dct.items():
            if key_lst[key]:
                kk_move[0] += mv[0]
                kk_move[1] += mv[1]
        
        kk_rct.move_ip(kk_move) # こうかとん移動

        # こうかとん画面外チェック
        if CheckBound(kk_rct) != (True, True):
            kk_rct.move_ip(-kk_move[0], -kk_move[1])
        
        # 爆弾画面外チェック
        yoko, tate = CheckBound(bb_rct)
        if not yoko: vx *= -1
        if not tate: vy *= -1

        bb_rct.move_ip(vx, vy) # 爆弾移動

        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()