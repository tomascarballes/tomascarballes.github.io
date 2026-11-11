# Blender 4.x — escena MASTER con todo y una escena por asset vinculada a ella.
#
#   - Modelás e iluminás todo en "MASTER", DENTRO de las colecciones que crea este script.
#     Lo que quede suelto (fuera de la colección MASTER) no aparece en ningún render.
#   - Cada escena WEB_* muestra la MISMA colección MASTER (sin copias) y solo agrega su cámara,
#     su resolución y qué colecciones se ven en ese render.
#   - Mirando por la cámara de una escena WEB_* (Numpad 0) aparece su plantilla. No sale en el render.
#
# Uso: Scripting > Open > este archivo DESDE la carpeta plantillas-3d > Run Script.
# Se puede correr las veces que quieras: no borra ni duplica, solo actualiza.
#
# Escala: 100 px de la web (compu) = 1 m. El muro mide 25,6 m de ancho x 76,8 m de alto,
# centrado en X = 0, base en Z = 0, la cara mirando a -Y (hacia las cámaras).

import bpy, os, math, json

# Si la plantilla no aparece, pegá acá la ruta de la carpeta plantillas-3d, por ejemplo:
# TEMPLATES_DIR = r"D:\Design\Work\Portfolio Web Page\plantillas-3d"
TEMPLATES_DIR = r""

# ---------------------------------------------------------------------------------------------
# ANTORCHAS: editá esta lista y volvé a correr el script.
#   id = nombre (sin espacios), x / z = posición de la BOCA de la antorcha en metros.
#   Compu: las laterales van entre 8,6 y 10,6 m del centro (x = ±8.6 a ±10.6) para que se vean
#   en cualquier pantalla y no queden detrás del contenido.
#   "arriba" está en la franja libre de arriba: es la única que se ve también en el celular.
TORCHES = [
    ("arriba",  0.0, 75.6),
    ("izq_1",  -9.6, 68.0),
    ("der_1",   9.6, 62.0),
    ("izq_2",  -9.6, 48.0),
    ("der_2",   9.6, 40.0),
]
TORCH_SIZE = 10.24      # lado del recuadro de cada video de antorcha, en metros (1024 px)
# ---------------------------------------------------------------------------------------------

WALL_W_M, WALL_H_M = 25.6, 76.8

BASE_COLLECTIONS = ["Luz_luna", "Cementerio", "Muro", "Antorchas_hierro", "Pasto", "Marco", "Niebla"]
FIRE = ["Fuego_" + t[0] for t in TORCHES]        # una colección por antorcha: su llama + su luz
ALL_FIRE = {f: "on" for f in FIRE}
SOLO_LUZ_FIRE = {f: "luz" for f in FIRE}

# escena, ancho, alto, plantilla, transparente, formato, salida, cámara, colecciones (on / luz / hold)
ASSETS = [
    ("WEB_banner",        2560, 1440, "01-banner_2560x1440.png",      False, "JPEG",  "banner.jpg",          "PERSP",
        {"Luz_luna":"on","Cementerio":"on","Niebla":"on", **SOLO_LUZ_FIRE}),
    ("WEB_muro_compu",    2560, 7680, "02-muro-compu_2560x7680.png",  True,  "PNG",   "muro_compu.png",      "WALL_D",
        {"Luz_luna":"on","Muro":"on","Antorchas_hierro":"on"}),
    ("WEB_muro_celular",   860,13440, "03-muro-celular_860x13440.png",True,  "PNG",   "muro_celular.png",    "WALL_M",
        {"Luz_luna":"on","Muro":"on","Antorchas_hierro":"on"}),
    ("WEB_pasto",         2560,  200, "05-pasto_2560x200.png",        True,  "PNG",   "grass.png",           "GRASS",
        {"Luz_luna":"on","Pasto":"on"}),
    ("WEB_marco",          600,  740, "06-marco_600x740.png",         True,  "PNG",   "frame.png",           "FRAME",
        {"Luz_luna":"on","Marco":"on"}),
    ("WEB_compartir",     1200,  630, "07-compartir_1200x630.png",    False, "JPEG",  "og.jpg",              "PERSP",
        {"Luz_luna":"on","Cementerio":"on","Niebla":"on","Muro":"on","Antorchas_hierro":"on", **ALL_FIRE}),
    ("WEB_niebla",        1920, 1080, "08-niebla_1920x1080.png",      False, "VIDEO", "fog.mp4",             "PERSP",
        {"Luz_luna":"on","Niebla":"on"}),
]
for tid, x, z in TORCHES:   # un video por antorcha: solo su fuego, sin luna, fondo negro
    ASSETS.append(("WEB_antorcha_" + tid, 1024, 1024, "04-antorcha_1024x1024.png", False, "VIDEO",
                   "antorchas/" + tid + ".mp4", "TORCH_" + tid,
                   {"Muro":"on","Antorchas_hierro":"on","Fuego_" + tid:"on"}))

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

# --- MASTER y colecciones ---
master = bpy.data.scenes.get("MASTER")
if not master:
    master = bpy.context.window.scene
    master.name = "MASTER"
master.render.engine = "CYCLES"
root = bpy.data.collections.get("MASTER") or bpy.data.collections.new("MASTER")
if root.name not in master.collection.children: master.collection.children.link(root)
for n in BASE_COLLECTIONS + FIRE:
    col = bpy.data.collections.get(n) or bpy.data.collections.new(n)
    if col.name not in root.children: root.children.link(col)

# mundo negro para los videos de antorcha (que no entre la luz de ambiente de la luna)
black = bpy.data.worlds.get("WEB_negro") or bpy.data.worlds.new("WEB_negro")
black.use_nodes = True
bg_node = black.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0, 0, 0, 1); bg_node.inputs[1].default_value = 0.0

# --- guías (no se renderizan) ---
guides = bpy.data.collections.get("GUIAS (no se renderiza)") or bpy.data.collections.new("GUIAS (no se renderiza)")
if guides.name not in master.collection.children: master.collection.children.link(guides)
guides.hide_render = True
def empty(name, loc, size=0.3, kind="PLAIN_AXES", scale=(1, 1, 1)):
    o = bpy.data.objects.get(name) or bpy.data.objects.new(name, None)
    o.empty_display_type, o.empty_display_size, o.location, o.scale = kind, size, loc, scale
    if o.name not in guides.objects: guides.objects.link(o)
    return o
empty("GUIA_muro_25.6x76.8m", (0, 0, WALL_H_M / 2), 1, "CUBE", (WALL_W_M / 2, 0.05, WALL_H_M / 2))
empty("GUIA_franja_celular_4.9m", (0, -0.1, WALL_H_M / 2), 1, "CUBE", (2.4571, 0.05, WALL_H_M / 2))
for tid, x, z in TORCHES:
    empty("GUIA_antorcha_" + tid, (x, 0, z), 0.15, "SPHERE")
for o in list(guides.objects):   # borrar guías de antorchas que ya no están en la lista
    if o.name.startswith("GUIA_antorcha_") and o.name[len("GUIA_antorcha_"):] not in [t[0] for t in TORCHES]:
        bpy.data.objects.remove(o)

def set_view(scene):
    for vt in ("AgX", "Filmic"):
        try: scene.view_settings.view_transform = vt; break
        except TypeError: pass
    scene.view_settings.look = "None"
    scene.display_settings.display_device = "sRGB"

def find_lc(lc, name):
    if lc is None: return None
    if lc.collection.name == name: return lc
    for ch in lc.children:
        r = find_lc(ch, name)
        if r: return r
    return None

def place_camera(cam, cd, kind):
    ortho = kind != "PERSP"
    cd.type = "ORTHO" if ortho else "PERSP"
    if ortho: cam.rotation_euler = (math.radians(90), 0, 0)
    if kind == "WALL_D":
        cd.ortho_scale = WALL_H_M; cam.location = (0, -40, WALL_H_M / 2)
    elif kind == "WALL_M":
        cd.ortho_scale = WALL_H_M; cam.location = (0, -40, WALL_H_M / 2)
    elif kind.startswith("TORCH_"):
        tid = kind[6:]; t = [t for t in TORCHES if t[0] == tid][0]
        cd.ortho_scale = TORCH_SIZE; cam.location = (t[1], -40, t[2])
    elif kind == "GRASS":
        cd.ortho_scale = 25.6; cam.location = (0, -40, -10 + 1.0)    # pasto con la base en Z = -10
    elif kind == "FRAME":
        cd.ortho_scale = 0.74; cam.location = (40, -5, 0.37)          # marco de 60 x 74 cm centrado en X = 40
    elif cam.location.length == 0:
        cam.location, cam.rotation_euler = (0, -60, 2), (math.radians(88), 0, 0)
    cd.clip_end = 500

def set_output(sc, fmt, transparent):
    r = sc.render
    if fmt == "VIDEO":
        r.image_settings.file_format = "FFMPEG"
        try:
            r.ffmpeg.format = "MPEG4"; r.ffmpeg.codec = "H264"
            r.ffmpeg.constant_rate_factor = "MEDIUM"; r.ffmpeg.ffmpeg_preset = "GOOD"
            r.ffmpeg.audio_codec = "NONE"
        except Exception as e:
            print("No pude configurar el video (revisalo a mano en Output):", e)
        r.image_settings.color_mode = "RGB"
    else:
        r.image_settings.file_format = fmt
        r.image_settings.color_mode = "RGBA" if transparent else "RGB"
        if fmt == "PNG": r.image_settings.compression = 90
        else: r.image_settings.quality = 88

for name, w, h, tpl, transparent, fmt, out, cam_kind, cols in ASSETS:
    sc = bpy.data.scenes.get(name) or bpy.data.scenes.new(name)
    if root.name not in sc.collection.children: sc.collection.children.link(root)
    sc.world = black if name.startswith("WEB_antorcha_") else master.world
    r = sc.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
    r.film_transparent = transparent
    set_output(sc, fmt, transparent)
    r.filepath = "//render_web/" + out
    set_view(sc)
    sc.render.fps = 24
    if name.startswith("WEB_antorcha_"): sc.frame_start, sc.frame_end = 1, 48    # 2 s en loop
    elif name == "WEB_niebla":           sc.frame_start, sc.frame_end = 1, 240   # 10 s en loop
    else:                                sc.frame_start, sc.frame_end = 1, 1

    bpy.context.window.scene = sc           # una escena nueva arma sus capas recién al abrirla
    vl = bpy.context.view_layer; vl.update()
    for n in BASE_COLLECTIONS + FIRE:
        lc = find_lc(vl.layer_collection, n)
        if not lc: continue
        mode = cols.get(n)
        lc.exclude = mode is None
        if mode is not None:
            lc.holdout = (mode == "hold"); lc.indirect_only = (mode == "luz")

    cn = name + "_CAM"
    cd = bpy.data.cameras.get(cn) or bpy.data.cameras.new(cn)
    cam = bpy.data.objects.get(cn) or bpy.data.objects.new(cn, cd)
    if cam.name not in sc.collection.objects: sc.collection.objects.link(cam)
    place_camera(cam, cd, cam_kind)
    sc.camera = cam
    path = os.path.join(HERE, tpl)
    cd.show_background_images = True
    if os.path.exists(path):
        img = bpy.data.images.load(path, check_existing=True)
        bg = cd.background_images[0] if cd.background_images else cd.background_images.new()
        bg.image, bg.alpha, bg.display_depth, bg.frame_method = img, 0.8, "FRONT", "FIT"

# escenas de antorchas que ya no están en la lista: se avisan (no se borran solas)
for s_ in bpy.data.scenes:
    if s_.name.startswith("WEB_antorcha_") and s_.name[13:] not in [t[0] for t in TORCHES]:
        print("Esta escena ya no está en TORCHES, podés borrarla:", s_.name)

# antorchas.json para la web (va en la carpeta img/ junto con los videos)
if bpy.data.filepath:
    od = os.path.join(os.path.dirname(bpy.data.filepath), "render_web")
    os.makedirs(od, exist_ok=True)
    with open(os.path.join(od, "antorchas.json"), "w") as f:
        json.dump([{"id": t, "x": x, "z": z, "size": TORCH_SIZE} for t, x, z in TORCHES], f, indent=1)
    print("Escribí render_web/antorchas.json")
else:
    print("Guardá el .blend y volvé a correr el script para que se genere render_web/antorchas.json")

bpy.context.window.scene = master
for area in bpy.context.window.screen.areas:
    if area.type == "VIEW_3D":
        for sp in area.spaces:
            if sp.type == "VIEW_3D": sp.overlay.show_overlays = True
print("Listo. Plantillas desde:", HERE)
