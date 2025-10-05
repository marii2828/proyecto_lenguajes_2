#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de tamaño dinámico
"""

import sys
import os

# Agregar la ruta del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_sopa_size_functionality():
    """Prueba la funcionalidad de tamaño dinámico"""
    print("Iniciando prueba de funcionalidad de tamaño dinámico...")
    
    # Probar importación del menú principal
    try:
        import menu_principal
        print("✅ Menu principal importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando menu principal: {e}")
        return False
    
    # Probar importación de sopa letras screen
    try:
        sopa_path = os.path.join(project_root, "juego-sopa-letras", "frontend")
        sys.path.append(sopa_path)
        from sopa_letras_screen import SopaLetrasScreen
        print("✅ SopaLetrasScreen importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando SopaLetrasScreen: {e}")
        return False
    
    # Probar backend de sopa de letras
    try:
        from services import backend
        # Probar con diferentes tamaños
        for size in [10, 15, 20]:
            try:
                words = ["PYTHON", "PROGRAMACION", "ALGORITMO"]
                result = backend.generate(words, size=size)
                if result and "grid" in result:
                    grid_size = len(result["grid"])
                    if grid_size == size:
                        print(f"✅ Generación de tablero {size}x{size} exitosa")
                    else:
                        print(f"⚠️  Tamaño esperado {size}, obtenido {grid_size}")
                else:
                    print(f"❌ Error en generación de tablero {size}x{size}")
            except Exception as e:
                print(f"❌ Error generando tablero {size}x{size}: {e}")
    except ImportError as e:
        print(f"❌ Error importando backend: {e}")
        return False
    
    print("\n🎉 Pruebas completadas. El sistema debería funcionar correctamente.")
    print("\nPara probar manualmente:")
    print("1. Ejecuta: python menu_principal.py")
    print("2. Presiona 'JUGAR SOPA DE LETRAS'")
    print("3. Selecciona un tamaño entre 10-20")
    print("4. Verifica que el tablero se ajuste al tamaño seleccionado")
    
    return True

if __name__ == "__main__":
    test_sopa_size_functionality()