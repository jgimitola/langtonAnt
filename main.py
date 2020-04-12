# Creado por Jesus Imitola
# GitHub User: jgimitola
# Fecha: del 19 de Marzo de 2020 hasta el 12 de Abril de 2020.

import pygame
import thorpy

import simulation


def main():
    pygame.init()  # Iniciamos pygame.
    infoObject = pygame.display.Info()
    icon = pygame.image.load('images/ant.png')

    preferredSize = int(infoObject.current_h * 0.88)  # Obtenemos la altura de la pantalla.
    application = thorpy.Application((preferredSize, preferredSize), "Langton's Ant", "pygame")

    # Verifica si el tamaño ingresado es válido y si lo es, inicia la simulación.
    def start():
        if tamaño.get_value().isdigit() and iteraciones.get_value().isdigit():
            tam = int(tamaño.get_value())
            it = int(iteraciones.get_value())
            if tam > 0 and it > 0:
                if tam > int(0.65 * (preferredSize // 2)):
                    thorpy.launch_blocking_alert(title="¡Tamaño no soportado!",
                                                 text="El tamaño actual generaría una grilla con celdas de tamaño cero.",
                                                 parent=background)
                    tamaño.set_value("")
                else:
                    simulation.simulate(tam, it, preferredSize)
            else:
                thorpy.launch_blocking_alert(title="¡Tamaño no soportado!",
                                             text="El tamaño no es válido.",
                                             parent=background)
        else:
            thorpy.launch_blocking_alert(title="¡Valores incorrectos!",
                                         text="Los valores introducidos no son válidos.",
                                         parent=background)
            tamaño.set_value("")
            iteraciones.set_value("")

    iteraciones = thorpy.Inserter(name="Iteraciones: ", value="1")  # Campo de número de iteraciones.
    tamaño = thorpy.Inserter(name="Tamaño: ", value="10")  # Campo de tamaño.
    boton = thorpy.make_button("Aceptar", start)  # Botón aceptar.

    title_element = thorpy.make_text("Configurar simulación", 22, (255, 255, 255))

    central_box = thorpy.Box(elements=[iteraciones, tamaño, boton])  # Contenedor central.
    central_box.fit_children(margins=(30, 30))
    central_box.center()  # center on screen
    central_box.set_main_color((220, 220, 220, 180))

    background = thorpy.Background((0, 0, 0), elements=[title_element, central_box])
    thorpy.store(background)

    menu = thorpy.Menu(background)
    menu.play()  # Lanzamos el menú.

    application.quit()


if __name__ == "__main__":
    main()
