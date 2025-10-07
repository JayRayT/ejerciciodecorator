# pylint: disable=all
"""
Juego de Squash con Pygame - Implementación del Patrón Decorator
"""
import sys
import pygame
import random


# =============================================================================
# PATRÓN DECORATOR - IMPLEMENTACIÓN PRINCIPAL
# =============================================================================
def modo_especial(func):
    """
    DECORATOR PRINCIPAL - Patrón Decorator aplicado a métodos de modos especiales
    
    El decorator 'modo_especial' envuelve los métodos de activación de modos para:
    1. Agregar funcionalidad común (logging, validaciones)
    2. Mantener la interfaz original de los métodos
    3. Permitir extensibilidad sin modificar código existente
    
    Principio Open/Closed: Abierto para extensión, cerrado para modificación
    """
    def wrapper(self, tecla_presionada):
        # PRE-PROCESAMIENTO: Validar si la tecla fue presionada
        if tecla_presionada:
            # EJECUCIÓN DEL MÉTODO ORIGINAL
            resultado = func(self)
            
            # POST-PROCESAMIENTO: Logging del modo activado
            if resultado:
                print(f"🎮 Modo activado: {func.__name__}")
            return resultado
        return False
    return wrapper
# =============================================================================


class Pelota:
    """Clase que representa la pelota de squash."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad_x = 5
        self.velocidad_y = 5
        self.radio = 10
        self.color = (255, 255, 255)  # Blanco
        self.activa = True
    
    def mover(self):
        """Mueve la pelota y maneja rebotes."""
        if not self.activa:
            return
        
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Rebotes en las paredes laterales
        if self.x <= 0 or self.x >= 800:
            self.velocidad_x *= -1
        
        # Rebote en el techo
        if self.y <= 0:
            self.velocidad_y *= -1
        
        # Si sale por abajo, se desactiva (pierde vida)
        if self.y >= 600:
            self.activa = False
    
    def dibujar(self, superficie):
        """Dibuja la pelota."""
        if self.activa:
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)
    
    def verificar_colision(self, raqueta):
        """Verifica colisión con la raqueta."""
        if not self.activa:
            return False
        
        # Detección de colisión simple con la raqueta
        if (self.y + self.radio >= raqueta.y and 
            self.x >= raqueta.x and 
            self.x <= raqueta.x + raqueta.ancho):
            
            # Física del rebote
            self.velocidad_y *= -1
            # Efecto direccional según dónde golpea la raqueta
            diferencia_centro = self.x - (raqueta.x + raqueta.ancho / 2)
            self.velocidad_x += diferencia_centro * 0.1
            
            return True
        return False


class Raqueta:
    """
    Clase que representa la raqueta de squash.
    Aquí se aplica el patrón Decorator mediante @modo_especial
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 100
        self.alto = 15
        self.velocidad = 8
        self.color = (0, 255, 0)  # Verde por defecto
        self.modo_actual = "Normal"
        self.ancho_original = 100
        
        # Configuraciones de cada modo - POLIMORFISMO DE DATOS
        self.modos = {
            "Normal": {
                "color": (0, 255, 0),      # Verde
                "velocidad": 8,
                "ancho": 100,
                "descripcion": "Modo balanceado"
            },
            "Rápido": {
                "color": (255, 255, 0),    # Amarillo
                "velocidad": 12,
                "ancho": 80,
                "descripcion": "Más velocidad, menos ancho"
            },
            "Ancho": {
                "color": (255, 0, 0),      # Rojo
                "velocidad": 6,
                "ancho": 150,
                "descripcion": "Más ancho, menos velocidad"
            },
            "Imantación": {
                "color": (0, 0, 255),      # Azul
                "velocidad": 8,
                "ancho": 100,
                "descripcion": "Atrae la pelota cuando está cerca"
            }
        }
    
    def cambiar_modo(self, nuevo_modo):
        """Cambia al modo especificado - MÉTODO CENTRAL DE CONFIGURACIÓN"""
        if nuevo_modo in self.modos:
            self.modo_actual = nuevo_modo
            config = self.modos[nuevo_modo]
            self.color = config["color"]
            self.velocidad = config["velocidad"]
            self.ancho = config["ancho"]
            return True
        return False
    
    # =========================================================================
    # MÉTODOS DECORADOS - Aplicación práctica del patrón Decorator
    # =========================================================================
    
    @modo_especial
    def activar_modo_rapido(self):
        """
        MÉTODO DECORADO - Modo rápido
        El decorator @modo_especial agrega:
        - Validación de tecla presionada
        - Logging automático
        - Manejo de retorno
        """
        return self.cambiar_modo("Rápido")
    
    @modo_especial
    def activar_modo_ancho(self):
        """MÉTODO DECORADO - Modo ancho"""
        return self.cambiar_modo("Ancho")
    
    @modo_especial
    def activar_modo_imantacion(self):
        """MÉTODO DECORADO - Modo imantación"""
        return self.cambiar_modo("Imantación")
    
    @modo_especial
    def activar_modo_normal(self):
        """MÉTODO DECORADO - Volver al modo normal"""
        return self.cambiar_modo("Normal")
    # =========================================================================
    
    def mover(self, teclas_presionadas):
        """Mueve la raqueta según las flechas - MOVIMIENTO BASE"""
        movimiento_realizado = False
        
        if teclas_presionadas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
            movimiento_realizado = True
        if teclas_presionadas[pygame.K_RIGHT] and self.x < 800 - self.ancho:
            self.x += self.velocidad
            movimiento_realizado = True
        
        return movimiento_realizado
    
    def aplicar_imantacion(self, pelota):
        """Aplica efecto de imantación si está en ese modo - COMPORTAMIENTO ESPECIAL"""
        if self.modo_actual == "Imantación" and pelota and pelota.activa:
            # Atraer pelota si está en la zona superior
            distancia_x = abs(pelota.x - (self.x + self.ancho / 2))
            if distancia_x < 100 and pelota.y > 300:  # Zona de influencia ampliada
                # Física de atracción suave
                pelota.velocidad_x -= (pelota.x - (self.x + self.ancho / 2)) * 0.05
                return True
        return False
    
    def dibujar(self, superficie):
        """Dibuja la raqueta con su color actual"""
        pygame.draw.rect(superficie, self.color, 
                        (self.x, self.y, self.ancho, self.alto))


class JuegoSquash:
    """
    Clase principal del juego - COORDINADOR GENERAL
    Maneja la lógica del juego, puntuación y estados
    """
    
    def __init__(self):
        # Estado del juego
        self.puntaje = 0
        self.vidas = 3
        self.nivel = 1
        self.raqueta = Raqueta(350, 550)  # Raqueta en posición inicial
        
        # PELOTA INICIA MÁS ARRIBA - 1/4 de la pantalla desde arriba
        self.pelota = Pelota(400, 80)  # Cambiado de 300 a 150 para mayor distancia
        
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        self.esta_ejecutando = True
        
        # Control de estados de teclas para evitar activación continua
        self.teclas_activadas = {
            pygame.K_a: False,
            pygame.K_s: False, 
            pygame.K_d: False,
            pygame.K_w: False
        }
    
    def reiniciar_pelota(self):
        """
        Reinicia la pelota en una posición aleatoria MÁS ALEJADA
        La pelota ahora inicia en el 25% superior de la pantalla
        """
        # Posición Y entre 100 y 200 (zona superior)
        posicion_y = random.randint(100, 200)
        self.pelota = Pelota(random.randint(100, 700), posicion_y)
        self.pelota.velocidad_x = random.choice([-5, 5])
        self.pelota.velocidad_y = 5
    
    def manejar_modos(self, teclas):
        """
        Maneja la activación de modos especiales usando el patrón Decorator
        Aquí es donde se ejecutan los métodos decorados
        """
        # Estado actual de las teclas de modo
        teclas_actuales = {
            pygame.K_a: teclas[pygame.K_a],
            pygame.K_s: teclas[pygame.K_s],
            pygame.K_d: teclas[pygame.K_d],
            pygame.K_w: teclas[pygame.K_w]
        }
        
        # Detectar cambios de estado (edge detection)
        for tecla, presionada in teclas_actuales.items():
            if presionada and not self.teclas_activadas[tecla]:
                # Tecla recién presionada - EJECUTAR MÉTODOS DECORADOS
                if tecla == pygame.K_a:
                    self.raqueta.activar_modo_rapido(True)  # Se ejecuta el decorator
                elif tecla == pygame.K_s:
                    self.raqueta.activar_modo_ancho(True)   # Se ejecuta el decorator
                elif tecla == pygame.K_d:
                    self.raqueta.activar_modo_imantacion(True)  # Se ejecuta el decorator
                elif tecla == pygame.K_w:
                    self.raqueta.activar_modo_normal(True)  # Se ejecuta el decorator
            
            # Actualizar estado para el próximo frame
            self.teclas_activadas[tecla] = presionada
    
    def actualizar(self, teclas):
        """Bucle principal de actualización del juego"""
        # 1. Manejar modos especiales (patrón Decorator)
        self.manejar_modos(teclas)
        
        # 2. Movimiento base de la raqueta
        self.raqueta.mover(teclas)
        
        # 3. Aplicar efectos del modo actual
        if self.raqueta.modo_actual == "Imantación":
            self.raqueta.aplicar_imantacion(self.pelota)
        
        # 4. Actualizar física de la pelota
        self.pelota.mover()
        
        # 5. Detectar colisiones y actualizar puntuación
        if self.pelota.verificar_colision(self.raqueta):
            self.puntaje += 10 * self.nivel
        
        # 6. Manejar pérdida de vidas
        if not self.pelota.activa:
            self.vidas -= 1
            if self.vidas > 0:
                self.reiniciar_pelota()
                # Reset al modo normal al perder vida
                self.raqueta.activar_modo_normal(True)
            else:
                self.esta_ejecutando = False
        
        # 7. Sistema de niveles progresivos
        if self.puntaje >= self.nivel * 100:
            self.nivel += 1
            self.pelota.velocidad_x *= 1.2
            self.pelota.velocidad_y *= 1.2
    
    def dibujar(self, pantalla):
        """Renderiza todos los elementos del juego"""
        pantalla.fill((0, 0, 0))  # Fondo negro
        
        # Dibujar elementos del juego
        self.pelota.dibujar(pantalla)
        self.raqueta.dibujar(pantalla)
        
        # =====================================================================
        # INTERFAZ DE USUARIO - Información del estado del juego
        # =====================================================================
        
        # Panel de estadísticas principales
        texto_puntaje = self.fuente.render(f"Puntos: {self.puntaje}", True, (255, 255, 255))
        texto_vidas = self.fuente.render(f"Vidas: {self.vidas}", True, (255, 255, 255))
        texto_nivel = self.fuente.render(f"Nivel: {self.nivel}", True, (255, 255, 255))
        texto_modo = self.fuente.render(f"Modo: {self.raqueta.modo_actual}", 
                                      True, self.raqueta.color)
        
        pantalla.blit(texto_puntaje, (10, 10))
        pantalla.blit(texto_vidas, (10, 50))
        pantalla.blit(texto_nivel, (10, 90))
        pantalla.blit(texto_modo, (10, 130))
        
        # Estadísticas detalladas del modo actual
        config = self.raqueta.modos[self.raqueta.modo_actual]
        stats_text = f"Velocidad: {config['velocidad']} | Ancho: {config['ancho']}"
        texto_stats = self.fuente_pequena.render(stats_text, True, (200, 200, 200))
        pantalla.blit(texto_stats, (10, 170))
        
        descripcion_text = f"Descripción: {config['descripcion']}"
        texto_desc = self.fuente_pequena.render(descripcion_text, True, (150, 150, 255))
        pantalla.blit(texto_desc, (10, 195))
        
        # =====================================================================
        # PANEL DE INSTRUCCIONES - Explicación del patrón Decorator
        # =====================================================================
        instrucciones = [
            "🎮 CONTROLES - PATRÓN DECORATOR APLICADO:",
            "FLECHAS ← → : Movimiento base (siempre activo)",
            "A : @modo_rapido → +Velocidad, -Ancho",
            "S : @modo_ancho → +Ancho, -Velocidad", 
            "D : @modo_imantacion → Atrae pelota",
            "W : @modo_normal → Vuelve a configuración base",
            "",
            "💡 EL DECORATOR AGREGA:",
            "- Logging automático de modos activados",
            "- Validación de entrada de teclas", 
            "- Mensajes informativos en consola"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            if i == 0:
                color = (255, 255, 0)  # Amarillo para título
            elif i >= 7:
                color = (0, 255, 255)  # Cyan para información del decorator
            else:
                color = (200, 200, 200)  # Gris para instrucciones normales
            texto = self.fuente_pequena.render(instruccion, True, color)
            pantalla.blit(texto, (400, 10 + i * 25))


def main():
    """
    Función principal del juego - PUNTO DE ENTRADA
    """
    # Inicialización de Pygame
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Squash - Patrón Decorator Implementado")
    reloj = pygame.time.Clock()
    
    # Instanciar el juego
    juego = JuegoSquash()
    
    # Mensajes iniciales explicativos
    print("=" * 60)
    print("🎯 SQUASH - IMPLEMENTACIÓN DEL PATRÓN DECORATOR")
    print("=" * 60)
    print("📖 EXPLICACIÓN DEL DECORATOR:")
    print("   - @modo_especial envuelve métodos de activación")
    print("   - Agrega funcionalidad sin modificar código original") 
    print("   - Ejemplo práctico de Open/Closed Principle")
    print("=" * 60)
    print("🎮 CONTROLES:")
    print("   FLECHAS: Mover raqueta")
    print("   A: Modo RÁPIDO (Decorator aplicado)")
    print("   S: Modo ANCHO (Decorator aplicado)")
    print("   D: Modo IMANTACIÓN (Decorator aplicado)")
    print("   W: MODO NORMAL (Decorator aplicado)")
    print("=" * 60)
    print("🚀 INICIANDO JUEGO...")
    print("   - Pelota inicia en posición más alejada (1/4 superior)")
    print("   - Observa los mensajes de decorator en consola")
    print("=" * 60)
    
    # Bucle principal del juego
    while juego.esta_ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego.esta_ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    juego.esta_ejecutando = False
        
        # Actualizar estado del juego
        teclas = pygame.key.get_pressed()
        juego.actualizar(teclas)
        juego.dibujar(pantalla)
        
        # Control de FPS y actualización de pantalla
        pygame.display.flip()
        reloj.tick(60)
    
    # Pantalla de Game Over
    pantalla.fill((0, 0, 0))
    texto_game_over = juego.fuente.render("GAME OVER", True, (255, 0, 0))
    texto_puntaje_final = juego.fuente.render(f"Puntaje Final: {juego.puntaje}", True, (255, 255, 255))
    texto_decorator_info = juego.fuente_pequena.render(
        "Patrón Decorator implementado exitosamente", True, (0, 255, 255))
    texto_salir = juego.fuente.render("Presiona cualquier tecla para salir", True, (200, 200, 200))
    
    pantalla.blit(texto_game_over, (350, 250))
    pantalla.blit(texto_puntaje_final, (300, 300))
    pantalla.blit(texto_decorator_info, (250, 340))
    pantalla.blit(texto_salir, (250, 380))
    pygame.display.flip()
    
    # Esperar input para salir
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:
                esperando = False
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()