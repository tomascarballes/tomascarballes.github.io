# Guía: assets 3D para la web

Esta carpeta tiene todo lo que necesitás para que lo que hagas en Blender encaje directo en https://tomascarballes.github.io. Si respetás nombre, tamaño, formato y posiciones, cada asset reemplaza solo a su placeholder.

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `01` a `08` `-*.png` | Plantillas guía, una por asset, al tamaño exacto. Marcan dónde va el texto, qué se recorta en celular, dónde tiene que haber transparencia y dónde va cada antorcha. **No salen en el render.** |
| `setup_web_assets.py` | Script de Blender. Arma la escena MASTER con sus colecciones y una escena por asset con la cámara, la resolución, la transparencia, el formato, qué se ve y qué solo ilumina, y la plantilla de fondo. |
| `GUIA.pdf` | Esta guía. |

## La idea: una sola escena, muchos renders

Se trabaja como en VFX: **todo vive en una sola escena con una sola iluminación**, y de ahí salen las piezas por separado. Así la luna ilumina todo igual, las antorchas iluminan el muro de verdad y todo parece del mismo mundo.

- **MASTER** es donde modelás, texturizás e iluminás todo.
- **Las escenas WEB_\*** no tienen copias de nada. Muestran la misma colección de MASTER (si movés una piedra, cambia en todos los renders) y cada una suma solo su cámara, su resolución y qué colecciones entran en ese render.

Cada escena WEB usa cada colección de una de cuatro formas:

| Modo | Qué hace | Ejemplo |
|---|---|---|
| Se ve | Sale normal en el render. | El muro en `WEB_muro`. |
| Solo luz (*Indirect only*) | No se ve, pero ilumina, se refleja y tira sombras. | El fuego en `WEB_muro`: ilumina la piedra sin aparecer. |
| Agujero (*Holdout*) | Tapa lo que está detrás y deja ese lugar transparente. | El hierro de la antorcha en las llamas: la llama queda "detrás" del soporte. |
| Excluida | No existe para ese render. | El cementerio en `WEB_muro`. |

Todo esto el script ya lo configura. Necesita **Cycles** (Eevee no tiene *Indirect only*), y lo deja puesto.

## Cómo arrancar

1. Copiá esta carpeta a tu compu.
2. En Blender (versión 4 o más nueva), con un archivo nuevo: **Scripting → Open**, elegí `setup_web_assets.py` **desde esta carpeta** → **Run Script**.
3. **Guardá el `.blend` dentro de esta carpeta.** Los renders van a salir en `render_web/`, al lado del `.blend`.
4. Vas a estar en la escena **MASTER**, con las colecciones de la tabla de abajo.

**Colecciones de MASTER:**

| Colección | Qué va adentro |
|---|---|
| `Luz_luna` | La luna (luz principal fría), el cielo y la luz de ambiente. |
| `Luz_neutra` | Una luz pareja y suave, **solo** para la textura de fondo. |
| `Cementerio` | El fondo de la intro: lápidas, árboles, rejas, suelo lejano. |
| `Muro` | El muro con almenas. |
| `Antorchas_hierro` | Los soportes de hierro, sin el fuego. |
| `Llamas` | El fuego: objetos emisivos o simulación. Es lo que ilumina el muro. |
| `Pasto` | El pasto y las calaveras. |
| `Textura_piedra` | Un plano con el material de piedra, para la textura repetible. |
| `Marco` | El marco dorado. |
| `Niebla` | El volumen de niebla. |
| `GUIAS (no se renderiza)` | Una caja del tamaño del muro y dos esferitas donde nace cada llama. |

**5.** Para renderizar, elegí una escena **WEB_\*** arriba a la derecha, mirá por la cámara (**Numpad 0**) para ver la plantilla encima, y **F12** (o **Ctrl+F12** para las animaciones).

Si la plantilla no aparece: revisá que estés en una escena WEB_\* y no en MASTER, que el botón **Overlays** del visor esté prendido y, si el script tiró un error de que no encuentra las plantillas, pegá la ruta de esta carpeta en `TEMPLATES_DIR`, arriba de todo en el script.

## Medidas y posiciones fijas

La web y Blender usan la misma escala: **100 px de la web = 1 m en Blender.**

- **El muro mide 25,6 × 3 m.** Va centrado en X = 0, con la base en Z = 0, mirando a −Y (la cámara está en Y = −20). La caja `GUIA_muro` marca el tamaño exacto.
- **Antorchas:** la boca de cada una (el punto donde nace la llama) tiene que caer **exacto** en las esferas `GUIA_llama_izq` y `GUIA_llama_der`, que en la imagen son los px (420, 135) y (2140, 135). La web pone la llama animada justo ahí. Si movés una antorcha, avisame y cambio las coordenadas en la web y en el script.
- Los demás assets tienen su lugar en la escena para que no se mezclen con el muro: el pasto con base en Z = −10, el marco centrado en X = 30 y Z = 3,7, y el plano de la textura delante de la cámara en Z = −50. Podés mover sus cámaras si te queda más cómodo.

## Reglas para todos

- **Lo primero es que se lea el texto y se vean tus trabajos.** Valores bajos, poco contraste y nada de detalle fuerte detrás del texto.
- **Paleta:** fondo #0a0d0b · musgo #6f8a68 · violeta #9a80c4 / #5d4785 · azul frío suave · hueso #e3e1d8. Lo único cálido es el fuego (ámbar #e8a24a).
- **Luz:** la luna fría y difusa ilumina todo. Las antorchas suman un rebote cálido solo cerca de ellas.
- **Mundo (World) oscuro:** lo comparten todas las escenas. Si lo hacés claro, la niebla deja de verse sobre negro.
- **Color:** view transform AgX (o Filmic), look None, salida sRGB. El script ya lo configura.
- **Peso:** antes de subir, pasá cada imagen por https://squoosh.app o https://tinypng.com, cuidando no romper la transparencia de los PNG.

## Cada asset

### 1. Banner de la intro → `img/banner.jpg`
- Escena `WEB_banner` · 2560×1440 JPG · menos de 500 KB · cámara en perspectiva, la ubicás vos.
- Entran luna, cementerio y niebla; las llamas solo como luz, si aparecen a lo lejos.
- Ocupa toda la pantalla de entrada, al 40% de opacidad y con la niebla animada encima.
- **Zona roja** (centro): ahí van tu nombre y los botones. Tiene que quedar oscura y limpia.
- **Franja celeste:** es lo único que se ve en un celular vertical. Lo importante va adentro.
- La web oscurece la parte de abajo hacia negro, así que no pongas nada clave ahí.

### 2. Muro con almenas y antorchas → `img/wall.png`
- Escena `WEB_muro` · 2560×300 PNG **con transparencia** · menos de 600 KB · cámara ortográfica frontal.
- Entran el muro, el hierro de las antorchas y la luna. **El fuego entra como "solo luz":** la piedra queda iluminada por las antorchas, pero sin la llama dibujada (esa la pone la web, animada).
- Es el muro que sube y tapa la intro al scrollear. Se estira al ancho de la pantalla con 140 a 220 px de alto.
- **Arriba de la línea celeste** van las almenas, con el espacio entre ellas transparente.
- **Recuadro violeta:** en celular solo se ve el centro, así que las antorchas quedan afuera. Está bien.
- **Punto rojo:** la boca de cada antorcha. Recuadro amarillo: el lugar aproximado del soporte. Recuadro rojo punteado: el área que ocupa la imagen de la llama.
- Abajo tiene que fundirse con piedra oscura (#101311).
- Ideal, aunque no obligatorio: que el muro se pueda repetir en horizontal sin que se note.

### 3. Llamas animadas → `img/flame-left.webp` y `img/flame-right.webp`
- Escenas `WEB_llama_izq` y `WEB_llama_der` · 128×192 cada una · 48 frames a 24 fps (2 s) · con transparencia.
- Entran las llamas y la luna. **El hierro y el muro van como agujero (Holdout):** el soporte tapa la base del fuego igual que en el muro, y todo lo que no es fuego queda transparente.
- Cada cámara es ortográfica, con la misma escala de pixel que el muro y encuadrada sobre su antorcha. Por eso la llama coincide pixel por pixel con el muro, sin que tengas que alinear nada.
- **Punto rojo de la plantilla:** donde nace la llama (px 64, 150). La llama sube hacia el recuadro celeste. En tamaño real, una llama de 50 a 90 px de alto queda bien.
- **Que sean distintas:** cambiá el *seed* o desfasá el ruido en una de las dos. Si son iguales y van sincronizadas, se nota que es la misma.
- **Loop perfecto:** el frame 48 tiene que empalmar con el 1. Si animás el fuego con ruido 4D, mové la coordenada W en círculo (seno y coseno del frame) o hacé un crossfade entre el final y el principio.
- **Brillo sobre el muro:** la luz fija de la antorcha ya sale en `wall.png`. Encima, la web suma un resplandor ámbar muy suave que titila, para que la pared "respire" con el fuego. Si no te gusta, se saca.
- **Cómo exportar:** **Ctrl+F12** renderiza la secuencia PNG en `render_web/llama_izq/` (y `llama_der/`). Para pasarla al formato de la web, mandame las dos carpetas y las convierto yo, o corré:
  - `ffmpeg -framerate 24 -i llama_izq_%04d.png -c:v libwebp_anim -loop 0 -lossless 0 -q:v 80 -pix_fmt yuva420p flame-left.webp`
  - `ffmpeg -framerate 24 -i llama_der_%04d.png -c:v libwebp_anim -loop 0 -lossless 0 -q:v 80 -pix_fmt yuva420p flame-right.webp`
- Las dos juntas tienen que pesar menos de 600 KB. WebP animado con transparencia funciona en todos los navegadores actuales, incluido Safari en iPhone.

### 4. Textura de piedra de fondo → `img/wall-tile.jpg`
- Escena `WEB_textura_fondo` · 1024×1024 JPG · **tileable sin costuras** · menos de 300 KB.
- **Es la excepción a la luz compartida:** entran solo `Textura_piedra` y `Luz_neutra`. Si la iluminaran la luna o las antorchas, al repetirse se verían las manchas de luz una y otra vez.
- Usá el mismo material de piedra del muro, en un plano que llene justo la cámara. Otra opción es bakear el color del material a 1024×1024.
- Es el fondo de toda la página, detrás de los bloques negros con el contenido.
- Muy oscura: valores entre #101311 y #1b1f1d (las muestras están en la plantilla). Sin piedras ni manchas que llamen la atención.
- Para probar que no tenga costuras, ponela en un plano con las UV escaladas 3×3 y mirá si se nota la repetición.

### 5. Pasto con calaveras → `img/grass.png`
- Escena `WEB_pasto` · 2560×200 PNG **con transparencia** · repetible en horizontal.
- Entran el pasto y la luna; el fuego solo como luz, por si querés un rebote cálido.
- Es el suelo al final de la página.
- Abajo una base sólida que toque el borde. Arriba, las puntas del pasto sobre fondo transparente.
- Entre 2 y 4 calaveras chicas semienterradas. En celular la imagen se ve de unos 30 px de alto, así que necesitan una silueta clara.

### 6. Marco dorado → `img/frame.png`
- Escena `WEB_marco` · 600×740 PNG **con transparencia**.
- Entran el marco y la luna; el fuego solo como luz, para que el dorado tenga brillo cálido.
- Marco ovalado barroco, dorado a la hoja, con remate tallado arriba.
- **El hueco va hasta la línea amarilla y tiene que ser transparente**, porque tu foto va debajo (el óvalo rojo). El marco tapa unos 10 px del borde de la foto.
- El clavo y el cordón ya los dibuja la web. Si los querés hacer en 3D, avisame y saco los de código.

### 7. Imagen para compartir el link → `img/og.jpg`
- Escena `WEB_compartir` · 1200×630 JPG · cámara en perspectiva.
- Es la vista previa que aparece cuando mandás el link por WhatsApp, Instagram o LinkedIn. Entra todo: cementerio, muro, antorchas, fuego y niebla.
- Poné "Tomas Carballes · 3D Generalist" en la zona roja (lo podés sumar en el compositor o en Photoshop).
- Algunas apps la recortan a cuadrado (línea celeste), así que el texto tiene que quedar adentro.

### 8. Niebla en loop → `img/fog.webm` y `img/fog.mp4`
- Escena `WEB_niebla` · 1920×1080 · 240 frames a 24 fps (10 s) · sin audio · menos de 3 MB.
- Entran solo la niebla y la luna, sobre el World oscuro. **Tiene que quedar fondo negro puro:** la web la mezcla en modo "screen", así que el negro desaparece y queda solo la niebla.
- Más densa abajo, más rala detrás del texto. Tonos verde, violeta y azul muy sutiles.
- **Ctrl+F12** renderiza la secuencia en `render_web/niebla/`. Para pasarla a video, mandámela y la convierto, o corré:
  - `ffmpeg -framerate 24 -i niebla_%04d.png -c:v libvpx-vp9 -b:v 0 -crf 40 -pix_fmt yuv420p -an fog.webm`
  - `ffmpeg -framerate 24 -i niebla_%04d.png -c:v libx264 -crf 26 -preset veryfast -pix_fmt yuv420p -movflags +faststart -an fog.mp4`

## Orden recomendado

1. Luna, World y material de piedra en MASTER.
2. El muro y las antorchas de hierro, ubicadas en las esferas guía.
3. El fuego en `Llamas` → renderizás `WEB_muro` y revisás que la luz sobre la piedra quede bien.
4. Las dos llamas animadas.
5. La textura de fondo, con el mismo material.
6. El pasto y el marco.
7. El cementerio, la niebla, el banner y la imagen para compartir.

## Cómo subirlo

- **Opción fácil:** pasame los archivos (o las carpetas de frames) en el chat y los subo yo.
- **Opción directa:** en GitHub, entrá al repo → carpeta `img` → **Add file → Upload files** → arrastrá los archivos con el nombre exacto → **Commit changes**. En uno o dos minutos ya se ven en la web.

Apenas subís `wall.png`, la web esconde las antorchas de código. Las llamas aparecen cuando subís `flame-left.webp` y `flame-right.webp`.

## Checklist antes de dar un asset por terminado

- [ ] Nombre, tamaño y formato exactos.
- [ ] Transparencia donde se pide (abrilo sobre un fondo de color para chequear).
- [ ] Antorchas en sus esferas guía y llamas que nacen en el punto rojo.
- [ ] Loops que empalman sin salto (llamas y niebla).
- [ ] Nada importante fuera de las zonas de celular.
- [ ] Zona del texto oscura y limpia.
- [ ] Comprimido y dentro del peso indicado.
- [ ] Probado en la web en compu y en celular.
