from PIL import Image, ImageDraw, ImageFont
import math, os

# ── CI Colors (from actual CI image) ─────────────────────────
GREEN_SAGE   = (78,  124, 106)   # sage green from logo
GREEN_DARK   = (45,   85,  68)   # deeper shade
GREEN_LIGHT  = (120, 168, 148)   # lighter accent
GREEN_PALE   = (220, 238, 230)   # very pale green
WHITE        = (255, 255, 255)
GOLD         = (212, 168,  67)   # amber/gold from CI
GOLD_LIGHT   = (240, 205, 110)
BLACK        = (26,   26,  26)
WARM_CREAM   = (252, 248, 240)   # warm white background
GREY_SOFT    = (230, 228, 224)

# ── Font paths ─────────────────────────────────────────────────
FB  = "/usr/share/fonts/truetype/tlwg/Laksaman-Bold.ttf"
FR  = "/usr/share/fonts/truetype/tlwg/Laksaman.ttf"
FEB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FER = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def f(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def rr(draw, xy, r, fill, outline=None, ow=2):
    x0,y0,x1,y1 = xy
    draw.rectangle([x0+r,y0,x1-r,y1], fill=fill)
    draw.rectangle([x0,y0+r,x1,y1-r], fill=fill)
    for ex,ey in [(x0,y0),(x1-2*r,y0),(x0,y1-2*r),(x1-2*r,y1-2*r)]:
        draw.ellipse([ex,ey,ex+2*r,ey+2*r], fill=fill)
    if outline:
        draw.rounded_rectangle(xy, radius=r, outline=outline, width=ow)

def cx_text(draw, text, y, font, color, W=1080):
    bb = draw.textbbox((0,0), text, font=font)
    x  = (W - (bb[2]-bb[0])) // 2
    draw.text((x, y), text, font=font, fill=color)

# ── Draw person sleeping (side silhouette) ─────────────────────
def draw_sleeping_person(draw, x, y, scale=1.0, color=GREEN_SAGE, facing='right'):
    s = scale
    flip = -1 if facing == 'left' else 1

    # Body (lying horizontal) — pill shape
    bx, by = x, y
    bw, bh = int(200*s), int(72*s)
    draw.ellipse([bx, by, bx+bh, by+bh], fill=color)                           # head
    draw.rounded_rectangle([bx+int(30*s), by+int(14*s), bx+bw, by+bh-int(14*s)],
                            radius=int(24*s), fill=color)

    # Arm over body
    ax = bx + int(60*s)
    draw.rounded_rectangle([ax, by+int(8*s), ax+int(90*s), by+int(26*s)],
                            radius=int(10*s), fill=color)

    # Pillow
    pw, ph = int(90*s), int(52*s)
    px = bx - int(16*s)
    py = by + int(6*s)
    rr(draw, [px, py, px+pw, py+ph], int(12*s), WHITE)
    # pillow shadow
    draw.ellipse([px+int(6*s), py+int(6*s), px+pw-int(6*s), py+ph-int(6*s)],
                 outline=GREY_SOFT, width=2)

    # Zzzs
    zx = bx + int(80*s)
    zy = by - int(50*s)
    for i, (sz, alpha) in enumerate([(16,180),(20,220),(26,255)]):
        zf = f(FEB, int(sz*s))
        zc = (*GOLD, alpha)
        draw.text((zx + i*int(18*s), zy - i*int(16*s)), "z", font=zf, fill=GOLD)

# ── Draw couple sleeping ────────────────────────────────────────
def draw_couple(draw, x, y, scale=1.0):
    # Two people spooning
    s = scale
    # back person
    draw_sleeping_person(draw, x, y+int(30*s), scale=s, color=GREEN_SAGE)
    # front person (slightly darker, offset)
    draw_sleeping_person(draw, x-int(20*s), y-int(10*s), scale=s*0.92, color=GREEN_DARK)

def draw_three(draw, x, y, scale=1.0):
    s = scale
    offsets = [0, int(50*s), int(100*s)]
    colors  = [GREEN_DARK, GREEN_SAGE, GREEN_LIGHT]
    for i, (oy, col) in enumerate(zip(offsets, colors)):
        draw_sleeping_person(draw, x, y + oy, scale=s*0.82, color=col)

def draw_family(draw, x, y, scale=1.0):
    s = scale
    # Adult 1
    draw_sleeping_person(draw, x, y, scale=s, color=GREEN_DARK)
    # Adult 2
    draw_sleeping_person(draw, x, y+int(60*s), scale=s*0.95, color=GREEN_SAGE)
    # Child
    draw_sleeping_person(draw, x+int(80*s), y+int(28*s), scale=s*0.58, color=GOLD)

# ── Build one card ─────────────────────────────────────────────
def make_card(variant):
    W, H = 1080, 1350
    img  = Image.new("RGBA", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── BG decorative blobs ───────────────────────────────────
    # top-left large circle
    blob = Image.new("RGBA", (W,H), (0,0,0,0))
    bd   = ImageDraw.Draw(blob)
    bd.ellipse([-120, -120, 400, 400], fill=(*GREEN_PALE, 180))
    img  = Image.alpha_composite(img, blob)

    # bottom-right circle
    blob2 = Image.new("RGBA", (W,H), (0,0,0,0))
    bd2   = ImageDraw.Draw(blob2)
    bd2.ellipse([700, 980, 1200, 1480], fill=(*GREEN_SAGE, 40))
    img   = Image.alpha_composite(img, blob2)

    draw  = ImageDraw.Draw(img)

    # ── Top green strip ───────────────────────────────────────
    draw.rectangle([0, 0, W, 8], fill=GREEN_SAGE)

    # ── Brand mark (top right) ────────────────────────────────
    f_brand = f(FEB, 18)
    f_brand_sub = f(FER, 12)
    draw.text((W-270, 22), "DE HYGIENIQUE", font=f_brand, fill=GREEN_SAGE)
    draw.text((W-222, 46), "Since 2008", font=f_brand_sub, fill=GREEN_LIGHT)

    # ── Tag pill (top left) ───────────────────────────────────
    tag_texts = {
        "solo":   "1 คน",
        "couple": "2 คน",
        "trio":   "3 คน",
        "family": "ครอบครัว",
    }
    tag = tag_texts[variant]
    f_tag = f(FB, 22)
    bb = draw.textbbox((0,0), tag, font=f_tag)
    tw = bb[2]-bb[0]
    rr(draw, [40, 20, 40+tw+32, 58], 18, GREEN_SAGE)
    draw.text((56, 26), tag, font=f_tag, fill=WHITE)

    # ── HEADLINE ─────────────────────────────────────────────
    f_h1  = f(FB, 62)
    f_h2  = f(FB, 46)
    f_sub = f(FR, 26)

    headlines = {
        "solo":   ("นอนหลับสนิท", "ไร้ภูมิแพ้"),
        "couple": ("คืนแห่งความสุข", "ของทั้งคู่"),
        "trio":   ("สามคนหัวใจเดียว", "นอนหลับปลอดภัย"),
        "family": ("ทั้งครอบครัวหลับสบาย", "ทุกคืน"),
    }
    h1, h2 = headlines[variant]
    cx_text(draw, h1, 88,  f_h1, BLACK)
    cx_text(draw, h2, 158, f_h2, GREEN_SAGE)

    # Gold underline
    bb1 = draw.textbbox((0,0), h2, font=f_h2)
    uw  = bb1[2]-bb1[0]
    ux  = (W - uw)//2
    draw.rectangle([ux, 212, ux+uw, 216], fill=GOLD)

    # ── ILLUSTRATION AREA (bed + sleeping figure) ─────────────
    ill_y = 250

    # Bed base
    bed_x, bed_y = 120, ill_y + 340
    bed_w, bed_h = 840, 60
    rr(draw, [bed_x, bed_y, bed_x+bed_w, bed_y+bed_h], 12, GREEN_DARK)
    # Bed legs
    for lx in [bed_x+40, bed_x+bed_w-80]:
        draw.rectangle([lx, bed_y+bed_h, lx+30, bed_y+bed_h+40], fill=GREEN_DARK)

    # Mattress
    mat_y = bed_y - 50
    rr(draw, [bed_x+10, mat_y, bed_x+bed_w-10, bed_y+6], 20, WHITE)
    draw.rounded_rectangle([bed_x+10, mat_y, bed_x+bed_w-10, bed_y+6],
                            radius=20, outline=GREEN_PALE, width=3)

    # Blanket
    bl_y = mat_y + 20
    rr(draw, [bed_x+100, bl_y, bed_x+bed_w-60, bed_y+2], 16, GREEN_PALE)
    # blanket fold
    draw.rounded_rectangle([bed_x+100, bl_y, bed_x+bed_w-60, bl_y+30],
                            radius=16, fill=(*GREEN_LIGHT, 180) if False else GREEN_LIGHT)

    # Headboard
    hb_x, hb_y = bed_x+10, mat_y-130
    rr(draw, [hb_x, hb_y, hb_x+100, mat_y+10], 18, GREEN_DARK)

    # Bedside lamp
    lamp_x = bed_x + bed_w - 20
    draw.ellipse([lamp_x+10, mat_y-80, lamp_x+60, mat_y-20], fill=GOLD_LIGHT)
    draw.rectangle([lamp_x+30, mat_y-20, lamp_x+40, mat_y+10], fill=GREEN_DARK)
    draw.ellipse([lamp_x+10, mat_y-90, lamp_x+60, mat_y-70],
                 fill=(*GOLD_LIGHT, 120) if False else GOLD_LIGHT)

    # ── SLEEPING FIGURES ─────────────────────────────────────
    fig_y = mat_y + 10
    if variant == "solo":
        draw_sleeping_person(draw, 270, fig_y - 55, scale=1.5, color=GREEN_SAGE)

    elif variant == "couple":
        draw_sleeping_person(draw, 220, fig_y - 50, scale=1.35, color=GREEN_DARK)
        draw_sleeping_person(draw, 260, fig_y - 78, scale=1.25, color=GREEN_SAGE)
        # heart
        hx, hy = 600, fig_y - 110
        draw.text((hx, hy), "♡", font=f(FEB, 36), fill=GOLD)

    elif variant == "trio":
        draw_sleeping_person(draw, 200, fig_y - 40, scale=1.1, color=GREEN_DARK)
        draw_sleeping_person(draw, 230, fig_y - 62, scale=1.0, color=GREEN_SAGE)
        draw_sleeping_person(draw, 280, fig_y - 84, scale=0.72, color=GOLD)  # child

    elif variant == "family":
        # Dad
        draw_sleeping_person(draw, 180, fig_y - 38, scale=1.2, color=GREEN_DARK)
        # Mom
        draw_sleeping_person(draw, 220, fig_y - 64, scale=1.08, color=GREEN_SAGE)
        # Kids
        draw_sleeping_person(draw, 380, fig_y - 44, scale=0.68, color=GOLD)
        draw_sleeping_person(draw, 430, fig_y - 58, scale=0.60, color=GREEN_LIGHT)

    # ── MOON & STARS deco ─────────────────────────────────────
    draw.text((880, ill_y+30), "☽", font=f(FEB, 52), fill=GOLD_LIGHT)
    for sx, sy, ss in [(820,ill_y+20,14),(950,ill_y+60,10),(870,ill_y+80,8),(820,ill_y+100,12)]:
        draw.text((sx, sy), "✦", font=f(FEB, ss), fill=GOLD)

    # ── CONTENT SECTION ───────────────────────────────────────
    cs_y = 690
    # section bg
    rr(draw, [60, cs_y, W-60, cs_y+380], 24, WHITE)
    draw.rounded_rectangle([60, cs_y, W-60, cs_y+380], radius=24,
                            outline=GREEN_PALE, width=2)
    # left accent bar
    draw.rectangle([60, cs_y+20, 68, cs_y+360], fill=GREEN_SAGE)

    f_sec  = f(FB, 30)
    f_body = f(FR, 22)
    f_num  = f(FEB, 38)

    cx_text(draw, "ปัญหาโรคภูมิแพ้จากที่นอน", cs_y+22, f_sec, GREEN_DARK)
    draw.rectangle([120, cs_y+64, W-120, cs_y+66], fill=GREEN_PALE)

    bullets = [
        ("80%",  "ของผู้ป่วยแพ้ไรฝุ่นในที่นอน"),
        ("2M",   "ไรฝุ่นอาศัยในที่นอน 1 ผืน"),
        ("6",    "เดือน คือรอบที่นอนสะสมไรฝุ่นสูงสุด"),
        ("100%", "สะอาดด้วย DE HYGIENIQUE"),
    ]
    colors_b = [GREEN_DARK, GREEN_SAGE, GOLD, GREEN_LIGHT]
    for i, ((num, txt), col) in enumerate(zip(bullets, colors_b)):
        by2 = cs_y + 84 + i * 74
        # number badge
        nb_w = 82
        rr(draw, [90, by2, 90+nb_w, by2+52], 12, col)
        bb = draw.textbbox((0,0), num, font=f(FEB,22))
        nw = bb[2]-bb[0]
        nx = 90 + (nb_w-nw)//2
        draw.text((nx, by2+10), num, font=f(FEB,22), fill=WHITE)
        # text
        draw.text((188, by2+12), txt, font=f_body, fill=BLACK)

    # ── CTA ───────────────────────────────────────────────────
    cta_y = 1100
    rr(draw, [100, cta_y, W-100, cta_y+72], 36, GREEN_SAGE)
    cx_text(draw, "ทำความสะอาดที่นอน  |  DE HYGIENIQUE", cta_y+18, f(FB,26), WHITE)

    # ── FOOTER ────────────────────────────────────────────────
    draw.rectangle([0, 1238, W, 1242], fill=GOLD)
    cx_text(draw, "DE HYGIENIQUE  ·  No.1 Total Hygiene Service Solutions  ·  Since 2008",
            1252, f(FEB,16), GREEN_SAGE)
    cx_text(draw, "German Technology  ·  ECARF Quality Tested",
            1278, f(FER,14), GREEN_LIGHT)
    cx_text(draw, "www.dehygienique.co.th",
            1304, f(FER,15), GOLD)

    # ── Bottom green strip ────────────────────────────────────
    draw.rectangle([0, 1342, W, 1350], fill=GREEN_SAGE)

    # convert & save
    out_img = img.convert("RGB")
    name    = f"/home/user/Gen-image/sleep_{variant}_DH.png"
    out_img.save(name, "PNG", dpi=(96,96))
    print(f"✓ {name}")
    return name

# Generate all 4
for v in ["solo", "couple", "trio", "family"]:
    make_card(v)

print("\nAll 4 images done!")
