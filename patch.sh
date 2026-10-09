#!/usr/bin/env bash
# Script de instalacion para el parche de traduccion de Danganronpa V3: Killing Harmony (Linux / SteamOS).
# Equivalente a patch.ps1. HarmonyTools.exe se ejecuta con Wine o, si no esta instalado, con el
# Proton de Steam; todo lo demas (mover, respaldar y copiar archivos) se hace de forma nativa.
#
# Variables de entorno opcionales:
#   HARMONY_TOOLS  Ruta a HarmonyTools (.exe o binario nativo de Linux)
#   WINE           Ruta al ejecutable de wine a usar
#   PROTON         Ruta al script 'proton' a usar (ej. ".../Proton - Experimental/proton")

set -uo pipefail

# -------------------------------------------------------------------------
# Versiones del parche disponibles
# -------------------------------------------------------------------------
VERSION_ACTUAL="v2.7"   # Numero de version mas reciente (solo para mostrar)
CARPETA_ACTUAL="latest" # Carpeta del parche para la version mas reciente
VERSION_BASE="v0.1"     # Version anterior estable (nombre de carpeta y version)

HARMONY_TOOLS_URL="https://github.com/redssu/Harmony-Tools/releases/download/v2.1.0/Harmony-Tools.zip"
CPK_FILES=(partition_data_win.cpk partition_data_win_us.cpk partition_resident_win.cpk)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=comun.sh
source "$SCRIPT_DIR/comun.sh"

# -------------------------------------------------------------------------
# Utilidades de rutas (el juego corre en Proton, que ignora mayusculas/minusculas;
# en Linux "chap0.SPC" y "chap0.spc" serian dos archivos distintos)
# -------------------------------------------------------------------------

# Imprime las entradas de <dir> cuyo nombre coincide con <nombre> sin importar mayusculas.
# La coincidencia exacta va primero.
buscar_ci() {
    local dir="$1" nombre="$2" entrada base
    [[ -e "$dir/$nombre" ]] && printf '%s\n' "$nombre"
    [[ -d "$dir" ]] || return 0
    for entrada in "$dir"/* "$dir"/.[!.]*; do
        [[ -e "$entrada" ]] || continue
        base="${entrada##*/}"
        [[ "$base" != "$nombre" && "${base,,}" == "${nombre,,}" ]] && printf '%s\n' "$base"
    done
    return 0
}

# Resuelve <ruta_relativa> dentro de <base> respetando los nombres que ya existen.
# Para el ultimo componente imprime todas las variantes existentes (o el nombre tal cual si no hay).
resolver_ci() {
    local actual="$1" rel="$2" parte encontrado
    local -a partes variantes
    IFS='/' read -ra partes <<< "$rel"
    local ultimo=$(( ${#partes[@]} - 1 )) i
    for (( i = 0; i < ultimo; i++ )); do
        parte="${partes[i]}"
        encontrado="$(buscar_ci "$actual" "$parte" | head -n 1)"
        actual="$actual/${encontrado:-$parte}"
    done
    mapfile -t variantes < <(buscar_ci "$actual" "${partes[ultimo]}")
    if (( ${#variantes[@]} == 0 )); then
        variantes=("${partes[ultimo]}")
    fi
    for encontrado in "${variantes[@]}"; do
        printf '%s\n' "$actual/$encontrado"
    done
}

# Mueve recursivamente el contenido de <origen> dentro de <destino>, sobrescribiendo archivos.
# Mover es instantaneo dentro del mismo disco y no duplica el espacio usado.
fusionar_directorio() {
    local origen="$1" destino="$2" entrada base existente
    mkdir -p "$destino" || return 1
    for entrada in "$origen"/* "$origen"/.[!.]*; do
        [[ -e "$entrada" ]] || continue
        base="${entrada##*/}"
        existente="$(buscar_ci "$destino" "$base" | head -n 1)"
        if [[ -d "$entrada" ]]; then
            if [[ -n "$existente" && -d "$destino/$existente" ]]; then
                fusionar_directorio "$entrada" "$destino/$existente" || return 1
            else
                mv -f "$entrada" "$destino/$base" || return 1
            fi
        else
            mv -f "$entrada" "$destino/${existente:-$base}" || return 1
        fi
    done
}

buscar_proton() {
    local lib raiz candidato
    local -a candidatos=()
    while IFS= read -r lib; do
        for candidato in "$lib"/steamapps/common/Proton*/proton; do
            [[ -f "$candidato" ]] && candidatos+=("$candidato")
        done
    done < <(bibliotecas_steam)
    for raiz in "${STEAM_ROOTS[@]}"; do
        for candidato in "$raiz"/compatibilitytools.d/*/proton; do
            [[ -f "$candidato" ]] && candidatos+=("$candidato")
        done
    done
    (( ${#candidatos[@]} )) || return 1
    # Preferir Proton Experimental; si no, la version mas alta
    for candidato in "${candidatos[@]}"; do
        [[ "$candidato" == *"Proton - Experimental/proton" ]] && { printf '%s\n' "$candidato"; return 0; }
    done
    printf '%s\n' "${candidatos[@]}" | sort -V | tail -n 1
}

# -------------------------------------------------------------------------
# Inicio
# -------------------------------------------------------------------------
clear 2>/dev/null || true
linea
say "$C_GREEN" "   Parche de Traduccion al Espanol - Danganronpa V3"
say "$C_GREEN" "   Instalador para Linux / SteamOS"
linea
echo

# Localizar HarmonyTools
HARMONY_EXE="${HARMONY_TOOLS:-}"
if [[ -z "$HARMONY_EXE" ]]; then
    for candidato in "$SCRIPT_DIR/HarmonyTools.exe" "$SCRIPT_DIR/Harmony-Tools/HarmonyTools.exe"; do
        [[ -f "$candidato" ]] && { HARMONY_EXE="$candidato"; break; }
    done
fi

if [[ -z "$HARMONY_EXE" ]]; then
    say "$C_YELLOW" "No se encontro HarmonyTools.exe en la carpeta del parche."
    say "$C_GRAY" "Se puede descargar automaticamente desde: $HARMONY_TOOLS_URL"
    if preguntar_si "Descargar HarmonyTools ahora? [S/N] (Por defecto: S): "; then
        zip_tmp="$(mktemp --suffix=.zip)"
        if curl -fL --progress-bar -o "$zip_tmp" "$HARMONY_TOOLS_URL"; then
            if command -v unzip >/dev/null; then
                unzip -oq "$zip_tmp" -d "$SCRIPT_DIR"
            elif command -v bsdtar >/dev/null; then
                bsdtar -xf "$zip_tmp" -C "$SCRIPT_DIR"
            else
                python3 -I -m zipfile -e "$zip_tmp" "$SCRIPT_DIR"
            fi
        fi
        rm -f "$zip_tmp"
        [[ -f "$SCRIPT_DIR/Harmony-Tools/HarmonyTools.exe" ]] && HARMONY_EXE="$SCRIPT_DIR/Harmony-Tools/HarmonyTools.exe"
    fi
fi

if [[ -z "$HARMONY_EXE" || ! -f "$HARMONY_EXE" ]]; then
    say "$C_RED" "[ERROR] No se encontro HarmonyTools."
    say "$C_YELLOW" "Descargalo de https://github.com/redssu/Harmony-Tools/releases y copia HarmonyTools.exe"
    say "$C_YELLOW" "en la carpeta del parche: $SCRIPT_DIR"
    pausa_y_salir 1
fi

# Elegir con que ejecutar HarmonyTools: binario nativo, Wine o Proton
MODO_HT=""
if [[ "${HARMONY_EXE,,}" != *.exe ]]; then
    MODO_HT="nativo"
elif [[ -n "${WINE:-}" ]] || command -v wine >/dev/null; then
    WINE="${WINE:-$(command -v wine)}"
    MODO_HT="wine"
else
    PROTON="${PROTON:-$(buscar_proton || true)}"
    if [[ -n "$PROTON" && -f "$PROTON" ]]; then
        MODO_HT="proton"
    fi
fi

if [[ -z "$MODO_HT" ]]; then
    say "$C_RED" "[ERROR] No se encontro Wine ni Proton para ejecutar HarmonyTools.exe."
    say "$C_YELLOW" "Instala 'Proton Experimental' desde la biblioteca de Steam (categoria Herramientas)"
    say "$C_YELLOW" "o define la variable PROTON con la ruta al script 'proton'."
    pausa_y_salir 1
fi

case "$MODO_HT" in
    nativo) say "$C_GREEN" "[+] HarmonyTools (nativo): $HARMONY_EXE" ;;
    wine)   say "$C_GREEN" "[+] HarmonyTools se ejecutara con Wine: $WINE" ;;
    proton) say "$C_GREEN" "[+] HarmonyTools se ejecutara con Proton: $(basename "$(dirname "$PROTON")")" ;;
esac
echo

# Ejecuta "HarmonyTools cpk extract -f <cpk>" con el modo elegido
extraer_cpk() {
    local cpk_path="$1"
    case "$MODO_HT" in
        nativo)
            "$HARMONY_EXE" cpk extract -f "$cpk_path" </dev/null ;;
        wine)
            WINEDEBUG=-all "$WINE" "$HARMONY_EXE" cpk extract -f "Z:${cpk_path//\//\\}" </dev/null ;;
        proton)
            local prefijo="${XDG_DATA_HOME:-$HOME/.local/share}/killer-harmony/proton-prefix"
            mkdir -p "$prefijo"
            STEAM_COMPAT_CLIENT_INSTALL_PATH="${STEAM_ROOTS[0]:-$HOME/.local/share/Steam}" \
            STEAM_COMPAT_DATA_PATH="$prefijo" WINEDEBUG=-all \
                "$PROTON" run "$HARMONY_EXE" cpk extract -f "Z:${cpk_path//\//\\}" </dev/null ;;
    esac
}

# -------------------------------------------------------------------------
# Ruta del juego
# -------------------------------------------------------------------------
DEFAULT_PATH=""
while IFS= read -r lib; do
    if [[ -d "$lib/steamapps/common/$CARPETA_JUEGO/data/win" ]]; then
        DEFAULT_PATH="$lib/steamapps/common/$CARPETA_JUEGO"
        break
    fi
done < <(bibliotecas_steam)

say "$C_YELLOW" "Introduce la ruta donde tienes instalado Danganronpa V3: Killing Harmony."
if [[ -n "$DEFAULT_PATH" ]]; then
    say "$C_GRAY" "Ruta detectada: $DEFAULT_PATH"
    say "$C_GRAY" "(Presiona Enter para usar la ruta detectada)"
fi

GAME_PATH=""
while [[ -z "$GAME_PATH" ]]; do
    read -rp "Ruta del juego: " entrada || pausa_y_salir 1
    entrada="${entrada#"${entrada%%[![:space:]]*}"}"
    entrada="${entrada%"${entrada##*[![:space:]]}"}"
    entrada="${entrada#[\"\']}"; entrada="${entrada%[\"\']}"
    entrada="${entrada/#\~/$HOME}"
    if [[ -z "$entrada" ]]; then
        if [[ -n "$DEFAULT_PATH" ]]; then
            GAME_PATH="$DEFAULT_PATH"
        else
            say "$C_YELLOW" "[!] Debes introducir una ruta valida."
            continue
        fi
    else
        GAME_PATH="${entrada%/}"
        # Aceptar tambien la ruta de data/win directamente
        [[ "${GAME_PATH,,}" == */data/win ]] && GAME_PATH="${GAME_PATH%/*/*}"
    fi
    if [[ ! -d "$GAME_PATH" ]]; then
        say "$C_RED" "[ERROR] La ruta especificada no existe: '$GAME_PATH'"
        GAME_PATH=""
    fi
done

WIN_DIR="$(resolver_ci "$GAME_PATH" "data/win" | head -n 1)"
if [[ ! -d "$WIN_DIR" ]]; then
    say "$C_RED" "[ERROR] No se encontro el directorio 'data/win' en la ruta proporcionada."
    say "$C_RED" "Ruta buscada: $GAME_PATH/data/win"
    pausa_y_salir 1
fi
if [[ ! -w "$WIN_DIR" ]]; then
    say "$C_RED" "[ERROR] No tienes permisos de escritura en: $WIN_DIR"
    pausa_y_salir 1
fi

echo
say "$C_GREEN" "[+] Directorio del juego validado: $WIN_DIR"
echo

# -------------------------------------------------------------------------
# Seleccion de version del parche
# -------------------------------------------------------------------------
say "$C_CYAN" "------------------------------------------------------------"
say "$C_YELLOW" "Deseas instalar la version mas reciente ($VERSION_ACTUAL)? [S/N]"
say "$C_GRAY" "  [S] Instalar version mas reciente ($VERSION_ACTUAL) - Puede contener errores del juego"
say "$C_GRAY" "  [N] Instalar version base ($VERSION_BASE) - Estable pero con mas errores de tipografia"
say "$C_CYAN" "------------------------------------------------------------"

VERSION_SELECCIONADA=""
while [[ -z "$VERSION_SELECCIONADA" ]]; do
    read -rp "Opcion (Por defecto: S): " ver || pausa_y_salir 1
    if [[ -z "$ver" || "$ver" =~ ^[sSyY] ]]; then
        VERSION_SELECCIONADA="$CARPETA_ACTUAL"
    elif [[ "$ver" =~ ^[nN] ]]; then
        VERSION_SELECCIONADA="$VERSION_BASE"
    else
        say "$C_YELLOW" "[!] Opcion no valida. Escribe S o N."
    fi
done
say "$C_GREEN" "[+] Version seleccionada para instalacion: $VERSION_SELECCIONADA"
echo

PATCH_SOURCE_DIR="$SCRIPT_DIR/$VERSION_SELECCIONADA/win"
if [[ ! -d "$PATCH_SOURCE_DIR" ]]; then
    say "$C_RED" "[ERROR] No se encontro la carpeta del parche en '$PATCH_SOURCE_DIR'."
    say "$C_YELLOW" "No se realizo ningun cambio en el juego."
    pausa_y_salir 1
fi

# -------------------------------------------------------------------------
# Verificar la presencia de los CPK
# -------------------------------------------------------------------------
CPK_PRESENTES=()
CPK_FALTANTES=()
for cpk in "${CPK_FILES[@]}"; do
    encontrado="$(buscar_ci "$WIN_DIR" "$cpk" | head -n 1)"
    if [[ -n "$encontrado" && -f "$WIN_DIR/$encontrado" ]]; then
        CPK_PRESENTES+=("$encontrado")
    else
        CPK_FALTANTES+=("$cpk")
    fi
done

if (( ${#CPK_FALTANTES[@]} > 0 )); then
    say "$C_YELLOW" "[ADVERTENCIA] No se encontraron los siguientes archivos CPK:"
    for cpk in "${CPK_FALTANTES[@]}"; do say "$C_RED" "  - $cpk"; done
    echo
    if (( ${#CPK_PRESENTES[@]} == 0 )); then
        say "$C_CYAN" "Esto puede deberse a que ya tienes un parche anterior instalado y los CPK ya fueron extraidos y eliminados."
        pregunta="Ya tienes un parche previo instalado? Se omitira la extraccion y se aplicaran solo los archivos del parche. [S/N] (Por defecto: S): "
    else
        say "$C_CYAN" "Los CPK que si estan presentes se extraeran igualmente."
        pregunta="Deseas continuar? [S/N] (Por defecto: S): "
    fi
    if ! preguntar_si "$C_YELLOW$pregunta$C_OFF"; then
        say "$C_GRAY" "Operacion cancelada por el usuario."
        exit 0
    fi
fi

# -------------------------------------------------------------------------
# Extraccion y fusion de los CPK
# -------------------------------------------------------------------------
CPK_EXTRAIDOS=()

if (( ${#CPK_PRESENTES[@]} == 0 )); then
    echo
    say "$C_GRAY" "[INFO] Extraccion y fusion de CPK omitidas (parche previo detectado)."
else
    # Espacio libre: cada CPK se extrae junto a si mismo antes de borrarse al final
    total_cpk=0
    for cpk in "${CPK_PRESENTES[@]}"; do
        total_cpk=$(( total_cpk + $(stat -c %s "$WIN_DIR/$cpk") ))
    done
    libre=$(df -B1 --output=avail "$WIN_DIR" | tail -n 1 | tr -d ' ')
    say "$C_GRAY" "Espacio necesario aprox.: $(( total_cpk / 1024 / 1024 / 1024 + 1 )) GB - Espacio libre: $(( libre / 1024 / 1024 / 1024 )) GB"
    if (( libre < total_cpk )); then
        say "$C_RED" "[ADVERTENCIA] Puede que no haya espacio suficiente para extraer los CPK."
        if ! preguntar_si "${C_YELLOW}Continuar de todos modos? [S/N] (Por defecto: S): $C_OFF"; then
            say "$C_GRAY" "Operacion cancelada por el usuario."
            exit 0
        fi
    fi

    say "$C_CYAN" "------------------------------------------------------------"
    say "$C_CYAN" "Se procedera a extraer y fusionar los archivos CPK."
    say "$C_YELLOW" "ADVERTENCIA: Este proceso puede tardar varios minutos dependiendo de la velocidad de tu disco."
    say "$C_YELLOW" "Por favor, ten paciencia y NO cierres esta ventana mientras se realiza la extraccion."
    if [[ "$MODO_HT" == "proton" ]]; then
        say "$C_GRAY" "La primera vez Proton prepara su entorno y puede tardar un poco mas en empezar."
    fi
    say "$C_CYAN" "------------------------------------------------------------"
    echo

    for cpk in "${CPK_PRESENTES[@]}"; do
        linea
        say "$C_GREEN" "Extrayendo: $cpk..."
        say "$C_YELLOW" "Por favor espera, este proceso tomara un momento..."
        linea

        extraer_cpk "$WIN_DIR/$cpk"
        codigo=$?

        # HarmonyTools extrae en "<nombre>.cpk.decompressed"; se aceptan variantes por compatibilidad
        carpeta_extraida=""
        for nombre in "$cpk.decompressed" "${cpk%.*}.decompressed" "${cpk%.*}"; do
            if [[ -d "$WIN_DIR/$nombre" ]]; then carpeta_extraida="$WIN_DIR/$nombre"; break; fi
        done

        if (( codigo != 0 )) || [[ -z "$carpeta_extraida" ]] || \
           [[ -z "$(find "$carpeta_extraida" -type f -print -quit)" ]]; then
            echo
            say "$C_RED" "[ERROR] Fallo la extraccion de $cpk (Codigo: $codigo)."
            say "$C_YELLOW" "Se detiene la instalacion. Los archivos CPK originales NO fueron eliminados."
            pausa_y_salir 1
        fi

        say "$C_GREEN" "[+] Se ha extraido exitosamente: $cpk"
        say "$C_GRAY" "Moviendo archivos de '${carpeta_extraida##*/}' a 'win'..."

        if ! fusionar_directorio "$carpeta_extraida" "$WIN_DIR"; then
            say "$C_RED" "[ERROR] No se pudieron mover los archivos extraidos de $cpk."
            say "$C_YELLOW" "Se detiene la instalacion. Los archivos CPK originales NO fueron eliminados."
            pausa_y_salir 1
        fi
        rm -rf "$carpeta_extraida" || say "$C_YELLOW" "[!] Advertencia: No se pudo eliminar la carpeta '$carpeta_extraida'."

        CPK_EXTRAIDOS+=("$cpk")
        echo
    done

    say "$C_GREEN" "------------------------------------------------------------"
    say "$C_GREEN" "[+] Extraccion y fusion de CPK completadas."
    say "$C_GREEN" "------------------------------------------------------------"
fi

# -------------------------------------------------------------------------
# Aplicar archivos del parche (copiar y reemplazar desde ./<version>/win hacia data/win)
# -------------------------------------------------------------------------
echo
linea
say "$C_GREEN" "Aplicando archivos del parche de traduccion ($VERSION_SELECCIONADA)..."
linea
say "$C_GRAY" "Copiando archivos modificados ($VERSION_SELECCIONADA) a '$WIN_DIR'..."

mapfile -t PATCH_FILES < <(cd "$PATCH_SOURCE_DIR" && find . -type f | sed 's|^\./||' | sort)
TOTAL_PATCH_FILES=${#PATCH_FILES[@]}

# Detectar la carpeta de revision de wrd_script que usa el juego instalado (003, 004, ..., 007).
# Se toma la de numero mas alto que contenga los scripts del juego (chap0.SPC). Como el propio
# parche tambien trae chap0.SPC, se prefieren las carpetas que tengan algun archivo que el parche
# no trae, para ignorar carpetas creadas solo por una instalacion anterior del parche.
CARPETA_WRD_JUEGO=""
WRD_SCRIPT_DIR="$(resolver_ci "$WIN_DIR" "wrd_script" | head -n 1)"
if [[ -d "$WRD_SCRIPT_DIR" ]]; then
    declare -A NOMBRES_PARCHE_WRD=()
    for rel in "${PATCH_FILES[@]}"; do
        [[ "${rel,,}" =~ ^wrd_script/[0-9]+/([^/]+)$ ]] && NOMBRES_PARCHE_WRD["${BASH_REMATCH[1]}"]=1
    done

    num_original=-1; num_cualquiera=-1
    carpeta_original=""; carpeta_cualquiera=""
    for dir in "$WRD_SCRIPT_DIR"/*/; do
        nombre="$(basename "$dir")"
        [[ "$nombre" =~ ^[0-9]+$ ]] || continue
        [[ -n "$(buscar_ci "$dir" "chap0.SPC")" ]] || continue
        num=$(( 10#$nombre ))
        if (( num > num_cualquiera )); then num_cualquiera=$num; carpeta_cualquiera="$nombre"; fi
        for archivo in "$dir"*; do
            [[ -f "$archivo" ]] || continue
            base="${archivo##*/}"
            if [[ -z "${NOMBRES_PARCHE_WRD[${base,,}]:-}" ]]; then
                if (( num > num_original )); then num_original=$num; carpeta_original="$nombre"; fi
                break
            fi
        done
    done
    CARPETA_WRD_JUEGO="${carpeta_original:-$carpeta_cualquiera}"
fi

if [[ -n "$CARPETA_WRD_JUEGO" ]]; then
    say "$C_GREEN" "[+] Carpeta de dialogos detectada en el juego: wrd_script/$CARPETA_WRD_JUEGO"
else
    say "$C_YELLOW" "[!] No se detecto la carpeta de dialogos del juego; se usaran las rutas del parche tal cual."
fi

# Respaldo en la carpeta del juego (ver comun.sh)
RESPALDO="$(carpeta_respaldo "$GAME_PATH")"
if [[ "$VERSION_SELECCIONADA" == "$CARPETA_ACTUAL" ]]; then ETIQUETA_VERSION="$VERSION_ACTUAL"; else ETIQUETA_VERSION="$VERSION_BASE"; fi
declare -A INSTALADOS=() AGREGADOS=()
VERSION_PREVIA=""
if leer_manifiesto "$RESPALDO/instalado.txt"; then
    VERSION_PREVIA="$MAN_VERSION"
    for r in "${MAN_ARCHIVOS[@]}"; do INSTALADOS["${r,,}"]="$r"; done
    INSTALACION_ANTIGUA=0
else
    # Parche instalado con un instalador antiguo (sin lista de archivos): lo que hay puede no ser el original
    (( ${#CPK_PRESENTES[@]} == 0 )) && INSTALACION_ANTIGUA=1 || INSTALACION_ANTIGUA=0
fi
leer_lista "$RESPALDO/agregados.txt" AGREGADOS
SIN_ORIGINAL=0

if [[ -n "$VERSION_PREVIA" && "$VERSION_PREVIA" != "$ETIQUETA_VERSION" ]]; then
    if ! guardar_version "$RESPALDO" "$WIN_DIR" "$VERSION_PREVIA" "${MAN_ARCHIVOS[@]}"; then
        say "$C_RED" "[ERROR] No se pudo guardar la copia de la version instalada."
        say "$C_YELLOW" "No se realizo ningun cambio en los archivos del juego."
        pausa_y_salir 1
    fi
fi

COPIADOS=0
ERRORES_COPIA=()
for rel in "${PATCH_FILES[@]}"; do
    origen="$PATCH_SOURCE_DIR/$rel"
    destino_rel="$rel"

    # Redirigir los textos de wrd_script/<NNN>/ a la carpeta de revision que usa el juego
    if [[ -n "$CARPETA_WRD_JUEGO" && "$rel" =~ ^[wW][rR][dD]_[sS][cC][rR][iI][pP][tT]/[0-9]+/(.+)$ ]]; then
        destino_rel="wrd_script/$CARPETA_WRD_JUEGO/${BASH_REMATCH[1]}"
    fi

    # Si el juego ya tiene el archivo con otras mayusculas, se reemplaza ese (y cualquier otra variante)
    mapfile -t destinos < <(resolver_ci "$WIN_DIR" "$destino_rel")
    ok=1
    for destino in "${destinos[@]}"; do
        r="${destino#"$WIN_DIR"/}"
        # Guardar el original del juego una sola vez (si el archivo no es de una instalacion anterior del parche)
        if [[ -f "$destino" ]]; then
            if [[ -z "${INSTALADOS[${r,,}]:-}" && ! -f "$RESPALDO/original/$r" ]]; then
                if [[ -f "$SCRIPT_DIR/backup_en/$r" ]]; then
                    copiar_con_carpeta "$SCRIPT_DIR/backup_en/$r" "$RESPALDO/original/$r" || ok=0
                elif (( ! INSTALACION_ANTIGUA )); then
                    copiar_con_carpeta "$destino" "$RESPALDO/original/$r" || ok=0
                else
                    SIN_ORIGINAL=$(( SIN_ORIGINAL + 1 ))
                fi
            fi
        elif [[ -z "${INSTALADOS[${r,,}]:-}" ]]; then
            AGREGADOS["${r,,}"]="$r"
        fi
        if (( ok )) && mkdir -p "$(dirname "$destino")" && cp -f "$origen" "$destino"; then
            INSTALADOS["${r,,}"]="$r"
        else
            ok=0
        fi
    done

    if (( ok )); then
        COPIADOS=$(( COPIADOS + 1 ))
        say "$C_CYAN" "  -> Instalado: ${destinos[0]#"$WIN_DIR"/}"
    else
        ERRORES_COPIA+=("$destino_rel")
        say "$C_RED" "  [!] Error al instalar $destino_rel"
    fi
done

escribir_manifiesto "$RESPALDO/instalado.txt" "$ETIQUETA_VERSION" "${INSTALADOS[@]}"
escribir_lista "$RESPALDO/agregados.txt" AGREGADOS

echo
if (( SIN_ORIGINAL > 0 )); then
    say "$C_YELLOW" "[!] $SIN_ORIGINAL archivos ya estaban modificados por un parche anterior sin respaldo."
    say "$C_YELLOW" "    Para recuperar el juego original en ingles, usa 'Verificar integridad' en Steam."
fi
if (( ${#ERRORES_COPIA[@]} == 0 )); then
    say "$C_GREEN" "[+] Se aplicaron con exito $COPIADOS de $TOTAL_PATCH_FILES archivos del parche ($VERSION_SELECCIONADA)."
else
    say "$C_YELLOW" "[!] Se aplicaron $COPIADOS de $TOTAL_PATCH_FILES archivos del parche ($VERSION_SELECCIONADA)."
fi

# -------------------------------------------------------------------------
# Eliminacion de archivos CPK originales (solo los que se extrajeron correctamente)
# -------------------------------------------------------------------------
if (( ${#CPK_EXTRAIDOS[@]} > 0 )); then
    echo
    say "$C_YELLOW" "Limpiando archivos CPK originales..."
    for cpk in "${CPK_EXTRAIDOS[@]}"; do
        if rm -f "$WIN_DIR/$cpk"; then
            say "$C_GRAY" "[+] Archivo eliminado: $cpk"
        else
            say "$C_RED" "[!] No se pudo eliminar $cpk"
        fi
    done
fi

echo
if (( ${#ERRORES_COPIA[@]} > 0 )); then
    say "$C_RED" "============================================================"
    say "$C_RED" "El proceso termino con errores. No se pudieron instalar:"
    for ruta in "${ERRORES_COPIA[@]}"; do say "$C_RED" "  - $ruta"; done
    say "$C_YELLOW" "Revisa los permisos de la carpeta del juego y vuelve a ejecutar el parche."
    say "$C_RED" "============================================================"
    pausa_y_salir 1
fi

say "$C_GREEN" "============================================================"
say "$C_GREEN" "El proceso ha finalizado con exito."
say "$C_GREEN" "============================================================"
pausa_y_salir 0
