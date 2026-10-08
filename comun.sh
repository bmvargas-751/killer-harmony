# Funciones compartidas por patch.sh y restaurar.sh: mensajes, deteccion de Steam y respaldo.
# shellcheck shell=bash
#
# El respaldo vive en la carpeta del juego, para no perderlo al descargar otra version del parche:
#   <juego>/killer-harmony-backup/
#     original/<ruta>             Archivo original del juego (ingles), se guarda una sola vez.
#     agregados.txt               Archivos que creo el parche y no existian en el juego.
#     instalado.txt               "version=<v>" y, debajo, los archivos que tiene instalados el parche.
#     versiones/<v>/archivos/     Copia de una version del parche, guardada antes de cambiar a otra.
#     versiones/<v>/instalado.txt Lista de archivos de esa version.
# Las rutas son relativas a data/win. Se comparan sin distinguir mayusculas, como hace el juego.

# ---------------------------------------------------------------------------
# Mensajes
# ---------------------------------------------------------------------------
if [[ -t 1 ]]; then
    C_RED=$'\e[31m'; C_GREEN=$'\e[32m'; C_YELLOW=$'\e[33m'; C_CYAN=$'\e[36m'; C_GRAY=$'\e[90m'; C_OFF=$'\e[0m'
else
    C_RED=""; C_GREEN=""; C_YELLOW=""; C_CYAN=""; C_GRAY=""; C_OFF=""
fi

say()   { printf '%s%s%s\n' "$1" "$2" "$C_OFF"; }
linea() { say "$C_CYAN" "============================================================"; }

pausa_y_salir() {
    local codigo="$1"
    if [[ -t 0 ]]; then
        echo
        read -rp "Presiona Enter para salir" _
    fi
    exit "$codigo"
}

preguntar_si() {
    # preguntar_si "<texto>" -> 0 si la respuesta es S/Y o vacia (por defecto S)
    local resp
    read -rp "$1" resp || resp="n"
    [[ -z "$resp" || "$resp" =~ ^[sSyY] ]]
}

# -------------------------------------------------------------------------
# Deteccion de Steam, Proton y el juego
# -------------------------------------------------------------------------
CARPETA_JUEGO="Danganronpa V3 Killing Harmony"
STEAM_ROOTS=()
for raiz in "$HOME/.local/share/Steam" "$HOME/.steam/steam" "$HOME/.steam/root" \
            "$HOME/.var/app/com.valvesoftware.Steam/.local/share/Steam"; do
    [[ -d "$raiz/steamapps" ]] || continue
    real="$(readlink -f "$raiz")"
    [[ " ${STEAM_ROOTS[*]:-} " == *" $real "* ]] || STEAM_ROOTS+=("$real")
done

bibliotecas_steam() {
    local raiz vdf
    for raiz in "${STEAM_ROOTS[@]}"; do
        printf '%s\n' "$raiz"
        for vdf in "$raiz/steamapps/libraryfolders.vdf" "$raiz/config/libraryfolders.vdf"; do
            [[ -f "$vdf" ]] && sed -n 's/^[[:space:]]*"path"[[:space:]]*"\(.*\)"[[:space:]]*$/\1/p' "$vdf"
        done
    done | sed 's/\\\\/\\/g' | awk '!visto[$0]++'
}

# ---------------------------------------------------------------------------
# Respaldo
# ---------------------------------------------------------------------------
carpeta_respaldo() { printf '%s/killer-harmony-backup\n' "$1"; }

# leer_manifiesto <archivo>: deja MAN_VERSION y MAN_ARCHIVOS (array). Devuelve 1 si no existe.
leer_manifiesto() {
    MAN_VERSION=""
    MAN_ARCHIVOS=()
    [[ -f "$1" ]] || return 1
    local linea
    while IFS= read -r linea || [[ -n "$linea" ]]; do
        linea="${linea%$'\r'}"
        [[ -z "$linea" ]] && continue
        if [[ "$linea" == version=* ]]; then
            MAN_VERSION="${linea#version=}"
        else
            MAN_ARCHIVOS+=("$linea")
        fi
    done < "$1"
    return 0
}

# escribir_manifiesto <archivo> <version> <rutas...>
escribir_manifiesto() {
    local archivo="$1" version="$2"
    shift 2
    mkdir -p "$(dirname "$archivo")"
    { printf 'version=%s\n' "$version"; printf '%s\n' "$@" | awk 'NF' | sort -u; } > "$archivo"
}

# leer_lista <archivo> <nombre_de_array_asociativo>: claves en minusculas -> ruta
leer_lista() {
    local -n _lista="$2"
    local linea
    [[ -f "$1" ]] || return 0
    while IFS= read -r linea || [[ -n "$linea" ]]; do
        linea="${linea%$'\r'}"
        [[ -n "$linea" ]] && _lista["${linea,,}"]="$linea"
    done < "$1"
}

# escribir_lista <archivo> <nombre_de_array_asociativo>
escribir_lista() {
    local -n _lista="$2"
    mkdir -p "$(dirname "$1")"
    if (( ${#_lista[@]} )); then printf '%s\n' "${_lista[@]}" | sort > "$1"; else : > "$1"; fi
}

copiar_con_carpeta() {
    mkdir -p "$(dirname "$2")" && cp -f "$1" "$2"
}

# guardar_version <respaldo> <win_dir> <version> <rutas...>: copia la version instalada si aun no existe
guardar_version() {
    local respaldo="$1" win="$2" version="$3"
    shift 3
    [[ -n "$version" ]] || return 0
    local dest="$respaldo/versiones/$version" rel
    [[ -f "$dest/instalado.txt" ]] && return 0
    echo "Guardando copia de la version instalada ($version)..."
    for rel in "$@"; do
        if [[ -f "$win/$rel" ]]; then
            copiar_con_carpeta "$win/$rel" "$dest/archivos/$rel" || return 1
        fi
    done
    escribir_manifiesto "$dest/instalado.txt" "$version" "$@"
}

# restaurar_original <respaldo> <win_dir> <ruta> <array_agregados>
# Devuelve 0 si lo restauro (o lo borro por ser un archivo agregado), 2 si no hay respaldo, 1 si fallo.
restaurar_original() {
    local respaldo="$1" win="$2" rel="$3"
    local -n _agregados="$4"
    if [[ -f "$respaldo/original/$rel" ]]; then
        copiar_con_carpeta "$respaldo/original/$rel" "$win/$rel" || return 1
        return 0
    fi
    if [[ -n "${_agregados[${rel,,}]:-}" ]]; then
        rm -f "$win/$rel" || return 1
        return 0
    fi
    return 2
}
