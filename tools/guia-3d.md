# Guía: assets 3D para la web

Esta carpeta tiene todo lo que necesitás para que lo que hagas en Blender encaje directo en https://tomascarballes.github.io. Si respetás nombres, tamaños, formatos y posiciones, cada asset reemplaza solo a su placeholder.

> **Si arrancaste con una versión anterior de esta carpeta:** empezá de nuevo. Bajá la carpeta nueva, reemplazá todo y arrancá con un `.blend` nuevo. Cambió la forma de armar el muro y las antorchas, y el script nuevo no es compatible con la escena vieja. Si ya modelaste algo (piedras, materiales, la antorcha), traelo al `.blend` nuevo con **File → Append** y metelo en su colección.

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `01` a `08` `-*.png` | Plantillas guía, una por asset. Marcan dónde va el contenido, qué se ve en celular, dónde tiene que haber transparencia y dónde conviene poner las antorchas. **No salen en el render.** |
| `setup_web_assets.py` | Script de Blender: arma la escena MASTER con sus colecciones y una escena por asset con cámara, resolución, formato, qué se ve y la plantilla de fondo. |
| `cortar_muro.py` | Script de Blender: corta los dos renders del muro en las partes que usa la web. |
| `GUIA.pdf` | Esta guía. |

## La idea

### Una sola escena, una sola luz

Se trabaja como en VFX: **todo vive en una escena con una sola iluminación** y de ahí salen las piezas por separado. La luna ilumina todo igual y todo parece del mismo mundo.

- **MASTER** es donde modelás, texturizás e iluminás.
- **Las escenas WEB_\*** no tienen copias: muestran la misma colección de MASTER. Si movés una piedra, cambia en todos los renders. Cada escena suma solo su cámara, su resolución y qué colecciones entran en ese render.

### Un muro enorme, en partes

El fondo de toda la página es **un solo muro gigante** (25,6 m de ancho por 76,8 m de alto), renderizado de una vez con su luz global. Después se corta en partes horizontales y la web las apila una debajo de la otra, en orden, así que se ve como una sola pared que vas scrolleando, con el contenido encima.

Del mismo muro salen **dos renders**, con dos cámaras:

| | Compu | Celular |
|---|---|---|
| Qué agarra la cámara | el muro entero, 25,6 m de ancho | la franja central del mismo muro, 4,9 m de ancho |
| Render | 2560 × 7680 px | 860 × 13440 px |
| Partes | 6 de 2560 × 1280 | 7 de 860 × 1920 |

En el celular la pantalla es angosta y la página mucho más larga, por eso se usa una franja del centro con más resolución: las piedras se ven más grandes y el muro alcanza para toda la página. No hay que modelar nada dos veces: es el mismo muro, con la misma luz, visto con otra cámara.

### Antorchas con luz real que titila

La luz se suma, y eso permite separarla en capas y sumarlas después sin perder realismo:

1. **El muro** se renderiza **solo con la luz de la luna**, quieto. Las antorchas de hierro salen en el muro, pero apagadas.
2. **Cada antorcha** tiene su propio **video animado**: un recuadro de 10,24 × 10,24 m alrededor de ella, con **solo su fuego encendido**, sin luna y con fondo negro. En ese video salen la llama, el hierro iluminado y la luz cálida titilando sobre los ladrillos, con sus sombras moviéndose.
3. **La web suma cada video encima del muro**, en modo *plus-lighter*, que es el "add" del compositor: lo negro no cambia nada y lo iluminado se suma a la piedra. El borde del recuadro se funde suave para que no se note el corte.

El resultado es igual a haber renderizado todo junto, pero con la luz de las antorchas animada.

**En celular** el contenido ocupa casi todo el ancho de la pantalla, así que solo se ve la antorcha que esté **arriba de todo**, en la franja libre bajo las almenas. Las laterales se ven solo en compu.

## Cómo arrancar (desde cero)

1. Bajá y descomprimí esta carpeta en tu compu.
2. Abrí Blender 4 o más nuevo, con un archivo nuevo, y **guardalo dentro de esta carpeta** (por ejemplo `web.blend`).
3. **Scripting → Open** → `setup_web_assets.py` (abrilo desde esta carpeta) → **Run Script**.
4. Quedás en la escena **MASTER**. Borrá el cubo, la luz y la cámara que vienen por defecto: están fuera de la colección MASTER y no se usan.
5. Modelá todo **adentro de la colección que corresponde**. Antes de agregar un objeto, hacé clic en la colección en el Outliner para que quede activa. Para mover algo ya creado: seleccionalo, **M** y elegí la colección.

**Colecciones de MASTER:**

| Colección | Qué va adentro |
|---|---|
| `Luz_luna` | La luna (luz principal fría), el cielo y el ambiente. |
| `Cementerio` | El fondo de la intro: lápidas, árboles, rejas, suelo lejano. |
| `Muro` | El muro gigante con almenas. |
| `Antorchas_hierro` | Los soportes de hierro de todas las antorchas, sin fuego. |
| `Fuego_<nombre>` | Una por antorcha (`Fuego_arriba`, `Fuego_izq_1`…): **su** llama y **su** luz. |
| `Pasto` | El pasto y las calaveras. |
| `Marco` | El marco dorado. |
| `Niebla` | El volumen de niebla. |
| `GUIAS (no se renderiza)` | El tamaño del muro, la franja del celular y una esfera donde va la boca de cada antorcha. |

**Para trabajar un asset en particular**, por ejemplo el banner, cambiá a su escena (`WEB_banner`) arriba a la derecha y mirá por la cámara (**Numpad 0**): aparece la plantilla encima. Podés modelar desde ahí, porque las colecciones son compartidas. Si una cámara está en perspectiva, encuadrás tu vista y **Ctrl+Alt+Numpad 0** mueve la cámara a donde estás mirando.

**Para renderizar**, en su escena: **F12** para imágenes o **Ctrl+F12** para animaciones (antorchas y niebla). Todo sale en `render_web/`, al lado del `.blend`.

**Si la plantilla no aparece**, revisá que estés en una escena WEB_\* y no en MASTER, y que el botón **Overlays** del visor (los dos circulitos) esté prendido. Si el script dice que no encuentra las plantillas, pegá la ruta de esta carpeta en `TEMPLATES_DIR`, arriba de todo en el script.

**Necesita Cycles.** El script ya lo deja puesto en todas las escenas.

## Medidas

- **Escala:** 100 px del render de compu = 1 m.
- **Muro:** X de −12,8 a 12,8 m, Z de 0 (abajo) a 76,8 m (arriba de las almenas), la cara en Y = 0 mirando a −Y. Las almenas ocupan los 60 cm de arriba.
- **Antorchas:** la boca de cada una va justo en su esfera `GUIA_antorcha_<nombre>`.
- **Pasto:** base en Z = −10, debajo del muro, para que no se mezcle.
- **Marco:** 60 × 74 cm, centrado en X = 40.

### Dónde poner las antorchas

Las posiciones están en la lista `TORCHES`, arriba de todo en `setup_web_assets.py`: cada una tiene nombre, X y Z en metros. Para agregar, sacar o mover una antorcha, **editás la lista y volvés a correr el script**. Eso crea o actualiza su esfera guía, su colección `Fuego_…`, su escena y el archivo `antorchas.json`, que es el que le dice a la web dónde va cada una.

- **Laterales (compu):** X entre ±8,6 y ±10,6 m. Más adentro quedan tapadas por el contenido y más afuera se cortan en pantallas chicas. Las zonas amarillas de la plantilla del muro de compu las marcan.
- **Arriba (compu y celular):** en la franja libre debajo de las almenas, cerca de X = 0 y Z = 75,6. Es la única que se ve en celular.
- **En altura** las podés distribuir como quieras a lo largo del muro. En pantallas grandes la página termina cerca de Z = 11 m y en las más chicas usa el muro hasta abajo: si querés que una antorcha se vea siempre, ponela arriba de Z = 12 m.
- **La lista que trae el script es un ejemplo:** una arriba y cuatro laterales. Cada antorcha es un video, así que con 4 a 7 en total la web sigue liviana.

## Reglas para todos

- **Lo primero es que se lea el texto y se vean tus trabajos.** Valores bajos, poco contraste y nada de detalle fuerte detrás del contenido.
- **Paleta:** fondo #0a0d0b · musgo #6f8a68 · violeta #9a80c4 / #5d4785 · azul frío suave · hueso #e3e1d8. Lo único cálido es el fuego (ámbar #e8a24a).
- **World oscuro:** lo usan todas las escenas menos las de antorcha, que usan uno negro (`WEB_negro`) que crea el script.
- **Color:** view transform AgX (o Filmic), look None, salida sRGB, igual en todas. El script ya lo configura. Si cambiás la exposición del muro, cambiala también en las antorchas, porque se suman.
- **Peso:** el script ya exporta en formatos livianos. Si algo pesa más de lo indicado, pasalo por https://squoosh.app.

## Cada asset

### 1. Banner de la intro → `img/banner.jpg`
- Escena `WEB_banner` · 2560×1440 JPG · menos de 500 KB · cámara en perspectiva, la ubicás vos.
- Entran luna, cementerio y niebla. El fuego entra solo como luz, por si alguna antorcha ilumina a lo lejos.
- Ocupa toda la pantalla de entrada, al 40% de opacidad y con la niebla animada encima.
- **Zona roja** (centro): ahí van tu nombre y los botones. Tiene que quedar oscura y limpia.
- **Franja celeste:** es lo único que se ve en un celular vertical. Lo importante va adentro.
- La web oscurece la parte de abajo hacia negro: no pongas nada clave ahí.

### 2. Muro para compu → `img/muro/compu_1.webp` … `compu_6.webp`
- Escena `WEB_muro_compu` · render de 2560×7680 PNG con transparencia arriba · cámara ortográfica de frente (ya puesta).
- Entran el muro, el hierro de las antorchas y la luna. **El fuego no entra**: su luz va en los videos de antorcha.
- **Almenas:** los 60 cm de arriba, con el espacio entre ellas transparente. Es el borde que sube y tapa la intro al scrollear.
- **Franja amarilla de arriba:** es pared que se ve antes del contenido. Es el lugar de la antorcha de arriba.
- **Zona roja central:** queda detrás del contenido. Piedra oscura, pareja y sin antorchas.
- **Zonas amarillas a los costados:** ahí van las antorchas laterales.
- **Líneas blancas:** los cortes entre partes. No pasa nada si una piedra queda cortada, porque la web las une sin costura.
- **Línea verde:** en pantallas grandes la página termina ahí; en las más chicas se usa el muro hasta abajo. Así que el muro tiene que verse bien de punta a punta.
- **Render pesado:** 20 megapíxeles. Usá el denoiser y las muestras que necesites. Es una sola imagen quieta, se hace una vez.

### 3. Muro para celular → `img/muro/celu_1.webp` … `celu_7.webp`
- Escena `WEB_muro_celular` · render de 860×13440 PNG con transparencia arriba. (Arriba se ve solo el comienzo de su plantilla; la plantilla completa está en la carpeta.)
- **Mismo muro y misma luz que el de compu.** La cámara agarra la franja central de 4,9 m (la caja `GUIA_franja_celular`). No hay que tocar nada en la escena: solo renderizar.
- En celular el contenido ocupa todo el ancho, así que la zona roja es casi toda la imagen. Lo único que queda a la vista sin contenido encima es la franja de arriba.

### Cortar el muro en partes
1. Renderizá `WEB_muro_compu` y `WEB_muro_celular` (**F12** en cada una). Quedan `render_web/muro_compu.png` y `render_web/muro_celular.png`.
2. **Scripting → Open** → `cortar_muro.py` → **Run Script**.
3. Te deja las partes en `render_web/muro/`: `compu_1.webp` a `compu_6.webp` y `celu_1.webp` a `celu_7.webp`.
4. Si el script falla, mandame los dos PNG y los corto yo.

### 4. Antorchas (llama + su luz) → `img/antorchas/<nombre>.mp4` + `img/antorchas.json`
- Una escena por antorcha: `WEB_antorcha_arriba`, `WEB_antorcha_izq_1`, etc. · 1024×1024 · 48 frames a 24 fps (2 s) · video MP4 directo desde Blender.
- Entran **el muro, el hierro y el fuego de ESA antorcha**, sin luna y con el mundo negro. Por eso cada antorcha necesita su propia colección `Fuego_<nombre>`: así en su video no se cuela la luz de las otras.
- La cámara es ortográfica, centrada en la boca de la antorcha y con la misma escala que el muro de compu, así que el video coincide exacto con la pared, sin alinear nada.

**Cómo armar cada antorcha**

1. **El hierro** va en `Antorchas_hierro`, con la boca justo en su esfera guía.
2. **La llama** va en `Fuego_<nombre>`. Puede ser una simulación de fuego (Mantaflow) o algo más simple y liviano: una forma con shader de **Emission**, animada con ruido.
3. **La luz** va en la misma colección `Fuego_<nombre>`: una **Point Light** ámbar dentro de la llama. Con su potencia y su radio decidís cuánta pared ilumina. Una llama emisiva ilumina sola, pero la Point Light es mucho más fácil de controlar.
4. **Que titile:** animá la potencia de la luz con un modificador **Noise** en el Graph Editor, y movela un poco (unos centímetros) también con Noise, para que las sombras se muevan. El fuego del shader, animado con ruido.
5. **Loop perfecto:** el frame 48 tiene que empalmar con el 1. Con los modificadores Noise, usá **Cyclic** o dejá que el inicio y el final coincidan. Para el ruido del shader, usá **4D noise** y mové la coordenada W en círculo con el frame: `sin` y `cos` de `frame / 48 · 2π`.
6. **Que se apague antes del borde:** la web funde el borde del video a negro desde un poco más de la mitad del recuadro hacia afuera (el círculo amarillo de la plantilla). La luz fuerte tiene que quedar adentro de ese círculo y llegar casi a negro en el borde.
7. **Que cada antorcha sea distinta:** cambiá el *seed* o el desfase del ruido en cada una. Si todas titilan igual, se nota.

**Exportar:** **Ctrl+F12** en cada escena de antorcha. Sale directo `render_web/antorchas/<nombre>.mp4`. Además, el script genera `render_web/antorchas.json` con las posiciones de todas (se crea cuando el `.blend` ya está guardado; si no está, volvé a correr el script). Ese archivo va junto con los videos.

### 5. Pasto con calaveras → `img/grass.png`
- Escena `WEB_pasto` · 2560×200 PNG **con transparencia** · repetible en horizontal.
- Entran el pasto y la luna. Es el suelo al final de la página, por delante del muro.
- Abajo una base sólida que toque el borde. Arriba, las puntas del pasto sobre fondo transparente.
- Entre 2 y 4 calaveras chicas semienterradas. En celular la imagen se ve de unos 30 px de alto, así que necesitan una silueta clara.

### 6. Marco dorado → `img/frame.png`
- Escena `WEB_marco` · 600×740 PNG **con transparencia** · 60 × 74 cm.
- Entran el marco y la luna.
- Marco ovalado barroco, dorado a la hoja, con remate tallado arriba.
- **El hueco va hasta la línea amarilla y tiene que ser transparente**, porque tu foto va debajo (el óvalo rojo). El marco tapa unos 10 px del borde de la foto.
- El clavo y el cordón ya los dibuja la web. Si los querés hacer en 3D, avisame y saco los de código.

### 7. Imagen para compartir el link → `img/og.jpg`
- Escena `WEB_compartir` · 1200×630 JPG · cámara en perspectiva.
- Es la vista previa que aparece cuando mandás el link por WhatsApp, Instagram o LinkedIn. Entra todo, con el fuego encendido.
- Poné "Tomas Carballes · 3D Generalist" en la zona roja (en el compositor o en Photoshop).
- Algunas apps la recortan a cuadrado (línea celeste): el texto tiene que quedar adentro.

### 8. Niebla en loop → `img/fog.mp4`
- Escena `WEB_niebla` · 1920×1080 · 240 frames a 24 fps (10 s) · video MP4 directo desde Blender · menos de 3 MB.
- Entran solo la niebla y la luna, sobre el World oscuro. **Tiene que quedar fondo negro puro:** la web la mezcla en modo "screen", así que el negro desaparece y queda solo la niebla.
- Más densa abajo, más rala detrás del texto. Tonos verde, violeta y azul muy sutiles.
- **Ctrl+F12** → sale `render_web/fog.mp4`.

## Orden recomendado

1. Luna, World y material de piedra, en MASTER.
2. El muro gigante y las almenas.
3. El hierro de las antorchas en sus esferas guía (y la lista `TORCHES` ajustada a tu gusto).
4. Render de prueba de `WEB_muro_compu` a resolución baja (Output → % al 25%) para ver la luz de luna.
5. Una antorcha completa con su llama y su luz animadas → video → probala sobre el muro.
6. Las demás antorchas.
7. Renders finales del muro (compu y celular) → `cortar_muro.py`.
8. El pasto y el marco.
9. El cementerio, la niebla, el banner y la imagen para compartir.

## Qué subir a la web

Dentro de la carpeta `img/` del repo:

| Archivo | De dónde sale |
|---|---|
| `muro/compu_1.webp` … `compu_6.webp` | `render_web/muro/` (después de `cortar_muro.py`) |
| `muro/celu_1.webp` … `celu_7.webp` | `render_web/muro/` |
| `antorchas/<nombre>.mp4` | `render_web/antorchas/` |
| `antorchas.json` | `render_web/antorchas.json` |
| `banner.jpg`, `grass.png`, `frame.png`, `og.jpg`, `fog.mp4` | `render_web/` |

- **Opción fácil:** pasame la carpeta `render_web` comprimida en el chat y subo todo yo.
- **Opción directa:** en GitHub, entrá al repo → carpeta `img` → **Add file → Upload files** → arrastrá respetando las carpetas → **Commit changes**. En uno o dos minutos se ve en la web.

Mientras no estén las partes del muro, la web muestra el muro de código que tiene ahora. Apenas subís `compu_1.webp` (o `celu_1.webp`), cambia al tuyo.

## Checklist antes de dar un asset por terminado

- [ ] Nombre, tamaño y formato exactos.
- [ ] Transparencia donde se pide (abrilo sobre un fondo de color para chequear).
- [ ] Antorchas en sus esferas guía y `antorchas.json` generado después del último cambio a la lista.
- [ ] La luz de cada antorcha se apaga antes del borde de su video.
- [ ] Loops que empalman sin salto (antorchas y niebla).
- [ ] Nada importante fuera de las zonas que se ven en celular.
- [ ] Zona del contenido oscura y pareja.
- [ ] Probado en la web en compu y en celular.
