# Blender 4.x — crea una escena por cada asset de la web, lista para renderizar.
# Uso:
#   1. Guardá tu .blend en la misma carpeta que este script y las plantillas PNG (carpeta plantillas-3d).
#   2. En Blender: Scripting > Open > setup_web_assets.py > Run Script.
#   3. Arriba a la derecha, en el selector de escenas, elegís el asset en el que vas a trabajar.
#   4. Mirá por la cámara (Numpad 0): la plantilla aparece de fondo con las zonas marcadas.
#      La plantilla NO sale en el render, es solo una guía.
# Correrlo de nuevo no duplica nada: si la escena ya existe, solo actualiza la configuración.

import bpy, os, math

HERE = bpy.path.abspath("//") or os.path.dirname(os.path.abspath(__file__))

ASSETS = [
    # nombre escena,        ancho, alto, plantilla,                          transparente, formato, salida,              cámara
    ("WEB_banner",          2560, 1440, "01-banner_2560x1440.png",          False, "JPEG", "banner.jpg",      "PERSP"),
    ("WEB_muro",            2560,  300, "02-muro_2560x300.png",             True,  "PNG",  "wall.png",        "ORTHO"),
    ("WEB_textura_fondo",   1024, 1024, "03-textura-fondo_1024x1024.png",   False, "JPEG", "wall-tile.jpg",   "ORTHO"),
    ("WEB_antorcha",         200,  320, "04-antorcha_200x320.png",          True,  "PNG",  "sconce.png",      "ORTHO"),
    ("WEB_pasto",           2560,  200, "05-pasto_2560x200.png",            True,  "PNG",  "grass.png",       "ORTHO"),
    ("WEB_marco",            600,  740, "06-marco_600x740.png",             True,  "PNG",  "frame.png",       "ORTHO"),
    ("WEB_compartir",       1200,  630, "07-compartir_1200x630.png",        False, "JPEG", "og.jpg",          "PERSP"),
    ("WEB_niebla",          1920, 1080, "08-niebla_1920x1080.png",          False, "PNG",  "fog/fog_####.png", "PERSP"),
]

def set_view(scene):
    vs = scene.view_settings
    for vt in ("AgX", "Filmic"):
        try:
            vs.view_transform = vt
            break
        except TypeError:
            pass
    vs.look = "None"
    scene.display_settings.display_device = "sRGB"

for name, w, h, tpl, transparent, fmt, out, cam_type in ASSETS:
    scene = bpy.data.scenes.get(name) or bpy.data.scenes.new(name)
    r = scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
    r.film_transparent = transparent
    r.image_settings.file_format = fmt
    if fmt == "PNG":
        r.image_settings.color_mode = "RGBA" if transparent else "RGB"
        r.image_settings.compression = 90
    else:
        r.image_settings.color_mode = "RGB"
        r.image_settings.quality = 88
    r.filepath = "//render_web/" + out
    set_view(scene)
    if name == "WEB_niebla":
        scene.render.fps = 24
        scene.frame_start, scene.frame_end = 1, 240   # 10 s; el último frame tiene que empalmar con el primero

    cam_name = name + "_CAM"
    cam_data = bpy.data.cameras.get(cam_name) or bpy.data.cameras.new(cam_name)
    cam_data.type = cam_type
    cam_data.sensor_fit = "AUTO"
    if cam_type == "ORTHO":
        cam_data.ortho_scale = max(w, h) / 100.0   # 100 px = 1 m: el ancho de la imagen en metros
    cam = bpy.data.objects.get(cam_name) or bpy.data.objects.new(cam_name, cam_data)
    if cam.name not in scene.collection.objects:
        scene.collection.objects.link(cam)
    if cam_type == "ORTHO":
        cam.location = (0, -10, 0)                  # vista frontal, mirando hacia +Y
        cam.rotation_euler = (math.radians(90), 0, 0)
    elif cam.location.length == 0:
        cam.location = (0, -12, 1.6)
        cam.rotation_euler = (math.radians(88), 0, 0)
    scene.camera = cam

    path = os.path.join(HERE, tpl)
    cam_data.show_background_images = True
    if os.path.exists(path):
        img = bpy.data.images.load(path, check_existing=True)
        bg = cam_data.background_images[0] if cam_data.background_images else cam_data.background_images.new()
        bg.image = img
        bg.alpha = 0.8
        bg.display_depth = "FRONT"   # la guía queda por encima del modelo en el visor
        bg.frame_method = "FIT"
    else:
        print("No encontré la plantilla:", path)

print("Listo: escenas WEB_* creadas. Elegí una en el selector de escenas y mirá por la cámara (Numpad 0).")
