import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんrectまたは爆弾rect
    戻り値：taple[bool,bool](横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面外ならFalse"""

    yoko , tate = True, True
    if rect.left < 0 or WIDTH < rect.right: #横
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom: #縦
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    bk_image = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bk_image,(0,0,0),bk_image.get_rect())
    pg.Surface.set_alpha(bk_image,150)
    font_gameover = pg.font.Font(None, 80)
    text_gameover = font_gameover.render("Game Over", True, (255,255,255))
    bk_image.blit(text_gameover,[WIDTH//2-150,HEIGHT//2-50])
    kk_cry_img = pg.image.load("fig/8.png")
    bk_image.blit(kk_cry_img, [WIDTH//2-200, HEIGHT//2-50])
    bk_image.blit(kk_cry_img, [WIDTH//2+200, HEIGHT//2-50])
    screen.blit(bk_image, (0,0))

    pg.display.update()
    pg.time.wait(2000)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200 
    bb_image = pg.Surface((20,20))
    pg.draw.circle(bb_image,(255,0,0),(10,10),10)
    bb_image.set_colorkey((0,0,0))
    bb_rct = bb_image.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs()

    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """

        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] #横方向の移動量
                sum_mv[1] += tpl[1] #縦方向の移動量

        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_image = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_image,bb_rct)
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #どこかしらがはみでている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #元に戻す  
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        bb_rct.width = bb_image.get_rect().width
        bb_rct.height = bb_image.get_rect().height
        bb_image.set_colorkey((0,0,0))



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
