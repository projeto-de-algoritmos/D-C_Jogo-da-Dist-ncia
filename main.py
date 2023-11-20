import pygame
import sys
import random
import math
import time

# Inicialização do Pygame
pygame.init()

# Definição de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Distância")

# Variáveis do jogo
points = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(25)]
selected_points = set()
game_over = False
game_won = False
start_time = None # Tempo de início


# Clock do Pygame para controlar a taxa de quadros
clock = pygame.time.Clock()

# Função para calcular a distância entre dois pontos
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Função para encontrar o par de pontos mais próximo usando o algoritmo de divisão e conquista
def dc_closest_pair(points):
    if len(points) <= 3:
        return brute_force_closest_pair(points)

    sorted_points = sorted(points)
    median_index = len(sorted_points) // 2
    median_point = sorted_points[median_index][0]

    left_points = [point for point in points if int(point[0]) <= median_point]
    right_points = [point for point in points if int(point[0]) > median_point]

    left_closest_pair = dc_closest_pair(left_points)
    right_closest_pair = dc_closest_pair(right_points)

    if left_closest_pair and right_closest_pair:
        min_distance = min(calculate_distance(left_closest_pair[0], left_closest_pair[1]),
                           calculate_distance(right_closest_pair[0], right_closest_pair[1]))

        strip_points = [point for point in points if abs(int(point[0]) - median_point) < min_distance]
        strip_closest_pair = closest_pair_strip(strip_points, min_distance)

        if strip_closest_pair and strip_closest_pair[0] and strip_closest_pair[1]:
            if calculate_distance(strip_closest_pair[0], strip_closest_pair[1]) < min_distance:
                return strip_closest_pair
        elif min_distance == calculate_distance(left_closest_pair[0], left_closest_pair[1]):
            return left_closest_pair
        else:
            return right_closest_pair
    elif left_closest_pair:
        return left_closest_pair
    elif right_closest_pair:
        return right_closest_pair
    else:
        return None

# Encontrar o par de pontos mais próximo usando o algoritmo de força bruta
def brute_force_closest_pair(points):
    min_distance = float('inf')
    closest_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = calculate_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = points[i], points[j]

    return closest_pair

# Define closest_pair_strip function
def closest_pair_strip(strip_points, d):
    min_distance = d
    closest_pair = None

    for i in range(len(strip_points)):
        for j in range(i + 1, min(len(strip_points), i + 7)):
            if calculate_distance(strip_points[i], strip_points[j]) < min_distance:
                min_distance = calculate_distance(strip_points[i], strip_points[j])
                closest_pair = strip_points[i], strip_points[j]

    return closest_pair

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if start_time is None:
                start_time = time.time()

            mouse_pos = pygame.mouse.get_pos()
            clicked_point = min(points, key=lambda p: calculate_distance(p, mouse_pos))
            
            # Encontrar o par de pontos mais próximo
            closest_pair_result = dc_closest_pair(points)
            # print(f"Clicked point: {clicked_point}")
            # print(f"Closest pair result: {closest_pair_result}")
            
            # Modifique a condição abaixo
            if clicked_point in closest_pair_result:
                game_over = True
            else:
                selected_points.add(clicked_point)
                points.remove(clicked_point)

    # Atualização da tela
    screen.fill(BLACK)

    # Desenhar pontos
    for point in points:
        color = BLACK if point in selected_points else WHITE
        pygame.draw.circle(screen, color, point, 10)

    # Exibir mensagem de game over ou vitória
    if game_over:
        font = pygame.font.Font(None, 30)
        text = font.render("Game Over - Você selecionou o par de pontos mais próximo!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    elif len(points) == 2:
        if not game_won:  # Apenas calcula o tempo final uma vez
            final_time = time.time() - start_time
            game_won = True
        font = pygame.font.Font(None, 30)
        text = font.render(f"Você venceu! Todos os pontos foram eliminados em {final_time:.2f} segundos.", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
