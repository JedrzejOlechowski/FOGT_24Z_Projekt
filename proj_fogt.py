import pygame
import sys
import numpy as np

def wave_animation(waves):
    amplitude = 50   # Amplituda fal (piksele)
    wavelength = 100 # Długość fali (piksele)

    # Ustawienia okna
    screen_width, screen_height = 800, 600
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Animacja fal z prędkościami fazową i grupową")

    clock = pygame.time.Clock()

    # Czas i przestrzeń
    x = np.linspace(0, screen_width, screen_width)
    time = 0
    input_speed = ""
    active_input = False
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_RETURN:
                        try:
                            speed = float(input_speed)
                            color = colors[len(waves) % len(colors)]
                            waves.append({"speed": speed, "color": color})
                        except ValueError:
                            pass
                        input_speed = ""
                        active_input = False

                    elif event.key == pygame.K_BACKSPACE:
                        input_speed = input_speed[:-1]

                    elif event.unicode.isdigit() or event.unicode == "." or (event.unicode == "-" and len(input_speed) == 0):
                        input_speed += event.unicode

                else:
                    if event.key == pygame.K_a:  # Dodawanie nowej fali
                        active_input = True

                    if event.key == pygame.K_r and waves:  # Usuwanie ostatniej fali
                        waves.pop()

                    if event.key == pygame.K_z:  # Zerowanie wszystkich fal
                        waves.clear()

        # Aktualizacja ekranu
        screen.fill((0, 0, 0))

        # Rysowanie siatki
        for i in range(0, screen_width, 50):
            pygame.draw.line(screen, (50, 50, 50), (i, 0), (i, screen_height))
        for j in range(0, screen_height, 50):
            pygame.draw.line(screen, (50, 50, 50), (0, j), (screen_width, j))

        combined_wave = np.zeros_like(x)

        # Rysowanie fal
        legend_y = 10
        line_spacing = 30
        for index, wave in enumerate(waves):
            wave_position = amplitude * np.sin(2 * np.pi * (x / wavelength - wave['speed'] * time))
            combined_wave += wave_position
            for i in range(len(x) - 1):
                pygame.draw.line(screen, wave['color'], (x[i], screen_height // 2 + wave_position[i]),
                                 (x[i + 1], screen_height // 2 + wave_position[i + 1]), 2)
            legend = pygame.font.SysFont(None, 24).render(f"Fala {index + 1}: v_f = {wave['speed']:.2f}", True, wave['color'])
            screen.blit(legend, (10, legend_y + index * line_spacing))

        # Wyświetlanie prędkości fazowej i grupowej
        if waves:
            phase_speed = wavelength * waves[0]['speed']  # Przykład dla pierwszej fali
            avg_speed = sum(wave['speed'] for wave in waves) / len(waves)
            phase_speed_label = pygame.font.SysFont(None, 24).render(f"Prędkość fazowa (pierwsza fala): {phase_speed:.2f}", True, (255, 255, 255))
            avg_speed_label = pygame.font.SysFont(None, 24).render(f"Prędkość grupowa: {avg_speed:.2f}", True, (255, 255, 0))
            screen.blit(phase_speed_label, (10, legend_y + len(waves) * line_spacing))
            screen.blit(avg_speed_label, (10, legend_y + (len(waves) + 1) * line_spacing))

        # Rysowanie sumy fal w głównym obszarze
        for i in range(len(x) - 1):
            pygame.draw.line(screen, (255, 255, 0), (x[i], screen_height // 2 + combined_wave[i]),
                             (x[i + 1], screen_height // 2 + combined_wave[i + 1]), 2)

        # Wyświetlanie fali sumarycznej na dole ekranu
        plot_height = 100
        pygame.draw.rect(screen, (50, 50, 50), (0, screen_height - plot_height, screen_width, plot_height))
        for i in range(len(x) - 1):
            pygame.draw.line(screen, (255, 255, 255),
                             (x[i], screen_height - plot_height + combined_wave[i] * 0.1 + plot_height // 2),
                             (x[i + 1], screen_height - plot_height + combined_wave[i + 1] * 0.1 + plot_height // 2), 1)

        # Wyświetlanie osi OY
        pygame.draw.line(screen, (200, 200, 200), (50, 0), (50, screen_height), 1)
        font = pygame.font.SysFont(None, 20)
        for j in range(-amplitude, amplitude + 1, 25):
            label = font.render(f"{j}", True, (200, 200, 200))
            screen.blit(label, (10, screen_height // 2 - j))

        # Obsługa dodawania prędkości nowej fali
        if active_input:
            instruction = pygame.font.SysFont(None, 36).render("Wprowadź prędkość nowej fali:", True, (255, 255, 255))
            input_surface = pygame.font.SysFont(None, 36).render(input_speed, True, (255, 255, 255))
            screen.blit(instruction, (10, 10))
            pygame.draw.rect(screen, (255, 255, 255), (10, 50, 300, 40), 2)
            screen.blit(input_surface, (15, 50))

        # Aktualizacja czasu
        time += 0.01

        # Odświeżanie ekranu
        pygame.display.flip()
        clock.tick(60)

def main():
    waves = []
    wave_animation(waves)

if __name__ == "__main__":
    main()
