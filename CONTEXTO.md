# CONTEXTO — Portfolio de Tomas Carballes

Memoria del proyecto: decisiones y pendientes. Actualizar en cada commit.

## Objetivo
Conseguir trabajo como **3D Generalist** (juegos, cine, publicidad). La web es la puerta de entrada: arte primero, rápida de leer para reclutadores (30–60 s por portfolio).

## Publicación
- Repo: `tomascarballes/tomascarballes.github.io` (público)
- GitHub Pages desde `main`, carpeta raíz. URL: https://tomascarballes.github.io/
- Cambios directo a `main`, commits firmados como Tomas <tomaspcarballes@gmail.com>.

## Estructura
- `index.html` — toda la web (HTML + CSS + JS en un archivo).
- `img/` — imágenes propias. `about.jpg` (foto). Placeholders que se activan solos si existen: `banner.jpg`, `wall.png` (con antorchas horneadas; esconde las de código), `flame-left.webp`/`flame-right.webp` (llamas animadas, ubicadas por JS en px 420,135 y 2140,135 del muro), `wall-tile.jpg`, `grass.png`, `frame.png`, `fog.webm`/`fog.mp4`, `og.jpg`, y portadas `fridge.jpg`, `potions.jpg`, `astros.jpg`, `bloodseer.jpg`, `bathroom.jpg` (respaldo si no cargan las de ArtStation).
- `cv/` — PDFs del CV (pendiente).
- `plantillas-3d/` — plantillas guía PNG, script de Blender (`setup_web_assets.py`, escena MASTER + escenas vinculadas) y `GUIA.pdf` con specs de cada asset 3D (fuente: `tools/guia-3d.md`, se regenera con `python3 tools/build_guia.py`).
- `drafts/` — versiones anteriores del diseño (minimalista, gótica bordó, cementerio v11).

## CV
- Contenido en `tools/build_cv.py` (dict DATA, inglés y español). Editar ahí y correr:
  - Web (público): `python3 tools/build_cv.py` → genera `cv/en.html`, `cv/es.html` y los PDF.
  - Completo (con teléfono, para postulaciones): `python3 tools/build_cv.py --phone "..." --area "Villa Ortuzar, Argentina" --out <carpeta fuera del repo>`.
- El teléfono NUNCA se guarda en el repo (es público). El script se niega a escribir la versión completa adentro del repo.
- Diseño: el mismo del CV original (blanco, azul, dos columnas), sin estética gótica, para lectura automática e impresión.

## Assets 3D
- Una sola escena MASTER con una sola iluminación; escenas WEB_* vinculadas (misma colección) con su cámara/resolución y modos por colección (se ve / solo luz / holdout / excluida). Cycles.
- Escala 100 px = 1 m. Muro 25,6×3 m. Antorchas horneadas en wall.png; la llama sale aparte como WebP animado 128×192 (base en px 64,150) renderizado con cámara ortográfica de igual escala. Textura de fondo con luz neutra aparte.
- Generadores: `tools/build_plantillas.py` (PNGs), `tools/build_guia.py` (PDF desde `tools/guia-3d.md`).

## Decisiones
- Título: nombre grande + "3D Generalist". Subtítulo: Modeling · Lookdev · Lighting · Rendering.
- Nada de "Open to work" en el banner (decisión de Tomas).
- Estética: cementerio gótico de noche (verde musgo, violeta, azul), referencias Bloodborne / Hollow Knight / Tim Burton. Siempre subordinada a la lectura y al trabajo.
- Texto sobre fondos animados o 3D: soporte negro difuminado detrás (estilo Hollow Knight).
- Intro a pantalla completa con niebla, estrellas y luna; flecha "See work"; al scrollear sube un muro de castillo que tapa la intro y aparece el menú.
- Todo el fondo es muro de piedra; contenido sobre bloques negros que se difuminan en los bordes.
- Pasto y calaveras al pie de la página. Foto del About en marco ovalado dorado colgado.
- Orden: Intro → Selected Work → About → CV → Other work → Contact.
- Proyecto destacado: Just a Normal Fridge.
- Lo de "storyteller" va en el About, no en el título.
- Elementos visuales del sitio se reemplazarán por modelos 3D propios (y se aclarará en el footer).

## Pendientes
- [ ] Portadas limpias de los 5 trabajos (sin título incrustado).
- [ ] Nombres y links de las 2 apps (Other work).
- [ ] Revisar texto del About (lo redactó Claude).
- [x] CV en HTML como fuente única (`tools/build_cv.py`). Versión web sin teléfono ni barrio en `cv/`; botones de descarga activos.
- [x] Web publicada en GitHub Pages; corregidos 2 links de portadas de ArtStation.
- [ ] Imagen og:image para la vista previa del link en DMs.
- [ ] Reemplazos 3D: muro, antorchas, pasto/calaveras, marco, niebla en loop, banner.
- [ ] Reel (re-render con cámara, 16:9, ~1 min).
- [ ] Mostrar retopología con las esculturas del curso: high poly vs low poly, wireframes y bakes (para el portfolio, ArtStation y el reel).
- [ ] ArtStation: titular a "3D Generalist", portada de Astros que muestre luz/render, revisar baño gótico, revisar Bloodseer.
- [ ] Opcional: dominio propio (tomascarballes.com).
