# Blender 4.x — corta los renders del muro en las partes que usa la web.
# Uso: después de renderizar WEB_muro_compu y WEB_muro_celular (quedan en render_web/),
#      Scripting > Open > cortar_muro.py > Run Script.
# Resultado: render_web/muro/compu_1..6.webp y celu_1..7.webp (con transparencia en las almenas).
# Si algo falla, mandame muro_compu.png y muro_celular.png y los corto yo.

import bpy, os
try:
    import numpy as np
except ImportError:
    raise RuntimeError("Este Blender no trae numpy. Mandame los PNG del muro y los corto yo.")

if not bpy.data.filepath:
    raise RuntimeError("Guardá el .blend primero (los renders se buscan en render_web/, al lado del .blend).")
base = os.path.join(os.path.dirname(bpy.data.filepath), "render_web")
out = os.path.join(base, "muro"); os.makedirs(out, exist_ok=True)

JOBS = [("muro_compu.png", "compu", 6), ("muro_celular.png", "celu", 7)]

for src, prefix, n in JOBS:
    path = os.path.join(base, src)
    if not os.path.exists(path):
        print("Falta", path, "- renderizá esa escena primero."); continue
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    if h % n:
        raise RuntimeError(f"{src} mide {w}x{h}: el alto tiene que ser {n} partes iguales. ¿Cambiaste la resolución?")
    px = np.empty(w * h * 4, dtype=np.float32); img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)                    # en Blender la fila 0 es la de ABAJO
    ph = h // n
    for i in range(n):                          # parte 1 = la de arriba
        top = h - i * ph
        part = px[top - ph:top]
        name = f"{prefix}_{i + 1}"
        im = bpy.data.images.new(name, w, ph, alpha=True)
        im.pixels.foreach_set(part.ravel())
        im.filepath_raw = os.path.join(out, name + ".webp")
        im.file_format = "WEBP"
        try:
            im.save(quality=85)
        except TypeError:
            im.save()
        bpy.data.images.remove(im)
        print("guardé", name + ".webp")
    bpy.data.images.remove(img)
print("Listo: partes en render_web/muro/")
