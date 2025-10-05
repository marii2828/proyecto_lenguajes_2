# Menu de Juegos - Proyecto Lenguajes

## Descripcion
Sistema de juegos integrado que proporciona acceso unificado a dos juegos implementados con arquitectura hibrida F#/Python:

- **Sopa de Letras**: Generacion de tableros dinamicos con busqueda de palabras
- **Ahorcado**: Juego clasico de adivinanza de palabras con dibujo interactivo

## Arquitectura del Sistema

### Menu Principal
- **Navegacion por pantallas**: Sistema unificado sin ventanas separadas
- **Interfaz consistente**: Paleta de colores y tipografia estandarizada
- **Gestion de memoria**: Limpieza automatica de widgets al cambiar pantallas
- **Experiencia fluida**: Transiciones suaves entre juegos

### Comunicacion Backend-Frontend
- **F# Backend**: Logica de negocio y algoritmos
- **Python Frontend**: Interfaz grafica e interaccion del usuario
- **Protocolo JSON**: Comunicacion estructurada via subprocess
- **Persistencia**: Estado de juego mantenido en archivos

## Juegos Implementados

### Sopa de Letras
**Funcionalidad**:
- Generacion aleatoria de tableros de diferentes tamanos
- Colocacion inteligente de palabras en multiples direcciones
- Validacion en tiempo real de selecciones del usuario
- Resolucion automatica con visualizacion de palabras restantes
- Temporizador de juego y estadisticas de progreso

**Componentes Tecnicos**:
- **Backend F# (.NET 9.0)**: 
  - `Sopa.Core`: Logica de dominio, generacion y validacion
  - `Sopa.Cli`: Interfaz de linea de comandos para comunicacion
- **Frontend Python**: 
  - `sopa_letras_screen.py`: Pantalla integrada al menu
  - `ui/board.py`: Componente de tablero interactivo
  - `services/backend.py`: Cliente para comunicacion con F#

**Algoritmos**:
- Generacion de grillas con semillas aleatorias
- Colocacion de palabras en 8 direcciones posibles
- Deteccion de colisiones y solapamientos
- Busqueda y validacion de patrones

### Ahorcado  
**Funcionalidad**:
- Seleccion aleatoria de palabras desde diccionario
- Visualizacion progresiva del dibujo del ahorcado
- Tracking de letras correctas e incorrectas
- Persistencia de estado entre sesiones
- Interfaz visual con retroalimentacion inmediata

**Componentes Tecnicos**:
- **Backend F# (.NET 6.0/8.0)**:
  - `GameState.fs`: Manejo de estado del juego
  - `GameLogic.fs`: Logica de adivinanza y validaciones
  - `WordManager.fs`: Gestion de diccionario de palabras
  - `HangmanAPI.fs`: API de comandos para frontend
- **Frontend Python**:
  - `ahorcado_screen.py`: Pantalla integrada al menu
  - `hangman.py`: Version standalone (legacy)

**Persistencia**:
- Estado guardado en formato: `PALABRA|letras_intentadas|errores|max_intentos|estado`
- Recuperacion automatica al reiniciar la aplicacion
- Manejo de multiples sesiones de juego

## Estructura de Directorios

```
proyecto_lenguajes_2/
├── menu_principal.py                    # Punto de entrada principal
├── README.md                           # Documentacion del proyecto
├── juego-sopa-letras/                  # Modulo completo sopa de letras
│   ├── backend/                        # Backend F# (.NET 9.0)
│   │   ├── Sopa.sln                   # Solucion de Visual Studio
│   │   ├── Sopa.Core/                 # Libreria principal
│   │   │   ├── Domain.fs              # Tipos de dominio
│   │   │   ├── Generator.fs           # Generacion de tableros
│   │   │   ├── Validator.fs           # Validacion de selecciones
│   │   │   ├── Solver.fs              # Resolucion automatica
│   │   │   └── Sopa.Core.fsproj       # Configuracion del proyecto
│   │   └── Sopa.Cli/                  # Interfaz de linea de comandos
│   │       ├── Program.fs             # Punto de entrada CLI
│   │       └── Sopa.Cli.fsproj        # Configuracion del proyecto
│   ├── frontend/                       # Frontend Python/tkinter
│   │   ├── sopa_letras_screen.py      # Pantalla principal del juego
│   │   ├── services/                   # Servicios de comunicacion
│   │   │   └── backend.py             # Cliente backend F#
│   │   └── ui/                        # Componentes de interfaz
│   │       ├── board.py               # Tablero interactivo
│   │       └── palette.py             # Paleta de colores
│   └── data/                          # Recursos del juego
│       └── words.txt                  # Diccionario de palabras
├── juego-ahorcado/                     # Modulo completo ahorcado
│   ├── backend/                        # Backend F# (.NET 6.0/8.0)
│   │   ├── main.fs                    # Punto de entrada
│   │   ├── GameState.fs               # Estado del juego
│   │   ├── GameLogic.fs               # Logica de adivinanza
│   │   ├── WordManager.fs             # Gestion de palabras
│   │   ├── HangmanAPI.fs              # API de comandos
│   │   ├── words.txt                  # Diccionario local
│   │   └── game-logic-fsharp.fsproj   # Configuracion del proyecto
│   ├── frontend/                       # Frontend Python/tkinter
│   │   ├── ahorcado_screen.py         # Pantalla integrada
│   │   └── hangman.py                 # Version standalone
│   └── flujodeejecucion.txt           # Documentacion de flujo
```

## Requisitos del Sistema

### Software Base
- **Python 3.8+** con tkinter (incluido en instalaciones estandar)
- **.NET 6.0+** para el modulo de ahorcado
- **.NET 9.0+** para el modulo de sopa de letras
- **Sistema operativo**: Windows, macOS, Linux

### Dependencias Python
- `tkinter`: Interfaz grafica (incluido con Python)
- `subprocess`: Comunicacion con procesos F#
- `json`: Serializacion de datos
- `os`: Manejo de rutas y archivos

### Dependencias .NET
- **FSharp.Core**: Runtime de F#
- **FSharp.SystemTextJson**: Serializacion JSON para F#
- **System.Text.Json**: Manejo de JSON en .NET

## Instrucciones de Uso

### Ejecutar el Sistema
```bash
cd proyecto_lenguajes_2
python menu_principal.py
```

### Compilacion Manual (Opcional)
```bash
# Compilar sopa de letras
cd juego-sopa-letras/backend
dotnet build

# Compilar ahorcado  
cd juego-ahorcado/backend
dotnet build
```
