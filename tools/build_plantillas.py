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

# 2 muro compu (plantilla a la mitad: 1280x3840 = render 2560x7680)
K=0.5; W,H=2560,7680; w,h=int(W*K),int(H*K)
im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); s=16
d.rectangle([0,0,w-1,h-1],outline=WHITE,width=2)
d.text((10,8),'MURO COMPU · render 2560x7680 (esta guía está a la mitad)',font=font(18,True),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0,255))
for i in range(1,6): y=i*1280*K; d.line([0,y,w,y],fill=WHITE,width=2); label(d,(w-150,y-22),f'corte {i} | {i+1}',WHITE,s)
d.rectangle([0,0,w,60*K],fill=(80,220,255,40)); label(d,(10,34),'almenas: transparente entre ellas',CYAN,s)
d.rectangle([0,60*K,w,293*K],outline=YEL,width=2); label(d,(10,60*K+6),'franja libre arriba (se ve antes del contenido): buen lugar para antorchas',YEL,s)
cx=W/2*K; cc=860*K; d.rectangle([cx-cc,293*K,cx+cc,6530*K],fill=(255,70,70,28)); dash_rect(d,(cx-cc,293*K,cx+cc,6530*K),RED,2,10)
label(d,(cx-cc+10,293*K+10),'DETRÁS DEL CONTENIDO: piedra oscura, sin antorchas',RED,s)
for x0,x1 in ((220,420),(2140,2340)):
    d.rectangle([x0*K,293*K,x1*K,6530*K],fill=(255,215,60,30)); dash_rect(d,(x0*K,293*K,x1*K,6530*K),YEL,2,10)
label(d,(220*K+4,400*K),'antorchas',YEL,s); label(d,(220*K+4,400*K+20),'laterales',YEL,s)
mx=491/2*K; dash_rect(d,(cx-mx,2,cx+mx,h-2),MAG,2,12); label(d,(cx-mx+6,h-30),'franja del celular',MAG,s)
y=6530*K; d.line([0,y,w,y],fill=GRN,width=3); label(d,(10,y+6),'en pantallas grandes la página termina acá; en las chicas se usa hasta abajo',GRN,s)
label(d,(10,h-60),'Solo luz de luna. Las antorchas (hierro) sí se ven; su fuego y su luz NO: van en los videos de antorcha.',WHITE,s)
im.save(OUT+'02-muro-compu_2560x7680.png')

# 3 muro celular (plantilla a la mitad: 430x6720 = render 860x13440)
W,H=860,13440; w,h=int(W*K),int(H*K)
im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); s=12
d.rectangle([0,0,w-1,h-1],outline=WHITE,width=2)
d.text((6,6),'MURO CELULAR · 860x13440',font=font(14,True),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0,255))
d.text((6,24),'(guía a la mitad)',font=font(12),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0,255))
for i in range(1,7): y=i*1920*K; d.line([0,y,w,y],fill=WHITE,width=2); label(d,(w-90,y-18),f'corte {i} | {i+1}',WHITE,s)
d.rectangle([0,0,w,105*K],fill=(80,220,255,40)); label(d,(6,44),'almenas',CYAN,s)
d.rectangle([0,105*K,w,226*K],outline=YEL,width=2); label(d,(6,105*K+4),'franja libre: antorcha de arriba',YEL,s)
d.rectangle([4,226*K,w-4,13100*K],fill=(255,70,70,28)); dash_rect(d,(4,226*K,w-4,13100*K),RED,2,10)
label(d,(8,226*K+10),'DETRÁS DEL CONTENIDO',RED,s); label(d,(8,226*K+26),'(todo el ancho en celular)',RED,s)
label(d,(8,h-40),'Mismo muro y misma luz que compu:',WHITE,s); label(d,(8,h-24),'es la franja central de 4,9 m.',WHITE,s)
im.save(OUT+'03-muro-celular_860x13440.png')

# 4 antorcha (video de luz) 1024x1024
w,h=1024,1024; im,d,s=base(w,h,'ANTORCHA: llama + su luz  img/antorchas/<id>.mp4'); s=22
center(d,w,h)
d.ellipse([w/2-10,h/2-10,w/2+10,h/2+10],fill=RED); label(d,(w/2+16,h/2-34),'boca de la antorcha (la esfera guía)',RED,s)
r=w/2*0.55; d.ellipse([w/2-r,h/2-r,w/2+r,h/2+r],outline=YEL,width=3); label(d,(w/2-r+10,h/2+r-40),'luz fuerte adentro de este círculo',YEL,s)
d.ellipse([4,4,w-4,h-4],outline=RED,width=3); label(d,(30,h-80),'Hacia el borde la web la funde a negro: la luz tiene que apagarse antes de llegar acá.',RED,s)
label(d,(30,80),'Fondo NEGRO, sin luna. Solo la luz de ESTA antorcha.',WHITE,s)
label(d,(30,112),'Se ve el muro y el hierro iluminados por el fuego, y el fuego.',WHITE,s)
label(d,(30,144),'Loop de 48 frames (2 s) a 24 fps.',WHITE,s)
im.save(OUT+'04-antorcha_1024x1024.png')

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
