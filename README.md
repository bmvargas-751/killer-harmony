# Parche de Traducción al Español - Danganronpa V3: Killing Harmony v2.5

Este repositorio contiene el script de instalación automática y los archivos correspondientes al parche de traducción al español para **Danganronpa V3: Killing Harmony** (versión de PC). 

> Esta traducción la hice yo solo, para mi comunidad en Youtube. Es mi primera traducción, y estaba originalmente pensada para mi propio uso y el de mi comunidad, comprendiendo que la calidad no es profesional. 

> **Fork v2.5**: esta copia incluye corrección de erratas y de palabras destacadas pegadas, el menú de pausa traducido, un instalador más seguro con opción para restaurar y soporte para Linux / SteamOS. Mira las [novedades del fork](#-novedades-de-la-v25-fork).

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
   * Presiona `S` (o `Enter`) para instalar la versión más reciente (**v2.5**).
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

### 🆕 Novedades de la v2.5 (fork)

* **Menú de pausa traducido**: los títulos del menú de pausa son imágenes, no texto. Ahora aparecen en español usando las letras del propio juego, con la misma fuente y el mismo brillo: SAVE → GUARDAR, LOAD → CARGAR, OPTION → OPCIONES, MAIN MENU → MENÚ PRINCIPAL, DRESS UP → PROBADOR y BACKLOG → REGISTRO.
* **Restaurar** (`restaurar.bat` / `restaurar.sh`): vuelve al juego original o a cualquier versión del parche que hayas tenido instalada. Consulta [cómo restaurar](#-desinstalar-o-volver-a-una-versión-anterior).
* **Respaldos dentro del juego**: el instalador ahora guarda los respaldos en `killer-harmony-backup`, dentro de la carpeta del juego, para que no se pierdan al descargar una versión nueva del parche. Los respaldos de instaladores anteriores (`backup_en`) se trasladan solos.
* **Herramientas para las imágenes de la interfaz (`tools/`)**:
  * `drv3srd.py`: exporta las texturas de los `.spc` a PNG e importa los PNG editados (deben conservar el tamaño original).
  * `rotulos.py` + `rotulos/*.json`: genera rótulos en español recortando y combinando las letras de las texturas del juego.

### Novedades de la v2.4 (fork)

* **Palabras destacadas pegadas (capítulo 1)**: el juego no agrega espacios alrededor de las palabras resaltadas, por lo que textos como "delPianista Definitivosabe" aparecían pegados. Esto ya estaba corregido en los capítulos 2 a 6, pero faltaba el capítulo 1: se corrigieron **496 líneas**, incluidas las frases con cambio de tamaño de los debates.
* **Puntuación**: comas dobles (`Shuichi,,`) y puntos suspensivos incompletos (`Jeje..`, `¡Kh..!`, o partidos por un salto de línea).
* **Herramientas**: nuevo `tools/separar_etiquetas.py`, que agrega el espacio que falta junto a las etiquetas de formato, y soporte para reglas con expresiones regulares (`~`) en `erratas.tsv`.

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

> **Pendiente**: todavía quedan en inglés algunos textos de la galería (los mensajes de Monokuma y el casino) y los nombres de algunos eventos.

---
## Cómo contribuir al proyecto
¿Quieres apoyar a este proyecto? Si estás jugando la versión más reciente y encuentras un error, [Abre un ticket](https://github.com/ManuelCMS/killer-harmony/issues) para que lo vea. Necesitarás una cuenta de Github para ello, pero es gratis. De lo contrario, puedes seguirme en Youtube y dejar un comentario en el [video](https://youtu.be/kRzn5imhHJc) más reciente del parche, o escríbeme en [Twitter](https://x.com/killerkoikingtv). Ten en cuenta que mensajes y comentarios se pierden, entonces lo mejor es abrir el ticket aquí.

Si quieres hacer una corrección directa del parche, mira la segunda mitad de este [video](https://youtu.be/kRzn5imhHJc) o revisa la wiki de [Harmony Tools](https://github.com/redssu/Harmony-Tools). Puedes editar los textos y reempacar el parche, y yo revisaré los cambios antes de postearlos. 

¿Eres un artista y quieres ayudar a corregir las fuentes que no encajan al 100% en el juego, o los CGs? Abre un ticket, o sube los archivos correspondientes al parche y lo reviso. Si tienes dudas, pero de verdad quieres apoyar con esto, contáctame para que te ayude a hacerlo.

---

## 🛠️ Créditos y Agradecimientos

* Herramientas de extracción y empaquetado: [Harmony Tools](https://github.com/redssu/Harmony-Tools) por **redssu**.
* Proyecto y traducción hecha por mi cuenta, con ayuda de @blackhawk42 para trabajar con algunos archivos de texto.
* Fork v2.3 – v2.5: corrección de erratas y de palabras destacadas pegadas, traducción del menú de pausa, mejoras del instalador, restauración e instalador para Linux / SteamOS.
