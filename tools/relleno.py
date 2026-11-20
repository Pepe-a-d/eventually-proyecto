#!/usr/bin/env python3
"""Dibuja cinco imágenes de RELLENO (esquemáticas) del montaje del reloj.

Sirven solo para construir y probar la web antes de tener las imágenes de
verdad. Sin dependencias: escribe PNG a mano con zlib.

Uso:  python3 tools/relleno.py   ->  relleno/01.png … 05.png
"""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

W, H = 720, 1280
CX, CY = W / 2, H / 2

PAPER = (244, 243, 239)
BLUE = (31, 63, 168)
STEEL = (188, 192, 197)
STEEL_DARK = (150, 155, 162)
STEEL_LIGHT = (214, 217, 221)
BRASS = (201, 164, 92)
WHITE = (251, 251, 248)
SHADOW = (60, 62, 70)


def hex_rows():
    return [bytearray(PAPER * W) for _ in range(H)]


def blend(rows, x, y, color, a):
    if a <= 0 or not (0 <= x < W and 0 <= y < H):
        return
    row = rows[y]
    i = x * 3
    for k in range(3):
        row[i + k] = int(row[i + k] + (color[k] - row[i + k]) * a + 0.5)


def paint(rows, sdf, bbox, color, alpha=1.0, soft=1.0):
    """Rellena donde sdf(x, y) < 0, con borde suavizado de `soft` píxeles."""
    x0, y0, x1, y1 = bbox
    pad = int(soft) + 2
    for y in range(max(0, int(y0) - pad), min(H, int(y1) + pad + 1)):
        for x in range(max(0, int(x0) - pad), min(W, int(x1) + pad + 1)):
            d = sdf(x + 0.5, y + 0.5)
            a = 0.5 - d / soft
            if a > 0:
                blend(rows, x, y, color, alpha * min(a, 1.0))


def disc(rows, cx, cy, r, color, alpha=1.0, soft=1.0):
    paint(rows, lambda x, y: math.hypot(x - cx, y - cy) - r,
          (cx - r, cy - r, cx + r, cy + r), color, alpha, soft)


def capsule(rows, ax, ay, bx, by, r, color, alpha=1.0, soft=1.0):
    dx, dy = bx - ax, by - ay
    ll = dx * dx + dy * dy or 1e-9

    def sdf(x, y):
        t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / ll))
        return math.hypot(x - ax - dx * t, y - ay - dy * t) - r

    paint(rows, sdf, (min(ax, bx) - r, min(ay, by) - r, max(ax, bx) + r, max(ay, by) + r),
          color, alpha, soft)


def rrect(rows, cx, cy, w, h, rad, color, alpha=1.0, soft=1.0):
    hw, hh = w / 2 - rad, h / 2 - rad

    def sdf(x, y):
        qx, qy = abs(x - cx) - hw, abs(y - cy) - hh
        return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - rad

    paint(rows, sdf, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), color, alpha, soft)


def polar(angle_deg, length):
    """Ángulo de reloj: 0 = las 12, sentido horario."""
    a = math.radians(angle_deg)
    return CX + math.sin(a) * length, CY - math.cos(a) * length


# ---------- piezas ----------

def movement(rows):
    disc(rows, CX + 7, CY + 9, 175, SHADOW, 0.16, 16)
    disc(rows, CX, CY, 173, (198, 199, 196))
    disc(rows, CX, CY, 171, (238, 238, 234))        # aro de fecha
    for i in range(31):
        ax, ay = polar(i * 360 / 31, 150)
        bx, by = polar(i * 360 / 31, 162)
        capsule(rows, ax, ay, bx, by, 1.4, (40, 42, 48), 0.8)
    disc(rows, CX, CY, 140, (176, 142, 76))
    disc(rows, CX, CY, 138, BRASS)
    disc(rows, CX - 38, CY - 62, 34, (222, 190, 120))
    disc(rows, CX - 38, CY - 62, 12, (240, 240, 238))
    disc(rows, CX + 58, CY + 30, 44, (214, 182, 112))
    disc(rows, CX - 60, CY + 20, 9, (170, 40, 70))   # rubí
    disc(rows, CX + 52, CY + 74, 8, (170, 40, 70))
    for px, py in ((-20, 96), (70, -70), (-96, -30), (10, -110)):
        disc(rows, CX + px, CY + py, 6, (150, 120, 62))
    disc(rows, CX, CY, 11, (120, 124, 130))
    disc(rows, CX, CY, 6, (232, 233, 235))


def dial(rows):
    r = 194
    disc(rows, CX + 6, CY + 8, r + 1, SHADOW, 0.18, 14)
    disc(rows, CX, CY, r, (212, 212, 207))
    disc(rows, CX, CY, r - 1.5, WHITE)

    def from_photo(px, py):   # coordenadas de la foto de la esfera -> lienzo
        return CX + (px - 655) / 455 * r, CY + (py - 640) / 455 * r

    # la frase: dos renglones de garabato azul
    for (x0, y0, x1, y1, n) in ((390, 378, 650, 380, 9), (375, 458, 815, 455, 15)):
        prev = None
        for i in range(n + 1):
            px = x0 + (x1 - x0) * i / n
            py = y0 + (y1 - y0) * i / n + (14 if i % 2 else -14)
            cur = from_photo(px, py)
            if prev:
                capsule(rows, *prev, *cur, 1.5, BLUE)
            prev = cur
    # los doce números, amontonados abajo
    for px, py in ((830, 660), (910, 720), (1000, 740), (690, 750), (460, 775), (600, 820),
                   (375, 840), (710, 850), (840, 850), (490, 905), (605, 950), (725, 945)):
        x, y = from_photo(px, py)
        capsule(rows, x - 5, y - 9, x + 5, y - 9, 1.5, BLUE)
        capsule(rows, x + 5, y - 9, x - 2, y + 10, 1.5, BLUE)
    disc(rows, CX, CY, 7, (150, 153, 158))


def steel_hands(rows):
    for angle, length, width in ((276, 100, 5.5), (72, 165, 4.2)):
        bx, by = polar(angle, length)
        tx, ty = polar(angle + 180, 22)
        capsule(rows, tx + 3, ty + 4, bx + 3, by + 4, width, SHADOW, 0.18, 5)
        capsule(rows, tx, ty, bx, by, width, (140, 145, 152))
        capsule(rows, tx, ty, bx, by, width - 1.4, (205, 208, 212))
        lx, ly = polar(angle, length * 0.35)
        capsule(rows, lx, ly, *polar(angle, length - 8), width * 0.38, (250, 250, 246))
    disc(rows, CX, CY, 10, (160, 164, 170))


def blue_hand(rows):
    tip = polar(50, 172)
    back = polar(230, 30)
    capsule(rows, back[0] + 3, back[1] + 4, tip[0] + 3, tip[1] + 4, 2, SHADOW, 0.2, 4)
    capsule(rows, *back, *tip, 1.6, BLUE)
    capsule(rows, *polar(230, 30), *polar(230, 62), 6, BLUE)        # contrapeso
    ax, ay = polar(50, 138)
    disc(rows, ax, ay, 9, BLUE)                                    # punta de flecha
    disc(rows, ax, ay, 5.5, WHITE)
    disc(rows, CX, CY, 11, BLUE)
    disc(rows, CX, CY, 2.2, (16, 34, 100))


def case(rows):
    # brazalete
    rrect(rows, CX + 8, CY, 330, H + 80, 6, SHADOW, 0.16, 18)
    rrect(rows, CX, CY, 330, H + 80, 4, STEEL)
    rrect(rows, CX, CY, 150, H + 80, 2, STEEL_LIGHT, 0.55)
    y = -20
    while y < H + 40:
        if abs(y - CY) > 215:
            capsule(rows, CX - 165, y, CX + 165, y, 1.3, STEEL_DARK, 0.9)
        y += 74
    # corona
    rrect(rows, CX + 262, CY, 34, 54, 7, STEEL_DARK)
    rrect(rows, CX + 262, CY, 30, 50, 6, STEEL_LIGHT)
    # caja
    rrect(rows, CX + 8, CY + 10, 504, 472, 120, SHADOW, 0.2, 20)
    rrect(rows, CX, CY, 504, 472, 120, STEEL_DARK)
    rrect(rows, CX, CY, 500, 468, 118, STEEL)
    disc(rows, CX, CY, 226, STEEL_DARK)
    disc(rows, CX, CY, 224, (226, 228, 231))                      # bisel pulido
    disc(rows, CX, CY, 204, (128, 132, 139))


STAGES = {
    "01": (movement,),
    "02": (movement, dial),
    "03": (movement, dial, steel_hands),
    "04": (movement, dial, steel_hands, blue_hand),
    "05": (case, dial, steel_hands, blue_hand),
}


def write_png(path: Path, rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    path.write_bytes(b"\x89PNG\r\n\x1a\n"
                     + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9))
                     + chunk(b"IEND", b""))


def main():
    out = Path(__file__).resolve().parent.parent / "relleno"
    out.mkdir(exist_ok=True)
    for name, parts in STAGES.items():
        rows = hex_rows()
        for part in parts:
            part(rows)
        write_png(out / f"{name}.png", rows)
        print(f"relleno/{name}.png")


if __name__ == "__main__":
    main()
