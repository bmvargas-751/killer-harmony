#!/usr/bin/env bash
# Restaura el juego al estado original (ingles) o a otra version del parche guardada en el respaldo.
# Equivalente a restaurar.ps1 para Linux / SteamOS.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=comun.sh
source "$SCRIPT_DIR/comun.sh"

clear 2>/dev/null || true
linea
say "$C_GREEN" "   Restaurar - Parche de Traduccion de Danganronpa V3"
linea
echo

# Ruta del juego
DEFAULT_PATH=""
while IFS= read -r lib; do
    if [[ -d "$lib/steamapps/common/$CARPETA_JUEGO/data/win" ]]; then
        DEFAULT_PATH="$lib/steamapps/common/$CARPETA_JUEGO"
        break
    fi
done < <(bibliotecas_steam)

say "$C_YELLOW" "Introduce la ruta donde tienes instalado Danganronpa V3: Killing Harmony."
[[ -n "$DEFAULT_PATH" ]] && say "$C_GRAY" "Ruta detectada: $DEFAULT_PATH (Presiona Enter para usarla)"
GAME_PATH=""
while [[ -z "$GAME_PATH" ]]; do
    read -rp "Ruta del juego: " entrada || pausa_y_salir 1
    entrada="${entrada#"${entrada%%[![:space:]]*}"}"
    entrada="${entrada%"${entrada##*[![:space:]]}"}"
    entrada="${entrada#[\"\']}"; entrada="${entrada%[\"\']}"
    entrada="${entrada/#\~/$HOME}"
    GAME_PATH="${entrada:-$DEFAULT_PATH}"
    GAME_PATH="${GAME_PATH%/}"
    [[ "${GAME_PATH,,}" == */data/win ]] && GAME_PATH="${GAME_PATH%/*/*}"
    if [[ -z "$GAME_PATH" || ! -d "$GAME_PATH/data/win" ]]; then
        say "$C_RED" "[ERROR] No se encontro 'data/win' en: '$GAME_PATH'"
        GAME_PATH=""
    fi
done
WIN_DIR="$GAME_PATH/data/win"
RESPALDO="$(carpeta_respaldo "$GAME_PATH")"

VERSION_ACTUAL_INST=""
ARCHIVOS_ACTUALES=()
if leer_manifiesto "$RESPALDO/instalado.txt"; then
    VERSION_ACTUAL_INST="$MAN_VERSION"
    ARCHIVOS_ACTUALES=("${MAN_ARCHIVOS[@]}")
fi
declare -A AGREGADOS=()
leer_lista "$RESPALDO/agregados.txt" AGREGADOS

# Opciones disponibles
OPC_TIPO=()
OPC_VALOR=()
OPC_TEXTO=()
if [[ -n "$VERSION_ACTUAL_INST" || -d "$RESPALDO/original" ]]; then
    OPC_TIPO+=(original); OPC_VALOR+=(""); OPC_TEXTO+=("Juego original (sin parche, en ingles)")
fi
for dir in "$RESPALDO"/versiones/*/; do
    [[ -f "$dir/instalado.txt" ]] || continue
    v="$(basename "$dir")"
    [[ "$v" == "$VERSION_ACTUAL_INST" ]] && continue
    OPC_TIPO+=(version); OPC_VALOR+=("$v"); OPC_TEXTO+=("Parche $v")
done
if (( ${#OPC_TIPO[@]} == 0 )) && [[ -d "$SCRIPT_DIR/backup_en" ]]; then
    OPC_TIPO+=(legado); OPC_VALOR+=(""); OPC_TEXTO+=("Juego original (respaldo backup_en de un instalador anterior)")
fi

echo
if [[ -n "$VERSION_ACTUAL_INST" ]]; then
    say "$C_GREEN" "Version del parche instalada: $VERSION_ACTUAL_INST"
else
    say "$C_GRAY" "No hay una version del parche registrada en este juego."
fi
if (( ${#OPC_TIPO[@]} == 0 )); then
    echo
    say "$C_YELLOW" "No se encontro ningun respaldo en '$RESPALDO'."
    say "$C_YELLOW" "Para recuperar el juego original usa en Steam: Propiedades > Archivos instalados > Verificar integridad."
    pausa_y_salir 1
fi

echo
say "$C_YELLOW" "A que quieres volver?"
for i in "${!OPC_TIPO[@]}"; do echo "  [$(( i + 1 ))] ${OPC_TEXTO[i]}"; done
echo "  [0] Cancelar"
ELECCION=""
while [[ -z "$ELECCION" ]]; do
    read -rp "Opcion: " r || pausa_y_salir 1
    if [[ "$r" =~ ^[0-9]+$ ]] && (( r <= ${#OPC_TIPO[@]} )); then ELECCION="$r"; else say "$C_YELLOW" "[!] Opcion no valida."; fi
done
if (( ELECCION == 0 )); then say "$C_GRAY" "Operacion cancelada."; exit 0; fi
TIPO="${OPC_TIPO[ELECCION - 1]}"
VALOR="${OPC_VALOR[ELECCION - 1]}"
TEXTO="${OPC_TEXTO[ELECCION - 1]}"

SIN_RESTAURAR=0
fallo() { say "$C_RED" "[ERROR] La restauracion se interrumpio en: $1"; pausa_y_salir 1; }

# Vuelve al original un archivo de la version actual (o lo cuenta si no hay respaldo)
a_original() {
    restaurar_original "$RESPALDO" "$WIN_DIR" "$1" AGREGADOS
    case $? in
        0) say "$C_CYAN" "  -> Restaurado: $1" ;;
        2) SIN_RESTAURAR=$(( SIN_RESTAURAR + 1 )) ;;
        *) fallo "$1" ;;
    esac
}

case "$TIPO" in
    legado)
        while IFS= read -r -d '' f; do
            rel="${f#"$SCRIPT_DIR/backup_en/"}"
            copiar_con_carpeta "$f" "$WIN_DIR/$rel" || fallo "$rel"
            say "$C_CYAN" "  -> Restaurado: $rel"
        done < <(find "$SCRIPT_DIR/backup_en" -type f -print0)
        ;;
    original)
        # Guardar la version actual para poder volver a ella
        guardar_version "$RESPALDO" "$WIN_DIR" "$VERSION_ACTUAL_INST" "${ARCHIVOS_ACTUALES[@]}" || fallo "copia de la version actual"
        for rel in "${ARCHIVOS_ACTUALES[@]}"; do a_original "$rel"; done
        rm -f "$RESPALDO/instalado.txt"
        ;;
    version)
        guardar_version "$RESPALDO" "$WIN_DIR" "$VERSION_ACTUAL_INST" "${ARCHIVOS_ACTUALES[@]}" || fallo "copia de la version actual"
        DIR_V="$RESPALDO/versiones/$VALOR"
        leer_manifiesto "$DIR_V/instalado.txt"
        declare -A EN_DESTINO=()
        for rel in "${MAN_ARCHIVOS[@]}"; do EN_DESTINO["${rel,,}"]=1; done
        # Archivos de la version actual que la otra version no tenia: volver al original
        for rel in "${ARCHIVOS_ACTUALES[@]}"; do
            [[ -n "${EN_DESTINO[${rel,,}]:-}" ]] || a_original "$rel"
        done
        for rel in "${MAN_ARCHIVOS[@]}"; do
            if [[ -f "$DIR_V/archivos/$rel" ]]; then
                copiar_con_carpeta "$DIR_V/archivos/$rel" "$WIN_DIR/$rel" || fallo "$rel"
                say "$C_CYAN" "  -> Restaurado: $rel"
            else
                SIN_RESTAURAR=$(( SIN_RESTAURAR + 1 ))
            fi
        done
        escribir_manifiesto "$RESPALDO/instalado.txt" "$MAN_VERSION" "${MAN_ARCHIVOS[@]}"
        ;;
esac

echo
if (( SIN_RESTAURAR > 0 )); then
    say "$C_YELLOW" "[!] No habia respaldo de $SIN_RESTAURAR archivos (por ejemplo, de un parche instalado con un instalador antiguo)."
    say "$C_YELLOW" "    Para recuperarlos usa en Steam: Propiedades > Archivos instalados > Verificar integridad."
fi
say "$C_GREEN" "============================================================"
say "$C_GREEN" "Restauracion completada: $TEXTO"
say "$C_GREEN" "============================================================"
if [[ "$TIPO" != "version" ]]; then
    say "$C_GRAY" "Nota: el juego queda en ingles usando los archivos extraidos. Si prefieres volver a los"
    say "$C_GRAY" "archivos .cpk originales, usa 'Verificar integridad' en Steam."
fi
pausa_y_salir 0
