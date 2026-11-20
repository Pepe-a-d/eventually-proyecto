# Resumen de las sesiones del Mac

Escrito el 20 de noviembre de 2026. Recoge lo hecho y decidido en el Mac entre el 19 y el 20 de noviembre, para poder seguir desde el PC sin perder nada. Lo escribe Claude a partir de las conversaciones; las conversaciones en bruto no están subidas.

## 1. El reloj

- **Nombre:** Eventually, con la línea «Late Edition · 1 of 1». Lo eligió Pepe el 19 de noviembre.
- **Para quién:** de Pepe para Pablo. La tarjeta dice «diciembre de 2026». **La fecha exacta de entrega no está dicha.**
- **Piezas:** caja de acero de 40 mm con brazalete integrado, cristal de zafiro, esfera blanca con números azules desordenados y la frase «Who cares, I'm already late», agujas de acero, segundero azul, movimiento automático Seiko NH36.
- **Estado:** no consta que el reloj esté montado. Las fotos de las piezas están en `referencias/`.
- **Medidas que faltan** y de las que depende la caja: contorno interior del brazalete cerrado (con una tira de papel), ancho con corona, ancho y grosor del brazalete, ancho por fuera de las asas, tipo y grosor del cierre.

## 2. La web

**Terminada y publicada** en <https://pepe-a-d.github.io/eventually/>. Repositorio `Pepe-a-d/eventually`, que es la carpeta `site/`.

- Se abre desde el QR de la tarjeta o desde la etiqueta NFC de la caja: está pensada primero para el móvil (película en vertical, 9:16).
- **Idea:** el reloj se monta solo, pieza a pieza, sobre papel blanco, visto desde arriba. La película avanza con el scroll.
- **Cómo está hecha:** HTML, CSS y JS sin dependencias. Los fotogramas salen de las cinco imágenes de `imagenes/` con `tools/pelicula.py`, que anima cada pieza cayendo desde la cámara. No hicieron falta vídeos. Pesa 3,5 MB en móvil y 7,2 MB en escritorio.
- **Qué tiene:** textos en español (la frase de la esfera, en inglés), reloj real en hora al final, la frase de la esfera que se escribe con el scroll, una nota a mano de Pepe, el contador «Llevas N minutos aquí», el botón «Apagar la luz» y copia sin conexión.
- **Estilo:** minimalista. Letra de la esfera (Reenie Beanie) en azul. A Pepe le gusta mucho esa letra.
- Los puntos del scroll donde llega cada pieza están en `TIMELINE` de `tools/pelicula.py` y los rangos de texto en `data-range` de `site/index.html`. Van emparejados: si se toca uno, se toca el otro.

**Falta:**

- Probarla en un móvil real.
- Grabar la etiqueta NFC con la dirección de la web.
- Decidir si se añade la pista de apertura de la caja («la aguja abre la caja: adelanta la hora») y el aviso del imán. Está propuesto y **sin contestar**.

## 3. La tarjeta de autenticidad

**Terminada, sin imprimir** (que conste).

- 85 × 55 mm, anverso y reverso, con las tipografías y el azul de la web. Diseñada en Figma: <https://www.figma.com/design/zTqZch5frY3qcnWlQMConH>. El QR lo colocó Pepe a mano.
- En `tarjeta/`:
  - `eventually-tarjeta-copisteria.pdf`: dos páginas, con 3 mm de sangrado y marcas de corte.
  - `eventually-tarjeta-casa-A4.pdf`: una hoja para recortar, doblar y pegar.
  - `per-la-copisteria.txt`: la nota en italiano para la copistería.
- `tools/imprimir.swift` rehace los dos PDF de imprimir a partir de los de Figma. Solo funciona en Mac.
- El QR está en `qr/`, en azul y en negro. Los dos comprobados.

## 4. La caja

Repositorio `Pepe-a-d/eventually-caja`. La modela la sesión de Claude del PC con Fusion; la sesión del Mac revisa cada versión y escribe un contra-reporte.

### La idea

Funda de campana con la frase y la etiqueta NFC. Dentro, una caja que se abre por delante. La **aguja azul es la llave**: lleva un imán que arrastra un rotor escondido tras el panel. Dentro, el reloj va en una pinza sobre una peana que sale deslizando y sirve de expositor. La tarjeta va detrás del panel.

### Lo que está decidido

- **Solo 14 imanes** de 5 × 1,6 mm. **Sin piezas de acero.**
- Impresora **Bambu Lab X1 Carbon con AMS**. Etiqueta NFC de 25 mm. Filamento mármol blanco para la funda.
- Sin palabras en la tapa. Sin pestaña de rasgar.
- Se cierra con la aguja puesta; el cierre de un empujón es opcional.
- **Ninguna caja entera sin medir antes el reloj.**

### Por dónde va

| Versión | Qué pasó |
| --- | --- |
| v2 | Caja-expositor. Contra-reporte: el reloj no se podía montar, cerrar era torpe, sin apertura de emergencia |
| v3 | Funda de campana, 8 imanes. Contra-reporte: el cierre de un empujón se acuña, la pinza estaba dibujada con una forma falsa |
| v4 | Rotor con tope, peana corredera, pinza a medida. Contra-reporte: 2 fallos graves y 8 importantes |
| v4.1 | Parche. Arregla los 2 graves (comprobado). Contra-reporte: 5 fallos importantes, ninguno grave |

Todo el detalle está en `caja/contra-reporte-v2.md`, `-v3.md`, `-v4.md` y `-v4.1.md`. Los cálculos que hay detrás, en `caja/calculos-mac/`.

### Lo que toca ahora

1. **Imprimir P0, P1 y el aro de P2** con los ficheros de `caja/probetas-v4/`. La tapa trasera de P1, sujeta con cinta.
2. **Medir el reloj** (las medidas del apartado 1).
3. Con lo que salga, un **segundo parche pequeño** de seis cambios. Están en el apartado 7 de `contra-reporte-v4.1.md`:
   - Clip de la tapa trasera que retenga en la dirección en que sale.
   - Rebajar el brazo entero del rotor, no solo las puntas.
   - Retén de la funda más suave y sin aprieto permanente; probarlo con la funda entera.
   - Lengüeta de la peana de 1,5 mm de grosor.
   - Acortar la ranura de emergencia y redondear sus extremos.
   - Empezar 8° antes el canal del taco.
4. **No hacer otro reporte en papel** antes de tener P1 y P2 impresas. Van seis rondas sin imprimir nada.

Los imanes: 8 en la caja, 2 en la aguja de repuesto, quedan 4.

## 5. Preguntas sin contestar

1. ¿Qué día se entrega?
2. ¿Está el reloj montado? Si lo está, faltan las medidas.
3. ¿Cómo quieres que la caja salga de la funda? Que se quede en la mesa al levantar la funda, que aguante colgada, o las dos cosas con dos medias lunas para los dedos.
4. ¿La aguja lleva pomo?
5. ¿Se añaden a la web la pista de apertura y el aviso del imán?

## 6. Cómo trabajamos

- En español, claro para alguien no técnico. Cada cifra dice de dónde sale (del modelo, medida, calculada, estimada).
- Pepe quiere que le digan lo que está mal, no que todo está bien.
- En la caja, nada de commit ni push sin que Pepe lo pida.
- **Lección de la v4.1:** al pedir un cambio de una pieza, decir siempre en qué dirección sujeta y con qué fuerza, no solo la forma. Tres de los cinco fallos del parche salieron de frases copiadas al pie de la letra.

## 7. Ideas propuestas que no se eligieron

Números de capítulo a mano, subrayados a boli, saludo al cargar, plegar las instrucciones. En la caja: palabras en la tapa («pronto/tarde») y pestaña de rasgar, las dos descartadas.
