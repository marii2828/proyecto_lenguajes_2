# 🎮 Menú de Juegos - Proyecto Lenguajes

## Descripción
Este proyecto incluye un menú principal que permite acceder a dos juegos implementados en diferentes lenguajes:

- **Sopa de Letras**: Implementado en F# (backend) y Python (frontend)
- **Ahorcado**: Implementado en F# (backend) y Python (frontend)

## 🚀 Cómo ejecutar

### Ejecutar el menú principal
```bash
python menu_principal.py
```

### Funcionalidades del menú

#### 🧩 Sopa de Letras
- **Cambio de pantalla**: Al seleccionar este juego, la ventana actual cambia para mostrar el juego de sopa de letras
- **Botón "Volver al menú"**: Permite regresar al menú principal sin cerrar la aplicación
- **Funcionalidades del juego**:
  - Selección secuencial de letras haciendo clic
  - Verificación de palabras
  - Resolución automática con retraso de 2 segundos
  - Temporizador del juego
  - Generación aleatoria de cada nueva partida

#### 🎯 Ahorcado
- **Ventana separada**: Al seleccionar este juego, se abre en una ventana independiente
- **Ejecución paralela**: Puedes mantener ambas ventanas abiertas simultáneamente
- **Backend F#**: Utiliza la lógica de negocio implementada en F#

## 📁 Estructura del proyecto

```
proyecto_lenguajes_2/
├── menu_principal.py          # Menú principal del sistema
├── juego-sopa-letras/         # Implementación completa de sopa de letras
│   ├── backend/               # Backend en F# (.NET 9.0)
│   ├── frontend/              # Frontend en Python/tkinter
│   │   ├── app.py             # Aplicación standalone original
│   │   ├── sopa_letras_screen.py  # Pantalla para el menú principal
│   │   ├── services/          # Comunicación con backend
│   │   └── ui/                # Componentes de interfaz
│   └── data/                  # Palabras para el juego
└── juego-ahorcado/            # Implementación completa de ahorcado
    ├── backend/               # Backend en F# (.NET 6.0/8.0)
    └── frontend/              # Frontend en Python/tkinter
```

## 🎨 Características del diseño

- **Estilo consistente**: Todos los componentes siguen la misma paleta de colores
- **Interfaz intuitiva**: Navegación clara entre pantallas
- **Responsive**: Diseño adaptado para una experiencia de usuario fluida
- **Gestión de memoria**: Limpieza apropiada de widgets al cambiar pantallas

## 🔧 Requisitos técnicos

- Python 3.8+
- .NET 6.0+ para el juego de ahorcado
- .NET 9.0+ para el juego de sopa de letras
- tkinter (incluido con Python)

## 📝 Notas de implementación

- **Sin comentarios**: Todo el código ha sido limpiado de comentarios según especificación
- **Generación aleatoria**: Cada partida de sopa de letras genera un tablero diferente
- **Gestión de procesos**: El juego de ahorcado se ejecuta como proceso independiente
- **Manejo de errores**: Validación de rutas y manejo de excepciones para mayor robustez