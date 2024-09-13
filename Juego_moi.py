import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurar dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MOI")

# Colores pastel
COLORES = [(255, 182, 193), (176, 224, 230), (255, 228, 196), (221, 160, 221)]

# Cargar sonidos
sonido_explosion = pygame.mixer.Sound("explosion.wav")

# Clase para los objetos que se mueven
class Objeto(pygame.sprite.Sprite):
    def __init__(self, imagen):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imagen), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - 50)
        self.rect.y = random.randint(0, ALTO - 50)
        self.velocidad = [random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(2)]

    def update(self):
        self.rect.x += self.velocidad[0]
        self.rect.y += self.velocidad[1]
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad[0] *= -1
        if self.rect.top < 0 or self.rect.bottom > ALTO:
            self.velocidad[1] *= -1

# Clase para el gato naranja
class GatoNaranja(Objeto):
    def __init__(self):
        super().__init__("gato_naranja.png")

# Función principal del juego
def main():
    reloj = pygame.time.Clock()
    objetos = pygame.sprite.Group()
    puntuacion = 0
    tiempo = 0
    dificultad = 1
    contador_objetos = 0

    # Cargar imágenes de los objetos
    imagenes = ["pez.png", "bandera.png", "raviol.png", "pajaro.png"]

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for objeto in objetos:
                    if objeto.rect.collidepoint(evento.pos):
                        if isinstance(objeto, GatoNaranja):
                            # Reiniciar el juego
                            objetos.empty()
                            puntuacion = 0
                            dificultad = 1
                            contador_objetos = 0
                        else:
                            sonido_explosion.play()
                            objetos.remove(objeto)
                            puntuacion += 1
                            contador_objetos += 1
                            if contador_objetos % 20 == 0:
                                gato = GatoNaranja()
                                objetos.add(gato)
                        break

        # Añadir nuevos objetos según la dificultad
        if len(objetos) < dificultad:
            imagen = random.choice(imagenes)
            objeto = Objeto(imagen)
            objetos.add(objeto)

        objetos.update()

        pantalla.fill(random.choice(COLORES))
        objetos.draw(pantalla)

        # Mostrar puntuación y tiempo
        fuente = pygame.font.SysFont(None, 36)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (0, 0, 0))
        pantalla.blit(texto_puntuacion, (10, 10))

        pygame.display.flip()
        reloj.tick(60)
        tiempo += 1

        # Incrementar dificultad con el tiempo
        if tiempo % 600 == 0:
            dificultad += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
