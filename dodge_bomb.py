import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    # 横
    if  rct.left < 0 or WIDTH < rct.right:
        yoko = False
    # 縦
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：無し
    戻り値：無し
    ゲームオーバーした際に、ブラックアウトし文字と画像が表示される
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # 背景画像
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    screen.blit(bg_img, [0, 0]) 
    # ブラックアウト
    go_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(80)
    screen.blit(go_img, [0,0])
    # 文字
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", False, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH/2,HEIGHT/2))
    screen.blit(txt,txt_rct)
    # こうかとん
    kt_img = pg.image.load("fig/9.png")
    screen.blit(kt_img, [WIDTH/4, 300]) 
    screen.blit(kt_img, [(WIDTH/4)*3, 300])

    pg.display.update()
    time.sleep(5)
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
    
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        tmr += 1
        clock.tick(50)
        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
