# Guía: assets 3D para la web

Esta carpeta tiene todo lo que necesitás para que lo que hagas en Blender encaje directo en https://tomascarballes.github.io. Si respetás nombre, tamaño y formato, el asset reemplaza solo al placeholder.

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `01` a `08` `-*.png` | Plantillas guía, una por asset, al tamaño exacto. Zonas marcadas: dónde va el texto, qué se recorta en celular, dónde tiene que haber transparencia. **No van en el render.** |
| `setup_web_assets.py` | Script de Blender: crea una escena por asset con la resolución, la cámara, la transparencia, el formato y la plantilla de fondo ya configurados. |
| `GUIA.pdf` | Esta guía. |

## Cómo arrancar

1. Copiá esta carpeta a tu compu y guardá tu `.blend` adentro.
2. Blender → **Scripting** → **Open** → `setup_web_assets.py` → **Run Script**.
3. Arriba a la derecha, en el selector de escenas, elegí el asset (`WEB_banner`, `WEB_muro`, etc.).
4. Mirá por la cámara (**Numpad 0**): la plantilla aparece encima, semitransparente.
5. **F12** para renderizar. Se guarda en `render_web/` con el nombre que pide la web.

Tip: armá un "kit" de materiales y piezas (piedra, hierro, pasto) en una escena aparte y usalo en todas con *Link* o *Append*. Así todo se ve del mismo mundo.

## Reglas para todos

- **Lo primero es que se lea el texto y se vean tus trabajos.** Valores bajos, poco contraste y nada de detalle fuerte detrás del texto.
- **Paleta:** fondo #0a0d0b · musgo #6f8a68 · violeta #9a80c4 / #5d4785 · azul frío suave · hueso #e3e1d8. El único cálido es el fuego de las antorchas (ámbar #e8a24a).
- **Luz:** luna fría y difusa + rebote cálido de antorchas donde corresponda. La misma en todos los assets.
- **Color:** view transform AgX (o Filmic), look None, salida sRGB. El script ya lo configura.
- **Peso:** pasá cada archivo por https://squoosh.app o https://tinypng.com antes de subirlo. Ojo de no romper la transparencia de los PNG.

## Cada asset

### 1. Banner de la intro → `img/banner.jpg`
- 2560×1440 JPG, menos de 500 KB.
- Ocupa toda la pantalla de entrada, al 40% de opacidad y con la niebla animada encima.
- **Zona roja** (centro): ahí van tu nombre y los botones. Oscura y limpia.
- **Franja celeste:** en un celular vertical solo se ve eso. Lo importante de la imagen tiene que estar adentro.
- La parte de abajo la web la oscurece hacia negro, así que no pongas nada clave ahí.

### 2. Muro con almenas → `img/wall.png`
- 2560×300 PNG **con transparencia**, menos de 600 KB. Cámara ortográfica frontal (ya configurada).
- Es el muro que sube y tapa la intro al scrollear. Se estira al ancho de la pantalla con 140 a 220 px de alto.
- **Arriba de la línea celeste:** almenas, con el espacio entre ellas transparente.
- **Recuadro violeta:** en celular solo se ve el centro.
- **Recuadros amarillos:** ahí la web pone las antorchas. Dejá ese espacio de pared despejado.
- Abajo tiene que fundirse con piedra oscura (#101311), porque sigue la textura de fondo.
- Ideal: que se pueda repetir en horizontal sin que se note.

### 3. Textura de piedra de fondo → `img/wall-tile.jpg`
- 1024×1024 JPG, **tileable sin costuras**, menos de 300 KB.
- Es el fondo de toda la página, detrás de los bloques negros con el contenido.
- Muy oscura: valores entre #101311 y #1b1f1d (las muestras están en la plantilla). Sin manchas ni piedras que llamen la atención.
- Para probar que no tenga costuras, en Blender ponela en un plano con escala de UV 3×3 y mirá si se nota la repetición.

### 4. Antorcha de pared → `img/sconce.png`
- 200×320 PNG **con transparencia**, vista frontal. Hierro forjado oscuro.
- **Sin fuego**: la llama la anima la web justo en el círculo amarillo (centrado, a un 31% desde arriba). El soporte de la llama tiene que quedar ahí.
- Hoy se ve chica (unos 44×70 px). Si te queda linda, después la agrandamos. En celular no se muestra.

### 5. Pasto con calaveras → `img/grass.png`
- 2560×200 PNG **con transparencia**, repetible en horizontal.
- Es el suelo al final de la página.
- Abajo una base sólida que toque el borde. Arriba, las puntas del pasto con fondo transparente.
- Entre 2 y 4 calaveras chicas semienterradas. En celular la imagen se ve de unos 30 px de alto, así que necesitan una silueta clara.

### 6. Marco dorado → `img/frame.png`
- 600×740 PNG **con transparencia**.
- Marco ovalado barroco, dorado a la hoja, con remate tallado arriba.
- **El hueco va hasta la línea amarilla y tiene que ser transparente**, porque tu foto va debajo (el óvalo rojo). El marco tapa unos 10 px del borde de la foto.
- El clavo y el cordón ya los dibuja la web. Si los querés hacer en 3D, avisame y saco los de código.

### 7. Imagen para compartir el link → `img/og.jpg`
- 1200×630 JPG. Es la vista previa cuando mandás el link por WhatsApp, Instagram o LinkedIn.
- Un render tuyo de fondo, con "Tomas Carballes · 3D Generalist" en la zona roja.
- Algunas apps la recortan a cuadrado (línea celeste), así que el texto tiene que quedar adentro.

### 8. Niebla en loop → `img/fog.webm` + `img/fog.mp4`
- 1920×1080, loop perfecto de 6 a 10 s (el script deja 240 frames a 24 fps), sin audio, menos de 3 MB.
- **Fondo negro puro:** la web lo mezcla en modo "screen", así que el negro desaparece y queda solo la niebla.
- Más densa abajo, más rala detrás del texto. Tonos verde, violeta y azul muy sutiles.
- Se renderiza como secuencia PNG en `render_web/fog/`. Para pasarla a video, mandámela y la convierto yo, o usá estos comandos:
  - `ffmpeg -framerate 24 -i fog_%04d.png -c:v libvpx-vp9 -b:v 0 -crf 40 -pix_fmt yuv420p -an fog.webm`
  - `ffmpeg -framerate 24 -i fog_%04d.png -c:v libx264 -crf 26 -preset veryfast -pix_fmt yuv420p -movflags +faststart -an fog.mp4`

## Cómo subirlo

- **Opción fácil:** pasame los archivos en el chat y los subo yo.
- **Opción directa:** en GitHub, entrá al repo → carpeta `img` → **Add file → Upload files** → arrastrá los archivos con el nombre exacto → **Commit changes**. En uno o dos minutos ya se ven en la web.

## Checklist antes de dar un asset por terminado

- [ ] Nombre, tamaño y formato exactos (ver arriba).
- [ ] Transparencia donde se pide (abrilo sobre un fondo de color para chequear).
- [ ] Nada importante fuera de las zonas de celular.
- [ ] Zona del texto oscura y limpia.
- [ ] Comprimido y dentro del peso indicado.
- [ ] Probado en la web en compu y en celular.
