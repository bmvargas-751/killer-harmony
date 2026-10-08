# Funciones de respaldo compartidas por patch.ps1 y restaurar.ps1.
#
# El respaldo vive en la carpeta del juego, para no perderlo al descargar otra version del parche:
#   <juego>\killer-harmony-backup\
#     original\<ruta>             Archivo original del juego (ingles), se guarda una sola vez.
#     agregados.txt               Archivos que creo el parche y no existian en el juego.
#     instalado.txt               "version=<v>" y, debajo, los archivos que tiene instalados el parche.
#     versiones\<v>\archivos\     Copia de una version del parche, guardada antes de cambiar a otra.
#     versiones\<v>\instalado.txt Lista de archivos de esa version.
# Las rutas se guardan relativas a data\win y con "/" como separador.

function Get-CarpetaRespaldo([string]$gamePath) {
    return (Join-Path $gamePath "killer-harmony-backup")
}

function Leer-Manifiesto([string]$ruta) {
    if (-not (Test-Path $ruta)) { return $null }
    $version = $null
    $archivos = New-Object System.Collections.Generic.List[string]
    foreach ($linea in [System.IO.File]::ReadAllLines($ruta)) {
        $linea = $linea.Trim()
        if (-not $linea) { continue }
        if ($linea.StartsWith("version=")) { $version = $linea.Substring(8); continue }
        $archivos.Add($linea)
    }
    return [pscustomobject]@{ Version = $version; Archivos = $archivos }
}

function Escribir-Manifiesto([string]$ruta, [string]$version, $archivos) {
    $dir = Split-Path $ruta -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $lineas = @("version=$version") + @($archivos | Sort-Object -Unique)
    [System.IO.File]::WriteAllLines($ruta, [string[]]$lineas, (New-Object System.Text.UTF8Encoding($false)))
}

function Leer-Lista([string]$ruta) {
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    if (Test-Path $ruta) {
        foreach ($l in [System.IO.File]::ReadAllLines($ruta)) { if ($l.Trim()) { [void]$set.Add($l.Trim()) } }
    }
    return ,$set
}

function Escribir-Lista([string]$ruta, $set) {
    $dir = Split-Path $ruta -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    [System.IO.File]::WriteAllLines($ruta, [string[]]@($set | Sort-Object), (New-Object System.Text.UTF8Encoding($false)))
}

function Copiar-Con-Carpeta([string]$origen, [string]$destino) {
    $dir = Split-Path $destino -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force -ErrorAction Stop | Out-Null }
    Copy-Item -Path $origen -Destination $destino -Force -ErrorAction Stop
}

# Guarda una copia de los archivos de la version instalada (si aun no existe esa copia).
function Guardar-Version([string]$backupDir, [string]$winDir, $manifiesto) {
    if (-not $manifiesto -or -not $manifiesto.Version) { return }
    $dest = Join-Path (Join-Path $backupDir "versiones") $manifiesto.Version
    if (Test-Path (Join-Path $dest "instalado.txt")) { return }
    Write-Host "Guardando copia de la version instalada ($($manifiesto.Version))..." -ForegroundColor Gray
    foreach ($rel in $manifiesto.Archivos) {
        $actual = Join-Path $winDir $rel
        if (Test-Path $actual) { Copiar-Con-Carpeta $actual (Join-Path (Join-Path $dest "archivos") $rel) }
    }
    Escribir-Manifiesto (Join-Path $dest "instalado.txt") $manifiesto.Version $manifiesto.Archivos
}

# Devuelve un archivo a su estado original: lo restaura desde el respaldo o, si lo creo el parche, lo borra.
# Devuelve $false si no hay forma de restaurarlo (instalacion antigua sin respaldo).
function Restaurar-Original([string]$backupDir, [string]$winDir, [string]$rel, $agregados) {
    $original = Join-Path (Join-Path $backupDir "original") $rel
    $actual = Join-Path $winDir $rel
    if (Test-Path $original) {
        Copiar-Con-Carpeta $original $actual
        return $true
    }
    if ($agregados.Contains($rel)) {
        if (Test-Path $actual) { Remove-Item -Path $actual -Force -ErrorAction Stop }
        return $true
    }
    return $false
}
