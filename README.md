🕹️ Squash con Patrón Decorator (Pygame)
Autores:
Juan David Rayo Tejada - 20231020023
Jonnatan Camargo Camacho - 20231020204
Este proyecto es una implementación educativa del Patrón de Diseño Decorator aplicada a un mini-juego tipo "Squash" desarrollado con Python y Pygame.  
El objetivo principal es demostrar cómo el patrón Decorator permite extender funcionalidades sin modificar el código original, siguiendo el Principio Abierto/Cerrado (Open/Closed Principle).

------------------------------------------------------------
🎯 Objetivo del Proyecto
------------------------------------------------------------
- Implementar un juego funcional en Pygame.
- Aplicar el Patrón de Diseño Decorator para la gestión de modos especiales de la raqueta.
- Mostrar cómo un decorator puede añadir comportamiento adicional (logging, validaciones, extensibilidad) sin alterar la lógica base.

------------------------------------------------------------
🧩 Patrón Decorator en Acción
------------------------------------------------------------
El decorador principal @modo_especial envuelve los métodos de activación de modos de la raqueta (Raqueta) para:

1. Validar la entrada del usuario (teclas presionadas).  
2. Ejecutar el método original sin modificarlo.  
3. Agregar logging automático e información en consola.  

Ejemplo:
@modo_especial
def activar_modo_rapido(self):
    return self.cambiar_modo("Rápido")

Esto permite agregar nuevos modos en el futuro sin alterar el código existente.

------------------------------------------------------------
⚙️ Requisitos
------------------------------------------------------------
- Python 3.8+
- Biblioteca Pygame

Para instalar dependencias:
pip install pygame

------------------------------------------------------------
▶️ Ejecución
------------------------------------------------------------
Clona o descarga este repositorio y ejecuta el juego:
python mi_juego.py

------------------------------------------------------------
🎮 Controles del Juego
------------------------------------------------------------
← / → : Mover raqueta
A : Activar modo rápido (Mayor velocidad, menor ancho)
S : Activar modo ancho (Mayor ancho, menor velocidad)
D : Activar modo imantación (Atrae la pelota al centro)
W : Volver al modo normal
ESC : Salir del juego

------------------------------------------------------------
🧠 Clases Principales
------------------------------------------------------------
Pelota:
- Controla el movimiento, rebotes y colisiones con la raqueta.

Raqueta:
- Implementa los modos especiales decorados con @modo_especial:
  Normal, Rápido, Ancho, Imantación.

JuegoSquash:
- Coordina el flujo principal del juego:
  Movimiento, colisiones, niveles, puntaje y renderizado.

------------------------------------------------------------
🧱 Estructura del Proyecto
------------------------------------------------------------
mi_juego.py      -> Código principal del juego
README.txt       -> Este documento

------------------------------------------------------------
🧪 Principios de Diseño Demostrados
------------------------------------------------------------
- Patrón Decorator: Extensión de comportamiento dinámico.
- Open/Closed Principle: Código abierto a extensión, cerrado a modificación.
- Polimorfismo de datos: Configuración de modos con diccionarios.
- Responsabilidad única: Cada clase cumple una función específica.
