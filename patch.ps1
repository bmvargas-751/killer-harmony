# Script de instalacion para el parche de traduccion de Danganronpa V3: Killing Harmony.

# -------------------------------------------------------------------------
# Versiones del parche disponibles
# -------------------------------------------------------------------------
$versionActual   = "v2.5"   # Numero de version mas reciente (solo para mostrar)
$carpetaActual   = "latest" # Carpeta del parche para la version mas reciente
$versionBase     = "v0.1"   # Version anterior estable (nombre de carpeta y version)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Desactivar QuickEdit Mode en la consola de Windows para evitar que clics pausen la ejecucion
try {
    $code = @'
    using System;
    using System.Runtime.InteropServices;
    public class ConsoleHelper {
        const uint ENABLE_QUICK_EDIT = 0x0040;
        const uint ENABLE_EXTENDED_FLAGS = 0x0080;
        const int STD_INPUT_HANDLE = -10;

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern IntPtr GetStdHandle(int nStdHandle);

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);

        public static void DisableQuickEdit() {
            IntPtr handle = GetStdHandle(STD_INPUT_HANDLE);
            if (handle == IntPtr.Zero || handle == new IntPtr(-1)) return;
            uint mode;
            if (!GetConsoleMode(handle, out mode)) return;
            mode &= ~ENABLE_QUICK_EDIT;
            mode |= ENABLE_EXTENDED_FLAGS;
            SetConsoleMode(handle, mode);
        }
    }
'@
    Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
    [ConsoleHelper]::DisableQuickEdit()
} catch {
    # Continuar normalmente si no es una consola interactiva estandar
}

. (Join-Path $PSScriptRoot "comun.ps1")

function Show-Header {
    Clear-Host
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "   Parche de Traduccion al Espanol - Danganronpa V3" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

Show-Header

# Verificar que HarmonyTools este disponible
$harmonyCmd = Get-Command "HarmonyTools.exe" -ErrorAction SilentlyContinue
if (-not $harmonyCmd) {
    if (Test-Path ".\HarmonyTools.exe") {
        $harmonyExe = (Resolve-Path ".\HarmonyTools.exe").Path
    } elseif (Test-Path "C:\Harmony-Tools\HarmonyTools.exe") {
        $harmonyExe = "C:\Harmony-Tools\HarmonyTools.exe"
    } else {
        Write-Host "[ERROR] No se encontro HarmonyTools.exe en el sistema ni en el directorio actual." -ForegroundColor Red
        Write-Host "Por favor asegurate de tener HarmonyTools instalado o configurado en el PATH." -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
} else {
    $harmonyExe = $harmonyCmd.Source
}

# Solicitar la ruta del juego
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
        if (Test-Path $defaultPath) {
            $gamePath = $defaultPath
        } else {
            Write-Host "[!] Debes introducir una ruta valida." -ForegroundColor Yellow
            continue
        }
    } else {
        $gamePath = $inputPath.Trim('"', "'", " ")
    }

    if (-not (Test-Path $gamePath)) {
        Write-Host "[ERROR] La ruta especificada no existe: '$gamePath'" -ForegroundColor Red
        $gamePath = ""
    }
}

# Comprobar la existencia del directorio data/win
$winDir = Join-Path (Join-Path $gamePath "data") "win"

if (-not (Test-Path $winDir)) {
    Write-Host "[ERROR] No se encontro el directorio 'data\win' en la ruta proporcionada." -ForegroundColor Red
    Write-Host "Ruta buscada: $winDir" -ForegroundColor DarkRed
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "[+] Directorio del juego validado: $winDir" -ForegroundColor Green
Write-Host ""

# Seleccion de version del parche
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "Deseas instalar la version mas reciente ($versionActual)? [S/N]" -ForegroundColor Yellow
Write-Host "  [S] Instalar version mas reciente ($versionActual) - Puede contener errores del juego" -ForegroundColor DarkGray
Write-Host "  [N] Instalar version base ($versionBase) - Estable pero con mas errores de tipografia" -ForegroundColor DarkGray
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
$versionSeleccionada = $null
while (-not $versionSeleccionada) {
    $verInput = Read-Host "Opcion (Por defecto: S)"
    if ([string]::IsNullOrWhiteSpace($verInput) -or $verInput -match "^[sSyY]") {
        $versionSeleccionada = $carpetaActual
    } elseif ($verInput -match "^[nN]") {
        $versionSeleccionada = $versionBase
    } else {
        Write-Host "[!] Opcion no valida. Escribe S o N." -ForegroundColor Yellow
    }
}

Write-Host "[+] Version seleccionada para instalacion: $versionSeleccionada" -ForegroundColor Green
Write-Host ""

# Validar la carpeta del parche ANTES de tocar el juego (si falta no se debe extraer ni borrar nada)
$patchSourceDir = Join-Path (Join-Path $PSScriptRoot $versionSeleccionada) "win"
if (-not (Test-Path $patchSourceDir)) {
    Write-Host "[ERROR] No se encontro la carpeta del parche en '$patchSourceDir'." -ForegroundColor Red
    Write-Host "No se realizo ningun cambio en el juego." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}
$patchSourceDir = (Resolve-Path $patchSourceDir).Path

# Lista de archivos CPK requeridos
$cpkFiles = @(
    "partition_data_win.cpk",
    "partition_data_win_us.cpk",
    "partition_resident_win.cpk"
)

# Verificar la presencia de los CPK
$missingCpk = @()
foreach ($cpk in $cpkFiles) {
    $fullPath = Join-Path $winDir $cpk
    if (-not (Test-Path $fullPath)) {
        $missingCpk += $cpk
    }
}

$parche_previo_instalado = $false

if ($missingCpk.Count -gt 0) {
    Write-Host "[ADVERTENCIA] No se encontraron los siguientes archivos CPK:" -ForegroundColor Yellow
    foreach ($cpk in $missingCpk) {
        Write-Host "  - $cpk" -ForegroundColor Red
    }
    Write-Host ""
    if ($missingCpk.Count -eq $cpkFiles.Count) {
        Write-Host "Esto puede deberse a que ya tienes un parche anterior instalado y los CPK ya fueron extraidos y eliminados." -ForegroundColor Cyan
        Write-Host "Ya tienes un parche previo instalado? Se omitira la extraccion y se aplicaran solo los archivos del parche. [S/N] (Por defecto: S): " -NoNewline -ForegroundColor Yellow
    } else {
        # Faltan solo algunos: los que si estan se extraen igual (si no, se borrarian sin extraer)
        Write-Host "Los CPK que si estan presentes se extraeran igualmente." -ForegroundColor Cyan
        Write-Host "Deseas continuar? [S/N] (Por defecto: S): " -NoNewline -ForegroundColor Yellow
    }
    $respPrevio = Read-Host
    if ([string]::IsNullOrWhiteSpace($respPrevio) -or $respPrevio -match "^[sSyY]") {
        if ($missingCpk.Count -eq $cpkFiles.Count) {
            $parche_previo_instalado = $true
            Write-Host "[+] Se omitira la extraccion de CPK. Solo se copiaran los archivos del parche." -ForegroundColor Green
        }
    } else {
        Write-Host "Operacion cancelada por el usuario." -ForegroundColor Gray
        exit 0
    }
}

# CPK extraidos y fusionados correctamente; solo estos se borraran al final
$cpkExtraidos = @()

# Mueve recursivamente el contenido de $origen dentro de $destino, sobrescribiendo archivos.
# Mover (en vez de copiar) es instantaneo dentro del mismo disco y no duplica el espacio usado.
function Merge-Directory([string]$origen, [string]$destino) {
    if (-not (Test-Path $destino)) {
        New-Item -ItemType Directory -Path $destino -Force -ErrorAction Stop | Out-Null
    }
    foreach ($item in Get-ChildItem -Path $origen -Force) {
        $target = Join-Path $destino $item.Name
        if ($item.PSIsContainer) {
            Merge-Directory $item.FullName $target
        } else {
            Move-Item -Path $item.FullName -Destination $target -Force -ErrorAction Stop
        }
    }
}

if (-not $parche_previo_instalado) {
    # Confirmacion antes de extraer
    Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "Se procedera a extraer y fusionar los archivos CPK." -ForegroundColor Cyan
    Write-Host "ADVERTENCIA: Este proceso puede tardar varios minutos dependiendo de la velocidad de tu disco." -ForegroundColor Yellow
    Write-Host "Por favor, ten paciencia y NO cierres esta ventana mientras se realiza la extraccion." -ForegroundColor Yellow
    Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host ""

    $originalLocation = Get-Location

    try {
        Set-Location -Path $winDir

        foreach ($cpk in $cpkFiles) {
            $cpkPath = Join-Path $winDir $cpk
            if (-not (Test-Path $cpkPath)) {
                Write-Host "[OMITIDO] El archivo $cpk no se encuentra en el directorio." -ForegroundColor DarkGray
                continue
            }

            Write-Host "============================================================" -ForegroundColor Cyan
            Write-Host "Extrayendo: $cpk..." -ForegroundColor Green
            Write-Host "Por favor espera, este proceso tomara un momento..." -ForegroundColor Yellow
            Write-Host "============================================================" -ForegroundColor Cyan

            $null | & $harmonyExe cpk extract -f $cpkPath
            $codigoExtraccion = $LASTEXITCODE

            # HarmonyTools extrae en "<nombre>.cpk.decompressed"; se aceptan variantes por compatibilidad
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($cpk)
            $extractedFolder = @("$cpk.decompressed", "$baseName.decompressed", $baseName) |
                ForEach-Object { Join-Path $winDir $_ } |
                Where-Object { Test-Path $_ -PathType Container } |
                Select-Object -First 1

            $extraccionVacia = (-not $extractedFolder) -or
                (-not (Get-ChildItem -Path $extractedFolder -Recurse -File -Force | Select-Object -First 1))

            if ($codigoExtraccion -ne 0 -or $extraccionVacia) {
                Write-Host ""
                Write-Host "[ERROR] Fallo la extraccion de $cpk (Codigo: $codigoExtraccion)." -ForegroundColor Red
                Write-Host "Se detiene la instalacion. Los archivos CPK originales NO fueron eliminados." -ForegroundColor Yellow
                Write-Host ""
                Read-Host "Presiona Enter para salir"
                exit 1
            }

            Write-Host "[+] Se ha extraido exitosamente: $cpk" -ForegroundColor Green
            Write-Host "Moviendo archivos de '$(Split-Path $extractedFolder -Leaf)' a 'win'..." -ForegroundColor Gray

            try {
                Merge-Directory $extractedFolder $winDir
            } catch {
                Write-Host "[ERROR] No se pudieron mover los archivos extraidos de $cpk : $_" -ForegroundColor Red
                Write-Host "Se detiene la instalacion. Los archivos CPK originales NO fueron eliminados." -ForegroundColor Yellow
                Write-Host ""
                Read-Host "Presiona Enter para salir"
                exit 1
            }

            try {
                Remove-Item -Path $extractedFolder -Recurse -Force -ErrorAction Stop
            } catch {
                Write-Host "[!] Advertencia: No se pudo eliminar la carpeta '$extractedFolder': $_" -ForegroundColor Yellow
            }

            $cpkExtraidos += $cpk
            Write-Host ""
        }

        Write-Host "------------------------------------------------------------" -ForegroundColor Green
        Write-Host "[+] Extraccion y fusion de CPK completadas." -ForegroundColor Green
        Write-Host "------------------------------------------------------------" -ForegroundColor Green
    }
    finally {
        Set-Location -Path $originalLocation
    }
} else {
    Write-Host ""
    Write-Host "[INFO] Extraccion y fusion de CPK omitidas (parche previo detectado)." -ForegroundColor DarkGray
}

# -------------------------------------------------------------------------
# Aplicar archivos del parche (Copiar y reemplazar desde ./<version>/win hacia data/win)
# -------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Aplicando archivos del parche de traduccion ($versionSeleccionada)..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "Copiando archivos modificados ($versionSeleccionada) a '$winDir'..." -ForegroundColor Gray

# Obtener todos los archivos del parche y copiarlos manteniendo la estructura
$patchFiles = Get-ChildItem -Path $patchSourceDir -Recurse -File
$totalPatchFiles = $patchFiles.Count
$copiedCount = 0
$erroresCopia = @()

# Detectar la carpeta de revision de wrd_script que usa el juego instalado (003, 004, ..., 007).
# Se toma la de numero mas alto que contenga los scripts del juego (chap0.SPC). Como el propio
# parche tambien trae chap0.SPC, se prefieren las carpetas que tengan algun archivo que el parche
# no trae, para ignorar carpetas creadas solo por una instalacion anterior del parche.
$wrdScriptDir = Join-Path $winDir "wrd_script"
$carpetaWrdJuego = $null
if (Test-Path $wrdScriptDir) {
    $nombresParcheWrd = $patchFiles |
        Where-Object { $_.Directory.Parent.Name -eq "wrd_script" } |
        ForEach-Object { $_.Name.ToLowerInvariant() }

    $candidatas = @(Get-ChildItem -Path $wrdScriptDir -Directory |
        Where-Object { $_.Name -match '^\d+$' -and (Test-Path (Join-Path $_.FullName "chap0.SPC")) } |
        Sort-Object { [int]$_.Name })

    $originales = @($candidatas | Where-Object {
        Get-ChildItem -Path $_.FullName -File | Where-Object { $nombresParcheWrd -notcontains $_.Name.ToLowerInvariant() }
    })

    if ($originales.Count -gt 0) {
        $carpetaWrdJuego = $originales[-1].Name
    } elseif ($candidatas.Count -gt 0) {
        $carpetaWrdJuego = $candidatas[-1].Name
    }
}

if ($carpetaWrdJuego) {
    Write-Host "[+] Carpeta de dialogos detectada en el juego: wrd_script\$carpetaWrdJuego" -ForegroundColor Green
} else {
    Write-Host "[!] No se detecto la carpeta de dialogos del juego; se usaran las rutas del parche tal cual." -ForegroundColor Yellow
}

# Respaldo en la carpeta del juego (ver comun.ps1)
$backupDir = Get-CarpetaRespaldo $gamePath
$etiquetaVersion = if ($versionSeleccionada -eq $carpetaActual) { $versionActual } else { $versionBase }
$manifiestoPrevio = Leer-Manifiesto (Join-Path $backupDir "instalado.txt")
$agregados = Leer-Lista (Join-Path $backupDir "agregados.txt")
$instalados = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
if ($manifiestoPrevio) { foreach ($r in $manifiestoPrevio.Archivos) { [void]$instalados.Add($r) } }
# Parche instalado con un instalador antiguo (sin lista de archivos): lo que hay en el juego puede no ser el original
$instalacionAntigua = (-not $manifiestoPrevio) -and $parche_previo_instalado
$sinOriginal = 0

if ($manifiestoPrevio -and $manifiestoPrevio.Version -ne $etiquetaVersion) {
    try {
        Guardar-Version $backupDir $winDir $manifiestoPrevio
    } catch {
        Write-Host "[ERROR] No se pudo guardar la copia de la version instalada: $_" -ForegroundColor Red
        Write-Host "No se realizo ningun cambio en los archivos del juego." -ForegroundColor Yellow
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

foreach ($file in $patchFiles) {
    # Obtener ruta relativa respecto a la carpeta 'win' del parche de la version elegida
    $relativePath = $file.FullName.Substring($patchSourceDir.Length).TrimStart('\', '/')

    # Redirigir los textos de wrd_script\<NNN>\ a la carpeta de revision que usa el juego
    if ($carpetaWrdJuego -and $relativePath -match '^wrd_script[\\/]\d+[\\/](.+)$') {
        $nombreArchivo = $Matches[1]
        $relativePath = Join-Path (Join-Path "wrd_script" $carpetaWrdJuego) $nombreArchivo
    }

    $destinationFilePath = Join-Path $winDir $relativePath
    $destinationSubDir = Split-Path $destinationFilePath -Parent

    try {
        $rel = $relativePath -replace '\\', '/'
        # Guardar el original del juego una sola vez (si el archivo no es de una instalacion anterior del parche)
        if (Test-Path $destinationFilePath) {
            $original = Join-Path (Join-Path $backupDir "original") $rel
            if (-not $instalados.Contains($rel) -and -not (Test-Path $original)) {
                $legado = Join-Path (Join-Path $PSScriptRoot "backup_en") $relativePath
                if (Test-Path $legado) {
                    Copiar-Con-Carpeta $legado $original      # respaldo de un instalador anterior
                } elseif (-not $instalacionAntigua) {
                    Copiar-Con-Carpeta $destinationFilePath $original
                } else {
                    $sinOriginal++
                }
            }
        } elseif (-not $instalados.Contains($rel)) {
            [void]$agregados.Add($rel)
        }

        # Asegurarse de que el subdirectorio de destino exista
        if (-not (Test-Path $destinationSubDir)) {
            New-Item -ItemType Directory -Path $destinationSubDir -Force -ErrorAction Stop | Out-Null
        }

        # Copiar y reemplazar
        Copy-Item -Path $file.FullName -Destination $destinationFilePath -Force -ErrorAction Stop
        [void]$instalados.Add($rel)
        $copiedCount++
        Write-Host "  -> Instalado: $relativePath" -ForegroundColor DarkCyan
    } catch {
        $erroresCopia += $relativePath
        Write-Host "  [!] Error al instalar $relativePath : $_" -ForegroundColor Red
    }
}

Escribir-Manifiesto (Join-Path $backupDir "instalado.txt") $etiquetaVersion $instalados
Escribir-Lista (Join-Path $backupDir "agregados.txt") $agregados

Write-Host ""
if ($sinOriginal -gt 0) {
    Write-Host "[!] $sinOriginal archivos ya estaban modificados por un parche anterior sin respaldo." -ForegroundColor Yellow
    Write-Host "    Para recuperar el juego original en ingles, usa 'Verificar integridad' en Steam." -ForegroundColor Yellow
}
if ($erroresCopia.Count -eq 0) {
    Write-Host "[+] Se aplicaron con exito $copiedCount de $totalPatchFiles archivos del parche ($versionSeleccionada)." -ForegroundColor Green
} else {
    Write-Host "[!] Se aplicaron $copiedCount de $totalPatchFiles archivos del parche ($versionSeleccionada)." -ForegroundColor Yellow
}

# -------------------------------------------------------------------------
# Eliminacion de archivos CPK originales (solo los que se extrajeron correctamente)
# -------------------------------------------------------------------------
if ($cpkExtraidos.Count -gt 0) {
    Write-Host ""
    Write-Host "Limpiando archivos CPK originales..." -ForegroundColor Yellow
    foreach ($cpk in $cpkExtraidos) {
        $cpkPath = Join-Path $winDir $cpk
        try {
            Remove-Item -Path $cpkPath -Force -ErrorAction Stop
            Write-Host "[+] Archivo eliminado: $cpk" -ForegroundColor Gray
        } catch {
            Write-Host "[!] No se pudo eliminar $cpk : $_" -ForegroundColor Red
        }
    }
}

Write-Host ""
if ($erroresCopia.Count -gt 0) {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "El proceso termino con errores. No se pudieron instalar:" -ForegroundColor Red
    foreach ($ruta in $erroresCopia) {
        Write-Host "  - $ruta" -ForegroundColor Red
    }
    Write-Host "Revisa los permisos de la carpeta del juego y vuelve a ejecutar el parche." -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "El proceso ha finalizado con exito." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = [System.Console]::ReadKey($true)

exit 0
