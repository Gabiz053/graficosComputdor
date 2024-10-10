#!/bin/bash

# Verificar si se proporciona un directorio como argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <directorio>"
    exit 1
fi

DIRECTORIO=$1

# Comprobar si el directorio existe
if [ ! -d "$DIRECTORIO" ]; then
    echo "El directorio no existe: $DIRECTORIO"
    exit 1
fi

# Contar las líneas en todos los archivos del directorio
TOTAL_LINEAS=$(find "$DIRECTORIO" -type f -exec cat {} + | wc -l)

echo "Total de líneas en '$DIRECTORIO': $TOTAL_LINEAS"