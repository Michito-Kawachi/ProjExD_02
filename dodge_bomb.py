from random import randint
import sys
import time
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
    end_img = pg.image.load("ex02/fig/6.png")
    end_img = pg.transform.rotozoom(end_img, 0, 3.0)

    # こうかとん
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_flip = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    move_dct = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5), 
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }

    # 追加機能1
    kk_rote = {
        (-5, 0): kk_img,
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
        (0, -5): pg.transform.rotozoom(kk_img_flip, 90, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_img_flip, 45, 1.0),
        (+5, 0): kk_img_flip,
        (+5, +5): pg.transform.rotozoom(kk_img_flip, -45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_img_flip, -90, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, 0): kk_img
    }
    
    clock = pg.time.Clock()

    # 爆弾
    # bomb = pg.Surface((20, 20))
    # pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)

    #追加機能2: 爆弾が加速&拡大
    accs = [a for a in range(1, 11)]
    bombs = []
    bomb = pg.Surface((20, 20))
    bb_rct = bomb.get_rect()
    for r in range(1, 11):
        bomb = pg.Surface((20*r, 20*r))
        pg.draw.circle(bomb, (255, 0, 0), (10*r, 10*r), 10*r)
        bomb.set_colorkey("black")
        bombs.append(bomb)
        
    bb_x: int = randint(0, WIDTH)
    bb_y: int = randint(0, HEIGHT)
    vx: int = +5
    vy: int = +5
    bb_rct.center = bb_x, bb_y

    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        """接触判定"""
        if kk_rct.colliderect(bb_rct): # 衝突: True
            # 機能追加3: エンドカード
            screen.blit(bg_img, [0, 0])
            screen.blit(end_img, kk_rct)
            pg.display.update()
            time.sleep(2)
            print("ゲームオーバー")
            return

        pg.display.update()
        tmr += 1
        kk_move = [0, 0]

        """移動処理"""
        # こうかとん移動
        key_lst = pg.key.get_pressed()
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
        
        # 追加機能2: 爆弾拡大&加速
        # 進行時間に応じて適切なサイズ・速度を選択
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bomb = bombs[min(tmr//500, 9)]         
        bb_rct.move_ip(avx, avy) # 爆弾移動

        clock.tick(50)

        screen.blit(bg_img, [0, 0])
        # 追加機能1: 回転こうかとん
        screen.blit(kk_rote[tuple(kk_move)], kk_rct)
        screen.blit(bomb, bb_rct)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()