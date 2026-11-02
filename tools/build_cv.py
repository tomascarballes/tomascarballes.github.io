#!/usr/bin/env python3
"""Build Tomas Carballes's CV (HTML + PDF) in English and Spanish.

Public (web) version, saved in cv/:      python3 tools/build_cv.py
Full version with phone, saved outside:  python3 tools/build_cv.py --phone "11 3009 1539" --area "Villa Ortuzar, Argentina" --out /some/private/folder

The phone number is never stored in this repo: it is only passed on the command line.
Edit the CV content in the DATA dict below.
"""
import argparse, html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

DATA = {
  "en": {
    "lang": "en", "role": "3D Generalist",
    "h_about": "About me", "h_contact": "Contact", "h_tools": "Tools", "h_hard": "Hard Skills",
    "h_soft": "Soft Skills", "h_lang": "Languages", "h_exp": "Experience", "h_edu": "Education",
    "location_public": "Buenos Aires, Argentina",
    "about": "I am a Multimedia Design graduate from ISEC. I consider myself a collaborative and communicative person, as I believe that effective dialogue is key to success in any work environment. I am passionate about art and the multimedia world, with a particular focus on the 3D industry and the creation of immersive worlds through detailed lorebuilding. My professional objective is to join a creative production team and contribute to the development of video games, film, or high-end advertising projects.",
    "hard": [
      ("3D Workflow", "High to Low poly Workflow, Digital Sculpting & Retopology, Hard Surface Modeling, UV Unwrapping & Optimization"),
      ("Surfacing & Environment", "PBR Texturing, Environment Set Dressing, Procedural Texturing"),
      ("Lighting & Rendering", "Cinematic Lighting, Shading & Global Illumination"),
      ("Post-production", "Video Composition & Color Grading, Asset Integration"),
    ],
    "soft": ["Quick Learner", "Problem-Solving", "Attention to Detail", "Adaptability", "Effective Communication / Teamwork", "Proactive self-learner"],
    "langs": [("English", "Advanced"), ("Spanish", "Native")],
    "exp": [
      {"icon": "assets/itdesarrollos.jpg", "role": "Web & Graphic Designer", "where": "IT Desarrollos SRL", "when": "2023 - Present", "items": [
        ("UI Design & Prototyping", "Created <b>high-fidelity interfaces</b> and <b>interactive prototypes</b> in <b>Figma</b>."),
        ("Cross-team Collaboration", "Partnered with <b>multidisciplinary teams</b> to ensure <b>design consistency</b> and <b>efficient project delivery</b>."),
        ("Brand Identity", "Developed and maintained the <b>corporate visual system</b> across all <b>digital assets</b>."),
        ("Visual Assets", "Designed <b>complex graphics</b> and compositions using <b>Photoshop</b> and <b>Illustrator</b>."),
      ]},
      {"icon": "assets/astros.jpg", "role": "Lighting & Render Director / 3D Artist", "where": "\"Astros de Papel\" (Short Film)", "when": "2023 - 2025", "items": [
        ("3D Modeling & Texturing", "Developed <b>high-quality assets</b> and environments using <b>Blender</b>."),
        ("Lighting & Shading", "<b>Co-developed</b> the <b>master lighting shader</b> and <b>visual style</b> with the directing team."),
        ("Rendering Pipeline", "<b>Designed and managed</b> the <b>technical workflow</b> to <b>optimize rendering times</b> for the production team."),
      ]},
      {"icon": "F", "role": "Freelance 3D Artist", "where": "", "when": "2022 - 2024", "items": [
        ("3D Prop & Environment Modeling", "Created <b>high-quality assets</b> and environments with a focus on <b>visual storytelling</b>."),
        ("PBR Texturing & Shading", "Applied <b>advanced PBR workflows</b> and material adjustments to achieve <b>photorealistic results</b> in <b>Blender</b>."),
        ("Asset Optimization", "Executed <b>Retopology and UV Unwrapping</b> to ensure <b>clean geometry</b> and <b>efficient rendering</b>."),
        ("Final Rendering", "Produced <b>high-resolution</b> stills and sequences, managing <b>lighting and composition</b> for portfolio-ready projects."),
      ]},
      {"icon": "P", "role": "Graphic Designer", "where": "Pristine Luxury Camps", "when": "2022 - 2023", "items": [
        ("Brand Identity", "Developed the <b>official brand manual</b> and <b>technical guidelines</b> for <b>visual consistency</b>."),
        ("Marketing & Social Media", "Designed <b>high-end brochures</b>, flyers, and <b>digital assets</b> using <b>Photoshop</b> and <b>Illustrator</b>."),
        ("Team Synergy", "Aligned <b>visual production</b> with <b>marketing strategies</b> through <b>cross-team collaboration</b>."),
      ]},
    ],
    "edu": [
      ("Multimedia Design", "March 2020 / 2023", "ISEC (South American Institute for Communication Studies)"),
      ("Video Game Design", "2017 / 2019", "Da Vinci First School of Multimedia Art"),
      ("Graphic Design", "2017", "University of Buenos Aires"),
      ("Graphic & Industrial Design Technician", "2012 / 2016", "ORT Technical School"),
    ],
  },
  "es": {
    "lang": "es", "role": "Generalista 3D",
    "h_about": "Sobre mí", "h_contact": "Contacto", "h_tools": "Herramientas", "h_hard": "Habilidades Técnicas",
    "h_soft": "Habilidades personales", "h_lang": "Idiomas", "h_exp": "Experiencia Laboral", "h_edu": "Educación",
    "location_public": "Buenos Aires, Argentina",
    "about": "Soy egresado en Diseño Multimedia por el ISEC. Me considero una persona colaborativa y comunicativa, ya que creo que el diálogo efectivo es fundamental para el éxito en cualquier entorno laboral. Me apasiona el arte y el mundo multimedia, con un enfoque particular en la industria 3D y la creación de mundos inmersivos a través de un detallado lorebuilding. Mi objetivo profesional es integrarme a un equipo de producción creativa y contribuir al desarrollo de videojuegos, cine o proyectos publicitarios de alto nivel.",
    "hard": [
      ("Flujo 3D", "Workflow High to Low poly, Escultura Digital y Retopología, Modelado Hard Surface, UV Unwrapping y Optimización"),
      ("Surfacing & Environment", "Texturizado PBR, Environment Set Dressing, Texturizado Procedural"),
      ("Lighting & Rendering", "Iluminación Cinematográfica, Shading e Iluminación Global"),
      ("Post-producción", "Composición de Video y Color Grading, Integración de Assets"),
    ],
    "soft": ["Aprendizaje rápido", "Resolución de problemas", "Atención al detalle", "Adaptabilidad", "Comunicación efectiva / Trabajo en equipo", "Aprendizaje proactivo y autónomo"],
    "langs": [("Inglés", "Avanzado"), ("Español", "Nativo")],
    "exp": [
      {"icon": "assets/itdesarrollos.jpg", "role": "Diseñador Web y Gráfico", "where": "IT Desarrollos SRL", "when": "2023 - Presente", "items": [
        ("Diseño UI y Prototipado", "Creación de <b>interfaces de alta fidelidad</b> y <b>prototipos interactivos</b> en <b>Figma</b>."),
        ("Colaboración Interdisciplinaria", "Trabajo conjunto con <b>equipos multidisciplinarios</b> para asegurar la <b>consistencia del diseño</b> y la <b>entrega eficiente</b> de proyectos."),
        ("Identidad de Marca", "Desarrollo y mantenimiento del <b>sistema visual corporativo</b> en todos los <b>activos digitales</b>."),
        ("Activos Visuales", "Diseño de <b>gráficos y composiciones complejas</b> utilizando <b>Photoshop</b> e <b>Illustrator</b>."),
      ]},
      {"icon": "assets/astros.jpg", "role": "Director de Iluminación y Render / Artista 3D", "where": "\"Astros de Papel\" (Cortometraje)", "when": "2023 - 2025", "items": [
        ("Modelado y Texturizado 3D", "Desarrollo de <b>assets y entornos de alta calidad</b> en <b>Blender</b>."),
        ("Iluminación y Shading", "<b>Codesarrollo</b> del <b>shader maestro de iluminación</b> y el <b>estilo visual</b> junto al equipo de dirección."),
        ("Pipeline de Renderizado", "<b>Diseño y gestión</b> del <b>flujo de trabajo técnico</b> para <b>optimizar los tiempos de renderizado</b> del equipo de producción."),
      ]},
      {"icon": "F", "role": "Artista 3D Freelance", "where": "", "when": "2022 - 2024", "items": [
        ("Modelado de Props y Entornos 3D", "Creación de <b>assets y entornos de alta calidad</b> con enfoque en <b>narrativa visual</b>."),
        ("Texturizado PBR y Shading", "Aplicación de <b>flujos de trabajo PBR avanzados</b> y ajuste de materiales para lograr <b>resultados fotorrealistas</b> en <b>Blender</b>."),
        ("Optimización de Assets", "Ejecución de <b>retopología y desplegado de UV</b> para garantizar una <b>geometría limpia</b> y un <b>renderizado eficiente</b>."),
        ("Renderizado Final", "Producción de <b>imágenes estáticas y secuencias de alta resolución</b>, gestionando la <b>iluminación y composición</b> para proyectos de portafolio."),
      ]},
      {"icon": "P", "role": "Diseñador Gráfico", "where": "Pristine Luxury Camps", "when": "2022 - 2023", "items": [
        ("Identidad de Marca", "Creación del <b>manual de marca oficial</b> y las <b>pautas técnicas</b> para la <b>consistencia visual</b>."),
        ("Marketing y Redes Sociales", "Diseño de <b>folletos de alta gama</b>, flyers y <b>activos digitales</b> con <b>Photoshop</b> e <b>Illustrator</b>."),
        ("Sinergia de Equipo", "Alineación de la <b>producción visual</b> con las <b>estrategias de marketing</b> mediante la <b>colaboración entre equipos</b>."),
      ]},
    ],
    "edu": [
      ("Diseño Multimedia", "2020 / 2023", "ISEC (Instituto Sudamericano para la Enseñanza de la Comunicación)"),
      ("Diseño de Videojuegos", "2017 / 2019", "Escuela Da Vinci de Arte Multimedial"),
      ("Diseño Gráfico", "2017", "Universidad de Buenos Aires (UBA)"),
      ("Técnico en Diseño Gráfico y Diseño Industrial", "2012 / 2016", "Escuelas Técnicas ORT"),
    ],
  },
}

TOOLS = ["Blender", "Adobe Substance 3D Painter", "ZBrush", "Adobe Substance 3D Designer", "Adobe Photoshop",
         "Adobe Illustrator", "Autodesk Maya", "Autodesk 3ds Max", "Marmoset Toolbag", "Figma",
         "Adobe After Effects", "Adobe Premiere", "Bootstrap", "CSS", "HTML"]
LINKS = [("assets/artstation.jpg", "ArtStation", "tomascarballes.artstation.com", "https://www.artstation.com/tomascarballes"),
         ("assets/behance.jpg", "Behance", "behance.net/tomascarballes", "https://behance.net/tomascarballes"),
         ("assets/linkedin.jpg", "LinkedIn", "linkedin.com/in/tomas-carballes", "https://linkedin.com/in/tomas-carballes")]
EMAIL = "tomaspcarballes@gmail.com"

CSS = """
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff}
body{font:400 8.2pt/1.32 "Inter",system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:#1f1d5c;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;margin:0 auto;padding:9mm 11mm 7mm;position:relative;overflow:hidden;background:#fff}
.page::before{content:"";position:absolute;left:-40mm;top:-40mm;width:150mm;height:110mm;background:radial-gradient(closest-side,rgba(150,120,255,.28),rgba(150,120,255,0));pointer-events:none}
a{color:inherit}
h1{font:700 27pt/1.02 "Inter",system-ui,Arial,sans-serif;margin:0;color:#1a1670;letter-spacing:-.01em}
.role{font:700 15pt/1.1 "Inter",system-ui,Arial,sans-serif;color:#1a1670;margin-top:3mm}
h2{font:600 10.5pt/1.2 "Inter",system-ui,Arial,sans-serif;color:#1a1670;margin:0 0 1.6mm}
.top{display:grid;grid-template-columns:34mm 1fr 72mm;gap:8mm;align-items:center;position:relative}
.photo{width:34mm;height:34mm;border-radius:5mm;object-fit:cover;box-shadow:0 2mm 6mm rgba(60,40,160,.18)}
.links{display:grid;gap:2.6mm}
.link{display:grid;grid-template-columns:11mm 1fr;gap:4mm;align-items:center}
.link img{width:10mm;height:10mm;border-radius:2mm;box-shadow:0 1mm 2.5mm rgba(0,0,0,.18)}
.link b{display:block;font-size:10pt;font-weight:600}
.link a{text-decoration:underline;font-size:8.8pt}
.mid{display:grid;grid-template-columns:1fr 72mm;gap:8mm;margin-top:4.5mm;position:relative}
.about p{margin:0}
.contact .row{display:flex;justify-content:space-between;gap:4mm;flex-wrap:wrap}
.contact p{margin:0 0 2mm}
.body{display:grid;grid-template-columns:48mm 1fr;gap:7mm;margin-top:4mm}
.side ul{margin:0 0 3.5mm;padding-left:4mm}
.side li{margin:0 0 .2mm}
.side .hs li b{font-weight:600}
.side .hs li span{display:block}
.langs li{display:grid;grid-template-columns:24mm 1fr}
.job{display:grid;grid-template-columns:10mm 1fr;gap:3mm;margin-bottom:2.6mm}
.job .ic{width:9.5mm;height:9.5mm;border-radius:2mm;object-fit:cover;box-shadow:0 1mm 2.5mm rgba(0,0,0,.2);display:grid;place-items:center;font:800 15pt "Inter",Arial,sans-serif}
.job .ic.F{background:#141070;color:#fff}
.job .ic.P{background:#f3f2f7;color:#1a1670;font-size:12pt}
.job .head{font-size:8.9pt;margin-bottom:.8mm}
.job .head b{font-weight:600}
.job ul{margin:0;padding-left:4.5mm}
.job li{margin:0 0 .3mm}
.job li b{font-weight:600}
.edu{margin:0;padding-left:5mm;list-style:disc}
.edu li{margin:0 0 1.1mm}
.edu b{font-weight:600}
@media screen{body{background:#e9e8f0}.page{margin:8mm auto;height:auto;min-height:297mm;box-shadow:0 4mm 14mm rgba(0,0,0,.18)}}
@media screen and (max-width:820px){.page{width:100%;min-height:0;height:auto;padding:20px 16px}.top,.mid,.body{grid-template-columns:1fr}.photo{width:120px;height:120px}}
"""

def e(t): return html.escape(t, quote=True)

def build(d, phone=None, area=None):
    loc = area or d["location_public"]
    contact_row = f'<a href="mailto:{EMAIL}">{EMAIL}</a>' + (f'<span>{e(phone)}</span>' if phone else "")
    links = "".join(f'<div class="link"><img src="{i}" alt=""><div><b>{n}</b><a href="{u}">{t}</a></div></div>' for i, n, t, u in LINKS)
    tools = "".join(f"<li>{e(t)}</li>" for t in TOOLS)
    hard = "".join(f"<li><b>{e(a)}:</b><span>{e(b)}</span></li>" for a, b in d["hard"])
    soft = "".join(f"<li>{e(s)}</li>" for s in d["soft"])
    langs = "".join(f"<li><span>{e(a)}</span><span>{e(b)}</span></li>" for a, b in d["langs"])
    jobs = ""
    for j in d["exp"]:
        ic = f'<img class="ic" src="{j["icon"]}" alt="">' if j["icon"].startswith("assets/") else f'<div class="ic {j["icon"]}">{j["icon"]}</div>'
        head = f'<b>{e(j["role"])}</b>' + (f' | {e(j["where"])}' if j["where"] else "") + f' | {e(j["when"])}'
        items = "".join(f"<li><b>{e(a)}:</b> {b}</li>" for a, b in j["items"])
        jobs += f'<div class="job">{ic}<div><div class="head">{head}</div><ul>{items}</ul></div></div>'
    edu = "".join(f"<li><b>{e(a)}</b> - {e(b)}<br>{e(c)}</li>" for a, b, c in d["edu"])
    return f"""<!doctype html>
<html lang="{d['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Tomas Carballes · CV</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <section class="top">
    <img class="photo" src="assets/photo.jpg" alt="Tomas Carballes">
    <div><h1>Tomas<br>Carballes</h1><div class="role">{e(d['role'])}</div></div>
    <div class="links">{links}</div>
  </section>
  <section class="mid">
    <div class="about"><h2>{e(d['h_about'])}</h2><p>{e(d['about'])}</p></div>
    <div class="contact"><h2>{e(d['h_contact'])}</h2><p class="row">{contact_row}</p><p>{e(loc)}</p></div>
  </section>
  <section class="body">
    <aside class="side">
      <h2>{e(d['h_tools'])}</h2><ul>{tools}</ul>
      <h2>{e(d['h_hard'])}</h2><ul class="hs">{hard}</ul>
      <h2>{e(d['h_soft'])}</h2><ul>{soft}</ul>
      <h2>{e(d['h_lang'])}</h2><ul class="langs">{langs}</ul>
    </aside>
    <div>
      <h2>{e(d['h_exp'])}</h2>{jobs}
      <h2>{e(d['h_edu'])}</h2><ul class="edu">{edu}</ul>
    </div>
  </section>
</main>
</body>
</html>
"""

def to_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(pathlib.Path(html_path).resolve().as_uri()); pg.wait_for_load_state("networkidle")
        pg.pdf(path=str(pdf_path), width="210mm", height="297mm", print_background=True, prefer_css_page_size=True)
        b.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phone"); ap.add_argument("--area"); ap.add_argument("--out")
    a = ap.parse_args()
    full = bool(a.phone)
    out = pathlib.Path(a.out) if a.out else ROOT / "cv"
    if full and out.resolve().is_relative_to(ROOT):
        raise SystemExit("Full CV (with phone) must be written outside the public repo. Use --out.")
    out.mkdir(parents=True, exist_ok=True)
    if full:  # copy assets next to the private files
        import shutil; shutil.copytree(ROOT / "cv" / "assets", out / "assets", dirs_exist_ok=True)
    for code, name in (("en", "Tomas_Carballes_EN"), ("es", "Tomas_Carballes_ES")):
        h = out / f"{code}.html"
        h.write_text(build(DATA[code], a.phone, a.area), encoding="utf-8")
        to_pdf(h, out / f"{name}.pdf")
        print("built", h, out / f"{name}.pdf")
