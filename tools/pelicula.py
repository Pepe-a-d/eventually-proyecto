#!/usr/bin/env python3
"""Convierte las imágenes (o los clips) en la película y en los fotogramas de la web.

La película son 5 tramos iguales: cuatro piezas que llegan y un tramo final con
el reloj ya montado. De ahí salen los fotogramas en WebP y un manifest.json que
le dice a la página cuántos hay y en qué punto del scroll va cada uno.

Uso:
    python3 tools/pelicula.py --imagenes relleno --relleno      # película de prueba
    python3 tools/pelicula.py --imagenes imagenes               # plan B: solo imágenes
    python3 tools/pelicula.py --master master.mp4               # plan A: vídeo ya unido
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SEGMENTS = 5

# En qué punto del scroll (0-1) llega cada pieza. Entre medias la imagen se
# queda quieta para que dé tiempo a leer el texto.
#   (scroll, tramo de película)  -> tramo 1.0 = ha terminado de llegar la esfera, etc.
TIMELINE = [
    (0.00, 0.0), (0.13, 0.0),
    (0.21, 1.0), (0.32, 1.0),
    (0.40, 2.0), (0.52, 2.0),
    (0.60, 3.0), (0.72, 3.0),
    (0.80, 4.0), (1.00, 5.0),
]


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"ffmpeg falló:\n{proc.stderr[-2500:]}")


def probe(path: Path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries", "format=duration",
         "-of", "json", str(path)], capture_output=True, text=True)
    data = json.loads(out.stdout)
    s = data["streams"][0]
    return int(s["width"]), int(s["height"]), float(data["format"].get("duration") or 0)


# Dónde está el centro del reloj en las imágenes (fracción del ancho y del alto)
# y el radio de la esfera (fracción del ancho). Las piezas caen hacia ese punto.
CENTER = (0.511, 0.492)
DIAL_R = 0.295
# Por pieza: cuánto «baja» (zoom inicial), si se respeta el interior de la esfera,
# y cuánto se redondea el recorte (píxeles; solo para piezas macizas como la esfera).
PIECES = [(0.16, False, 26), (0.24, False, 0), (0.28, False, 0), (0.13, True, 0)]
MASTER_W = 1080
FPS = 20


def find_stills(folder: Path):
    stills = []
    for i in range(1, SEGMENTS + 1):
        found = [f for stem in (f"{i:02d}", str(i)) for ext in ("png", "jpg", "jpeg", "webp")
                 if (f := folder / f"{stem}.{ext}").exists()]
        if not found:
            sys.exit(f"Falta la imagen {i} en {folder}")
        stills.append(found[0])
    return stills


def film_from_stills(folder: Path, master: Path, seconds: float):
    """Cada tramo: la pieza nueva baja desde la cámara, desenfocada, y se posa.

    La pieza nueva se saca comparando una imagen con la siguiente: lo que cambia
    es la pieza. Solo esa zona se anima; el resto de la imagen no se toca.
    """
    stills = find_stills(folder)
    w0, h0, _ = probe(stills[0])
    W = min(MASTER_W, w0 - w0 % 2)
    H = int(W * h0 / w0) // 2 * 2
    cx, cy = CENTER
    T = seconds

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        norm = []
        for i, s in enumerate(stills):
            out = tmp / f"s{i}.png"
            run(["ffmpeg", "-y", "-i", str(s), "-vf",
                 f"scale={W}:-2:flags=lanczos,crop={W}:{H}:0:0,setsar=1,"
                 # aclara un poco el papel sin quemar la esfera
                 "curves=all='0/0 0.5/0.5 0.9/0.932 1/1'", "-frames:v", "1", str(out)])
            norm.append(out)

        segs = []
        debug = ROOT / "relleno" / "recortes"
        debug.mkdir(parents=True, exist_ok=True)
        for i, (zoom, keep_dial, rounding) in enumerate(PIECES):
            a, b, mask = norm[i], norm[i + 1], tmp / f"m{i}.png"

            # --- recorte de la pieza nueva ---
            # «fino» sigue el contorno exacto de lo que cambia; «grueso» es una mancha
            # holgada que solo sirve para descartar ruido suelto y rellenar el interior.
            hole = (f",geq=lum='lum(X,Y)*clip((hypot(X-{W * cx:.1f},Y-{H * cy:.1f})-{W * DIAL_R:.1f})/3,0,1)'"
                    if keep_dial else "")
            corners = ",".join(f"floodfill=x={x}:y={y}:s0=0:d0=128"
                               for x, y in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)))
            # La pieza es la mancha que toca estos puntos; lo demás (retoques sueltos
            # que la IA hizo en el borde o en la letra) se descarta.
            seeds = [(cx, 0.002), (cx, 0.998)] if keep_dial else [(0.504, cy), (cx, cy)]
            pick = ",".join(f"floodfill=x={int(W * x)}:y={int(H * y)}:s0=255:d0=200" for x, y in seeds)
            # En la caja, un eslabón pulido es tan blanco como el papel: se cierra en vertical.
            bridge = (f",dilation=coordinates=66{',dilation=coordinates=66' * 49}"
                      f",erosion=coordinates=66{',erosion=coordinates=66' * 49}" if keep_dial else "")
            solid = (f",{','.join(['dilation'] * rounding)},{','.join(['erosion'] * rounding)}"
                     if rounding else "")
            run(["ffmpeg", "-y", "-i", str(a), "-i", str(b), "-filter_complex",
                 "[0:v]format=gbrp[a];[1:v]format=gbrp[b];"
                 "[a][b]blend=all_mode=difference,format=gray,split[d1][d2];"
                 "[d2]gblur=sigma=4,lut=y='if(gt(val,14),255,0)',gblur=sigma=10,"
                 "lut=y='if(gt(val,40),255,0)',split[co1][co2];"
                 "[d1]gblur=sigma=1.2,lut=y='if(gt(val,22),255,0)'[ti];"
                 "[ti][co1]blend=all_mode=darken[tight];"
                 f"[co2]{','.join(['erosion'] * 16)}[core];"
                 f"[tight][core]blend=all_mode=lighten,{','.join(['dilation'] * 3)},{','.join(['erosion'] * 3)}"
                 f"{bridge}{solid},"
                 # rellena los huecos interiores: todo lo que no toca el borde de la imagen
                 f"{corners},lut=y='if(eq(val,128),0,255)',"
                 f"{pick},lut=y='if(eq(val,200),255,0)'{hole},"
                 # suaviza el contorno y le da un borde de un píxel
                 f"gblur=sigma={5 if rounding else 1.6},lut=y='if(gt(val,115),255,0)',gblur=sigma=1.1",
                 "-frames:v", "1", str(mask)])
            shutil.copy(mask, debug / f"recorte{i + 1}.png")

            seg = tmp / f"seg{i}.mp4"
            graph = (
                f"[0:v]format=gbrp[a];"
                f"[1:v]format=gbrp,split[b1][b3];"
                f"[2:v]format=gray[m];"
                # la pieza recortada aparece poco a poco…
                f"[b1][m]alphamerge,fade=t=in:st=0:d={T * 0.45}:alpha=1,premultiply=inplace=1,split[c1][c2];"
                # …desenfocada al principio (el desenfoque se hace sobre el recorte, así
                # no arrastra color de la esfera) y nítida al posarse…
                f"[c2]gblur=sigma=14[cb];"
                f"[c1][cb]blend=all_expr='A+(B-A)*pow(clip(1-T/{T},0,1),2)',"
                # …y más grande al principio, como si bajara desde la cámara.
                f"scale=w='2*trunc({W}*(1+{zoom}*pow(clip(1-t/{T},0,1),3))/2)'"
                f":h='2*trunc({H}*(1+{zoom}*pow(clip(1-t/{T},0,1),3))/2)':eval=frame[bz];"
                f"[a][bz]overlay=x='(W-w)*{cx}':y='(H-h)*{cy}':eval=frame:alpha=premultiplied,format=gbrp[comp];"
                # al final funde con la imagen exacta, para que el siguiente tramo empalme
                f"[comp][b3]blend=all_expr='A+(B-A)*clip((T/{T}-0.8)/0.2,0,1)',format=yuv420p[out]"
            )
            cmd = ["ffmpeg", "-y"]
            for src in (a, b, mask):
                cmd += ["-loop", "1", "-t", str(T), "-r", str(FPS), "-i", str(src)]
            cmd += ["-filter_complex", graph, "-map", "[out]", "-t", str(T), "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", "-an", str(seg)]
            run(cmd)
            segs.append(seg)

        # Tramo final: el reloj ya montado, con un acercamiento muy lento.
        seg = tmp / "seg4.mp4"
        z = f"(1+0.05*clip(t/{T},0,1))"
        run(["ffmpeg", "-y", "-loop", "1", "-t", str(T), "-r", str(FPS), "-i", str(norm[-1]),
             "-filter_complex",
             f"[0:v]scale={W * 2}:{H * 2}:flags=bicubic,split[base][top];"
             f"[top]scale=w='2*trunc({W * 2}*{z}/2)':h='2*trunc({H * 2}*{z}/2)':eval=frame:flags=bicubic[zoomed];"
             f"[base][zoomed]overlay=x='(W-w)*{cx}':y='(H-h)*{cy}':eval=frame,"
             f"scale={W}:{H}:flags=lanczos,format=yuv420p[out]",
             "-map", "[out]", "-t", str(T), "-r", str(FPS), "-c:v", "libx264", "-crf", "10", "-an", str(seg)])
        segs.append(seg)

        lst = tmp / "list.txt"
        lst.write_text("".join(f"file '{s}'\n" for s in segs))
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(master)])


def extract(master: Path, outdir: Path, fps: float, width: int, quality: int):
    """Saca los fotogramas en PNG a una carpeta temporal y los pasa a WebP con cwebp
    (el ffmpeg de este Mac no trae codificador WebP)."""
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        run(["ffmpeg", "-y", "-i", str(master),
             "-vf", f"fps={fps},scale={width}:-2:flags=lanczos,unsharp=5:5:0.5:3:3:0.2",
             "-compression_level", "1", str(Path(tmp) / "f_%04d.png")])

        def encode(png: Path):
            subprocess.run(["cwebp", "-quiet", "-q", str(quality), "-m", "6", "-sharp_yuv",
                            str(png), "-o", str(outdir / (png.stem + ".webp"))], check=True)

        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(encode, sorted(Path(tmp).glob("f_*.png"))))
    return sorted(outdir.glob("f_*.webp"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imagenes", help="carpeta con 01.png … 05.png")
    ap.add_argument("--master", help="vídeo ya unido (5 tramos iguales)")
    ap.add_argument("--relleno", action="store_true", help="marca la web como de prueba")
    ap.add_argument("--por-tramo", type=int, default=24, help="fotogramas por tramo")
    ap.add_argument("--calidad", type=int, default=76, help="calidad WebP del tamaño grande")
    ap.add_argument("--calidad-movil", type=int, default=70)
    args = ap.parse_args()

    master = ROOT / "master.mp4"
    if args.imagenes:
        film_from_stills(ROOT / args.imagenes, master, seconds=1.5)
    elif args.master:
        if Path(args.master).resolve() != master.resolve():
            shutil.copy(args.master, master)
    if not master.exists():
        sys.exit("No hay master.mp4: pasa --imagenes o --master")

    w, h, dur = probe(master)
    fps = args.por_tramo * SEGMENTS / dur
    print(f"película {w}x{h}, {dur:.1f} s -> {args.por_tramo} fotogramas por tramo")

    frames_dir = SITE / "frames"
    tiers = []
    for name, width, minvw in (("d", 1080, 768), ("m", 720, 0)):
        width = min(width, w)
        if any(t["width"] == width for t in tiers):
            continue                      # la fuente es pequeña: un solo tamaño basta
        files = extract(master, frames_dir / name, fps, width,
                        args.calidad if name == "d" else args.calidad_movil)
        tiers.append({"name": name, "path": f"frames/{name}", "pattern": "f_%04d.webp",
                      "width": width, "height": round(width * h / w / 2) * 2,
                      "minViewportWidth": minvw, "bytes": sum(f.stat().st_size for f in files),
                      "count": len(files)})
    for stale in ("d", "m"):
        if not any(t["name"] == stale for t in tiers) and (frames_dir / stale).exists():
            shutil.rmtree(frames_dir / stale)
    tiers[-1]["minViewportWidth"] = 0

    counts = {t["count"] for t in tiers}
    if len(counts) != 1:
        sys.exit(f"Los tamaños no tienen los mismos fotogramas: {counts}")
    count = counts.pop()
    per = count / SEGMENTS
    timeline = [[p, min(count - 1, round(seg * per))] for p, seg in TIMELINE]

    # Póster: el reloj terminado (final del cuarto tramo).
    poster_t = dur * 4 / SEGMENTS + 0.02
    run(["ffmpeg", "-y", "-ss", f"{poster_t:.3f}", "-i", str(master), "-frames:v", "1",
         "-q:v", "3", str(SITE / "poster.jpg")])

    manifest = {
        "version": int(time.time()),      # cambia en cada montaje: renueva la copia sin conexión
        "placeholder": bool(args.relleno),
        "frameCount": count,
        "aspect": w / h,
        "timeline": timeline,
        "poster": "poster.jpg",
        "tiers": [{k: v for k, v in t.items() if k != "count"} for t in tiers],
    }
    (frames_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"\n{'tamaño':<8}{'fotogramas':>12}{'cada uno':>12}{'total':>12}")
    for t in tiers:
        print(f"{t['name']:<8}{count:>12}{t['bytes'] / count / 1024:>10.0f} KB{t['bytes'] / 1048576:>9.2f} MB")
    print(f"\nmanifest: {frames_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
