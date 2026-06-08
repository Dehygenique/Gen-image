from PIL import Image, ImageDraw, ImageFont
import math

# Canvas size
W, H = 1080, 1350

# DH Thailand CI Colors
GREEN_DARK   = (27,  94,  32)   # #1B5E20
GREEN_MAIN   = (46, 125,  50)   # #2E7D32
GREEN_LIGHT  = (56, 142,  60)   # #388E3C
GREEN_PALE   = (200, 230, 201)  # light green bg
WHITE        = (255, 255, 255)
CHARCOAL     = (33,  33,  33)   # #212121
GOLD         = (255, 193,   7)  # #FFC107
LIGHT_GREY   = (245, 245, 245)  # #F5F5F5
RED_SOFT     = (229,  57,  53)
ORANGE_SOFT  = (251, 140,   0)

# Fonts
FONT_TH_BOLD    = "/usr/share/fonts/truetype/tlwg/Laksaman-Bold.ttf"
FONT_TH_REG     = "/usr/share/fonts/truetype/tlwg/Laksaman.ttf"
FONT_EN_BOLD    = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_EN_REG     = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.ellipse([x0, y0, x0+2*radius, y0+2*radius], fill=fill)
    draw.ellipse([x1-2*radius, y0, x1, y0+2*radius], fill=fill)
    draw.ellipse([x0, y1-2*radius, x0+2*radius, y1], fill=fill)
    draw.ellipse([x1-2*radius, y1-2*radius, x1, y1], fill=fill)
    if outline:
        draw.arc([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=outline, width=outline_width)
        draw.arc([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=outline, width=outline_width)
        draw.arc([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=outline, width=outline_width)
        draw.arc([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=outline, width=outline_width)
        draw.line([x0+radius, y0, x1-radius, y0], fill=outline, width=outline_width)
        draw.line([x0+radius, y1, x1-radius, y1], fill=outline, width=outline_width)
        draw.line([x0, y0+radius, x0, y1-radius], fill=outline, width=outline_width)
        draw.line([x1, y0+radius, x1, y1-radius], fill=outline, width=outline_width)

def centered_text(draw, text, y, font, color, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)

# ── Create canvas ──────────────────────────────────────────────
img  = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

# ── BACKGROUND: gradient-like strips ───────────────────────────
# Top header block
draw_rounded_rect(draw, (0, 0, W, 210), 0, GREEN_DARK)

# Subtle pale-green mid section
draw.rectangle([0, 210, W, H-120], fill=LIGHT_GREY)

# Footer bar
draw.rectangle([0, H-120, W, H], fill=GREEN_DARK)

# ── DECORATIVE: circles in header ──────────────────────────────
for cx, cy, r, alpha in [(950,30,80,40),(1040,160,60,30),(-20,180,70,35)]:
    circle_img = Image.new("RGBA", (W, H), (0,0,0,0))
    cd = ImageDraw.Draw(circle_img)
    cd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*GREEN_LIGHT, alpha))
    img.paste(Image.alpha_composite(img.convert("RGBA"), circle_img).convert("RGB"))
    draw = ImageDraw.Draw(img)

# ── LOGO AREA (top-left) ────────────────────────────────────────
# Draw text logo since image file is partial
f_logo_main = load_font(FONT_EN_BOLD, 36)
f_logo_sub  = load_font(FONT_EN_REG, 13)
draw.text((40, 24), "DE HYGIENIQUE", font=f_logo_main, fill=WHITE)
draw.text((40, 66), "No.1 Total Hygiene Service Solutions Since 2008", font=f_logo_sub, fill=(200,230,201))

# ECARF badge (simple badge shape)
draw_rounded_rect(draw, (40, 88, 178, 114), 8, GOLD)
f_badge = load_font(FONT_EN_BOLD, 11)
draw.text((50, 96), "ECARF Quality Tested", font=f_badge, fill=GREEN_DARK)

# German tech badge
draw_rounded_rect(draw, (186, 88, 330, 114), 8, (200,230,201))
draw.text((196, 96), "German Technology", font=f_badge, fill=GREEN_DARK)

# ── MAIN HEADLINE ───────────────────────────────────────────────
f_news_tag  = load_font(FONT_EN_BOLD, 15)
f_h1_th     = load_font(FONT_TH_BOLD, 46)
f_h1_th2    = load_font(FONT_TH_BOLD, 40)
f_sub_th    = load_font(FONT_TH_REG,  22)
f_year_tag  = load_font(FONT_EN_BOLD, 18)

# Year tag pill
draw_rounded_rect(draw, (370, 128, 710, 162), 16, GOLD)
centered_text(draw, "NEWS SUMMARY  2025-2026", 135, f_news_tag, GREEN_DARK)

# Headline Thai
centered_text(draw, "โรคภูมิแพ้จากที่นอน", 174, f_h1_th, WHITE)
centered_text(draw, "ปัญหาสุขภาพที่คุณมองข้าม", 224, f_h1_th2, GOLD)

# ── DIVIDER ─────────────────────────────────────────────────────
draw.rectangle([80, 278, W-80, 282], fill=GREEN_LIGHT)

# ── INTRO TEXT ──────────────────────────────────────────────────
f_intro = load_font(FONT_TH_REG, 24)
centered_text(draw, "สาเหตุหลักของโรคภูมิแพ้ที่พบมากที่สุด", 294, f_intro, CHARCOAL)
centered_text(draw, "คือ ไรฝุ่นที่สะสมในที่นอนที่ไม่ได้ทำความสะอาด", 326, f_intro, CHARCOAL)

# ── 4 STAT CARDS ────────────────────────────────────────────────
cards = [
    {
        "icon_text": "🦠",
        "num": "2,000,000",
        "unit": "ตัว",
        "desc": "ไรฝุ่นในที่นอน 1 ผืน",
        "color": (183, 28, 28),
        "bg": (255, 235, 235),
    },
    {
        "icon_text": "😷",
        "num": "80%",
        "unit": "",
        "desc": "ผู้แพ้ไรฝุ่น\nในผู้ป่วยภูมิแพ้",
        "color": GREEN_DARK,
        "bg": (200, 230, 201),
    },
    {
        "icon_text": "🛏",
        "num": "6",
        "unit": "เดือน",
        "desc": "ที่นอนสะสมไรฝุ่น\nสูงสุดหากไม่ทำความสะอาด",
        "color": (230, 81, 0),
        "bg": (255, 243, 224),
    },
    {
        "icon_text": "🤧",
        "num": "4",
        "unit": "อาการ",
        "desc": "คัดจมูก จาม\nตาแดง หอบหืด",
        "color": (21, 101, 192),
        "bg": (227, 242, 253),
    },
]

card_w = 220
card_h = 200
gap    = 26
total_w = 4 * card_w + 3 * gap
start_x = (W - total_w) // 2
card_y  = 380

f_num  = load_font(FONT_EN_BOLD, 40)
f_unit = load_font(FONT_TH_BOLD, 18)
f_desc = load_font(FONT_TH_REG,  17)
f_icon = load_font(FONT_EN_BOLD, 30)

for i, card in enumerate(cards):
    cx = start_x + i * (card_w + gap)
    cy = card_y
    # shadow
    draw_rounded_rect(draw, (cx+4, cy+4, cx+card_w+4, cy+card_h+4), 16, (200,200,200))
    # card bg
    draw_rounded_rect(draw, (cx, cy, cx+card_w, cy+card_h), 16, card["bg"])
    # top color stripe
    draw_rounded_rect(draw, (cx, cy, cx+card_w, cy+44), 16, card["color"])
    draw.rectangle([cx, cy+28, cx+card_w, cy+44], fill=card["color"])

    # icon
    draw.text((cx+14, cy+8), card["icon_text"], font=f_icon, fill=WHITE)

    # number
    bbox = draw.textbbox((0,0), card["num"], font=f_num)
    nw = bbox[2]-bbox[0]
    nx = cx + (card_w - nw)//2
    draw.text((nx, cy+56), card["num"], font=f_num, fill=card["color"])

    # unit
    if card["unit"]:
        bbox2 = draw.textbbox((0,0), card["unit"], font=f_unit)
        uw = bbox2[2]-bbox2[0]
        ux = cx + (card_w - uw)//2
        draw.text((ux, cy+104), card["unit"], font=f_unit, fill=card["color"])

    # description
    desc_lines = card["desc"].split("\n")
    dy = cy + 132 if not card["unit"] else cy + 130
    for line in desc_lines:
        bbox3 = draw.textbbox((0,0), line, font=f_desc)
        lw = bbox3[2]-bbox3[0]
        lx = cx + (card_w - lw)//2
        draw.text((lx, dy), line, font=f_desc, fill=CHARCOAL)
        dy += 26

# ── MAIN INFO SECTION ───────────────────────────────────────────
section_y = 614
draw_rounded_rect(draw, (50, section_y, W-50, section_y+290), 20, WHITE)
# left accent bar
draw.rectangle([50, section_y+20, 60, section_y+270], fill=GREEN_MAIN)

f_sec_title = load_font(FONT_TH_BOLD, 28)
f_sec_body  = load_font(FONT_TH_REG,  21)
f_bullet    = load_font(FONT_EN_BOLD, 22)

draw.text((80, section_y+18), "ทำไมที่นอนเป็นแหล่งสะสมไรฝุ่น?", font=f_sec_title, fill=GREEN_DARK)
draw.rectangle([80, section_y+56, W-70, section_y+58], fill=GREEN_PALE)

info_items = [
    "เซลล์ผิวหนังที่หลุดร่วงระหว่างนอนหลับเป็นอาหารของไรฝุ่น",
    "ความอุ่นและความชื้นในที่นอนเหมาะสมต่อการเพาะพันธุ์ไรฝุ่น",
    "ไรฝุ่น 1 ตัว สร้างมูลสูงถึง 200 เม็ดต่อวัน",
    "มูลไรฝุ่นเป็นตัวกระตุ้นอาการภูมิแพ้โดยตรง",
]

for j, item in enumerate(info_items):
    iy = section_y + 70 + j * 52
    # bullet circle
    draw.ellipse([78, iy+4, 98, iy+24], fill=GREEN_MAIN)
    draw.text((84, iy+4), str(j+1), font=load_font(FONT_EN_BOLD, 14), fill=WHITE)
    draw.text((110, iy), item, font=f_sec_body, fill=CHARCOAL)

# ── SOLUTION BANNER ─────────────────────────────────────────────
sol_y = 928
draw_rounded_rect(draw, (50, sol_y, W-50, sol_y+124), 20, GREEN_MAIN)
draw.ellipse([55, sol_y+10, 105, sol_y+60], fill=GOLD)
f_sol_icon = load_font(FONT_EN_BOLD, 28)
draw.text((65, sol_y+16), "✓", font=f_sol_icon, fill=GREEN_DARK)
f_sol_title = load_font(FONT_TH_BOLD, 28)
f_sol_sub   = load_font(FONT_TH_REG, 20)
draw.text((118, sol_y+14), "วิธีแก้ไข: ทำความสะอาดที่นอนอย่างน้อย", font=f_sol_title, fill=WHITE)
draw.text((118, sol_y+52), "ทุก 3-6 เดือน ด้วยระบบมืออาชีพ", font=f_sol_sub, fill=(200,230,201))
draw.text((118, sol_y+82), "เพื่อกำจัดไรฝุ่นและสารก่อภูมิแพ้อย่างสมบูรณ์", font=f_sol_sub, fill=GOLD)

# ── CTA BUTTON ──────────────────────────────────────────────────
cta_y = 1074
draw_rounded_rect(draw, (200, cta_y, W-200, cta_y+60), 30, GOLD)
f_cta = load_font(FONT_TH_BOLD, 26)
centered_text(draw, "ทำความสะอาดที่นอนของคุณวันนี้!", cta_y+14, f_cta, GREEN_DARK)

# ── FOOTER ──────────────────────────────────────────────────────
f_foot_brand = load_font(FONT_EN_BOLD, 20)
f_foot_sub   = load_font(FONT_TH_REG,  15)
f_foot_en    = load_font(FONT_EN_REG,  13)

centered_text(draw, "DE HYGIENIQUE", H-104, f_foot_brand, WHITE)
centered_text(draw, "ผู้เชี่ยวชาญด้านสุขอนามัยภายในบ้านอันดับ 1 ของไทย", H-78, f_foot_sub, (200,230,201))
centered_text(draw, "German Technology  |  ECARF Quality Tested  |  Since 2008", H-52, f_foot_en, GOLD)

# ── WATERMARK LINE ──────────────────────────────────────────────
draw.rectangle([0, H-26, W, H-25], fill=GOLD)

# Save
out = "/home/user/Gen-image/allergy_infographic_DH.png"
img.save(out, "PNG", dpi=(96,96))
print(f"Saved: {out}  ({W}x{H}px)")
