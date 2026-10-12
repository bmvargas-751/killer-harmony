# Parche de Traducción al Español - Danganronpa V3: Killing Harmony v3.5

Este repositorio contiene el script de instalación automática y los archivos correspondientes al parche de traducción al español para **Danganronpa V3: Killing Harmony** (versión de PC). 

> Esta traducción la hice yo solo, para mi comunidad en Youtube. Es mi primera traducción, y estaba originalmente pensada para mi propio uso y el de mi comunidad, comprendiendo que la calidad no es profesional. 

> **Fork v3.5**: esta copia incluye los rótulos de los capítulos y de la interfaz del juicio traducidos (los cut-ins del juicio se dejan en inglés), corrección de erratas y de palabras destacadas pegadas, términos unificados con Danganronpa 1 y 2, la galería y el menú de pausa traducidos, un instalador más seguro con opción para restaurar y soporte para Linux / SteamOS. Mira las [novedades del fork](#-novedades-de-la-v35-fork).

Lee el final de este documento para saber [cómo](#cómo-contribuir-al-proyecto) contribuir. Si descargaste una versión anterior del parche y tienes algún problema, revisa que no haya una versión más reciente. 
---

## 📌 Requisitos Previos

Antes de ejecutar el script de instalación, necesitas contar con lo siguiente:

1. **Danganronpa V3: Killing Harmony** instalado en tu PC (vía Steam u otra plataforma en Windows).
2. **Harmony Tools** instalado y accesible en tu sistema:
   * Repositorio oficial y descargas: [Harmony-Tools en GitHub](https://github.com/redssu/Harmony-Tools).
   * Asegúrate de tener `HarmonyTools.exe` agregado a las variables de entorno (`PATH`) o ubicado en su ruta por defecto (`C:\Harmony-Tools\HarmonyTools.exe`).

---

## 🚀 Instrucciones de Instalación

1. **Descarga o clona este repositorio** en cualquier carpeta de tu ordenador.
2. Haz **doble clic en `patch.bat`** (o ejecuta `patch.ps1` desde PowerShell como Administrador).
3. **Introduce la ruta de instalación del juego** cuando el script te lo solicite:
   * Ejemplo de ruta habitual: `C:\Program Files (x86)\Steam\steamapps\common\Danganronpa V3 Killing Harmony`
   * Si el script detecta automáticamente tu instalación, puedes simplemente presionar `Enter`.
4. **Selecciona la versión del parche** que deseas instalar:
   * Presiona `S` (o `Enter`) para instalar la versión más reciente (**v3.5**).
   * Presiona `N` para instalar la versión previa (**v0.1**).
5. **Espera a que el proceso termine**:
   * El script extraerá y combinará los archivos `.cpk` de `data/win`. Este proceso puede tardar varios minutos dependiendo de tu disco.
   * A continuación, aplicará los archivos traducidos y limpiará los archivos temporales y `.cpk` originales.
6. Al finalizar, verás un mensaje de confirmación en verde indicando que el parche ha sido instalado correctamente. Presiona cualquier tecla para cerrar la consola y ya podrás iniciar el juego.

> **¿Ya tienes un parche anterior instalado?**
> Si los archivos `.cpk` originales ya no están presentes (porque fueron eliminados al aplicar un parche previo), el script lo detectará automáticamente y te preguntará si deseas omitir la extracción. Confirma con `S` (opción por defecto) y el instalador aplicará únicamente los nuevos archivos del parche sobre los datos ya extraídos, sin necesidad de volver a extraer nada.

---

## 🔄 Desinstalar o volver a una versión anterior

Cada vez que instalas el parche, el instalador guarda un respaldo dentro de la carpeta del juego, en `killer-harmony-backup`:

* Los archivos originales del juego (en inglés) que el parche reemplaza.
* La lista de archivos que el parche agrega, para poder quitarlos.
* Una copia de cada versión del parche que tenías instalada antes de cambiar a otra.

Como el respaldo vive en la carpeta del juego, no se pierde si descargas una versión nueva del parche en otra carpeta. Si instalaste con un instalador antiguo (que guardaba el respaldo en `backup_en`, dentro de la carpeta del parche), se traslada automáticamente la próxima vez que instales.

Para restaurar:

1. Haz **doble clic en `restaurar.bat`** (en Linux / SteamOS: `./restaurar.sh`).
2. Introduce la ruta del juego (o presiona `Enter` si se detectó sola).
3. El script muestra la versión instalada y te deja elegir entre:
   * **Juego original** (sin parche, en inglés).
   * **Cualquier versión del parche** que hayas tenido instalada antes.

> Al volver al juego original, este queda en inglés usando los archivos ya extraídos (los `.cpk` originales no se recuperan). Si prefieres volver exactamente al estado de Steam, o si no hay respaldo, usa *Propiedades → Archivos instalados → Verificar integridad de los archivos*.

---

## 🐧 Instalación en Linux / SteamOS (Steam Deck, Legion Go, etc.)

En Linux se usa `patch.sh` en lugar de `patch.bat`. Hace lo mismo que el instalador de Windows, pero de forma nativa: solo `HarmonyTools.exe` se ejecuta con Wine o, si no tienes Wine (como en SteamOS), con el **Proton** que ya trae Steam. No hace falta instalar nada en el sistema.

1. Entra al **Modo Escritorio** y descarga o clona este repositorio.
2. Asegúrate de tener algún Proton instalado en Steam (por ejemplo **Proton Experimental**, en la biblioteca, categoría *Herramientas*). Si ya jugaste Danganronpa V3 en Linux, ya lo tienes.
3. Abre **Konsole** en la carpeta del parche y ejecuta:
   ```bash
   chmod +x patch.sh
   ./patch.sh
   ```
4. Si no encuentra `HarmonyTools.exe` en la carpeta del parche, el script ofrece descargarlo de su [repositorio oficial](https://github.com/redssu/Harmony-Tools/releases). También puedes copiarlo tú en la carpeta del parche.
5. El script detecta el juego en tus bibliotecas de Steam (también en la tarjeta SD); presiona `Enter` para usar la ruta detectada. Luego sigue los mismos pasos que en Windows.

> La primera vez Proton prepara un entorno propio para el parche (en `~/.local/share/killer-harmony`), por lo que la extracción puede tardar un poco más en empezar. Si quieres usar un Proton o Wine concreto, puedes indicarlo con las variables `PROTON=/ruta/a/proton` o `WINE=/ruta/a/wine`.

> Si algo sale mal, desde Steam puedes usar *Propiedades → Archivos instalados → Verificar integridad de los archivos* para recuperar los archivos originales del juego.

---

## ℹ️ Información sobre las Versiones

* **Versión v0.1**:
  * Es la versión base que ya fue probada y jugada completamente en una serie de gameplays en YouTube en [mi canal](https://www.youtube.com/@killerkoiking).
* **Versiones más recientes (v1.0 y posteriores)**:
  * Incluyen revisiones ortográficas, mejoras en el formateo de texto, fuentes y correcciones de estilo.
  * *Nota*: Estas versiones no han sido probadas exhaustivamente de principio a fin, por lo que si encuentras algún detalle visual o error tipográfico, puedes reportarlo.

### 🆕 Novedades de la v3.5 (fork)

* **Correcciones reportadas con capturas** (capítulo 4), traducidas desde el texto original en inglés:
  * Una frase de Kokichi tenía un espacio después del "¿" y una segunda línea que no sonaba natural ("Deberías ser capaz de abrir, fácil.").
  * Una frase en letras grandes no tenía el "¡" inicial y repetía el "es".
  * Una frase de Kaito tenía un "+" que sobraba.
* **Espacio después de "¿" y "¡"**: en 38 líneas de los capítulos 0 a 7 quedaba un espacio entre el "¿" o el "¡" y la palabra destacada que lo sigue (`¿ Academia Definitiva para Jóvenes Dotados?`). Ya no queda ninguno.

<details>
<summary><b>Textos que cambiaron en esta versión</b></summary>

| Dónde | Antes (v3.4.2) | Ahora (v3.5) | En inglés |
|---|---|---|---|
| Cap. 4, Kokichi | ¿ Abrir cerraduras no era tu especialidad?<br>Deberías ser capaz de abrir, fácil. | ¿Abrir cerraduras no era tu especialidad?<br>Podrías haberla abierto fácilmente. | But isn't lock picking your specialty?<br>You should've been able to open it, easy. |
| Cap. 4, letras grandes | Es en realidad no<br>es imposible en absoluto! | ¡En realidad no es<br>imposible en absoluto! | It's not actually<br>impossible at all! |
| Cap. 4, Kaito | Solo significa que hasta+ yo cometo errores. | Solo significa que hasta yo cometo errores. | It just means even I make mistakes. |
| Caps. 0 a 7 (38 líneas) | ¿ Definitivos...? / ¿¡ Definitivos!? / ¡ Gracias, gracias! ... | ¿Definitivos...? / ¿¡Definitivos!? / ¡Gracias, gracias! ... | — |

No cambió ningún término ni rótulo en esta versión.
</details>

### Novedades de la v3.4.2 (fork)

* **Kokichi Oma**: en 26 textos su apellido aparecía como "Ouma" (su nombre en los menús y el Monopad, su habitación en el mapa, los niveles de vínculo, los avisos de afecto, "Conversación con Kokichi Ouma" y su presentación en el prólogo), mientras que en el resto del juego era "Oma". Ahora es "Oma" en todos lados, como se presenta en el original en inglés ("I'm Kokichi Oma").

<details>
<summary><b>Términos que cambiaron en esta versión</b></summary>

| Antes (v3.4.1) | Ahora (v3.4.2) | Usos | En inglés |
|---|---|---|---|
| Kokichi Ouma | Kokichi Oma | 26 | Kokichi Oma |
</details>

### Novedades de la v3.4.1 (fork)

* **Angie vuelve a decir "Dios"**: en la v3.4, la frase de Angie a Himiko se cambió de más ("¡Y Atua también te ama a ti, Himiko!"). El error reportado era solo el género, así que ahora queda como estaba, pero en femenino. En japonés Angie dice 神さま ("Dios"); "Atua" es como lo llamó la localización al inglés.

<details>
<summary><b>Textos que cambiaron en esta versión</b></summary>

| Dónde | Antes (v3.4) | Ahora (v3.4.1) | En inglés |
|---|---|---|---|
| Cap. 3, Angie | ¡Y Atua también te ama a ti, Himiko! | ¡Y eres \*amada\* por Dios también, Himiko! | And you are loved by Atua in return, Himiko! |

No cambió ningún término ni rótulo en esta versión.
</details>

### Novedades de la v3.4 (fork)

* **Correcciones reportadas con capturas**, traducidas desde el texto original en inglés:
  * Angie le decía "amado" a Himiko; además decía "Dios" en vez de "Atua", como en el resto del juego.
  * Una frase de Angie con un salto de línea de más antes de "motivo", una de Maki sin espacio después del punto y una de Miu con un "es" sobrante.
  * La Munición de Verdad "Katana Batida en Oro" ahora se llama "Katana de Pan de Oro", como ya la llamaba el resto del diálogo.
* **Cut-ins del juicio otra vez en inglés**: las letras editadas no quedaban bien con el diseño original, así que vuelven las imágenes originales de los cut-ins (Counter, Perjury, GOT IT, Consent...), de los títulos de inicio de fase (Non-Stop Debate, Closing Argument...), de ALL RISE! / Intermission / Resume y del "In Session" al empezar el juicio. La interfaz del juicio (Municiones de Verdad, Votación, Resultados, ¡Golpe final!, ¡Avanza! / ¡Retrocede!...) y "Preparación del juicio" siguen traducidas.
* **Instalador**: al actualizar, los archivos que instaló la versión anterior y que la nueva ya no trae vuelven al original del juego (antes se quedaban como estaban). Así, al pasar de la v3.3 a la v3.4 los cut-ins vuelven al inglés sin tener que restaurar nada a mano.
* **Herramientas**: las recetas de los rótulos que se dejaron en inglés se guardan en `tools/rotulos/descartados/`.

<details>
<summary><b>Textos y rótulos que cambiaron en esta versión</b></summary>

| Dónde | Antes (v3.3) | Ahora (v3.4) | En inglés |
|---|---|---|---|
| Cap. 3, Angie | ¡Y eres \*amado\* por Dios también, Himiko! | ¡Y Atua también te ama a ti, Himiko! | And you are loved by Atua in return, Himiko! |
| Cap. 3, Angie | Probablemente todavía estés preocupado por el<br>motivo,<br>Shuichi, pero está bien. | Probablemente todavía estés preocupado por el<br>motivo, Shuichi, pero está bien. | You're probably still worried about the motive, Shuichi, but it's okay. |
| Cap. 3, Maki | ...de dónde vino esta arma.Puede que encontremos una pista allí. | ...de dónde vino esta arma. Puede que encontremos una pista allí. | We should investigate where this weapon came from. We might find a clue there. |
| Cap. 3, Miu | No, sigue siendo es un error pensar que Tenko fue asesinada durante la sesión. | No, sigue siendo un error pensar que Tenko fue asesinada durante la sesión. | No, it's still wrong to think that Tenko was killed during the seance. |
| Munición de Verdad, objeto del mapa y avisos del Monopad (5 líneas) | Katana Batida en Oro | Katana de Pan de Oro | Gold Leaf Katana |
| Cut-ins del juicio | Refutado / Objeción / Consenso / Perjurio / Ruptura / Refutación total / ¡Lo tengo! / Fin / Confesando / ¡Monokuma oculto encontrado! | (imagen original en inglés) | Counter / Argue / Consent / Perjury / Break / Full Counter / GOT IT / End / Confessing / Obtained Hidden Monokuma |
| Inicio de fase | Debate Continuo, Debate de Pánico Masivo, Confrontación Refutadora, Debate de Choque, Paseo Mental, Epifanía Anagrámica, Excavación Cerebral, Armamento Teorético, Clímax Lógico | (imagen original en inglés) | Non-Stop Debate, Mass Panic Debate, Rebuttal Showdown, Debate Scrum, Psyche Taxi, Hangman's Gambit, Mind Mine, Argument Armament, Closing Argument |
| Juicio Escolar | ¡De pie! / Receso / Se reanuda / En sesión | (imagen original en inglés) | ALL RISE! / Intermission / Resume / In Session |

| Término | Antes | Ahora | Usos | En inglés |
|---|---|---|---|---|
| Munición de Verdad del cap. 3 | Katana Batida en Oro | Katana de Pan de Oro | 5 | Gold Leaf Katana |
</details>

### Novedades de la v3.3 (fork)

* **Correcciones reportadas con capturas**, traducidas desde el texto original en inglés:
  * Tres pensamientos de Shuichi (capítulos 1 y 2) empezaban con un "502" que no debía verse.
  * Una frase de Monokuma en el segundo juicio a la que le faltaba el verbo, y frases de Miu y Gonta que no decían lo mismo que el original.
  * La descripción del regalo "Helado Duro y Grueso" estaba a medio traducir, y la de la "Brújula de Un Solo Sentido" tenía un "one." de más.
* **Frases destacadas entre comillas pegadas**: en 16 líneas de los capítulos 0 a 5, las frases resaltadas entre comillas aparecían pegadas al texto (`Kirumi"hacer a este país grande de nuevo"y`). `tools/separar_etiquetas.py` ahora también reconoce las comillas.
* **README**: cada versión tiene ahora la lista completa de lo que cambió (erratas, puntuación, nombres de la galería, objetos del mapa, textos de la interfaz y rótulos).
* **Herramientas**: nueva lista `tools/correcciones/capturas.tsv` con las correcciones de esta versión.

<details>
<summary><b>Textos que cambiaron en esta versión</b></summary>

| Dónde | Antes (v3.2) | Ahora (v3.3) | En inglés |
|---|---|---|---|
| Cap. 1 y 2, pensamientos de Shuichi (3 líneas) | 502 Y entonces, de repente... / 502 Pero no había... / 502 Pero... supongo que... | (sin el "502") | — |
| Cap. 2, Monokuma | ¡Lo siento! ¡Se me olvidó! ¡Definitivamente no me lo para hacer el juicio más interesante! | ¡Perdón! ¡Lo olvidé! ¡De verdad no lo guardé en secreto para hacer el juicio más interesante! | Sorry! Forgot! I definitely didn't keep it a secret to make the trial more interesting! |
| Cap. 2, Miu | Pensé que me quitaría la ropa para que Gonta estuviera demasiado nervioso para tocarme. | ¡Pensé que me quitaría la ropa para que Gonta estuviera demasiado nervioso para tocarme! | I figured I'd take my clothes off so Gonta would be too flustered to touch me! |
| Cap. 2, Gonta | ¡Los caballeros, no arrojen cadáveres! | ¡Los caballeros no arrojan cadáveres! | Gentlemen not chuck dead bodies! |
| Regalo: Helado Duro y Grueso | Puede an be carried around for a long time, even in summer. But it's so hard, ordinary spoons can't penetrate it. | Puede llevarse por mucho tiempo, incluso en verano. Pero es tan duro que las cucharas normales no pueden penetrarlo. | (el mismo texto en inglés) |
| Regalo: Brújula de Un Solo Sentido | ...la persona amada del dueño. one. | ...la persona amada del dueño. | — |

No cambió ningún término ni rótulo en esta versión.
</details>

### Novedades de la v3.2 (fork)

* **Tiempo libre con Angie completo**: a uno de los tiempos libres con Angie del capítulo 1 le faltaban las primeras 8 líneas de diálogo. Se agregaron, tomadas de la versión 2.3 del parche original. El resto de la traducción del fork no cambia.

<details>
<summary><b>Términos que cambiaron en esta versión</b></summary>

No cambió ningún término en esta versión; solo se agregaron las líneas que faltaban.
</details>

### Novedades de la v3.1 (fork)

* **Rótulo de capítulo en blanco**: el indicador de capítulo que aparece durante el juego ("Capítulo", "Prólogo", "Epílogo", "Extra" y "Demo") se veía en negro. Ahora es blanco con borde negro, como el original.

<details>
<summary><b>Términos que cambiaron en esta versión</b></summary>

No cambió ningún término ni rótulo en esta versión; solo el color del indicador de capítulo.
</details>

### Novedades de la v3.0 (fork)

* **Rótulos del juicio y de los capítulos traducidos**: las imágenes con texto que seguían en inglés ahora están en español, con el mismo tamaño, color y brillo que las originales (unas 150 pantallas):
  * **Capítulos**: Días (a)típicos / Días atípicos, Capítulo N, los títulos de cada capítulo, Continuará, Supervivientes, FIN, la lista de capítulos y CAPÍTULO / ESCENA.
  * **Inicio de cada fase**: Debate Continuo, Debate de Pánico Masivo, Confrontación Refutadora, Debate de Choque, Paseo Mental, Epifanía Anagrámica, Excavación Cerebral, Armamento Teorético y Clímax Lógico (con ¡EMPIEZA!).
  * **Cut-ins**: Refutado, Objeción, Consenso, Perjurio, Ruptura, Refutación total, ¡Lo tengo!, Fin, ¡Golpe final!, ¡CORTE!, ¡Avanza! / ¡Retrocede!, Cruce de espadas, Éxito / Fallo.
  * **Pantallas del juicio**: JUICIO ESCOLAR, Preparación del juicio, En sesión / Receso / ¡De pie! / Se reanuda, Elegir / Acusar / Decidir, Votación, Hora de Votar, Resultados, CASO N, N.º Juicio Escolar, Reintentar, Municiones de Verdad, Opción y más.
* **Se quedan en inglés a propósito**: las palabras de los minijuegos y del casino (TIME, SCORE, COMBO, GO!!...), los kanji decorativos de los cut-ins y "Split Opinion" del Debate de Choque (sus letras están pintadas sobre recuadros decorados).
* **Herramienta nueva `tools/rotulos_fuente.py`**: rehace rótulos en imagen con tipografías libres (OFL / Apache, se descargan solas y no se incluyen en el parche). Cada pantalla tiene su receta en `tools/rotulos/` (capítulos, fases, juicio, cut-ins, otros). Necesita Python con Pillow.

> **Importante**: las animaciones de algunos títulos (por ejemplo Debate Continuo o Confrontación Refutadora) mueven las letras por trozos. Se repartió el texto en español en los mismos trozos, pero conviene revisarlas en el juego; si algo se ve desacomodado, [abre un ticket](https://github.com/bmvargas-751/killer-harmony/issues) con una captura.

<details>
<summary><b>Rótulos que cambiaron en esta versión</b></summary>

| Antes (inglés, imagen) | Ahora (v3.0) |
|---|---|
| Daily Life / Deadly Life | Días (a)típicos / Días atípicos |
| Chapter N / Prologue / Epilogue | Capítulo N / Prólogo / Epílogo |
| To Be Continued / Surviving Members / END | Continuará / Supervivientes / FIN |
| Ultimate Revival | Renacer Definitivo |
| My Class Trial, Our Class Trial | Mi Juicio Escolar, nuestro Juicio Escolar |
| A Thin Line Divides Heaven and Hell | Una delgada línea entre el cielo y el infierno |
| Transfer Student From Beyond the Grave | Estudiante transferido desde el más allá |
| Live and Let The Languid World Live | Vive y deja vivir al lánguido mundo |
| Voyage Without Passion or Purpose | Viaje sin pasión ni propósito |
| Goodbye Danganronpa | Adiós, Danganronpa |
| Everyone's Killing Game Closing Ceremony | Ceremonia de clausura del juego de asesinato de todos |
| Non-Stop Debate START! | Debate Continuo ¡EMPIEZA! |
| Mass Panic Debate START! | Debate de Pánico Masivo ¡EMPIEZA! |
| Rebuttal Showdown -Truth Blade- | Confrontación Refutadora -Filo de Verdad- |
| Debate Scrum START! | Debate de Choque ¡EMPIEZA! |
| Psyche Taxi / Hangman's Gambit / Mind Mine / Argument Armament | Paseo Mental / Epifanía Anagrámica / Excavación Cerebral / Armamento Teorético |
| Closing Argument Start! | Clímax Lógico ¡Empieza! |
| Counter / Argue / Consent / Perjury | Refutado / Objeción / Consenso / Perjurio |
| Break / Full Counter / GOT IT / End | Ruptura / Refutación total / ¡Lo tengo! / Fin |
| Final Blow! / SLASH / Advance! / Retreat! | ¡Golpe final! / ¡CORTE! / ¡Avanza! / ¡Retrocede! |
| Blade Lock / Success / Fail | Cruce de espadas / Éxito / Fallo |
| Agree / Lie | Consenso / Mentira |
| CLASS TRIAL / Court Preparation / In Session | JUICIO ESCOLAR / Preparación del juicio / En sesión |
| Intermission / ALL RISE! / Resume | Receso / ¡De pie! / Se reanuda |
| Select / Accuse / Spot Selection / Decide | Elegir / Acusar / Elegir lugar / Decidir |
| Voting / Voting Time / Results / No Votes / ATTENTION | Votación / Hora de Votar / Resultados / Sin votos / ATENCIÓN |
| CASE N / Rank / Nth Class Trial / SKILL BONUS / Retry | CASO N / Rango / N.º Juicio Escolar / BONO DE HABILIDAD / Reintentar |
| Truth Bullets / status / Answer / Confirm Opinion | Municiones de Verdad / estado / Opción / Confirmar opinión |
| Confessing / Obtained Hidden Monokuma! | Confesando / ¡Monokuma oculto encontrado! |
| Select Difficulty / CHAPTER / SCENE | Elige la dificultad / CAPÍTULO / ESCENA |

No cambió ningún término del texto en esta versión.
</details>

### Novedades de la v2.7 (fork)

* **Segunda revisión de términos**: se compararon los nombres con el parche de la demo de V3 de [V3ducciones](https://tradusquare.es/proyectos/danganronpa-v3/) y con DR1/DR2. Se cambiaron los títulos de Ryoma y Kirumi, los nombres de las fases del capítulo y se unificaron los Filos de Verdad (antes se mezclaba con "Espada de Verdad").
* **Restos de términos viejos**: 12 líneas que la v2.6 no cambió porque el término estaba partido en dos renglones ("Archivo / Monokuma", "Cuida / Niños"...).
* **Correcciones de interfaz**:
  * Las descripciones de dificultad decían "Para débiles de mente" y "Para mancos"; ahora dicen lo que dice el original ("Para quienes quieren disfrutar la historia").
  * Nombres de habilidades que no coincidían con su descripción (Foco Extraordinario / Foco Amenazante) y errores de redacción en otras.
  * Botones del casino que seguían en inglés (BET, MAX BET → APOSTAR, APOSTAR TODO).
  * "Ver Manual de Estudiante" → "Ver Monopad" antes del juicio, y otros detalles.
  * Los juegos del casino se llaman igual en todo el juego (¡CAZADOR DE TESOROS! Monolith, AGARRÓN DE SALMÓN, Tragaperras MonoMono).
* **Herramientas**: nueva lista `tools/correcciones/interfaz.tsv` con las correcciones de interfaz.

<details>
<summary><b>Textos de la interfaz que se corrigieron</b></summary>

Los botones aparecen entre corchetes, por ejemplo [△].

| Antes (v2.6) | Ahora (v2.7) |
|---|---|
| En N respuesta(s) correctas más, el bloqueo será levantado. | Responde correctamente N vez/veces más para desbloquearlo. |
| Foco Extraordinaria | Foco Extraordinario |
| Aumenta un poco la concentración máxima. Efectiva durante todo el juicio escolar. No se puede combinar con Foco Amenazador. | Aumenta un poco la concentración máxima. Efectiva durante todo el juicio escolar. No se puede combinar con Foco Amenazante. |
| La primera letra estará llenada desde el inicio. Efectiva durante la Epifanía Anagrámica V3.0. | La primera letra aparecerá desde el inicio. Efectiva durante la Epifanía Anagrámica V3.0. |
| Se borraran piezas desde el comienzo. Efectiva durante Excavaciones Cerebrales. | Algunas piezas faltarán desde el comienzo. Efectiva durante Excavaciones Cerebrales. |
| Ver Manual de Estudiante | Ver Monopad |
| Unidos contra la mente maestra, Kokichi, los estudiantes deben sobrevivir a un Juicio Escolar sin conocer la identidad del asesino ni de Víctima. Este es el comienzo de un juicio impredecible... | Unidos contra la mente maestra, Kokichi, los estudiantes deben sobrevivir a un Juicio Escolar sin conocer la identidad del asesino ni de la víctima. Este es el comienzo de un juicio impredecible... |
| Para débiles de mente. | Para quienes quieren disfrutar la historia. |
| Penalizaciones más duras ¡pero más recompensas! | Penalizaciones más duras y más opciones, ¡pero más recompensas! |
| Para mancos. | Menos acción, para quienes solo quieren disfrutar la historia. |
| [□]Cambiar playback | [□]Cambiar reproducción |
| [△]MAX BET | [△]APOSTAR TODO |
| [Ｌ１] [Ｒ１]ＢＥＴ×１０ | [Ｌ１] [Ｒ１]APOSTAR x10 |
| [Ｐ上下]ＢＥＴ | [Ｐ上下]APOSTAR |
| [Ｐ上下]ＢＥＴ [Ｌ１] [Ｒ１]ＢＥＴ×１０ [△]MAX BET | [Ｐ上下]APOSTAR [Ｌ１] [Ｒ１]APOSTAR x10 [△]APOSTAR TODO |
| ¡TREASURE HUNTER! MONOLITH. Es un juego de búsqueda de tesoros... | ¡CAZADOR DE TESOROS! Monolith. Es un juego de búsqueda de tesoros... |
| ¡TREASURE HUNTER! MONOLITH Guía del cazador de tesoros | ¡CAZADOR DE TESOROS! Monolith Guía del cazador de tesoros |
| ¡SALMON FISHING! Es un juego de pescar salmones. | ¡AGARRÓN DE SALMÓN! Es un juego de pescar salmones. |
| ¡SALMON FISHING! Noche de salmones | ¡AGARRÓN DE SALMÓN! Noche de salmones |
| MonoMono Slots... Parece un juego de tragamonedas. | Tragaperras MonoMono... Parece un juego de tragaperras. |
| MonoMono Slots Cómo ganar en las tragamonedas | Tragaperras MonoMono Cómo ganar en las tragaperras |
| TREASURE HUNTER! MONOLITH | ¡CAZADOR DE TESOROS! Monolith |
| SALMON FISHING | AGARRÓN DE SALMÓN |
| Tragamonedas MonoMono | Tragaperras MonoMono |
</details>


<details>
<summary><b>Palabras que cambiaron en esta versión</b></summary>

| Antes (v2.6) | Ahora (v2.7) | Veces | En inglés |
|---|---|---:|---|
| Tenista Pro Definitivo | Tenista Definitivo | 32 | Ultimate Tennis Pro |
| Mucama Definitiva / mucama | Sirvienta Definitiva / sirvienta | 45 | Ultimate Maid / maid |
| Vida Diaria / Vida Mortal (menús) | Días (a)típicos / Días atípicos | 5 | Daily Life / Deadly Life |
| Espada de Verdad / Filo de la Verdad | Filo de Verdad | 29 | Truth Blade |
| AGARRÓN DE SALMÓN, ¡CAZADOR DE TESOROS! y Tragaperras MonoMono en la galería y el mapa (estaban en inglés) | Igual que en el resto del parche | 22 | Casino games |

"Días (a)típicos" es el término de las traducciones de DR1 y DR2. Para los Filos de Verdad no se usó "Vaina" (DR2) porque esa palabra ya aparece en el capítulo 3 con su sentido literal (la vaina de la katana).
</details>

### Novedades de la v2.6 (fork)

* **Términos unificados con Danganronpa 1 y 2**: los nombres de mecánicas y objetos ahora son los mismos que usan las traducciones al español de DR1 y DR2 (de [TranScene](https://tradusquare.es/grupos-de-traduccion/transcene/)), para que la saga se lea igual de un juego a otro. Se ajustaron los artículos cuando el término cambia de género ("el Archivo Monokuma" → "la Ficha Monokuma").
* **Galería traducida**: el casino, las reglas y todos los segmentos del Teatro Monokuma, que seguían en inglés.
* **Nombres de la galería**: eventos, videos y presentaciones de personajes. También se corrigieron nombres que habían quedado a medio traducir ("Why Irse the Inner Tube?", "What Kaito Izquierda Behind"...).
* **Objetos del mapa**: los nombres que aparecen al apuntar a algo mientras exploras ("Door", "Blackboard"...) ahora están en español.
* **Otros textos en inglés**: descripciones actualizadas de algunas pruebas, una habilidad, una entrada de la ficha de Himiko y una frase del Armamento Teorético contra Kaede.
* **Herramientas**: nueva lista `tools/correcciones/terminos.tsv` con los cambios de términos, y las traducciones nuevas guardadas en `tools/correcciones/` para poder volver a aplicarlas.

<details>
<summary><b>Nombres de la galería que se tradujeron (eventos)</b></summary>

| En inglés | En español |
|---|---|
| Invitation to Despair | Invitación a la desesperación |
| Who Came Rolling In | Los que llegaron rodando |
| Kidnapping | Secuestro |
| Beginning of Despair | El comienzo de la desesperación |
| 15 Friends | 15 amigos |
| Despair Robot | Robot de la desesperación |
| Re: Vida Escolar From 0 | Re: Vida Escolar Desde 0 |
| Invitation to Despair Level 2 | Invitación a la desesperación nivel 2 |
| Who Came Rolling In Again | Los que llegaron rodando otra vez |
| Kaede's Story | La historia de Kaede |
| Mysterious Device | Dispositivo misterioso |
| The Sealed Academy | La academia sellada |
| Hello Despair Robot! | ¡Hola, robot de la desesperación! |
| Super Exisal Battle | Súper batalla de Exisals |
| Punish the Monokuma God | Castigo al dios Monokuma |
| Punish the Red Bear | Castigo al oso rojo |
| Trial Explanation V3 | Explicación del juicio V3 |
| Monokuma's Eyes V3 | Los ojos de Monokuma V3 |
| Fight to Survive! | ¡Lucha por sobrevivir! |
| The Killing Game Begins | Empieza el juego de asesinato |
| Academy Rules | Reglas de la academia |
| The Reliable Gonta! | ¡El confiable Gonta! |
| Welcome to Despair | Bienvenidos a la desesperación |
| You Want Despair Again!? | ¡¿Quieren desesperación otra vez?! |
| Monokuma's Motive Videos | Los videos de motivación de Monokuma |
| Monokuma Dead!? | ¡¿Monokuma muerto?! |
| Spoil the Children | Malcriar a los niños |
| Bowing Down | Reverencia |
| Invitation to the Underground | Invitación al subterráneo |
| Air Circulation! | ¡Ventilación! |
| Sketch | Boceto |
| Hidden Cameras! | ¡Cámaras ocultas! |
| Guilt | Culpa |
| Hand of Despair | La mano de la desesperación |
| Slowly... | Poco a poco... |
| Monokuma FIle | Ficha Monokuma |
| Film Everything | Grabarlo todo |
| Equivalent Exchange | Intercambio equivalente |
| Murder! | ¡Asesinato! |
| Everyone, Come Quick! | ¡Todos, vengan rápido! |
| Ultimate Talent Academy | Academia de Talentos Definitivos |
| Investigating the Photos | Investigando las fotos |
| Rantaro Appears! | ¡Aparece Rantaro! |
| Story of the Photos | La historia de las fotos |
| Searching Rantaro | Buscando a Rantaro |
| No Photography! | ¡Prohibido tomar fotos! |
| Silent Elevator | El ascensor silencioso |
| Secrets | Secretos |
| Juicio Escolar Participant 1 | Participante del Juicio Escolar 1 |
| Juicio Escolar Participant 2 | Participante del Juicio Escolar 2 |
| Juicio Escolar Participant 3 | Participante del Juicio Escolar 3 |
| Pasillo Sketch | Boceto del pasillo |
| Using A Long Pole... | Usando una vara larga... |
| Photo from Above | Foto desde arriba |
| Shot Put Ball Route | La ruta de la bala de cañón |
| Fight the Exisals! | ¡Lucha contra los Exisals! |
| Believe in Me, Who Punched You! | ¡Cree en mí, que te golpeé! |
| Kaede's Wish | El deseo de Kaede |
| Killing Game Promotional Video | Video promocional del juego de asesinato |
| Talent Annihilation | Aniquilación de talentos |
| Mysterious Letters | Cartas misteriosas |
| Fresh Start! | ¡Nuevo comienzo! |
| Secret Items | Objetos secretos |
| Attack on Shadow | Ataque a la sombra |
| Mysterious Device B Side | Dispositivo misterioso lado B |
| Kaito's Motive Video | El video de motivación de Kaito |
| Monokubs Meal | La comida de los Monokubs |
| Training Begins! | ¡Empieza el entrenamiento! |
| Let's Build a Tower | Construyamos una torre |
| What Is This Aura!? | ¡¿Qué es esta aura?! |
| It's Gonta! | ¡Es Gonta! |
| Kokichi's Surprise Attack | El ataque sorpresa de Kokichi |
| Insect Meet and Greet | Encuentro con insectos |
| Insect Meet and Greet LOL | Encuentro con insectos XD |
| Kibo's Recording Device | La grabadora de Kibo |
| Magic Show Opening! | ¡Comienza el show de magia! |
| Magic Show Opening!! | ¡Comienza el show de magia!! |
| Magic Show Opening!!! | ¡Comienza el show de magia!!! |
| Magic Show Opening!!!! | ¡Comienza el show de magia!!!! |
| Magic Show Opening!!!!! | ¡Comienza el show de magia!!!!! |
| Disquiet on Stage | Inquietud en el escenario |
| Go! Kibo! | ¡Adelante, Kibo! |
| Secret Ficha Monokuma | Ficha Monokuma secreta |
| Looking Down... | Mirando hacia abajo... |
| Imagining Escape | Imaginando el escape |
| Switching Bodies | Intercambio de cuerpos |
| A Woman's Weapon | El arma de una mujer |
| I Brought This Item | Traje este objeto |
| Rope Magic | Magia con cuerda |
| Edificio Principal Construction | Construcción del edificio principal |
| Let's Do It Together! | ¡Hagámoslo juntos! |
| Ropeway Magic | Magia de teleférico |
| Kirumi's Motive Video | El video de motivación de Kirumi |
| Burden | La carga |
| Giving Up on Surviving | Renunciar a sobrevivir |
| Ryoma's Motive Video | El video de motivación de Ryoma |
| I WILL NOT DIE! | ¡NO VOY A MORIR! |
| Public Execution!? | ¡¿Ejecución pública?! |
| Why Irse the Inner Tube? | ¿Por qué el flotador? |
| Deep Impact | Impacto profundo |
| Social Upheaval | Agitación social |
| Secret Items II | Objetos secretos II |
| Tenko's Practice! Boys Edition | ¡La práctica de Tenko! Edición chicos |
| Tenko's Practice! Girls Edition | ¡La práctica de Tenko! Edición chicas |
| This Is My First Time... | Es mi primera vez... |
| Ultimate Loss | Pérdida definitiva |
| Maki's Super Fast Push-ups | Las lagartijas ultrarrápidas de Maki |
| A Shocking Motive! | ¡Un motivo impactante! |
| Mysteriously Changing Message | El mensaje que cambia misteriosamente |
| God's Gift | Regalo de los dioses |
| Student Council | Consejo estudiantil |
| Training Together | Entrenando juntos |
| God with Red Hair and Black Eyes | El dios de pelo rojo y ojos negros |
| The Student Council's Authority | La autoridad del consejo estudiantil |
| Ficha Monokuma For Trouble | Ficha Monokuma problemática |
| Necronomicon | Necronomicón |
| The Caged Dog Village | La aldea del perro enjaulado |
| Ritual Preparation: Fate | Preparación del ritual: destino |
| Ritual Preparation: Salt | Preparación del ritual: sal |
| Ritual Preparation: Banquet | Preparación del ritual: banquete |
| The Candle Disappears | La vela desaparece |
| Caged Child | Niño enjaulado |
| Burning Candle | Vela encendida |
| Ritual: Grudge | Ritual: rencor |
| Ritual: Favor | Ritual: favor |
| Licking Licking | Lamer y lamer |
| Additional Ficha Monokuma | Ficha Monokuma adicional |
| Cursed!? | ¡¿Maldición?! |
| Light from the Eyes! | ¡Luz de los ojos! |
| Lockpicking Trick | El truco de la ganzúa |
| A Cool See-saw | Un subibaja genial |
| The Plotting Witch | La bruja conspiradora |
| Recording Function! | ¡Función de grabación! |
| Photo Just Before the Ritual | Foto justo antes del ritual |
| Angie in the Spare Room | Angie en el cuarto de sobra |
| Eternal Love | Amor eterno |
| What Was Lost | Lo que se perdió |
| Carry the Feeling | Llevar el sentimiento |
| Like I'm Gonna Die Here... | Siento que voy a morir aquí... |
| A Message from Rantaro | Un mensaje de Rantaro |
| Additional Message | Mensaje adicional |
| The Frying Pan is the Weapon! | ¡La sartén es el arma! |
| Secret Items III | Objetos secretos III |
| Tsumugi's Cabaret | El cabaret de Tsumugi |
| The Cult | La secta |
| Huge Space Abs | Abdominales espaciales enormes |
| Crushing Punch! | ¡Puñetazo aplastante! |
| Ultimate Child Caregiver...? | ¿Cuidadora Definitiva...? |
| Life at the Orphanage | La vida en el orfanato |
| Life as an Assassin | La vida de una asesina |
| 3 at Night | Las 3 de la noche |
| I Want to Talk | Quiero hablar |
| Latest Technology | Tecnología de punta |
| Mansion Map | Mapa de la mansión |
| World Map | Mapa del mundo |
| Parallel Universe Ficha Monokuma | Ficha Monokuma de un universo paralelo |
| Strike the Fire | Golpe de fuego |
| Login/Logout Record | Registro de entradas y salidas |
| The Latest Technology Resurrected | La tecnología de punta resucitada |
| Virtual World | Mundo Virtual |
| Killing Game Busters | Cazadores del juego de asesinato |
| Toilet Paper Murder | El asesinato del papel higiénico |
| Usar the Paper | Usar el papel |
| Kokichi's Insanity | La locura de Kokichi |
| True Kokichi's Insanity | La verdadera locura de Kokichi |
| Justice Punch! | ¡Puñetazo de justicia! |
| It's Just a Cold... | Es solo un resfriado... |
| An Ultimate Leader | Un Líder Definitivo |
| This World Belongs to Me | Este mundo me pertenece |
| Monokuma's Funeral | El funeral de Monokuma |
| Secret Items IV | Objetos secretos IV |
| Robot Body Experiment | Experimento con el cuerpo robótico |
| Crossbow Assembly | Armando la ballesta |
| Like Hell I'm Gonna Die Here... | Ni de broma voy a morir aquí... |
| Annihilation Plan | Plan de aniquilación |
| Assassination Skills Activate! | ¡Habilidades de asesina activadas! |
| Gofer Project | Proyecto Gofer |
| 16 High School Students | 16 estudiantes de preparatoria |
| Launching the Ark | El lanzamiento del arca |
| Academy Panorama | Panorama de la academia |
| The View Outside | La vista del exterior |
| The Mastermind Unmasked! | ¡La Mente Maestra desenmascarada! |
| That's What You Call Despair! | ¡A eso le llaman desesperación! |
| Kibougamine Panorama | Panorama de Kibougamine |
| The Tragedy | La tragedia |
| The Girl in Despair | La chica de la desesperación |
| High School Despair Student | Estudiante de preparatoria de la desesperación |
| The Despair Begins | Empieza la desesperación |
| Future Foundation vs Remnants | Fundación del Futuro contra los Vestigios |
| The Rebuilt Kibougamine | La Kibougamine reconstruida |
| The Virus Spreads | El virus se propaga |
| It's All Connected... | Todo está conectado... |
| The Ultimate Despair has Arrived! | ¡Llegó la Desesperación Definitiva! |
| Killing Game in Despair | Juego de asesinato en la desesperación |
| A Man's Promise | Promesa de hombre |
| Confusion Like Never Before | Una confusión como nunca antes |
| Human Press | Prensa humana |
| It's Punishment Time! | ¡Es la hora del castigo! |
| Dubious Ficha Monokuma | Ficha Monokuma dudosa |
| The Sneaking Magician | El mago sigiloso |
| Hangar Layout | Plano del hangar |
| Kaito's Rebellion | La rebelión de Kaito |
| Assassinate the Remnants | Asesinar a los Vestigios |
| In Order to Survive... | Para sobrevivir... |
| Let's Put an End to This... | Pongamos fin a esto... |
| The Real Kokichi | El verdadero Kokichi |
| The Second Coming of the Cubs | El regreso de los Kubs |
| Kibo's Awakening! | ¡El despertar de Kibo! |
| Annihilated Academy | La academia aniquilada |
| A Special Memory! | ¡Un recuerdo especial! |
| Ultimate Despair! | ¡Desesperación Definitiva! |
| What Kaito Izquierda Behind | Lo que Kaito dejó atrás |
| Makoto's Vida Diaria | La vida diaria de Makoto |
| Something to Focus on | Algo en qué concentrarse |
| Kibo the Destroyer | Kibo el Destructor |
| Killing Game Squad | Escuadrón del juego de asesinato |
| The Ultimate War | La guerra definitiva |
| Kibougamine Official Documents | Documentos oficiales de Kibougamine |
| Memories with the Baby | Recuerdos con el bebé |
| The Despair Incident | El incidente de la desesperación |
| Kokichi's Motive Video | El video de motivación de Kokichi |
| Writing on the Wall | Escrito en la pared |
| The Fate of Humanity | El destino de la humanidad |
| Fire the Rocket Launcher! | ¡Dispara el lanzacohetes! |
| Ultimate Survivor | Superviviente Definitivo |
| Our Hope | Nuestra esperanza |
| What's Up!? The Exisals! | ¡¿Qué onda?! ¡Los Exisals! |
| I Won't Let You Interfere! | ¡No dejaré que interfieras! |
| Fire the Rockets! | ¡Disparen los cohetes! |
| Survivor Perks | Ventajas del Superviviente |
| Kibo vs The Exisals | Kibo contra los Exisals |
| The Beginning of the End | El principio del fin |
| Kibo's Eyes for Magnifying! | ¡Los ojos de aumento de Kibo! |
| Kibo's Sharp Ears! | ¡El oído agudo de Kibo! |
| The Case of Rantaro Amami | El caso de Rantaro Amami |
| The Mastermind's Crime | El crimen de la Mente Maestra |
| The Suspect's Actions | Las acciones del sospechoso |
| Junko Enoshima has Arrived | Llegó Junko Enoshima |
| The Neverending Migration | La migración sin fin |
| A Laboratory in a Flask | Un laboratorio en un frasco |
| The Charm of Danganronpa | El encanto de Danganronpa |
| Past Danganronpas | Los Danganronpa anteriores |
| New Danganronpa V3! | ¡El nuevo Danganronpa V3! |
| Shuichi's Audition | La audición de Shuichi |
| Kaede's Audition | La audición de Kaede |
| Kaito's Audition | La audición de Kaito |
| Memories of V3 | Recuerdos de V3 |
| Inside Voices | Voces internas |
| The Viewers' Eyes | Los ojos de los espectadores |
| Victims of the Killing Game | Víctimas del juego de asesinato |
| Kibo's Final Form | La forma final de Kibo |
| Kaede's Nail Art | El arte de uñas de Kaede |
| Kaito's Gambling Problem | El problema de apuestas de Kaito |
| Faux Celebrity | Falsa celebridad |
| A Man's Passion, Space Edition | La pasión de un hombre, edición espacial |
| Maki and the Katana | Maki y la katana |
| Himiko's Training | El entrenamiento de Himiko |
| Monokuma & Monokubs TV Clip | Clip de TV de Monokuma y los Monokubs |
| Kibo's Eyes! | ¡Los ojos de Kibo! |
| Kibo's Ears! | ¡Los oídos de Kibo! |
| Elevator to the Showdown | El ascensor al enfrentamiento |
| Rantaro's Body Discovery | El hallazgo del cuerpo de Rantaro |
| Kaede Akamatsu? | ¿Kaede Akamatsu? |
| The Mastermind's Crimes | Los crímenes de la Mente Maestra |
| 15 Trapped Students | 15 estudiantes atrapados |
| The Death of Junko Enoshima | La muerte de Junko Enoshima |
| Flashback Light Blackboard | Pizarrón de la Linterna Flashback |
| Tsumugi's Flashback Light | La Linterna Flashback de Tsumugi |
| Fabricated Memories | Recuerdos fabricados |
| Fiction and Reality | Ficción y realidad |
| Escape from Fiction | Escape de la ficción |
| Beyond the Wall | Más allá del muro |
| Hope or an Abyss? | ¿Esperanza o abismo? |
| What Lies Ahead | Lo que nos espera |
| The Final Scene | La escena final |
| Love Across the Universe | Amor a través del universo |
| Ultimate Intro: Shuichi Saihara | Presentación definitiva: Shuichi Saihara |
| Ultimate Intro: Kaito Momota | Presentación definitiva: Kaito Momota |
| Ultimate Intro: Ryoma Hoshi | Presentación definitiva: Ryoma Hoshi |
| Ultimate Intro: Rantaro Amami | Presentación definitiva: Rantaro Amami |
| Ultimate Intro: Gonta Gokuhara | Presentación definitiva: Gonta Gokuhara |
| Ultimate Intro: Kokichi Ouma | Presentación definitiva: Kokichi Ouma |
| Ultimate Intro: Korekiyo Shinguji | Presentación definitiva: Korekiyo Shinguji |
| Ultimate Intro: K1-B0 | Presentación definitiva: K1-B0 |
| Ultimate Intro: Kirumi Tojo | Presentación definitiva: Kirumi Tojo |
| Ultimate Intro: Himiko Yumeno | Presentación definitiva: Himiko Yumeno |
| Ultimate Intro: Maki Harukawa | Presentación definitiva: Maki Harukawa |
| Ultimate Intro: Tenko Chabashira | Presentación definitiva: Tenko Chabashira |
| Ultimate Intro: Tsumugi Shirogane | Presentación definitiva: Tsumugi Shirogane |
| Ultimate Intro: Angie Yonaga | Presentación definitiva: Angie Yonaga |
| Ultimate Intro: Miu Iruma | Presentación definitiva: Miu Iruma |
| Ultimate Intro: Kaede Akamatsu | Presentación definitiva: Kaede Akamatsu |
| Ultimate Intro: Monokuma | Presentación definitiva: Monokuma |
| New Ultimate Intro: Junko Enoshima | Nueva presentación definitiva: Junko Enoshima |
| Ultimate Intro: Hope Robot | Presentación definitiva: Hope Robot |
| Monokuma Theater 1 (Cap. 1) | Teatro Monokuma 1 (Cap. 1) |
| Monokuma Theater 2 (Cap. 1) | Teatro Monokuma 2 (Cap. 1) |
| Monokuma Theater 3 (Cap. 1) | Teatro Monokuma 3 (Cap. 1) |
| Monokuma Theater 4 (Cap. 2) | Teatro Monokuma 4 (Cap. 2) |
| Monokuma Theater 5 (Cap. 2) | Teatro Monokuma 5 (Cap. 2) |
| Monokuma Theater 6 (Cap. 2) | Teatro Monokuma 6 (Cap. 2) |
| Monodam Theater 1 (Cap. 3) | Teatro Monodam 1 (Cap. 3) |
| Monodam Theater 2 (Cap. 3) | Teatro Monodam 2 (Cap. 3) |
| Monodam Theater 3 (Cap. 3) | Teatro Monodam 3 (Cap. 3) |
| Monokuma Theater 7 (Cap. 4) | Teatro Monokuma 7 (Cap. 4) |
| Monokuma Theater 8 (Cap. 4) | Teatro Monokuma 8 (Cap. 4) |
| Monokuma Theater 9 (Cap. 5) | Teatro Monokuma 9 (Cap. 5) |
| Monokuma Theater 10 (Cap. 5) | Teatro Monokuma 10 (Cap. 5) |
| Monokuma Theater 11 (Cap. 5) | Teatro Monokuma 11 (Cap. 5) |
| Monokuma Theater 12 (Cap. 5) | Teatro Monokuma 12 (Cap. 5) |
| Monokuma Theater 4 (Cap. 1) | Teatro Monokuma 4 (Cap. 1) |
| Monokuma Theater 7 (Cap. 2) | Teatro Monokuma 7 (Cap. 2) |
| Monokuma Theater 1 (Cap. 3) | Teatro Monokuma 1 (Cap. 3) |
| Monokuma Theater 2 (Cap. 3) | Teatro Monokuma 2 (Cap. 3) |
| Monokuma Theater 9 (Cap. 4) | Teatro Monokuma 9 (Cap. 4) |
| Monokuma Theater 13 (Cap. 5) | Teatro Monokuma 13 (Cap. 5) |
| Monokuma & Monokubs Theater 1 | Teatro de Monokuma y los Monokubs 1 |
| Monokuma & Monokubs Theater 2 | Teatro de Monokuma y los Monokubs 2 |
| Monokuma & Monokubs Theater 3 | Teatro de Monokuma y los Monokubs 3 |
| Monokuma & Monokubs Theater 4 | Teatro de Monokuma y los Monokubs 4 |
| Monokuma & Monokubs Theater 5 | Teatro de Monokuma y los Monokubs 5 |
</details>

<details>
<summary><b>Nombres de la galería que se tradujeron (videos)</b></summary>

| En inglés | En español |
|---|---|
| Staff Roll | Créditos |
| Promo Movie | Video promocional |
| The Monokubs Arrive | Llegan los Monokubs |
| The 16 Transform | La transformación de los 16 |
| Epilogue | Epílogo |
| Promo Movie Revisited | Video promocional revisitado |
| Punishment: Der Flohwalzer | Castigo: Der Flohwalzer |
| Punishment: Strand of Agony | Castigo: Hilo de agonía |
| Punishment: Cultural Melting Pot | Castigo: Crisol cultural |
| Punishment: Wild West Insecticide | Castigo: Insecticida del Viejo Oeste |
| Punishment: Blast Off! 2do Ignition | Castigo: ¡Despegue! 2.ª ignición |
| Punishment: Ultimate Annihilation | Castigo: Aniquilación definitiva |
| The Suspect Arrives | Llega el sospechoso |
| Rantaro's Body Discovery | El hallazgo del cuerpo de Rantaro |
| Ryoma's Body Discovery | El hallazgo del cuerpo de Ryoma |
| Angie's Body Discovery | El hallazgo del cuerpo de Angie |
| Tenko's Body Discovery | El hallazgo del cuerpo de Tenko |
| Miu's Body Discovery | El hallazgo del cuerpo de Miu |
| Kaito's? Body Discovery | ¿El hallazgo del cuerpo de Kaito? |
| Kokichi's Body Discovery | El hallazgo del cuerpo de Kokichi |
| The Elevator Descends | El ascensor desciende |
| Magic Key | Llave mágica |
| The Barrier Falls | Cae la barrera |
| Escape from the Academy | Escape de la academia |
| The Door to the Future | La puerta al futuro |
| K1-B0 Returns | El regreso de K1-B0 |
| The End of Danganronpa | El fin de Danganronpa |
| Trial Ground Transformation (Cap.1) | Transformación del Santuario del Juicio (Cap. 1) |
| Trial Ground Transformation (Cap.2) | Transformación del Santuario del Juicio (Cap. 2) |
| Trial Ground Transformation (Cap.3) | Transformación del Santuario del Juicio (Cap. 3) |
| Trial Ground Transformation (Cap.4) | Transformación del Santuario del Juicio (Cap. 4) |
| Trial Ground Transformation (Cap.5) | Transformación del Santuario del Juicio (Cap. 5) |
| Trial Ground Transformation (Cap.6) | Transformación del Santuario del Juicio (Cap. 6) |
| Kaede's Flashback Light | La Linterna Flashback de Kaede |
| Monokuma Arrives | Llega Monokuma |
| Shuichi's Flashback Light | La Linterna Flashback de Shuichi |
| Cap. 5 Flashback Light | Linterna Flashback del Cap. 5 |
| Remember | Recuerda |
| K1-B0's Rampage | El arrebato de K1-B0 |
| Vote: Cap.1 "Kaede Akamatsu" | Votación: Cap. 1 "Kaede Akamatsu" |
| Vote: Cap. 2 "Kirumi Tojo" | Votación: Cap. 2 "Kirumi Tojo" |
| Vote: Cap.3 "Korekiyo Shinguji" | Votación: Cap. 3 "Korekiyo Shinguji" |
| Vote: Cap.4 "Gonta Gokuhara" | Votación: Cap. 4 "Gonta Gokuhara" |
| Vote: Cap.5 "Kaito Momota" | Votación: Cap. 5 "Kaito Momota" |
| Vote: Cap.6 "Tsumugi Shirogane" | Votación: Cap. 6 "Tsumugi Shirogane" |
| Santuario del Juicio Elevator | Ascensor al Santuario del Juicio |
| Ancient Passport | Pasaporte Antiguo |
| Dragon Gem | Gema de Dragón |
| Hexagon Crank | Manivela Hexagonal |
| Ninja Scroll | Pergamino Ninja |
| Golden Hammer | Martillo Dorado |
| Levistone | Cristal de Volucita |
| Octobrush | Cefalocepillo |
| Academy Annihilation | Aniquilación de la academia |
| Santuario del Juicio Elevator Cap. 6 | Ascensor al Santuario del Juicio Cap. 6 |
| Recibidor Annihilation | Aniquilación del recibidor |
| Patio Annihilation | Aniquilación del patio |
| Virtual World Trip | Viaje al Mundo Virtual |
| K1-B0 Attacks | K1-B0 ataca |
</details>

<details>
<summary><b>Objetos del mapa que se tradujeron</b></summary>

Los nombres que aparecen al apuntar a algo mientras exploras, en orden alfabético.

| En inglés | En español |
|---|---|
| 1st Floor | 1er Piso |
| 1st Floor Hallway | Pasillo del 1er Piso |
| 2nd Floor | 2do Piso |
| 3F Research Lab A ※Already removed | Laboratorio A del 3er Piso ※Ya eliminado |
| 3F Research Lab B ※Already removed | Laboratorio B del 3er Piso ※Ya eliminado |
| 3rd Floor | 3er Piso |
| 4th Floor | 4to Piso |
| 5.1ch Speaker | Altavoz 5.1 |
| 5th Floor | 5to Piso |
| A/V Room | Sala de Medios A/V |
| Above the Bookcase | Encima del Librero |
| Air Vent | Ventilación |
| Alarm System | Sistema de Alarma |
| Angie's Body | Cadáver de Angie |
| Arranged Books | Libros Ordenados |
| Back Bookcase | Librero del Fondo |
| Back Door | Puerta Trasera |
| Back of the Library | Fondo de la Biblioteca |
| Back Sliding Door | Puerta Corrediza Trasera |
| Backyard | Patio Trasero |
| Balance Pole | Barra de Equilibrio |
| Bar Set | Barra de Bar |
| Barbed Wire | Alambre de Púas |
| Barrier | Barrera |
| Basement | Sótano |
| Basketball Net | Canasta de Básquetbol |
| Bathroom Door | Puerta del Baño |
| Bathroom Window | Ventana del Baño |
| Bed | Cama |
| Behind the Stage | Detrás del Escenario |
| Birdcage | Jaula de Pájaro |
| Bit of Clothing | Trozo de Ropa |
| Bits of Fabric | Trozos de Tela |
| Black & White Door | Puerta Blanca y Negra |
| Black Case | Estuche Negro |
| Blackboard | Pizarrón |
| Bloodstain | Mancha de Sangre |
| Bloodstained Board | Tabla Ensangrentada |
| Bloody Shot Put Ball | Bola de Peso Ensangrentada |
| Bloody Sickle | Hoz Ensangrentada |
| Bloody Tank | Tanque Ensangrentado |
| Body Sawing Box | Caja para Serrar Personas |
| Book | Libro |
| Bookcase | Librero |
| Bookshelf | Estante de Libros |
| Box of Documents | Caja de Documentos |
| Boys Bathroom | Baño de Chicos |
| Broken Tank | Tanque Roto |
| Bronze Dragon Statue | Estatua de Dragón de Bronce |
| Bucket | Cubeta |
| Bug Cage | Jaula de Insectos |
| Bundled Cord | Cable Enrollado |
| Cabinet 1 | Gabinete 1 |
| Cable In | Entrada de Cable |
| Cable Out | Salida de Cable |
| Card Reader | Lector de Tarjetas |
| Casino Area | Área de Casino |
| Cauldron | Caldero |
| Cave Wall | Pared de la Cueva |
| CD Rack | Estante de CD |
| Center Room | Sala Central |
| Central Chair | Silla Central |
| Chair | Silla |
| Chandelier | Candelabro |
| Chemicals Shelf | Estante de Químicos |
| Child | Niño |
| Classroom | Aula |
| Classroom A | Aula A |
| Classroom B | Aula B |
| Classroom C | Aula C |
| Clean Floor | Piso Limpio |
| Cleaning Machine | Máquina de Limpieza |
| Clock | Reloj |
| Closed Curtain | Cortina Cerrada |
| Closed Door | Puerta Cerrada |
| Closed Window | Ventana Cerrada |
| Closet | Clóset |
| Closet Door | Puerta del Clóset |
| Cloth | Tela |
| Cluttered Books | Libros Desordenados |
| Cockpit | Cabina |
| Collected Evidence | Pruebas Reunidas |
| Computer | Computadora |
| Computer Room | Sala de Cómputo |
| Crane | Grúa |
| Crooked Floorboard | Tabla Torcida |
| Crossbow | Ballesta |
| Crossbow Arrow | Flecha de Ballesta |
| Crystal Ball | Bola de Cristal |
| Curled Up Tenko | Tenko Acurrucada |
| Curtain | Cortina |
| Cut Crosspiece | Travesaño Cortado |
| Dealer Mask | Máscara de Crupier |
| Desk | Escritorio |
| Dining Hall | Comedor |
| Dining Table | Mesa del Comedor |
| Disposable Camera | Cámara Desechable |
| Diving Board | Trampolín |
| Documents | Documentos |
| Dog Statue | Estatua de Perro |
| Dog Statue on Iron Cage | Estatua de Perro sobre la Jaula |
| Door | Puerta |
| Door to Hallway | Puerta al Pasillo |
| Dormitory | Dormitorio |
| Down the Big Stairs | Bajando las Escaleras Grandes |
| Drawer | Cajón |
| Dried Blood | Sangre Seca |
| Electric Barrier | Barrera Eléctrica |
| Electrohammer | Electromartillo |
| Emblem | Emblema |
| End of Hallway | Final del Pasillo |
| Entrance Door | Puerta de Entrada |
| Exchange Counter | Caja de Cambio |
| Exhibit Case | Vitrina |
| Exisal Blue | Exisal Azul |
| Exisal Green | Exisal Verde |
| Exisal Pink | Exisal Rosa |
| Exisal Red | Exisal Rojo |
| Exisal Yellow | Exisal Amarillo |
| Exit Signboard | Letrero de Salida |
| Extravagant Door | Puerta Extravagante |
| Fake Money | Dinero Falso |
| Family | Familia |
| Filming Set | Set de Filmación |
| Firearms | Armas de Fuego |
| Flashback Light | Linterna Flashback |
| Floor | Piso |
| Floor With Removed Floorboard | Piso sin una Tabla |
| Folded Cloth | Tela Doblada |
| Front Bookcase | Librero del Frente |
| Front Door | Puerta Principal |
| Front Double Doors | Puertas Dobles del Frente |
| Futuristic Art | Arte Futurista |
| Game Room | Sala de Juegos |
| Geometric Pattern Door | Puerta con Diseño Geométrico |
| Giant Door | Puerta Gigante |
| Giant Studio Set | Set de Estudio Gigante |
| Giant Vault | Bóveda Gigante |
| Giant Wooden Doll | Muñeco de Madera Gigante |
| Girls Bathroom | Baño de Chicas |
| Glass | Vidrio |
| Glass Bottle | Botella de Vidrio |
| Glass Panel | Panel de Vidrio |
| Globe | Globo Terráqueo |
| Gold Leaf Katana | Katana Batida en Oro |
| Grass | Pasto |
| Guillotine | Guillotina |
| Gym | Gimnasio |
| Gym Window | Ventana del Gimnasio |
| Half Broken Door | Puerta Medio Rota |
| Hammer on Dolly | Martillo sobre Carretilla |
| Handcuffs | Esposas |
| Hangar Security Lamp | Lámpara de Seguridad del Hangar |
| Hangar Shutter | Portón del Hangar |
| Hanging Paper | Papel Colgado |
| Hanging Scroll | Pergamino Colgante |
| Hanging Wax Doll of Kaede | Efigie Colgada de Kaede |
| Hanging Wax Doll of Kirumi | Efigie Colgada de Kirumi |
| Hanging Wax Doll of Rantaro | Efigie Colgada de Rantaro |
| Hanging Wax Doll of Ryoma | Efigie Colgada de Ryoma |
| Helicopter | Helicóptero |
| Helicopter Controller | Control del Helicóptero |
| Hexagonal Protrusion | Saliente Hexagonal |
| Hidden Monokuma No. 1 | Monokuma Oculto N.º 1 |
| Hidden Monokuma No. 10 | Monokuma Oculto N.º 10 |
| Hidden Monokuma No. 11 | Monokuma Oculto N.º 11 |
| Hidden Monokuma No. 12 | Monokuma Oculto N.º 12 |
| Hidden Monokuma No. 13 | Monokuma Oculto N.º 13 |
| Hidden Monokuma No. 14 | Monokuma Oculto N.º 14 |
| Hidden Monokuma No. 15 | Monokuma Oculto N.º 15 |
| Hidden Monokuma No. 16 | Monokuma Oculto N.º 16 |
| Hidden Monokuma No. 17 | Monokuma Oculto N.º 17 |
| Hidden Monokuma No. 18 | Monokuma Oculto N.º 18 |
| Hidden Monokuma No. 19 | Monokuma Oculto N.º 19 |
| Hidden Monokuma No. 2 | Monokuma Oculto N.º 2 |
| Hidden Monokuma No. 20 | Monokuma Oculto N.º 20 |
| Hidden Monokuma No. 21 | Monokuma Oculto N.º 21 |
| Hidden Monokuma No. 22 | Monokuma Oculto N.º 22 |
| Hidden Monokuma No. 23 | Monokuma Oculto N.º 23 |
| Hidden Monokuma No. 24 | Monokuma Oculto N.º 24 |
| Hidden Monokuma No. 25 | Monokuma Oculto N.º 25 |
| Hidden Monokuma No. 26 | Monokuma Oculto N.º 26 |
| Hidden Monokuma No. 27 | Monokuma Oculto N.º 27 |
| Hidden Monokuma No. 28 | Monokuma Oculto N.º 28 |
| Hidden Monokuma No. 29 | Monokuma Oculto N.º 29 |
| Hidden Monokuma No. 3 | Monokuma Oculto N.º 3 |
| Hidden Monokuma No. 30 | Monokuma Oculto N.º 30 |
| Hidden Monokuma No. 4 | Monokuma Oculto N.º 4 |
| Hidden Monokuma No. 5 | Monokuma Oculto N.º 5 |
| Hidden Monokuma No. 6 | Monokuma Oculto N.º 6 |
| Hidden Monokuma No. 7 | Monokuma Oculto N.º 7 |
| Hidden Monokuma No. 8 | Monokuma Oculto N.º 8 |
| Hidden Monokuma No. 9 | Monokuma Oculto N.º 9 |
| Hidden Passage Entrance | Entrada al Pasadizo Oculto |
| Hidden Room | Habitación Secreta |
| High Jump Bar | Barra de Salto Alto |
| Hole | Agujero |
| Hole in the Corner | Agujero en la Esquina |
| Hole in the Floor | Agujero en el Piso |
| Hologram | Holograma |
| Hologram Display | Pantalla Holográfica |
| Hurdle | Valla |
| Hydraulic Press | Prensa Hidráulica |
| Indirect Lighting | Luz Indirecta |
| Innertube | Flotador |
| Insect Specimens | Especímenes de Insectos |
| Iron Cage | Jaula de Hierro |
| Iron Cage Covering Something | Jaula de Hierro Cubriendo Algo |
| Kaito Lab ※Already removed | Laboratorio de Kaito ※Ya eliminado |
| Key | Llave |
| Key Stand | Soporte de Llaves |
| Keyhole | Cerradura |
| Kitchen Entrance | Entrada a la Cocina |
| Knife | Cuchillo |
| Knives Hanging on the Wall | Cuchillos Colgados en la Pared |
| Kokichi's Clothes | Ropas de Kokichi |
| Ladder | Escalera de Mano |
| Large Door | Puerta Grande |
| Large Hole | Agujero Grande |
| Large Round Door | Puerta Redonda Grande |
| Large Water Tank | Tanque de Agua Grande |
| Left Door | Puerta Izquierda |
| Left Empty Room | Sala Vacía - Izquierda |
| Left Room | Sala Izquierda |
| Library | Biblioteca |
| Light Panel | Panel de Luz |
| Lighting | Iluminación |
| Lit Candle | Vela Encendida |
| Lock | Candado |
| Locker | Casillero |
| Love Suite | Suite del Amor |
| Lump of Wax | Trozo de Cera |
| Magic Circle | Círculo Mágico |
| Manhole | Alcantarilla |
| Manhole Cover | Tapa de Alcantarilla |
| Manhole Cover Used for Reference | Tapa de Alcantarilla de Referencia |
| Marker Stone | Piedra Marcadora |
| Mat | Colchoneta |
| Metal Cage | Jaula de Metal |
| Metal Rods | Barras de Metal |
| Middle Bookcase | Librero del Medio |
| Middle Empty Room | Sala Vacía - Medio |
| Modified Camera | Cámara Modificada |
| Monokuma Statue | Estatua de Monokuma |
| Monokuma USB | USB de Monokuma |
| Monomono Machine | Máquina MonoMono |
| Monomono Slot | Tragamonedas MonoMono |
| Mountain of Weapons | Montaña de Armas |
| Moving Bookcase | Estantería Móvil |
| Moving Ladder | Escalera Móvil |
| Music Stand | Atril |
| Mysterious Letters | Cartas Misteriosas |
| Mysterious Machine | Máquina Misteriosa |
| Mysterious Monument | Monumento Misterioso |
| Nameplate | Placa con Nombre |
| Near Miu's Body | Cerca del Cadáver de Miu |
| Near the Body | Cerca del Cadáver |
| Near the Water Tank | Cerca del Tanque de Agua |
| Neon Signboard | Letrero de Neón |
| Ninja Statue | Estatua de Ninja |
| Object 0 | Objeto 0 |
| Object 1 | Objeto 1 |
| Object 2 | Objeto 2 |
| Object 3 | Objeto 3 |
| Object 4 | Objeto 4 |
| Object 5 | Objeto 5 |
| Object 6 | Objeto 6 |
| Object 7 | Objeto 7 |
| Object 8 | Objeto 8 |
| Object 9 | Objeto 9 |
| Object with Indentation | Objeto con una Hendidura |
| Open Door | Puerta Abierta |
| Open Moving Bookcase | Estantería Móvil Abierta |
| Open Window | Ventana Abierta |
| Operation Panel | Panel de Control |
| Organized Books | Libros Organizados |
| Overgrown Grass | Pasto Crecido |
| Painting Machine | Máquina de Pintura |
| Passage Entrance | Entrada al Pasadizo |
| Photographic Developer | Revelador Fotográfico |
| Piranha Tank | Tanque de Pirañas |
| Piranhas | Pirañas |
| Planetarium Device | Proyector de Planetario |
| Plants | Plantas |
| Pod | Cápsula |
| Pole Scaffold | Andamio de Tubos |
| Pool | Piscina |
| Pool Entrance | Entrada a la Piscina |
| Pool of Blood | Charco de Sangre |
| Poster Bucket | Cubeta del Póster |
| Premium Exchange Counter | Caja de Cambio Premium |
| Press Operation Panel | Panel de Control de la Prensa |
| Projector | Proyector |
| Puddle | Charco |
| Rantaro's Body | Cadáver de Rantaro |
| RC Helicopter | Helicóptero a Control Remoto |
| Rear Sliding Door | Puerta Corrediza Trasera |
| Right Door | Puerta Derecha |
| Right Empty Room | Sala Vacía - Derecha |
| Right Room | Sala Derecha |
| Rocking Chair | Mecedora |
| Rope | Cuerda |
| Rotating Bed | Cama Giratoria |
| Rubble | Escombros |
| Ruined Magic Circle | Círculo Mágico Arruinado |
| Rules | Reglas |
| Rules Sign | Letrero de Reglas |
| Russian Roulette Gun | Pistola de Ruleta Rusa |
| Ryoma's Belongings | Pertenencias de Ryoma |
| Ryoma's Body | Cadáver de Ryoma |
| Saw | Sierra |
| School Building | Edificio Principal |
| School Building Window | Ventana del Edificio Principal |
| School Store | Tienda Escolar |
| Scoreboard | Marcador |
| Screen | Pantalla |
| Scroll | Pergamino |
| Shelf | Estante |
| Shot Put Ball | Bola de Peso |
| Showcase | Vitrina |
| Shower Room | Sala de Ducha |
| Shrine of Judgment | Santuario del Juicio |
| Shutter Operation Panel | Panel de Control del Portón |
| Side of School Building | Costado del Edificio Principal |
| Sink | Lavabo |
| Sliding Door | Puerta Corrediza |
| Small Bottle | Botellita |
| Small Glass Bottles | Botellitas de Vidrio |
| Small Table | Mesita |
| Small Water Tank | Tanque de Agua Pequeño |
| Sofa | Sofá |
| Sofa A | Sofá A |
| Sofa B | Sofá B |
| Speakers | Altavoces |
| Special Modified Camera | Cámara Modificada Especial |
| Stage | Escenario |
| Stage Staircase | Escaleras del Escenario |
| Stairs | Escaleras |
| Stairs to 1st Floor | Escaleras al 1er Piso |
| Storage Room Door | Puerta del Almacén |
| Supercar | Superauto |
| Suspended Scaffold | Andamio Colgante |
| Suspended Water Tank | Tanque de Agua Colgante |
| Sword Stabbing Box | Caja de Espadas |
| Table | Mesa |
| Teacher's Desk | Escritorio del Profesor |
| Tenko's Body | Cadáver de Tenko |
| Tennis Net | Red de Tenis |
| Terrace Door | Puerta de la Terraza |
| Thick Metal Door | Puerta de Metal Gruesa |
| Things on the Desk | Cosas sobre el Escritorio |
| Timer | Temporizador |
| Toilet | Inodoro |
| Torn Power Cord | Cable de Corriente Roto |
| Traces of Blood | Rastros de Sangre |
| Trap | Trampa |
| Trash Can | Bote de Basura |
| Trashed Room | Habitación Destrozada |
| Treasure Chest | Cofre del Tesoro |
| Tree Root | Raíz de Árbol |
| Ultimate ??? Lab | Laboratorio del ??? Definitivo |
| Ultimate Aikido Master Lab | Laboratorio de la Maestra del Aikido Definitiva |
| Ultimate Anthropologist Lab | Laboratorio del Antropólogo Definitivo |
| Ultimate Anthropologist Lab (Rear) | Laboratorio del Antropólogo Definitivo (Fondo) |
| Ultimate Artist Lab | Laboratorio de la Artista Definitiva |
| Ultimate Artist Lab (Rear) | Laboratorio de la Artista Definitiva (Fondo) |
| Ultimate Assassin Lab | Laboratorio de la Asesina Definitiva |
| Ultimate Astronaut Lab | Laboratorio del Astronauta Definitivo |
| Ultimate Cosplayer Lab | Laboratorio de la Cosplayer Definitiva |
| Ultimate Detective Lab | Laboratorio del Detective Definitivo |
| Ultimate Entomologist Lab | Laboratorio del Entomólogo Definitivo |
| Ultimate Inventor Lab | Laboratorio de la Inventora Definitiva |
| Ultimate Magician Lab | Laboratorio de la Maga Definitiva |
| Ultimate Maid Lab | Laboratorio de la Mucama Definitiva |
| Ultimate Pianist Lab | Laboratorio de la Pianista Definitiva |
| Ultimate Robot Lab | Laboratorio del Robot Definitivo |
| Ultimate Tennis Pro Lab | Laboratorio del Tenista Pro Definitivo |
| Underground Stairs | Escaleras Subterráneas |
| Utility Closet | Cuarto de Servicio |
| Utility Closet Wall | Pared del Cuarto de Servicio |
| Video Player | Reproductor de Video |
| Video Rack | Estante de Videos |
| Warehouse | Almacén |
| Washing Machine | Lavadora |
| Wax Doll of Kaede | Efigie de Cera de Kaede |
| Wax Doll of Kirumi | Efigie de Cera de Kirumi |
| Wax Doll of Rantaro | Efigie de Cera de Rantaro |
| Wax Doll of Ryoma | Efigie de Cera de Ryoma |
| Weapon Shelf | Estante de Armas |
| White Cloth | Sábana Blanca |
| White Cloth Over Something | Sábana Blanca Cubriendo Algo |
| Window | Ventana |
| Work Table | Mesa de Trabajo |
| Workshop | Taller |
| Yasuhiro's Body | Cadáver de Yasuhiro |
</details>

Los textos completos del casino, las reglas y el Teatro Monokuma (unas 300 líneas) están en `tools/correcciones/galeria.tsv`.

<details>
<summary><b>Palabras que cambiaron en esta versión</b></summary>

| Antes (v2.5) | Ahora (v2.6) | Veces | En inglés |
|---|---|---:|---|
| Debate Sin Freno | Debate Continuo | 130 | Non-Stop Debate |
| Duelo de Refutación | Confrontación Refutadora | 24 | Rebuttal Showdown |
| Argumento de Cierre | Clímax Lógico | 14 | Closing Argument |
| Deducción de Ahorcado | Epifanía Anagrámica | 19 | Hangman's Gambit |
| Monocoins | Medallas Monokuma | 40 | Monocoins |
| Archivo Monokuma | Ficha Monokuma | 56 | Monokuma File |
| Cuida Niños Definitiva | Cuidadora Definitiva | 18 | Ultimate Child Caregiver |
| Balas de Verdad / Municiones de la Verdad | Municiones de Verdad | 12 | Truth Bullets |

No cambiaron porque ya coincidían con DR1 y DR2: Juicio Escolar, Munición, Mente Maestra y Kibougamine.
</details>

### Novedades de la v2.5 (fork)

* **Menú de pausa traducido**: los títulos del menú de pausa son imágenes, no texto. Ahora aparecen en español usando las letras del propio juego, con la misma fuente y el mismo brillo: SAVE → GUARDAR, LOAD → CARGAR, OPTION → OPCIONES, MAIN MENU → MENÚ PRINCIPAL, DRESS UP → PROBADOR y BACKLOG → REGISTRO.
* **Restaurar** (`restaurar.bat` / `restaurar.sh`): vuelve al juego original o a cualquier versión del parche que hayas tenido instalada. Consulta [cómo restaurar](#-desinstalar-o-volver-a-una-versión-anterior).
* **Respaldos dentro del juego**: el instalador ahora guarda los respaldos en `killer-harmony-backup`, dentro de la carpeta del juego, para que no se pierdan al descargar una versión nueva del parche. Los respaldos de instaladores anteriores (`backup_en`) se trasladan solos.
* **Herramientas para las imágenes de la interfaz (`tools/`)**:
  * `drv3srd.py`: exporta las texturas de los `.spc` a PNG e importa los PNG editados (deben conservar el tamaño original).
  * `rotulos.py` + `rotulos/*.json`: genera rótulos en español recortando y combinando las letras de las texturas del juego.

<details>
<summary><b>Rótulos que cambiaron en esta versión</b></summary>

| Antes (inglés, imagen) | Ahora (v2.5) |
|---|---|
| SAVE | GUARDAR |
| LOAD | CARGAR |
| OPTION | OPCIONES |
| MAIN MENU | MENÚ PRINCIPAL |
| DRESS UP | PROBADOR |
| BACKLOG | REGISTRO |

No cambió ningún término del texto en esta versión.
</details>

### Novedades de la v2.4 (fork)

* **Palabras destacadas pegadas (capítulo 1)**: el juego no agrega espacios alrededor de las palabras resaltadas, por lo que textos como "delPianista Definitivosabe" aparecían pegados. Esto ya estaba corregido en los capítulos 2 a 6, pero faltaba el capítulo 1: se corrigieron **496 líneas**, incluidas las frases con cambio de tamaño de los debates.
* **Puntuación**: comas dobles (`Shuichi,,`) y puntos suspensivos incompletos (`Jeje..`, `¡Kh..!`, o partidos por un salto de línea).
* **Herramientas**: nuevo `tools/separar_etiquetas.py`, que agrega el espacio que falta junto a las etiquetas de formato, y soporte para reglas con expresiones regulares (`~`) en `erratas.tsv`.

<details>
<summary><b>Correcciones de puntuación de esta versión</b></summary>

El salto de línea se muestra como ⏎.

**Puntuacion duplicada o incompleta** (5)

| Antes | Ahora |
|---|---|
| `,,` | `,` |
| `,..Pero` | `...Pero` |
| `.⏎.. ` | `...⏎` |
| `sobrevivir..⏎..Incluso` | `sobrevivir...⏎...Incluso` |

Además, todos los puntos suspensivos de solo dos puntos (`..`) pasaron a tres (`...`). Las 496 líneas con palabras destacadas pegadas solo recibieron el espacio que faltaba; no cambió ninguna palabra.
</details>

### Novedades de la v2.3 (fork)

Esta versión es un fork del [parche original](https://github.com/ManuelCMS/killer-harmony) con estos cambios:

* **Corrección de erratas (460 líneas)**: se revisaron todos los textos de la versión más reciente contra un diccionario de español y se corrigieron, una por una, las erratas que se le pasaron a la traducción:
  * Letras cambiadas, faltantes o sobrantes (`acompñamiento`, `duriante`, `santurario`, `pisicna`, `veredcito`...).
  * Palabras pegadas (`ahoramismo`, `estáactuando`, `evidenciaen`...).
  * Tildes y diéresis (`huír`, `crímen`, `pónte`, `vergenza`...).
  * Verbos mal conjugados (`abstenimos`, `hicista`, `entendrás`, `veniste`...).
  * Se respetaron a propósito los tartamudeos, las palabras cortadas, los juegos de palabras, la jerga y la forma de hablar de cada personaje.
  * La versión v0.1 no se modificó.
* **Instalador más seguro (`patch.ps1`)**:
  * Si falla la extracción de un CPK, la instalación se detiene **sin borrar** los archivos originales del juego (antes los borraba igual).
  * Si falta solo alguno de los CPK, los demás se extraen en lugar de borrarse sin extraer.
  * Se comprueba que la carpeta del parche exista antes de tocar el juego, y se informan los errores de copia en vez de indicar siempre "éxito".
  * La detección de la carpeta de diálogos (`wrd_script`) ya no se confunde con carpetas que dejó un parche anterior.
* **Instalador para Linux / SteamOS (`patch.sh`)**, *experimental*: consulta la sección de [Linux](#-instalación-en-linux--steamos-steam-deck-legion-go-etc).
* **Herramientas para editar los textos (`tools/`)**:
  * `drv3text.py`: extrae los textos de los `.SPC` a un archivo de texto (`dump`) y aplica correcciones (`apply`), sin necesidad de Harmony Tools.
  * `aplicar_erratas.py` + `correcciones/erratas.tsv`: lista de erratas (`texto_erróneo<TAB>texto_correcto`). Para corregir una errata nueva, agrega una línea y ejecuta `python3 tools/aplicar_erratas.py tools/correcciones/erratas.tsv`.

<details>
<summary><b>Erratas que se corrigieron en esta versión</b></summary>

Cada regla corrige también sus variantes con mayúscula inicial y en MAYÚSCULAS. El salto de línea se muestra como ⏎.

**Letras cambiadas, faltantes o sobrantes** (211)

| Antes | Ahora |
|---|---|
| `abilidad` | `habilidad` |
| `acompñamiento` | `acompañamiento` |
| `actualiizados` | `actualizados` |
| `afriman` | `afirman` |
| `agradble` | `agradable` |
| `amenzante` | `amenazante` |
| `ansisosa` | `ansiosa` |
| `apagueb` | `apaguen` |
| `arruniaría` | `arruinaría` |
| `avivava` | `avivaba` |
| `ayudamre` | `ayudarme` |
| `ayudaráía` | `ayudaría` |
| `blancaa` | `blanca` |
| `buchos` | `bichos` |
| `burjo` | `brujo` |
| `cabezasos` | `cabezazos` |
| `callaa` | `callas` |
| `captadp` | `captado` |
| `cargaó` | `cargó` |
| `castrófica` | `catastrófica` |
| `causea` | `causa` |
| `cballeros` | `caballeros` |
| `ciudadanoa` | `ciudadana` |
| `colocqué` | `coloqué` |
| `comparió` | `compartió` |
| `conentración` | `concentración` |
| `confudió` | `confundió` |
| `confuncí` | `confundí` |
| `conpu` | `compu` |
| `considereq` | `considere` |
| `consientidos` | `consentidos` |
| `consiguido` | `conseguido` |
| `consistío` | `consistió` |
| `continurar` | `continuar` |
| `conviertida` | `convertida` |
| `cooperamo` | `cooperamos` |
| `creles` | `crueles` |
| `cryó` | `creyó` |
| `cuchila` | `cuchilla` |
| `dabido` | `sabido` |
| `ded` | `de` |
| `dedcidle` | `decidle` |
| `dedl` | `del` |
| `dedrribar` | `derribar` |
| `definitivmante` | `definitivamente` |
| `definitva` | `definitiva` |
| `defintiva` | `definitiva` |
| `defintivo` | `definitivo` |
| `defnitivo` | `definitivo` |
| `dehabilitar` | `deshabilitar` |
| `demasaida` | `demasiada` |
| `derrana` | `derrama` |
| `descrubrir` | `descubrir` |
| `descubieron` | `descubrieron` |
| `deseperación` | `desesperación` |
| `deshinibida` | `desinhibida` |
| `desonciertan` | `desconciertan` |
| `desperó` | `despertó` |
| `detner` | `detener` |
| `devuélbanme` | `devuélvanme` |
| `diciendoe` | `diciendo` |
| `difficultad` | `dificultad` |
| `dormmido` | `dormido` |
| `dulwe` | `dulce` |
| `duriante` | `durante` |
| `encargamre` | `encargarme` |
| `enegrecido` | `ennegrecido` |
| `enfrfentarlos` | `enfrentarlos` |
| `enredadedras` | `enredaderas` |
| `entendrás` | `entenderás` |
| `entineda` | `entienda` |
| `entoncecs` | `entonces` |
| `equipamento` | `equipamiento` |
| `esbiros` | `esbirros` |
| `escúpleo` | `escúpelo` |
| `esrá` | `está` |
| `estadfadora` | `estafadora` |
| `esterlar` | `estelar` |
| `estrañas` | `extrañas` |
| `ests` | `esta` |
| `esuchó` | `escuchó` |
| `evacución` | `evacuación` |
| `floclore` | `folclore` |
| `fuea` | `fue` |
| `fueraza` | `fuerza` |
| `habierta` | `abierta` |
| `himilko` | `Himiko` |
| `imeginen` | `imaginen` |
| `imporara` | `importara` |
| `imporible` | `imposible` |
| `inconcevible` | `inconcebible` |
| `inicó` | `inició` |
| `inimos` | `vinimos` |
| `inputil` | `inútil` |
| `insensibile` | `insensible` |
| `insginia` | `insignia` |
| `insgnias` | `insignias` |
| `instructiones` | `instrucciones` |
| `interfierencias` | `interferencias` |
| `juguetenado` | `jugueteando` |
| `kibougmaine` | `Kibougamine` |
| `kirum` | `Kirumi` |
| `letero` | `letrero` |
| `lingística` | `lingüística` |
| `llamste` | `llamaste` |
| `llevantar` | `levantar` |
| `lugat` | `lugar` |
| `malechor` | `malhechor` |
| `maneoseadores` | `manoseadores` |
| `manetner` | `mantener` |
| `mencionárterlo` | `mencionártelo` |
| `metalíca` | `metálica` |
| `mientiendo` | `mintiendo` |
| `mimso` | `mismo` |
| `mismísmo` | `mismísimo` |
| `mmalinterpretar` | `malinterpretar` |
| `molestida` | `molestia` |
| `molestémolos` | `molestémoslos` |
| `monkuma` | `Monokuma` |
| `monotar` | `Monotaro` |
| `mononopad` | `Monopad` |
| `murrieron` | `murieron` |
| `muucho` | `mucho` |
| `ncontraste` | `encontraste` |
| `nostoros` | `nosotros` |
| `nostros` | `nosotros` |
| `obetnido` | `obtenido` |
| `obivamente` | `obviamente` |
| `obivo` | `obvio` |
| `ocrrió` | `ocurrió` |
| `ocultsimo` | `ocultismo` |
| `opcíón` | `opción` |
| `orquestrado` | `orquestado` |
| `orquestrando` | `orquestando` |
| `orquestrar` | `orquestar` |
| `ozesnos` | `oseznos` |
| `paraa` | `para` |
| `pareche` | `parece` |
| `pareción` | `pareció` |
| `parpaedeo` | `parpadeo` |
| `patéricos` | `patéticos` |
| `peligroa` | `peligro` |
| `perobabilidad` | `probabilidad` |
| `persuadiendos` | `persuadiendo` |
| `pienese` | `piense` |
| `pisicna` | `piscina` |
| `plam` | `Plan` |
| `pordía` | `podría` |
| `portunidad` | `oportunidad` |
| `posibile` | `posible` |
| `prefrencia` | `preferencia` |
| `pregunstaste` | `preguntaste` |
| `preparanos` | `prepararnos` |
| `preparía` | `prepararía` |
| `preprara` | `prepara` |
| `prese` | `preste` |
| `prisón` | `prisión` |
| `probrar` | `probar` |
| `proviniente` | `proveniente` |
| `pueberto` | `puberto` |
| `puediera` | `pudiera` |
| `puntitaa` | `puntita` |
| `pusto` | `puso` |
| `quedabass` | `quedabas` |
| `quee` | `que` |
| `querdármelo` | `quedármelo` |
| `querete` | `quererte` |
| `quq` | `que` |
| `raguños` | `rasguños` |
| `ralmente` | `realmente` |
| `realida` | `realidad` |
| `referes` | `refieres` |
| `refrescarmer` | `refrescarme` |
| `rendirmos` | `rendirnos` |
| `resisitió` | `resistió` |
| `respeecta` | `respecta` |
| `respero` | `respeto` |
| `reveleador` | `revelador` |
| `rompien` | `rompían` |
| `rrealmente` | `realmente` |
| `sabisdo` | `sabido` |
| `santurario` | `santuario` |
| `sguir` | `seguir` |
| `shuich` | `Shuichi` |
| `siguea` | `sigue` |
| `sirviena` | `sirvienta` |
| `siénese` | `siéntese` |
| `sobresfuerces` | `sobreesfuerces` |
| `tencuidado` | `ten cuidado` |
| `todps` | `todos` |
| `tonero` | `torneo` |
| `traciende` | `trasciende` |
| `tratse` | `tratase` |
| `tsmugi` | `Tsumugi` |
| `uns` | `una` |
| `utela` | `tutela` |
| `vececs` | `veces` |
| `veoo` | `veo` |
| `verdads` | `verdad` |
| `veredcito` | `veredicto` |
| `videdomotivo` | `videomotivo` |
| `videonotivo` | `videomotivo` |
| `vienesd` | `vienes` |
| `vieniendo` | `viniendo` |
| `vivs` | `viva` |
| `von` | `con` |
| `voyeourismo` | `voyeurismo` |
| `vueno` | `bueno` |
| `vverduras` | `verduras` |
| `vvamos` | `vamos` |
| `iniciative` | `iniciativa` |

**Palabras pegadas** (17)

| Antes | Ahora |
|---|---|
| `ahoramismo` | `ahora mismo` |
| `añadidoa` | `añadido a` |
| `aúnmejor` | `aún mejor` |
| `buscómatar` | `buscó matar` |
| `elcuerpo` | `el cuerpo` |
| `élsupiera` | `él supiera` |
| `esla` | `es la` |
| `evidenciaen` | `evidencia en` |
| `haceralgo` | `hacer algo` |
| `mismotablón` | `mismo tablón` |
| `nobiliarioes` | `nobiliario es` |
| `piezade` | `pieza de` |
| `títulode` | `título de` |
| `trucoscon` | `trucos con` |
| `detela` | `de tela` |
| `aTenko` | `a Tenko` |
| `quéte` | `qué te` |

**Tildes y dieresis** (105)

| Antes | Ahora |
|---|---|
| `absténte` | `abstente` |
| `aciérten` | `acierten` |
| `actua` | `actúa` |
| `actúar` | `actuar` |
| `ahogárte` | `ahogarte` |
| `algúnos` | `algunos` |
| `apareceran` | `aparecerán` |
| `aqui` | `aquí` |
| `asi` | `así` |
| `avergenzas` | `avergüenzas` |
| `averigemos` | `averigüemos` |
| `besuquéandose` | `besuqueándose` |
| `calmate` | `cálmate` |
| `casí` | `casi` |
| `castigame` | `castígame` |
| `cállanse` | `cállense` |
| `cómos` | `cómo` |
| `confíar` | `confiar` |
| `confíemos` | `confiemos` |
| `crímen` | `crimen` |
| `dejemoslo` | `dejémoslo` |
| `dejáme` | `déjame` |
| `dejénlo` | `déjenlo` |
| `desnúdemonos` | `desnudémonos` |
| `despiérten` | `despierten` |
| `dáme` | `dame` |
| `dános` | `danos` |
| `dáte` | `date` |
| `déjanmelo` | `déjenmelo` |
| `dénse` | `dense` |
| `dés` | `des` |
| `dínos` | `dinos` |
| `diós` | `dios` |
| `dósis` | `dosis` |
| `emision` | `emisión` |
| `encontraramos` | `encontráramos` |
| `encontre` | `encontré` |
| `entrémos` | `entremos` |
| `escúchen` | `escuchen` |
| `estan` | `están` |
| `estára` | `estará` |
| `estó` | `esto` |
| `estóico` | `estoico` |
| `éstá` | `está` |
| `excavaciónes` | `excavaciones` |
| `facilmente` | `fácilmente` |
| `fenomeno` | `fenómeno` |
| `físicoculturismo` | `fisicoculturismo` |
| `guíar` | `guiar` |
| `hablémos` | `hablemos` |
| `habria` | `habría` |
| `haciéndo` | `haciendo` |
| `hagámos` | `hagamos` |
| `házlo` | `hazlo` |
| `házlos` | `hazlos` |
| `házte` | `hazte` |
| `hipotésis` | `hipótesis` |
| `huímos` | `huimos` |
| `huír` | `huir` |
| `impreción` | `impresión` |
| `incluída` | `incluida` |
| `insinuas` | `insinúas` |
| `interes` | `interés` |
| `jovenes` | `jóvenes` |
| `leiste` | `leíste` |
| `levantámos` | `levantamos` |
| `limpiate` | `límpiate` |
| `malgastándo` | `malgastando` |
| `manténte` | `mantente` |
| `matandome` | `matándome` |
| `mentalizandome` | `mentalizándome` |
| `miralas` | `míralas` |
| `muñon` | `muñón` |
| `omitieramos` | `omitiéramos` |
| `padré` | `padre` |
| `pais` | `país` |
| `páneles` | `paneles` |
| `pásando` | `pasando` |
| `percataramos` | `percatáramos` |
| `ponéos` | `poneos` |
| `pónte` | `ponte` |
| `póngamonos` | `pongámonos` |
| `póngamos` | `pongamos` |
| `prepárandose` | `preparándose` |
| `pudieramos` | `pudiéramos` |
| `quédemonos` | `quedémonos` |
| `refutalo` | `refútalo` |
| `refutála` | `refútala` |
| `reimos` | `reímos` |
| `relajate` | `relájate` |
| `reporténse` | `repórtense` |
| `reuna` | `reúna` |
| `salámos` | `salimos` |
| `sonriendome` | `sonriéndome` |
| `soportenlo` | `sopórtenlo` |
| `sucedio` | `sucedió` |
| `tambaléandose` | `tambaleándose` |
| `tambié` | `también` |
| `tranquilizate` | `tranquilízate` |
| `ustéd` | `usted` |
| `vamonos` | `vámonos` |
| `vergenza` | `vergüenza` |
| `virgenes` | `vírgenes` |
| `véis` | `veis` |
| `comencémos` | `comencemos` |

**Conjugaciones mal formadas** (22)

| Antes | Ahora |
|---|---|
| `abstenimos` | `abstuvimos` |
| `comienzamos` | `comenzamos` |
| `comienzó` | `comenzó` |
| `confiesaré` | `confesaré` |
| `corrije` | `corrige` |
| `elegiera` | `eligiera` |
| `elegió` | `eligió` |
| `eligido` | `elegido` |
| `emperoraste` | `empeoraste` |
| `enamoraía` | `enamoraría` |
| `entiendos` | `entiendo` |
| `exudía` | `exudaba` |
| `hicista` | `hiciste` |
| `reorganizé` | `reorganicé` |
| `seguría` | `seguiría` |
| `transportarté` | `transporté` |
| `tosé` | `tosí` |
| `veniste` | `viniste` |
| `apretan` | `aprietan` |
| `digos` | `digo` |
| `dicee` | `dices` |
| `sabí` | `sabía` |

**Correcciones de frase completa (texto literal exacto)** (37)

| Antes | Ahora |
|---|---|
| `Sí,aspi es.` | `Sí, así es.` |
| `cáda—` | `cadá—` |
| `¿Q-Aué pasaría?` | `¿Q-Qué pasaría?` |
| `discusi[on` | `discusión` |
| `Kibo está siend ocontrolado` | `Kibo está siendo controlado` |
| `Deber+ias` | `Deberías` |
| `No tengo ide de` | `No tengo idea de` |
| `Tal vez fue qen esa época` | `Tal vez fue en esa época` |
| `hasta quí llegué` | `hasta aquí llegué` |
| `en su mano entía` | `en su mano tenía` |
| `¡Wow! ¿¡Tienes caño derebral` | `¡Wow! ¿¡Tienes daño cerebral` |
| `hacía mí a toda velocidad` | `hacia mí a toda velocidad` |
| `y desmayó...` | `y se desmayó...` |
| `Una jaula de insector` | `Una jaula de insectos` |
| `piezas inborrables` | `piezas irrompibles` |
| `Culpable Incognisible` | `Culpable Incognoscible` |
| `No hya forma` | `No hay forma` |
| `¡Os a digo que` | `¡Os digo que` |
| `¡Mis habilidad en baloncesto` | `¡Mi habilidad en baloncesto` |
| `un⏎líbido fuerte` | `una⏎libido fuerte` |
| `Sentémos en algún lugar` | `Sentémonos en algún lugar` |
| `sigoestoy vivo` | `sigo vivo` |
| `Hay una razón p<or la que` | `Hay una razón por la que` |
| `Tienes muchas huevos` | `Tienes muchos huevos` |
| `AOS-MAS TARDE` | `AÑOS-MÁS TARDE` |
| `POBLACIN VIEJA` | `POBLACIÓN VIEJA` |
| `EJECUCIN EXTERIOR` | `EJECUCIÓN EXTERIOR` |
| `LA.MENTE-MAESTRA` | `LA-MENTE-MAESTRA` |
| `<CLT=cltSTRONG>ltimo Pianista` | `<CLT=cltSTRONG>Último Pianista` |
| `HDD. As requieren` | `HDD. Se requieren` |
| `No importa⏎si es se está confiando, o estáactuando...` | `No importa⏎si se está confiando, o está actuando...` |
| `Puedes comenzar casualy mejorar.` | `Puedes comenzar casualmente y mejorar.` |
| `me pareció rar...` | `me pareció rara...` |
| `¡Haría<CLT=size2>unamontón` | `¡Haría<CLT=size2>un montón` |
| `no pudieron conrecoger` | `no pudieron recoger` |
| `Sí. Parecía undergroundpassage.⏎Gontathoughtitmmaybeexit...` | `Sí. Parecía pasajesubterráneo.⏎Gontapensóqueeralasalida...` |
| `del estudiantes coucil` | `del consejo estudiantil` |
</details>

> **Pendiente**: algunos menús que son imágenes (fuera del juicio) todavía están en inglés. Si encuentras uno, o cualquier texto sin traducir, [abre un ticket](https://github.com/bmvargas-751/killer-harmony/issues).

---
## Cómo contribuir al proyecto
¿Quieres apoyar a este proyecto? Si estás jugando la versión más reciente y encuentras un error, [Abre un ticket](https://github.com/ManuelCMS/killer-harmony/issues) para que lo vea. Necesitarás una cuenta de Github para ello, pero es gratis. De lo contrario, puedes seguirme en Youtube y dejar un comentario en el [video](https://youtu.be/kRzn5imhHJc) más reciente del parche, o escríbeme en [Twitter](https://x.com/killerkoikingtv). Ten en cuenta que mensajes y comentarios se pierden, entonces lo mejor es abrir el ticket aquí.

Si quieres hacer una corrección directa del parche, mira la segunda mitad de este [video](https://youtu.be/kRzn5imhHJc) o revisa la wiki de [Harmony Tools](https://github.com/redssu/Harmony-Tools). Puedes editar los textos y reempacar el parche, y yo revisaré los cambios antes de postearlos. 

¿Eres un artista y quieres ayudar a corregir las fuentes que no encajan al 100% en el juego, o los CGs? Abre un ticket, o sube los archivos correspondientes al parche y lo reviso. Si tienes dudas, pero de verdad quieres apoyar con esto, contáctame para que te ayude a hacerlo.

---

## 🛠️ Créditos y Agradecimientos

* Herramientas de extracción y empaquetado: [Harmony Tools](https://github.com/redssu/Harmony-Tools) por **redssu**.
* Proyecto y traducción hecha por mi cuenta, con ayuda de @blackhawk42 para trabajar con algunos archivos de texto.
* Fork v2.3 – v3.5: rótulos del juicio y los capítulos, corrección de erratas y de palabras destacadas pegadas, términos unificados con DR1/DR2, traducción de la galería y del menú de pausa, mejoras del instalador, restauración e instalador para Linux / SteamOS.
