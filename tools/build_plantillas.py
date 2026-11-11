from PIL import Image, ImageDraw, ImageFont
import os
import pathlib; OUT=str(pathlib.Path(__file__).resolve().parent.parent/'plantillas-3d')+'/'
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s,b=False): return ImageFont.truetype(FB if b else F,s)
RED=(255,70,70,255); CYAN=(80,220,255,255); YEL=(255,215,60,255); GRN=(120,255,140,255); MAG=(230,120,255,255); WHITE=(255,255,255,255)
def base(w,h,title):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,w-1,h-1],outline=WHITE,width=2)
    s=max(12,min(28,w//60))
    d.text((10,8),title+f'  ·  {w}x{h}px',font=font(s,True),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0,255))
    return im,d,s
def label(d,xy,t,c,s): d.text(xy,t,font=font(s),fill=c,stroke_width=2,stroke_fill=(0,0,0,255))
def dash_rect(d,box,c,w=3,dash=18):
    x0,y0,x1,y1=box
    for x in range(int(x0),int(x1),dash*2): d.line([x,y0,min(x+dash,x1),y0],fill=c,width=w); d.line([x,y1,min(x+dash,x1),y1],fill=c,width=w)
    for y in range(int(y0),int(y1),dash*2): d.line([x0,y,x0,min(y+dash,y1)],fill=c,width=w); d.line([x1,y,x1,min(y+dash,y1)],fill=c,width=w)
def center(d,w,h,c=(255,255,255,120)):
    d.line([w/2,0,w/2,h],fill=c,width=1); d.line([0,h/2,w,h/2],fill=c,width=1)

# 1 banner
w,h=2560,1440; im,d,s=base(w,h,'BANNER  img/banner.jpg')
fy=int(h*0.62)
for y in range(fy,h,6): d.line([0,y,w,y],fill=(0,0,0,int(140*(y-fy)/(h-fy))),width=6)
d.rectangle([0,0,w-1,h-1],outline=WHITE,width=2); d.text((10,8),'BANNER  img/banner.jpg  ·  2560x1440px',font=font(28,True),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0,255))
center(d,w,h)
tb=(w/2-600,h/2-350,w/2+600,h/2+350); d.rectangle(tb,fill=(255,70,70,45)); dash_rect(d,tb,RED)
label(d,(tb[0]+12,tb[1]+10),'ZONA DEL TEXTO: nombre, "3D Generalist", botones.',RED,s); label(d,(tb[0]+12,tb[1]+46),'Mantenerla oscura y sin detalle fuerte.',RED,s)
mw=666; mb=(w/2-mw/2,0,w/2+mw/2,h); dash_rect(d,mb,CYAN)
label(d,(mb[0]+10,60),'CELULAR (vertical): solo se ve esta franja',CYAN,s)
label(d,(14,fy+10),'Desde acá la web oscurece hacia abajo (degradé a negro)',YEL,s)
ab=(w/2-150,h-150,w/2+150,h-40); dash_rect(d,ab,YEL); label(d,(ab[0]-40,ab[1]-38),'flecha "See work"',YEL,s)
label(d,(14,h-44),'Se ve al 40% de opacidad, con niebla animada encima. Valores bajos, paleta musgo / violeta / azul.',WHITE,s)
im.save(OUT+'01-banner_2560x1440.png')

# 2 wall
w,h=2560,300; im,d,s=base(w,h,'MURO CON ALMENAS Y ANTORCHAS  img/wall.png'); s=18
cy=60; d.rectangle([0,0,w,cy],fill=(80,220,255,35)); d.line([0,cy,w,cy],fill=CYAN,width=2)
label(d,(14,34),'Almenas: arriba de esta línea, entre almena y almena TRANSPARENTE',CYAN,s)
mw=1064; dash_rect(d,(w/2-mw/2,2,w/2+mw/2,h-2),MAG); label(d,(w/2-mw/2+10,cy+10),'CELULAR: solo se ve el centro (las antorchas quedan afuera)',MAG,s)
for side,(fx,fy) in {'IZQ':(420,135),'DER':(2140,135)}.items():
    d.rectangle([fx-40,fy-10,fx+40,fy+120],outline=YEL,width=2)
    d.ellipse([fx-7,fy-7,fx+7,fy+7],fill=RED); d.line([fx-20,fy,fx+20,fy],fill=RED,width=2); d.line([fx,fy-20,fx,fy+20],fill=RED,width=2)
    tb=(fx-64,fy-150,fx+64,fy+42); dash_rect(d,tb,RED,2,6)
    label(d,(fx+46,fy+10),f'antorcha {side} ({fx}, {fy})',YEL,s)
label(d,(14,h-62),'Punto rojo = boca de la antorcha: la llama nace acá (posición fija). Recuadro rojo = imagen de la llama.',RED,s)
d.rectangle([0,h-34,w,h],fill=(120,255,140,40)); label(d,(14,h-30),'Borde inferior: fundir a piedra oscura (#101311). Antorchas y su luz SÍ van en este render; el fuego NO (solo su luz).',GRN,s)
im.save(OUT+'02-muro_2560x300.png')

# 3 tile
w,h=1024,1024; im,d,s=base(w,h,'TEXTURA DE FONDO  img/wall-tile.jpg'); s=22
for p in (0,w//2,w-1): d.line([p,0,p,h],fill=(255,255,255,90)); d.line([0,p,w,p],fill=(255,255,255,90))
dash_rect(d,(2,2,w-3,h-3),RED,4)
label(d,(20,60),'Tileable: el borde izquierdo continúa en el derecho',RED,s)
label(d,(20,92),'y el de arriba en el de abajo (sin costuras).',RED,s)
for i,(c,n) in enumerate([((16,19,17),'#101311'),((20,24,22),'#141816'),((27,31,29),'#1b1f1d')]):
    y=180+i*70; d.rectangle([20,y,90,y+55],fill=c+(255,),outline=WHITE); label(d,(105,y+12),f'{n}  rango de valores objetivo',WHITE,s)
label(d,(20,h-70),'Va detrás de TODO el contenido: bajo contraste, sin manchas grandes.',WHITE,s)
im.save(OUT+'03-textura-fondo_1024x1024.png')

# 4 flame
w,h=128,192; im,d,s=base(w,h,'LLAMA'); s=10
bx,by=64,150
d.rectangle([bx-40,by-10,bx+40,h-1],fill=(255,215,60,40)); label(d,(4,by+14),'hierro = holdout',YEL,s)
d.ellipse([bx-5,by-5,bx+5,by+5],fill=RED); d.line([bx-14,by,bx+14,by],fill=RED,width=1); d.line([bx,by-14,bx,by+14],fill=RED,width=1)
label(d,(bx+8,by-18),'nace acá',RED,s)
dash_rect(d,(14,24,w-14,by),CYAN,1,5); label(d,(4,26),'la llama sube',CYAN,s); label(d,(4,38),'por acá',CYAN,s)
im.save(OUT+'04-llama_128x192.png')

# 5 grass
w,h=2560,200; im,d,s=base(w,h,'PASTO + CALAVERAS  img/grass.png'); s=18
d.rectangle([0,h-60,w,h],fill=(120,255,140,45)); d.line([0,h-60,w,h-60],fill=GRN,width=2)
label(d,(14,h-56),'Base sólida (tierra/pasto denso), toca el borde de abajo. Repetible en horizontal.',GRN,s)
d.rectangle([0,0,w,60],fill=(80,220,255,30)); label(d,(14,34),'Puntas del pasto: arriba TRANSPARENTE',CYAN,s)
for x in (0.22,0.55,0.8): b=(x*w-50,h-110,x*w+50,h-30); dash_rect(d,b,YEL,2,8)
label(d,(0.22*w-50,h-140),'calaveras (2 a 4)',YEL,s)
label(d,(w-900,70),'En celular se ve de ~30 px de alto: calaveras con silueta clara',MAG,s)
im.save(OUT+'05-pasto_2560x200.png')

# 6 frame
w,h=600,740; im,d,s=base(w,h,'MARCO'); s=16
x0,y0,ww,hh=w*0.11,h*0.12,w*0.78,h*0.80
d.ellipse([x0,y0,x0+ww,y0+hh],fill=(255,70,70,50),outline=RED,width=3)
ins=10; d.ellipse([x0+ins,y0+ins,x0+ww-ins,y0+hh-ins],outline=YEL,width=2)
label(d,(w/2-150,h/2-30),'FOTO (va debajo)',RED,s); label(d,(w/2-170,h/2-6),'hueco TRANSPARENTE: línea amarilla',YEL,s)
label(d,(14,40),'img/frame.png  ·  remate tallado arriba',WHITE,s)
label(d,(14,h-26),'el marco tapa ~10 px del borde de la foto',WHITE,s)
im.save(OUT+'06-marco_600x740.png')

# 7 og
w,h=1200,630; im,d,s=base(w,h,'IMAGEN PARA COMPARTIR  img/og.jpg'); s=20
sq=(w/2-h/2,0,w/2+h/2,h); dash_rect(d,sq,CYAN); label(d,(sq[0]+10,40),'Algunas apps recortan a cuadrado',CYAN,s)
tb=(w/2-260,h/2-90,w/2+260,h/2+90); d.rectangle(tb,fill=(255,70,70,45)); dash_rect(d,tb,RED)
label(d,(tb[0]+12,tb[1]+10),'Nombre + 3D Generalist',RED,s)
im.save(OUT+'07-compartir_1200x630.png')

# 8 fog
w,h=1920,1080; im,d,s=base(w,h,'NIEBLA EN LOOP  img/fog.webm + img/fog.mp4'); s=26
label(d,(30,80),'Fondo NEGRO puro: la web lo mezcla en modo "screen" (el negro desaparece).',WHITE,s)
label(d,(30,120),'Loop perfecto de 6 a 10 s · sin audio · menos de 3 MB · tonos verde/violeta/azul muy sutiles.',WHITE,s)
tb=(w/2-450,h/2-260,w/2+450,h/2+260); dash_rect(d,tb,RED); label(d,(tb[0]+12,tb[1]+10),'Detrás del texto: niebla más rala',RED,s)
d.rectangle([0,h*0.6,w,h],fill=(120,255,140,30)); label(d,(30,h*0.6+10),'Más densa abajo (como niebla de suelo)',GRN,s)
im.save(OUT+'08-niebla_1920x1080.png')
print(sorted(os.listdir(OUT)))
