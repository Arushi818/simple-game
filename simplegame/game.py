import cv2
import numpy as np
import random
import pygame

# Initialize game variables
width, height = 1429, 2000
paddle_width, paddle_height = 300, 150
ball_radius = 40

paddle_x = (width - paddle_width) // 2
paddle_y = height - paddle_height - 20

ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = 0
ball_speed = 10

paused = False
score = 0

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create a black image (background)
backgroundImg = cv2.imread('background.jpg')

def draw_paddle(image):
    # Draw a cake as the paddle
    cv2.rectangle(image, (paddle_x, paddle_y), (paddle_x + paddle_width, paddle_y + paddle_height), (34, 62, 102), -1)
    cv2.rectangle(image, (paddle_x + 20, paddle_y - 60), (paddle_x + paddle_width - 20, paddle_y), (17, 21, 66), -1)

def draw_ball(image):
    # Draw a white candle with an orange flame as the ball
    cv2.rectangle(image, (ball_x, ball_y), (ball_x + 23, ball_y + 60), (255,113,82), -1)  # White candle
    flame_radius = ball_radius // 3
    cv2.circle(image, (ball_x + 10, ball_y - ball_radius), flame_radius, (0, 165, 255), -1)  # Orange flame

def draw_instructions(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    instructions = [
        "Game Instructions:",
        "Move the paddle using the left and right arrow keys.",
        "Catch the falling ball.",
        "Press 'P' to pause or resume the game.",
        "Hit the Q button to exit the game."
    ]

    for i, line in enumerate(instructions):
        cv2.putText(image, line, (20, 30 * (i + 1)), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

def draw_score(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 5
    font_thickness = 5
    score_text = f"Score: {score}"
    cv2.putText(image, score_text, (50,150), font, font_scale, (0,0,0), font_thickness, cv2.LINE_AA)

def update_game():
    global paddle_x, ball_x, ball_y, score

    if not paused:
        # Move the ball
        ball_y += ball_speed

        # Check for collision with the paddle
        if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y < paddle_y + paddle_height:
            # Ball caught, reset its position and increase the score
            ball_x = random.randint(ball_radius, width - ball_radius)
            ball_y = 0
            score += 1

        # Check if the ball has reached the bottom
        if ball_y > height:
            # Ball missed, reset its position
            ball_x = random.randint(ball_radius, width - ball_radius)
            ball_y = 0

def main():
    global paddle_x, paused, score

    show_menu()

    pygame.display.set_caption("Catch the Ball")

    while True:
        key = cv2.waitKey(10)

        if key == ord('s') or key == ord('S'):
            # Start the game
            break
        elif key == ord('q') or key == ord('Q'):
            # Exit the game
            cv2.destroyAllWindows()
            return
        elif key == ord('i') or key == ord('I'):
            # Show instructions
            show_instructions()

    cv2.destroyWindow("Menu")

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Create a copy of the background image
        game_image = backgroundImg.copy()

        # Update game elements
        update_game()

        # Draw the game elements on the copy
        draw_paddle(game_image)
        draw_ball(game_image)
        draw_score(game_image)

        if paused:
            show_pause_message(game_image)

        # Show the copy with game elements
        cv2.imshow("Catch the Ball", game_image)

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move paddle based on pressed keys
        if keys[pygame.K_LEFT]:
            paddle_x = (paddle_x - 20) % (width - paddle_width)
        if keys[pygame.K_RIGHT]:
            paddle_x = (paddle_x + 20) % (width - paddle_width)

        clock.tick(30)  # Cap the background rate to 30 FPS

        # Check for keyboard input
        key = cv2.waitKeyEx(10)
        if key == 27:  # Press 'Esc' to exit
            break
        elif key == ord('p') or key == ord('P'):
            # Pause or resume the game
            paused = not paused

    cv2.destroyAllWindows()

def show_menu():
    menu_img = np.zeros((height, width, 3), dtype=np.uint8)
    menu_img[:] = (193,182,255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    start_text = "Press 'S' to start the game"
    exit_text = "Hit the escape key to exit the game"
    instructions_text = "Press 'I' for instructions"

    start_text_size = cv2.getTextSize(start_text, font, font_scale, font_thickness)[0]
    exit_text_size = cv2.getTextSize(exit_text, font, font_scale, font_thickness)[0]
    instructions_text_size = cv2.getTextSize(instructions_text, font, font_scale, font_thickness)[0]

    start_x = (width - start_text_size[0]) // 2
    start_y = height // 3

    exit_x = (width - exit_text_size[0]) // 2
    exit_y = 2 * height // 3

    instructions_x = (width - instructions_text_size[0]) // 2
    instructions_y = 2 * height // 3 + 50

    cv2.putText(menu_img, start_text, (start_x, start_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
    cv2.putText(menu_img, exit_text, (exit_x, exit_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
    cv2.putText(menu_img, instructions_text, (instructions_x, instructions_y), font, font_scale, (255, 255, 255),
                font_thickness, cv2.LINE_AA)

    cv2.imshow("Menu", menu_img)

def show_instructions():
    instructions_img = np.zeros((height, width, 3), dtype=np.uint8)
    instructions_img[:] = (193,182,255)  # Light Pink color
    draw_instructions(instructions_img)
    cv2.imshow("Instructions", instructions_img)
    cv2.waitKey(0)
    cv2.destroyWindow("Instructions")

if __name__ == "__main__":
    main()