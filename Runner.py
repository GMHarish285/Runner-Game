import pygame
from sys import exit
from random import randint

pygame.init()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # .time.get_ticks - returns the time im milliseconds(1sec=1000ms)
    score_surf = test_font.render(f'SCORE: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Pixeltype.ttf", 50)  # if we wanna use default text, give (None, 50)

game_active = False
start_time = 0
score = 0

# creating surfaces(basically images); the img that is called the latest, will appear on the top
# in a surface topleft point is always considered and position of a surface depends only on the topleft point
sky_surf = pygame.image.load("Sky.png").convert()  # .convert() - changes the img to something which can be interpreted easily
ground_surf = pygame.image.load("ground.png").convert()

# score_surf = test_font.render("My game", False, (64, 64, 64))  # (text, AA*smoothing text(here not needed)*, colour)
# score_rect = score_surf.get_rect(center=(400, 50))

# obstacles
snail_frame_1 = pygame.image.load("snail1.png").convert_alpha()  # _alpha - to remove the white bg of the img
snail_frame_2 = pygame.image.load("snail2.png").convert_alpha()
snail_frame_list = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frame_list[snail_frame_index]

fly_frame_1 = pygame.image.load("Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("Fly2.png").convert_alpha()
fly_frame_list = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frame_list[fly_frame_index]

obstacle_rect_list = []

# player  # in a rectangle there are 8 points at each corner and centre of each edge, we can specify coordinates of each point
player_walk_1 = pygame.image.load("player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))  # .get_rect - it takes a surface and draws a rectangle around it
player_gravity = 0
# intro screen
player_stand = pygame.image.load("player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # .rotozoom(surf, angle, scale times)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("RUNNER", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press SPACE to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  # (event, time interval)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # pygame.quit is the exact opposite of pygame.init, it uninitialise pygame
            exit()  # closes any kind of code, so while True loop is *gone* and code will end

        if game_active:
            # control with mouse
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):  # .pos - returns the position of mouse(event is mouse movement)
                    player_gravity = -20

            # control with keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int((pygame.time.get_ticks() - start_time) / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frame_list[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frame_list[fly_frame_index]


    if game_active:
        screen.blit(sky_surf, (0, 0))  # (img, coordinates)
        screen.blit(ground_surf, (0, 300))  # #RRBBGG - hexadecimal value of RGB
        # pygame.draw.rect(screen, '#c8c8ec', score_rect)   # .draw.rect(surface on which to draw, colour, the actual rectangle we wanna draw, line width, border radius)
        # pygame.draw.rect(screen, '#c8c8ec', score_rect, 10)  # above line for inner part, this line for outer part(cuz without the adjustment of border it looks weird)
        # screen.blit(score_surf, score_rect)
        score = display_score()  # storing current time(it is returned) in score

        # snail_rect.x -= 4
        # if snail_rect.right <= 0:  # when the right of snail disappears, left of snail appears on right
        #     snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)  # instead of directly giving coordinates, we can give the position of the rectangle

        # player
        player_gravity += 1
        player_rect.y += player_gravity  # .y - rectangle's Y-axis
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision:
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)  # tells the computer to not run faster than 60fps(maximum fps)

''' TIP: if we wanna know about the coordinates of the edge or vertex of a rectangle, print(rectangleObj.left)
flappy: gravity = -20, player_rect.y += 1

pygame.transform.scale(img, (x, y coord) - scale an img; .scale2x - 2 times
'''
