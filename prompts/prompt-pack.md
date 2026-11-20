# Eventually — paquete de prompts

5 imágenes y después 5 clips de vídeo. La película es una sola idea: **el reloj se monta solo, pieza a pieza, sobre una hoja de papel blanco, visto desde arriba**. La cámara no se mueve nunca; lo único que cambia es que en cada imagen hay una pieza más.

Los prompts van en inglés porque los modelos los siguen mejor. Las instrucciones, en español.

## Cómo se hace (léelo antes de generar nada)

1. **Las imágenes van en orden y de una en una.** Cada imagen es la anterior con una pieza añadida, así que no puedes generarlas todas a la vez: necesitas la 01 para hacer la 02, la 02 para la 03, etc.
2. **En cada paso adjuntas dos cosas**: la imagen que acabas de generar y la foto de la pieza nueva (están en la carpeta `referencias/`). La imagen 01 solo lleva la foto de la pieza.
3. **Hazlas todas en el mismo chat de Gemini** y pide formato vertical 9:16.
4. **No cambies el texto de los prompts.** El bloque final que se repite en todos (el que empieza por «Vertical 9:16 photoreal…») es lo que hace que las cinco parezcan la misma foto. Si lo reescribes, cambia la luz o el papel.
5. **Antes de pasar a la siguiente, mira la lista de «Comprueba»** de cada imagen. Si falla algo, repite esa imagen; no sigas, porque el fallo se arrastra a todas las siguientes.
6. **Guarda las imágenes** en `imagenes/` como `01.png`, `02.png`… y **enséñamelas antes de hacer los vídeos**: los vídeos gastan mucha más cuota y conviene que las imágenes estén bien primero.

---

## Imágenes

### Imagen 01 — el movimiento
*Adjunta: `referencias/2-movimiento.jpg`*

```
Use the attached photo only as a reference for what the object looks like; ignore its background and anything printed over it.

A single round automatic watch movement lying flat, dial side up, exactly like the one in the reference: a white date ring with small black numerals 1 to 31 around the edge, a brass-coloured metal plate in the middle with a few screws and two red jewels, and a small central post. No black plastic holder ring, no winding stem, no crown, nothing else in the frame. The movement is perfectly centred in the frame and its diameter is 48% of the frame width.

Vertical 9:16 photoreal studio product photograph. Background: a seamless sheet of matte white cotton paper with a fine visible grain, filling the whole frame edge to edge. 90mm macro lens, camera locked off directly overhead, perfectly perpendicular top-down view, everything in sharp focus. Soft diffused daylight from the top-left, one short soft shadow falling to the bottom-right, no hard reflections. Clean neutral whites, low contrast, true-to-life colour, no vignette. No watermark, no store logo, no brand name, no extra text, no human hands, no tools.
```

Comprueba: está centrado · se ve desde arriba del todo, sin inclinación · ocupa más o menos la mitad del ancho · el fondo es papel blanco liso · no hay aro negro ni tija suelta.

### Imagen 02 — la esfera
*Adjunta: tu imagen 01 + `referencias/4-esfera.jpg`*

```
Edit the first attached image. Keep the paper, the light, the shadow direction, the framing and the scale exactly as they are.

Place the white watch dial from the second attached image flat on top of the movement, concentric with it, covering it completely. The dial is slightly larger than the movement: its diameter is 54% of the frame width. Copy the dial exactly from the reference: matte white surface, the phrase "Who cares / I'm already late" handwritten in blue ink on two lines in the upper-left area, and the blue handwritten numerals 1 to 12 scattered in a messy pile in the lower half, in the same positions and the same handwriting as the reference. The dial is upright, not rotated: phrase at the top, pile of numerals at the bottom. In the centre there is a small hole with the tip of the metal post showing through. No hands yet. No hour markers, no logo, no date window.

Vertical 9:16 photoreal studio product photograph. Background: a seamless sheet of matte white cotton paper with a fine visible grain, filling the whole frame edge to edge. 90mm macro lens, camera locked off directly overhead, perfectly perpendicular top-down view, everything in sharp focus. Soft diffused daylight from the top-left, one short soft shadow falling to the bottom-right, no hard reflections. Clean neutral whites, low contrast, true-to-life colour, no vignette. No watermark, no store logo, no brand name, no extra text, no human hands, no tools.
```

Comprueba (esta es la imagen más importante): la frase se lee bien y está escrita igual que en tu esfera · están los doce números, sin repetidos ni inventados, amontonados abajo · la esfera está derecha · sigue centrada donde estaba el movimiento · el papel y la sombra no han cambiado.

### Imagen 03 — las agujas de acero
*Adjunta: tu imagen 02 + `referencias/3-agujas.jpg`*

```
Edit the first attached image. Do not move, resize, rotate or redraw anything already in it: the dial and all its blue handwriting stay exactly as they are.

Add only the hour hand and the minute hand from the second attached image, mounted on the centre post: polished silver baton hands, each with a thin white luminous strip. The short hour hand points straight to the left, to where 9 o'clock would be. The long minute hand points to the right and slightly upward, to where the 12-minute mark would be (between 2 and 3 o'clock), and reaches almost to the edge of the dial. The watch shows about 9:12. Neither hand covers the handwritten phrase or the numerals. Each hand casts a very thin soft shadow on the dial. Do not add a seconds hand.

Vertical 9:16 photoreal studio product photograph. Background: a seamless sheet of matte white cotton paper with a fine visible grain, filling the whole frame edge to edge. 90mm macro lens, camera locked off directly overhead, perfectly perpendicular top-down view, everything in sharp focus. Soft diffused daylight from the top-left, one short soft shadow falling to the bottom-right, no hard reflections. Clean neutral whites, low contrast, true-to-life colour, no vignette. No watermark, no store logo, no brand name, no extra text, no human hands, no tools.
```

Comprueba: solo hay dos agujas · la corta apunta a la izquierda y la larga a la derecha un poco hacia arriba (las 9:12), sin tapar la frase ni los números · la esfera es idéntica a la de la imagen 02 (compara la letra).

### Imagen 04 — el segundero azul
*Adjunta: tu imagen 03 + `referencias/1-segundero-azul.jpg`*

```
Edit the first attached image. Do not move, resize, rotate or redraw anything already in it: the dial, its blue handwriting and the two steel hands stay exactly as they are.

Add only the blue seconds hand from the second attached image, mounted on the centre on top of the other two hands: matte royal blue, a very thin needle ending in a small open arrow tip filled with white, a round hub at the centre, and a short paddle-shaped counterweight on the opposite side. The needle points up and to the right, to where the 8-second mark would be (between 1 and 2 o'clock), passing just to the right of the end of the handwritten phrase without touching it, and reaches almost to the edge of the dial. The counterweight points the opposite way, down and to the left.

Vertical 9:16 photoreal studio product photograph. Background: a seamless sheet of matte white cotton paper with a fine visible grain, filling the whole frame edge to edge. 90mm macro lens, camera locked off directly overhead, perfectly perpendicular top-down view, everything in sharp focus. Soft diffused daylight from the top-left, one short soft shadow falling to the bottom-right, no hard reflections. Clean neutral whites, low contrast, true-to-life colour, no vignette. No watermark, no store logo, no brand name, no extra text, no human hands, no tools.
```

Comprueba: la aguja azul apunta arriba a la derecha, justo después del final de la frase y sin tocarla · tiene la punta de flecha blanca · las dos de acero no se han movido.

### Imagen 05 — la caja y el brazalete
*Adjunta: tu imagen 04 + `referencias/5-caja.jpg`*

```
Edit the first attached image. The dial, its blue handwriting and the three hands stay exactly as they are: same size, same position, same orientation.

The dial is now inside the watch case from the second attached image. Use that photo only as a reference for the shape and finish of the case and bracelet; ignore its background. A brushed stainless steel barrel-shaped case with a thin polished round bezel ring, a flat clear crystal over the dial, and a small steel crown on the right side at 3 o'clock. An integrated brushed steel bracelet with flat wide links leaves the case at the top and at the bottom and runs straight out of the top and bottom edges of the frame, lying flat on the paper. The case is 70% of the frame width. No brand name, no logo, no engraving, no reflections hiding the dial.

Vertical 9:16 photoreal studio product photograph. Background: a seamless sheet of matte white cotton paper with a fine visible grain, filling the whole frame edge to edge. 90mm macro lens, camera locked off directly overhead, perfectly perpendicular top-down view, everything in sharp focus. Soft diffused daylight from the top-left, one short soft shadow falling to the bottom-right, no hard reflections. Clean neutral whites, low contrast, true-to-life colour, no vignette. No watermark, no store logo, no brand name, no extra text, no human hands, no tools.
```

Comprueba: la esfera no ha cambiado de tamaño ni de sitio respecto a la imagen 04 · el brazalete sale recto por arriba y por abajo · la corona está a la derecha · no hay ninguna marca ni logo en la caja · se parece a tu caja de verdad.

---

## Vídeos

Cada clip une dos imágenes seguidas: empieza exactamente en una y termina exactamente en la siguiente. Para eso la herramienta tiene que dejarte poner **imagen inicial e imagen final**.

- **Si tu Gemini te deja poner las dos** (en Flow, la herramienta de vídeo de Google, se llama «Frames to video» o «De fotogramas a vídeo»): usa el plan A. Es el que mejor queda.
- **Si solo te deja poner una imagen de inicio**: no generes los clips 1 a 4. Sin imagen final, el modelo se inventa la pieza que llega y la letra de la esfera no coincidirá con tus imágenes. Mándame solo las 5 imágenes y hago yo en la web la animación de cada pieza cayendo en su sitio. El clip 5 sí puedes hacerlo, porque solo necesita imagen inicial.

Formato vertical 9:16, la mayor resolución que te deje (1080p mejor que 720p), duración la que dé por defecto (unos 8 s). El sonido da igual, lo quito.

### Clip 1 — llega la esfera
*Imagen inicial: 01 · Imagen final: 02*

```
Locked-off overhead shot, the camera does not move at all. A white watch dial descends slowly and gently from just above the lens and settles flat onto the watch movement, covering it. The paper, the light and the shadows stay the same. Slow, calm, one continuous take, no cuts.
```

### Clip 2 — llegan las agujas
*Imagen inicial: 02 · Imagen final: 03*

```
Locked-off overhead shot, the camera does not move at all. Two slim polished steel watch hands descend slowly from just above the lens and settle onto the centre of the dial. The dial and its blue handwriting stay perfectly still and unchanged. Slow, calm, one continuous take, no cuts.
```

### Clip 3 — llega la azul
*Imagen inicial: 03 · Imagen final: 04*

```
Locked-off overhead shot, the camera does not move at all. A thin blue seconds hand descends slowly from just above the lens and settles onto the centre of the dial, on top of the two steel hands. The dial and its blue handwriting stay perfectly still and unchanged. Slow, calm, one continuous take, no cuts.
```

### Clip 4 — llega la caja
*Imagen inicial: 04 · Imagen final: 05*

```
Locked-off overhead shot, the camera does not move at all. A brushed steel watch case with its bracelet descends slowly from just above the lens and settles around the dial, enclosing it. The dial, its blue handwriting and the hands stay perfectly still and unchanged. Slow, calm, one continuous take, no cuts.
```

### Clip 5 — el reloj echa a andar
*Imagen inicial: 05 · Sin imagen final*

```
Locked-off overhead shot, the camera does not move at all. The thin blue seconds hand sweeps smoothly and steadily clockwise around the dial. Everything else stays perfectly still: the two steel hands, the dial, its blue handwriting, the steel case, the light. Slow, calm, one continuous take, no cuts.
```

Los prompts de vídeo son aburridos a propósito: un solo movimiento lento y nada más. Al pasar el vídeo con el scroll, cualquier cosa rápida se convierte en una mancha.

---

## Qué me tienes que devolver

Guárdalo en la carpeta del proyecto:

| Qué | Dónde | Cómo |
|---|---|---|
| Las 5 imágenes | `imagenes/01.png` … `05.png` | Tal cual salen, sin recortar |
| Los clips | `videos/clip1.mp4` … `clip5.mp4` | Vertical 9:16, sin bordes negros, tal cual salen |

Si Gemini deja una marca pequeña en una esquina de las imágenes o de los vídeos, no la quites tú: mándalo así y la tapo yo, que cae sobre papel blanco.

## Si algo sale mal

| Qué ves | Por qué | Qué hacer |
|---|---|---|
| La frase o los números salen distintos a tu esfera | El modelo ha redibujado la esfera en vez de copiarla | Repite la imagen 02 y añade al principio: `Copy the handwriting from the reference stroke for stroke.` |
| En la 03, 04 o 05 cambia la letra de la esfera | Ha vuelto a generar toda la imagen en vez de editarla | Repite ese paso empezando por: `Change nothing except what I describe.` |
| Cambia el tamaño o la posición entre una imagen y la siguiente | Ha reencuadrado | Repite ese paso y añade: `Same framing and same scale as the first attached image, pixel for pixel.` |
| La luz o la sombra cambian de lado | Se ha tocado el bloque final del prompt | Vuelve a pegar el prompt tal cual |
| Aparece un logo o un texto de tienda | Lo ha copiado de la foto de referencia | Repite; si insiste, añade: `The object has no branding of any kind.` |
| En el vídeo la letra de la esfera se deforma mientras llega una pieza | Normal en movimiento; lo que importa es que empiece y termine bien | Si se deforma mucho, repite el clip; si sigue, lo resuelvo yo con las imágenes fijas |
| En el vídeo la cámara se mueve o hace zoom | El modelo ha ignorado «locked-off» | Repite el clip |
| Se nota un salto entre un clip y el siguiente | El clip no ha terminado exactamente en la imagen final | Dímelo y lo arreglo al unirlos |
