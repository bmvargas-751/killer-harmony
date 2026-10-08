# Restaura el juego al estado original (ingles) o a otra version del parche guardada en el respaldo.

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

. (Join-Path $PSScriptRoot "comun.ps1")

Clear-Host
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   Restaurar - Parche de Traduccion de Danganronpa V3" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Ruta del juego
$defaultPath = "C:\SteamLibrary\steamapps\common\Danganronpa V3 Killing Harmony"
Write-Host "Introduce la ruta donde tienes instalado Danganronpa V3: Killing Harmony." -ForegroundColor Yellow
if (Test-Path $defaultPath) {
    Write-Host "Ruta por defecto detectada: $defaultPath" -ForegroundColor DarkGray
    Write-Host "(Presiona Enter para usar la ruta por defecto)" -ForegroundColor DarkGray
}
$gamePath = ""
while (-not $gamePath) {
    $inputPath = Read-Host "Ruta del juego"
    if ([string]::IsNullOrWhiteSpace($inputPath)) {
        if (Test-Path $defaultPath) { $gamePath = $defaultPath } else { Write-Host "[!] Debes introducir una ruta valida." -ForegroundColor Yellow; continue }
    } else {
        $gamePath = $inputPath.Trim('"', "'", " ")
    }
    if (-not (Test-Path (Join-Path (Join-Path $gamePath "data") "win"))) {
        Write-Host "[ERROR] No se encontro 'data\win' en: '$gamePath'" -ForegroundColor Red
        $gamePath = ""
    }
}
$winDir = Join-Path (Join-Path $gamePath "data") "win"
$backupDir = Get-CarpetaRespaldo $gamePath
$manifiesto = Leer-Manifiesto (Join-Path $backupDir "instalado.txt")
$agregados = Leer-Lista (Join-Path $backupDir "agregados.txt")
$legado = Join-Path $PSScriptRoot "backup_en"

# Opciones disponibles
$opciones = @()
if ($manifiesto -or (Test-Path (Join-Path $backupDir "original"))) {
    $opciones += [pscustomobject]@{ Tipo = "original"; Texto = "Juego original (sin parche, en ingles)" }
}
$dirVersiones = Join-Path $backupDir "versiones"
if (Test-Path $dirVersiones) {
    foreach ($d in Get-ChildItem -Path $dirVersiones -Directory | Sort-Object Name) {
        if ((Test-Path (Join-Path $d.FullName "instalado.txt")) -and (-not $manifiesto -or $d.Name -ne $manifiesto.Version)) {
            $opciones += [pscustomobject]@{ Tipo = "version"; Version = $d.Name; Texto = "Parche $($d.Name)" }
        }
    }
}
if ($opciones.Count -eq 0 -and (Test-Path $legado)) {
    $opciones += [pscustomobject]@{ Tipo = "legado"; Texto = "Juego original (respaldo backup_en de un instalador anterior)" }
}

Write-Host ""
if ($manifiesto) {
    Write-Host "Version del parche instalada: $($manifiesto.Version)" -ForegroundColor Green
} else {
    Write-Host "No hay una version del parche registrada en este juego." -ForegroundColor Gray
}
if ($opciones.Count -eq 0) {
    Write-Host ""
    Write-Host "No se encontro ningun respaldo en '$backupDir'." -ForegroundColor Yellow
    Write-Host "Para recuperar el juego original usa en Steam: Propiedades > Archivos instalados > Verificar integridad." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "A que quieres volver?" -ForegroundColor Yellow
for ($i = 0; $i -lt $opciones.Count; $i++) {
    Write-Host "  [$($i + 1)] $($opciones[$i].Texto)"
}
Write-Host "  [0] Cancelar"
$eleccion = $null
while ($null -eq $eleccion) {
    $r = Read-Host "Opcion"
    if ($r -match '^\d+$' -and [int]$r -ge 0 -and [int]$r -le $opciones.Count) { $eleccion = [int]$r }
    else { Write-Host "[!] Opcion no valida." -ForegroundColor Yellow }
}
if ($eleccion -eq 0) { Write-Host "Operacion cancelada." -ForegroundColor Gray; exit 0 }
$opcion = $opciones[$eleccion - 1]

$sinRestaurar = @()
try {
    switch ($opcion.Tipo) {
        "legado" {
            foreach ($f in Get-ChildItem -Path $legado -Recurse -File) {
                $rel = $f.FullName.Substring((Resolve-Path $legado).Path.Length).TrimStart('\', '/')
                Copiar-Con-Carpeta $f.FullName (Join-Path $winDir $rel)
                Write-Host "  -> Restaurado: $rel" -ForegroundColor DarkCyan
            }
        }
        "original" {
            # Guardar la version actual para poder volver a ella
            Guardar-Version $backupDir $winDir $manifiesto
            if ($manifiesto) {
                foreach ($rel in $manifiesto.Archivos) {
                    if (Restaurar-Original $backupDir $winDir $rel $agregados) {
                        Write-Host "  -> Restaurado: $rel" -ForegroundColor DarkCyan
                    } else {
                        $sinRestaurar += $rel
                    }
                }
                Remove-Item -Path (Join-Path $backupDir "instalado.txt") -Force
            }
        }
        "version" {
            Guardar-Version $backupDir $winDir $manifiesto
            $dirV = Join-Path $dirVersiones $opcion.Version
            $destino = Leer-Manifiesto (Join-Path $dirV "instalado.txt")
            $enDestino = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
            foreach ($rel in $destino.Archivos) { [void]$enDestino.Add($rel) }
            # Archivos de la version actual que la otra version no tenia: volver al original
            if ($manifiesto) {
                foreach ($rel in $manifiesto.Archivos) {
                    if (-not $enDestino.Contains($rel) -and -not (Restaurar-Original $backupDir $winDir $rel $agregados)) {
                        $sinRestaurar += $rel
                    }
                }
            }
            foreach ($rel in $destino.Archivos) {
                $copia = Join-Path (Join-Path $dirV "archivos") $rel
                if (Test-Path $copia) {
                    Copiar-Con-Carpeta $copia (Join-Path $winDir $rel)
                    Write-Host "  -> Restaurado: $rel" -ForegroundColor DarkCyan
                } else {
                    $sinRestaurar += $rel
                }
            }
            Escribir-Manifiesto (Join-Path $backupDir "instalado.txt") $destino.Version $destino.Archivos
        }
    }
} catch {
    Write-Host ""
    Write-Host "[ERROR] La restauracion se interrumpio: $_" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
if ($sinRestaurar.Count -gt 0) {
    Write-Host "[!] No habia respaldo de $($sinRestaurar.Count) archivos (por ejemplo, de un parche instalado con un instalador antiguo)." -ForegroundColor Yellow
    Write-Host "    Para recuperarlos usa en Steam: Propiedades > Archivos instalados > Verificar integridad." -ForegroundColor Yellow
}
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Restauracion completada: $($opcion.Texto)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
if ($opcion.Tipo -ne "version") {
    Write-Host "Nota: el juego queda en ingles usando los archivos extraidos. Si prefieres volver a los" -ForegroundColor Gray
    Write-Host "archivos .cpk originales, usa 'Verificar integridad' en Steam." -ForegroundColor Gray
}
Write-Host ""
Read-Host "Presiona Enter para salir"
exit 0
