# Eventually — Late Edition · 1 of 1

Un reloj montado a mano por Pepe para su amigo Pablo, con su web, su tarjeta de autenticidad y su caja impresa en 3D.

Este repositorio guarda **todo lo que no es la web publicada ni la caja**: las fotos de las piezas, las imágenes de la película, los prompts, las herramientas, la tarjeta y el QR. También el resumen de lo hecho en el Mac: [SESION-MAC.md](SESION-MAC.md).

## El proyecto está en tres repositorios

| Repositorio | Qué tiene | Visible |
| --- | --- | --- |
| [`eventually-proyecto`](https://github.com/Pepe-a-d/eventually-proyecto) (este) | Fuentes de la web, tarjeta, QR, fotos del reloj, resumen de la sesión | Público |
| [`eventually`](https://github.com/Pepe-a-d/eventually) | La web publicada: <https://pepe-a-d.github.io/eventually/> | Público |
| [`eventually-caja`](https://github.com/Pepe-a-d/eventually-caja) | La caja: generadores de Fusion, piezas, reportes y contra-reportes | Público |

## Cómo tenerlo todo en el PC

En el Mac las tres cosas viven en la misma carpeta (`~/Watchpage`), con la web en `site/` y la caja en `caja/`. Para montar lo mismo en el PC:

```
git clone https://github.com/Pepe-a-d/eventually-proyecto.git Watchpage
cd Watchpage
git clone https://github.com/Pepe-a-d/eventually.git site
git clone https://github.com/Pepe-a-d/eventually-caja.git caja
```

La caja ya está en el PC, en `C:\Users\pepea\Documents\FusionClaude\WatchBox`: ahí basta con `git pull`. El último paso solo hace falta si quieres también una copia dentro de esta carpeta.

Las carpetas `site/` y `caja/` están en el `.gitignore` de este repositorio: cada una se sube al suyo.

## Qué hay en cada carpeta

| Carpeta o fichero | Qué es |
| --- | --- |
| `SESION-MAC.md` | Resumen de todo lo hecho y decidido en el Mac, y lo que falta |
| `referencias/` | Las fotos de las cinco piezas del reloj, sin marcas de tienda |
| `imagenes/` | Las cinco imágenes definitivas de la película (hechas en Gemini) |
| `storyboard.json` | Guion de la web: planos, textos y estilo |
| `prompts/prompt-pack.md` | Los prompts de las cinco imágenes y los cinco clips |
| `tools/pelicula.py` | Convierte las imágenes en la película y en los fotogramas de la web |
| `tools/relleno.py` | Dibuja imágenes de relleno para probar sin el material real |
| `tools/imprimir.swift` | Prepara la tarjeta para imprimir (solo funciona en Mac) |
| `master.mp4` | La película unida, de la que salen los fotogramas |
| `relleno/` | Las imágenes de relleno. Ya no se usan |
| `tarjeta/` | La tarjeta de autenticidad: PDF para la copistería, PDF para casa, nota en italiano |
| `qr/` | El QR de la web, en azul y en negro |
| `.claude/launch.json` | Servidor de prueba de la web (puerto 4319) |

## Para tocar la web

1. Cambiar lo que haga falta en `site/` (HTML, CSS, JS). Si cambias CSS o JS, sube el `?v=` de `index.html`.
2. Si cambian las imágenes: `python3 tools/pelicula.py --imagenes imagenes`. Necesita `ffmpeg` y `cwebp`.
3. Publicar: dentro de `site/`, `git add -A`, `git commit` y `git push`. GitHub Pages sirve la rama `main` tal cual.
