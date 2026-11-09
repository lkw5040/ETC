from PIL import Image, ImageOps, ImageDraw, ImageFont
IMG="/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/images"
OUT="/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad"
FONT="/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
BOX=(250,330,1270,1420)
TW=660                      # 타일 가로 픽셀
items=[("8.jpg","추 1 (알루미늄)  59.235 g"),
       ("6.jpg","추 2 (쇠구슬)  164.955 g"),
       ("7.jpg","추 3 (구리구슬)  188.120 g"),
       ("9.jpg","실 연결용 고리  3.100 g")]
tiles=[]
f=ImageFont.truetype(FONT,30)
for fn,label in items:
    im=ImageOps.exif_transpose(Image.open(f"{IMG}/{fn}")).crop(BOX)
    h=round(im.height*TW/im.width)
    im=im.resize((TW,h), Image.LANCZOS)
    canvas=Image.new("RGB",(TW,h+52),"white")
    canvas.paste(im,(0,0))
    d=ImageDraw.Draw(canvas)
    w=d.textbbox((0,0),label,font=f)[2]
    d.text(((TW-w)//2,h+11),label,fill=(25,45,80),font=f)
    tiles.append(canvas)
tw,th=tiles[0].size
GAP=16
sheet=Image.new("RGB",(tw*2+GAP, th*2+GAP),"white")
for i,t in enumerate(tiles):
    sheet.paste(t, ((i%2)*(tw+GAP), (i//2)*(th+GAP)))
sheet.save(f"{OUT}/photo_mass.jpg", quality=88, optimize=True)
print("photo_mass.jpg", sheet.size, round(sheet.width/sheet.height,3))
