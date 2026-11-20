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

**Tutorial de la caja (añadido el 20 de noviembre).** Lo hizo la sesión del PC (rama `tutorial-caja`, pull request 1 de `eventually`); la sesión del Mac lo revisó, lo fusionó y lo publicó.

- Es una segunda película movida por el scroll, al final de la página, entre «Por si acaso» y el reloj en hora: cómo se abre la caja en cinco gestos y cómo se cierra. 189 fotogramas en `site/frames/caja/`, código en `site/caja.js` y `site/caja.css`. No se descarga hasta que te acercas.
- Trae también dos notas nuevas en «Por si acaso»: «Si pierdes la aguja» e «Imanes». Con esto quedan puestos la pista de apertura y el aviso del imán.
- Comprobado en el Mac: móvil y escritorio, sin errores, la película del reloj sigue igual, y funciona sin conexión.
- En la portada hay un enlace discreto, «¿Cómo se abre la caja?», que baja directo al tutorial: quien llega con la caja cerrada no tiene que recorrer toda la página. Lo pidió Pepe.
- Al probar la copia sin conexión salió un fallo que ya existía: una dirección con «?algo» podía enseñar una copia vieja de la página. Arreglado en `site/sw.js`.

**Primera visita sin spoiler (añadido el 20 de noviembre, lo pidió Pepe).**

- La primera vez que alguien abre la web en un teléfono solo ve las instrucciones de la caja. No se enseña nada del reloj, y su película ni se descarga.
- El reloj sale de dos maneras: al pulsar «Ya lo tengo», al final de las instrucciones, o en cualquier visita hecha **más de 15 minutos después de la primera**. Recargar antes de ese tiempo no enseña el reloj: el iPhone recarga las pestañas por su cuenta al cambiar de aplicación, y eso lo habría destripado a media apertura.
- La web lo recuerda en cada teléfono por separado. Si se abre en modo privado no puede recordarlo: salen siempre las instrucciones hasta pulsar «Ya lo tengo».
- **Para probar:** la dirección acabada en `?caja` vuelve a la primera visita; acabada en `?reloj` va directa al reloj.
- La decisión está en el script de la cabecera de `site/index.html`; lo que se esconde, al final de `site/caja.css`.
- La vista previa del enlace (la que sale al mandarlo por WhatsApp) enseña la caja cerrada, `site/img/enlace.jpg`, y solo la frase «Llegará. Cuando llegue.». Si la caja cambia a la vista, hay que rehacer también esta imagen.
- Lo que todavía puede destripar: el paso 5 de las instrucciones enseña el maniquí gris del reloj, y el icono que queda si alguien añade la web a la pantalla de inicio es la esfera del reloj.

**Revisión completa (20 de noviembre, la pidió Pepe).**

- Fallo gordo arreglado: con el móvil en horizontal el texto quedaba montado sobre la película y no se leía. Ahora usa la disposición de escritorio (texto a la izquierda, película a la derecha).
- Otros arreglos: un solo color de papel en toda la web (`#ECEEF0`, el de la película); el lema de la portada ya no se parte en pantallas muy estrechas; el enlace de la portada no coge el foco del teclado cuando no se ve; texto alternativo en el reloj en hora; manifiesto sin «Un reloj…».
- Textos: «la caja» es ya solo la caja del regalo (la del reloj pasa a «Por fuera»); en las instrucciones la aguja suelta se llama «la llave», para no confundirla con las agujas del reloj; tutorial sin jerga (frente en vez de panel, soporte en vez de peana, sin nervios, rotor ni pestillos).
- Instrucciones del reloj: se unieron «Si se ha parado» y «Si lo dejas quieto», se avisa de que el primer clic de la corona no hace nada, y entra «Si adelanta o atrasa».
- Ficha: fuera las filas «Nombre» y «Edición», que repetían la portada.
- **No se tocó:** la nota de Pepe a Pablo, la portada, el lema, la frase de la esfera, el reloj en hora y el pie.
- Sin arreglar, a propósito: en un teléfono de 320 px de ancho (muy raro hoy) el nombre roza la foto del movimiento; el icono de la web es la esfera del reloj; en la primera visita la página no tiene título principal para lectores de pantalla.

**Ojo con el tutorial:**

- Las imágenes salen del modelo v4.1 de la caja, que no está impresa. **Si la caja cambia a la vista, hay que rehacer los fotogramas** (medias lunas en la funda, pomo en la aguja, otro tamaño al medir el reloj).
- Dos frases prometen cosas sin probar: que la funda sale con «un tirón suave» y que el panel sale tirando de la aguja. Hay que releerlas con la caja en la mano.
- El reloj del tutorial es un maniquí gris, no el reloj de verdad.
- **El programa que genera los fotogramas no está en GitHub.** Solo lo tiene el PC. Hay que subirlo.

**Falta:**

- Probarla en un móvil real, sobre todo en un iPhone.
- Grabar la etiqueta NFC con la dirección de la web.
- Dar por buenos los textos del tutorial, que son una propuesta de la sesión del PC.
- Dar por buenos los textos de la puerta al reloj («Esto sigue. Luego.» y «Ya lo tengo»), que son una propuesta de la sesión del Mac.

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
5. ¿Valen los textos del tutorial de la caja?

## 6. Cómo trabajamos

- En español, claro para alguien no técnico. Cada cifra dice de dónde sale (del modelo, medida, calculada, estimada).
- Pepe quiere que le digan lo que está mal, no que todo está bien.
- En la caja, nada de commit ni push sin que Pepe lo pida.
- **Lección de la v4.1:** al pedir un cambio de una pieza, decir siempre en qué dirección sujeta y con qué fuerza, no solo la forma. Tres de los cinco fallos del parche salieron de frases copiadas al pie de la letra.

## 7. Ideas propuestas que no se eligieron

Números de capítulo a mano, subrayados a boli, saludo al cargar, plegar las instrucciones. En la caja: palabras en la tapa («pronto/tarde») y pestaña de rasgar, las dos descartadas.
