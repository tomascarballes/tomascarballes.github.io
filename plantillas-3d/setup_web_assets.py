# Blender 4.x — una escena MASTER con todo, y una escena por asset vinculada a ella.
#
# Cómo funciona:
#   - Todo lo que modelás e iluminás va en la escena "MASTER", dentro de las colecciones que crea este script.
#   - Cada escena WEB_* NO tiene copias: muestra la misma colección MASTER (si movés algo, cambia en todas)
#     y solo agrega su cámara, su resolución y qué colecciones se ven, se ocultan o solo aportan luz.
#   - La plantilla de cada asset aparece al mirar por la cámara (Numpad 0). No sale en el render.
#
# Uso:
#   1. Scripting > Open > elegí este archivo DESDE la carpeta plantillas-3d > Run Script.
#   2. Modelá en la escena MASTER. Para renderizar, cambiá a una escena WEB_* (arriba a la derecha) y F12.
#   3. Podés volver a correrlo cuando quieras: no borra ni duplica nada, solo actualiza la configuración.
#
# Escala: 100 px de la web = 1 metro en Blender. El muro mide 25,6 m de ancho y 3 m de alto (base en Z = 0, centrado en X = 0).

import bpy, os, math

# Si la plantilla no aparece, pegá acá la ruta de la carpeta plantillas-3d, por ejemplo:
# TEMPLATES_DIR = r"C:\Users\Tomas\Documents\plantillas-3d"
TEMPLATES_DIR = r""

# --- posiciones fijas (en px de la imagen del muro, 2560 x 300). La web pone las llamas exactamente acá. ---
WALL_W, WALL_H = 2560, 300
FLAMES = {"izq": (420, 135), "der": (2140, 135)}   # punto donde nace la llama (centro de la boca de la antorcha)
FLAME_W, FLAME_H = 128, 192                        # tamaño de cada secuencia de llama
FLAME_BASE = (64, 150)                             # dónde cae ese punto dentro de la imagen de la llama

def px_to_world(x, y):
    """px del muro -> (X, Z) en metros. El muro va de X=-12.8 a 12.8 y de Z=0 a 3."""
    return (x - WALL_W / 2) / 100.0, (WALL_H - y) / 100.0

COLLECTIONS = [
    "Luz_luna",          # luna, cielo, ambiente frío
    "Luz_neutra",        # luz pareja SOLO para la textura de fondo
    "Cementerio",        # fondo de la intro: lápidas, árboles, rejas, suelo lejano
    "Muro",              # el muro con almenas
    "Antorchas_hierro",  # soportes de hierro de las antorchas
    "Llamas",            # el fuego (objetos emisivos / simulación) — también ilumina el muro
    "Pasto",             # pasto y calaveras del pie de página
    "Textura_piedra",    # plano con el material de piedra para la textura repetible
    "Marco",             # marco dorado de la foto
    "Niebla",            # volumen de niebla
]

# Por escena: qué colecciones se renderizan. Lo que no figura queda excluido.
#   "on" = se ve normal · "luz" = no se ve pero ilumina y se refleja (Indirect only) · "hold" = tapa como un agujero transparente (Holdout)
ASSETS = [
    # escena,             ancho, alto, plantilla,                         transp., formato, salida,                          cámara,  colecciones
    ("WEB_banner",         2560, 1440, "01-banner_2560x1440.png",         False, "JPEG", "banner.jpg",                   "PERSP", {"Luz_luna":"on","Cementerio":"on","Niebla":"on","Llamas":"luz"}),
    ("WEB_muro",           2560,  300, "02-muro_2560x300.png",            True,  "PNG",  "wall.png",                     "ORTHO", {"Luz_luna":"on","Muro":"on","Antorchas_hierro":"on","Llamas":"luz"}),
    ("WEB_llama_izq",       128,  192, "04-llama_128x192.png",            True,  "PNG",  "llama_izq/llama_izq_####.png", "FLAME_izq", {"Luz_luna":"on","Llamas":"on","Antorchas_hierro":"hold","Muro":"hold"}),
    ("WEB_llama_der",       128,  192, "04-llama_128x192.png",            True,  "PNG",  "llama_der/llama_der_####.png", "FLAME_der", {"Luz_luna":"on","Llamas":"on","Antorchas_hierro":"hold","Muro":"hold"}),
    ("WEB_textura_fondo",  1024, 1024, "03-textura-fondo_1024x1024.png",  False, "JPEG", "wall-tile.jpg",                "TILE",  {"Luz_neutra":"on","Textura_piedra":"on"}),
    ("WEB_pasto",          2560,  200, "05-pasto_2560x200.png",           True,  "PNG",  "grass.png",                    "GRASS", {"Luz_luna":"on","Pasto":"on","Llamas":"luz"}),
    ("WEB_marco",           600,  740, "06-marco_600x740.png",            True,  "PNG",  "frame.png",                    "FRAME", {"Luz_luna":"on","Marco":"on","Llamas":"luz"}),
    ("WEB_compartir",      1200,  630, "07-compartir_1200x630.png",       False, "JPEG", "og.jpg",                       "PERSP", {"Luz_luna":"on","Cementerio":"on","Niebla":"on","Muro":"on","Antorchas_hierro":"on","Llamas":"on"}),
    ("WEB_niebla",         1920, 1080, "08-niebla_1920x1080.png",         False, "PNG",  "niebla/niebla_####.png",       "PERSP", {"Luz_luna":"on","Niebla":"on"}),
]

def find_templates_dir():
    c = []
    if TEMPLATES_DIR: c.append(TEMPLATES_DIR)
    for t in bpy.data.texts:
        if t.filepath and t.name.startswith("setup_web_assets"):
            c.append(os.path.dirname(bpy.path.abspath(t.filepath)))
    if bpy.data.filepath:
        d = os.path.dirname(bpy.data.filepath); c += [d, os.path.join(d, "plantillas-3d")]
    for d in c:
        if os.path.exists(os.path.join(d, "01-banner_2560x1440.png")): return d
    return None

HERE = find_templates_dir()
if not HERE:
    raise RuntimeError("No encuentro las plantillas. Abrí el script desde la carpeta plantillas-3d "
                       "(Scripting > Open) o escribí la ruta en TEMPLATES_DIR, arriba de todo.")

# --- escena MASTER y colecciones ---
master = bpy.data.scenes.get("MASTER")
if not master:
    master = bpy.context.window.scene
    master.name = "MASTER"
root = bpy.data.collections.get("MASTER") or bpy.data.collections.new("MASTER")
if root.name not in master.collection.children:
    master.collection.children.link(root)
for n in COLLECTIONS:
    col = bpy.data.collections.get(n) or bpy.data.collections.new(n)
    if col.name not in root.children:
        root.children.link(col)
master.render.engine = "CYCLES"

# Guías visuales en MASTER: un rectángulo del tamaño del muro y los puntos de las llamas (no se renderizan)
guides = bpy.data.collections.get("GUIAS (no se renderiza)") or bpy.data.collections.new("GUIAS (no se renderiza)")
if guides.name not in master.collection.children:
    master.collection.children.link(guides)
guides.hide_render = True
def empty(name, loc, size=0.3, kind="PLAIN_AXES"):
    o = bpy.data.objects.get(name) or bpy.data.objects.new(name, None)
    o.empty_display_type, o.empty_display_size, o.location = kind, size, loc
    if o.name not in guides.objects: guides.objects.link(o)
    return o
empty("GUIA_muro_25.6x3m", (0, 0, 1.5), 1, "CUBE").scale = (12.8, 0.05, 1.5)
for side, (x, y) in FLAMES.items():
    wx, wz = px_to_world(x, y)
    empty(f"GUIA_llama_{side}", (wx, 0, wz), 0.15, "SPHERE")

def set_view(scene):
    for vt in ("AgX", "Filmic"):
        try: scene.view_settings.view_transform = vt; break
        except TypeError: pass
    scene.view_settings.look = "None"
    scene.display_settings.display_device = "sRGB"

def find_lc(layer_coll, name):
    if layer_coll.collection.name == name: return layer_coll
    for ch in layer_coll.children:
        r = find_lc(ch, name)
        if r: return r
    return None

def place_camera(cam, cam_data, kind, w, h):
    ortho = kind != "PERSP"
    cam_data.type = "ORTHO" if ortho else "PERSP"
    if ortho:
        cam_data.ortho_scale = max(w, h) / 100.0      # 1 px = 1 cm
        cam.rotation_euler = (math.radians(90), 0, 0)  # de frente, mirando hacia +Y
    if kind == "ORTHO":   # muro
        cam.location = (0, -20, WALL_H / 200.0)
    elif kind.startswith("FLAME_"):
        x, y = FLAMES[kind.split("_")[1]]
        wx, wz = px_to_world(x, y)
        # mismo tamaño de pixel que el muro, encuadrado para que la llama caiga en FLAME_BASE
        cam.location = (wx + (FLAME_W / 2 - FLAME_BASE[0]) / 100.0, -20, wz + (FLAME_BASE[1] - FLAME_H / 2) / 100.0)
    elif kind == "TILE":
        cam.location = (0, -5, -50)                   # lejos del resto; poné el plano de piedra acá
    elif kind == "GRASS":
        cam.location = (0, -20, -10 + h / 200.0)      # el pasto va con su base en Z = -10
    elif kind == "FRAME":
        cam.location = (30, -5, 3.7)                  # el marco va centrado en X = 30, Z = 3,7
    elif cam.location.length == 0:
        cam.location, cam.rotation_euler = (0, -30, 1.7), (math.radians(88), 0, 0)

for name, w, h, tpl, transparent, fmt, out, cam_kind, cols in ASSETS:
    sc = bpy.data.scenes.get(name) or bpy.data.scenes.new(name)
    if root.name not in sc.collection.children:
        sc.collection.children.link(root)          # misma colección que MASTER: sin copias
    sc.world = master.world
    r = sc.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
    r.film_transparent = transparent
    r.image_settings.file_format = fmt
    r.image_settings.color_mode = ("RGBA" if transparent else "RGB")
    if fmt == "PNG": r.image_settings.compression = 90
    else: r.image_settings.quality = 88
    r.filepath = "//render_web/" + out
    set_view(sc)
    if name.startswith("WEB_llama"):
        sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, 48      # 2 s en loop
    if name == "WEB_niebla":
        sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, 240     # 10 s en loop

    vl = sc.view_layers[0]
    for n in COLLECTIONS:
        lc = find_lc(vl.layer_collection, n)
        if not lc: continue
        mode = cols.get(n)
        lc.exclude = mode is None
        if mode is not None:
            lc.holdout = (mode == "hold")
            lc.indirect_only = (mode == "luz")

    cam_name = name + "_CAM"
    cd = bpy.data.cameras.get(cam_name) or bpy.data.cameras.new(cam_name)
    cam = bpy.data.objects.get(cam_name) or bpy.data.objects.new(cam_name, cd)
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    place_camera(cam, cd, cam_kind, w, h)
    sc.camera = cam

    path = os.path.join(HERE, tpl)
    cd.show_background_images = True
    if os.path.exists(path):
        img = bpy.data.images.load(path, check_existing=True)
        bg = cd.background_images[0] if cd.background_images else cd.background_images.new()
        bg.image, bg.alpha, bg.display_depth, bg.frame_method = img, 0.8, "FRONT", "FIT"
    else:
        print("No encontré la plantilla:", path)

bpy.context.window.scene = master
for area in bpy.context.window.screen.areas:
    if area.type == "VIEW_3D":
        for sp in area.spaces:
            if sp.type == "VIEW_3D": sp.overlay.show_overlays = True

print("Listo. Plantillas desde:", HERE)
print("Modelá en MASTER. Para renderizar, cambiá a una escena WEB_* y mirá por la cámara (Numpad 0).")
