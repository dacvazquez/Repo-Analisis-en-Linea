#!/usr/bin/env python3
"""
Script para limpiar la caché de Hugging Face y forzar la re-descarga de modelos.
Útil cuando se tienen archivos corruptos o problemas de descarga.
"""

import os
import shutil
from pathlib import Path

def clear_huggingface_cache():
    """Limpia completamente la caché de Hugging Face"""
    try:
        # Obtener el directorio de caché de Hugging Face
        cache_dir = Path.home() / ".cache" / "huggingface"
        
        if not cache_dir.exists():
            print("No se encontró el directorio de caché de Hugging Face")
            return False
        
        print(f"Directorio de caché encontrado: {cache_dir}")
        
        # Contar archivos antes de eliminar
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(cache_dir):
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
                file_count += 1
        
        print(f"Archivos a eliminar: {file_count}")
        print(f"Tamaño total: {total_size / (1024*1024):.2f} MB")
        
        # Confirmar eliminación
        response = input("¿Deseas continuar con la eliminación? (y/N): ")
        if response.lower() != 'y':
            print("Operación cancelada")
            return False
        
        # Eliminar todo el contenido de la caché
        shutil.rmtree(cache_dir)
        
        print("Caché de Hugging Face limpiada completamente")
        print("Los modelos se descargarán nuevamente en la próxima ejecución")
        
        return True
        
    except Exception as e:
        print(f"Error al limpiar la caché: {e}")
        return False

def clear_pysentimiento_cache():
    """Limpia específicamente la caché de modelos de pysentimiento"""
    try:
        cache_dir = Path.home() / ".cache" / "huggingface"
        
        if not cache_dir.exists():
            print("No se encontró el directorio de caché de Hugging Face")
            return False
        
        # Buscar y eliminar directorios de pysentimiento
        pysentimiento_dirs = list(cache_dir.rglob("*pysentimiento*"))
        
        if not pysentimiento_dirs:
            print("No se encontraron modelos de pysentimiento en la caché")
            return True
        
        print(f"Encontrados {len(pysentimiento_dirs)} directorios de pysentimiento")
        
        for model_dir in pysentimiento_dirs:
            if model_dir.is_dir():
                print(f"Eliminando: {model_dir.name}")
                shutil.rmtree(model_dir, ignore_errors=True)
        
        print("Caché de pysentimiento limpiada")
        return True
        
    except Exception as e:
        print(f"Error al limpiar la caché de pysentimiento: {e}")
        return False

if __name__ == "__main__":
    print("Limpiador de caché de Hugging Face")
    print("=" * 40)
    
    print("\nOpciones disponibles:")
    print("1. Limpiar toda la caché de Hugging Face")
    print("2. Limpiar solo modelos de pysentimiento")
    print("3. Salir")
    
    while True:
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            clear_huggingface_cache()
            break
        elif choice == "2":
            clear_pysentimiento_cache()
            break
        elif choice == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, selecciona 1, 2 o 3.")
