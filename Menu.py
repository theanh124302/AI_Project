import pygame
import subprocess
import sys
import EngineProcess.Engine

pygame.init()
window_width = 512
window_height = 512
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chess AI G15")
black = (0, 0, 0)
white = (255, 255, 255)
gray = (120, 120, 120)
dark_gray = (70, 70, 70)
font = pygame.font.Font(None, 36)
font_icon = pygame.font.Font('DejaVuSans.ttf', 36)
font_icon2 = pygame.font.Font('NotoEmoji-VariableFont_wght.ttf',36)
start_button_x = window_width // 2 - 50
start_button_y = window_height // 2 + 50
guide_button_x = window_width // 2 - 50
guide_button_y = window_height // 2 +110
quit_button_x = window_width // 2 - 50
quit_button_y = window_height // 2 + 170
back_button_x = 20
back_button_y = 20
button_width = 100
button_height = 45
text_x1 = 95
text_y1 = 180
text_y2 = text_y1 + 35
text_y3 = text_y2 + 35
text_y4 = text_y3 + 35
text_y5 = text_y4 + 35
text_y6 = text_y5 + 35
text_y7 = text_y6 + 35
gt = "menu"
start_button_hovered = False
start_button_pressed = False
guide_button_hovered = False
guide_button_pressed = False
back_button_hovered = False
back_button_pressed = False
quit_button_hovered = False
quit_button_pressed = False
running = True
chessStart = False
background_image = pygame.image.load("images/wallpaper.png")

def drawMenu():
    scaled_background = pygame.transform.scale(background_image, (window_width, window_height))
    window.blit(scaled_background, (0, 0))

    # Vẽ nút "Start" với hiệu ứng hover, press và click
    if start_button_pressed:
        pygame.draw.rect(window, dark_gray, (start_button_x, start_button_y, button_width, button_height), border_radius=5)
    elif start_button_hovered:
        pygame.draw.rect(window, gray, (start_button_x, start_button_y, button_width, button_height), border_radius=5)
    else:
        pygame.draw.rect(window, black, (start_button_x, start_button_y, button_width, button_height), border_radius=5)

    if start_button_hovered:
        start_text = font_icon.render("\u2694", True, white)
        text_x = start_button_x + (button_width - start_text.get_width()) // 2
        text_y = start_button_y + (button_height - start_text.get_height()) // 2
        window.blit(start_text, (text_x, text_y))
    else:
        start_text = font.render("Start", True, white)
        text_x = start_button_x + (button_width - start_text.get_width()) // 2
        text_y = start_button_y + (button_height - start_text.get_height()) // 2
        window.blit(start_text, (text_x, text_y))

    # Vẽ nút "Guide" với hiệu ứng hover, press và click

    if guide_button_pressed:
        pygame.draw.rect(window, dark_gray, (guide_button_x, guide_button_y, button_width, button_height), border_radius=5)
    elif guide_button_hovered:
        pygame.draw.rect(window, gray, (guide_button_x, guide_button_y, button_width, button_height), border_radius=5)
    else:
        pygame.draw.rect(window, black, (guide_button_x, guide_button_y, button_width, button_height), border_radius=5)

    if guide_button_hovered:
        guide_text = font_icon2.render("\U0001F4D6", True, white)
        text_x = guide_button_x + (button_width - guide_text.get_width()) // 2
        text_y = guide_button_y + (button_height - guide_text.get_height()) // 2
        window.blit(guide_text, (text_x, text_y))
    else:
        guide_text = font.render("Control", True, white)
        text_x = guide_button_x + (button_width - guide_text.get_width()) // 2
        text_y = guide_button_y + (button_height - guide_text.get_height()) // 2
        window.blit(guide_text, (text_x, text_y))

    if quit_button_pressed:
        pygame.draw.rect(window, dark_gray, (quit_button_x, quit_button_y, button_width, button_height), border_radius=5)
    elif quit_button_hovered:
        pygame.draw.rect(window, gray, (quit_button_x, quit_button_y, button_width, button_height), border_radius=5)
    else:
        pygame.draw.rect(window, black, (quit_button_x, quit_button_y, button_width, button_height), border_radius=5)

    if quit_button_hovered:
        quit_text = font_icon.render("\U0001F61E", True, white)
        text_x = quit_button_x + (button_width - quit_text.get_width()) // 2
        text_y = quit_button_y + (button_height - quit_text.get_height()) // 2
        window.blit(quit_text, (text_x, text_y))
    else:
        quit_text = font.render("Quit", True, white)
        text_x = quit_button_x + (button_width - quit_text.get_width()) // 2
        text_y = quit_button_y + (button_height - quit_text.get_height()) // 2
        window.blit(quit_text, (text_x, text_y))

def drawGuide():
    window.fill(white)
    scaled_background = pygame.transform.scale(background_image, (window_width, window_height))
    window.blit(scaled_background, (0, 0))

    if back_button_pressed:
        pygame.draw.rect(window, dark_gray, (back_button_x, back_button_y, button_width, button_height),
                         border_radius=5)
    elif back_button_hovered:
        pygame.draw.rect(window, gray, (back_button_x, back_button_y, button_width, button_height), border_radius=5)
    else:
        pygame.draw.rect(window, black, (back_button_x, back_button_y, button_width, button_height), border_radius=5)

    if back_button_hovered:
        back_text = font_icon.render("\u2190", True, white)
        text_x = back_button_x + (button_width - back_text.get_width()) // 2
        text_y = back_button_x + (button_height - back_text.get_height()) // 2
        window.blit(back_text, (text_x, text_y))
    else:
        back_text = font.render("Back", True, white)
        text_x = back_button_x + (button_width - back_text.get_width()) // 2
        text_y = back_button_x + (button_height - back_text.get_height()) // 2
        window.blit(back_text, (text_x, text_y))

    background_rect = pygame.Rect(66, 150, 400, 300)
    pygame.draw.rect(window, (0, 0, 0), background_rect)
    # Vẽ văn bản mới
    guide_text = font.render("Difficulty Level (Depth) : 0-5", True, white)
    window.blit(guide_text, (text_x1, text_y1))

    guide_text = font.render("Undo : Z", True, white)
    window.blit(guide_text, (text_x1, text_y2))

    guide_text = font.render("Reset : R", True, white)
    window.blit(guide_text, (text_x1, text_y3))

    guide_text = font.render("MiniMax Algorithm : M", True, white)
    window.blit(guide_text, (text_x1, text_y4))

    guide_text = font.render("NegaMax Algorithm : N", True, white)
    window.blit(guide_text, (text_x1, text_y5))

    guide_text = font.render("Monte Carlo Tree Search : C", True, white)
    window.blit(guide_text, (text_x1, text_y6))

    guide_text = font.render("Principal Variation Search : P", True, white)
    window.blit(guide_text, (text_x1, text_y7))



def run_game():
    subprocess.run(["python", "Main.py"])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_x <= mouse_pos[0] <= start_button_x + button_width and \
                start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                start_button_pressed = True
            elif guide_button_x <= mouse_pos[0] <= guide_button_x + button_width and \
                guide_button_y <= mouse_pos[1] <= guide_button_y + button_height:
                guide_button_pressed = True
            elif back_button_x <= mouse_pos[0] <= back_button_x + button_width and \
                back_button_y <= mouse_pos[1] <= back_button_y + button_height:
                back_button_pressed = True
            elif quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                quit_button_y <= mouse_pos[1] <= quit_button_y + button_height:
                quit_button_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if start_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_x <= mouse_pos[0] <= start_button_x + button_width and \
                   start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                    run_game()
                    pygame.quit()
                    sys.exit()
                start_button_pressed = False
            if guide_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                if guide_button_x <= mouse_pos[0] <= guide_button_x + button_width and \
                   guide_button_y <= mouse_pos[1] <= guide_button_y + button_height:
                    gt = "guide"
                guide_button_pressed = False
            if quit_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                   quit_button_y <= mouse_pos[1] <= quit_button_y + button_height:
                    pygame.quit()
                    sys.exit()
                quit_button_pressed = True
            if back_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_x <= mouse_pos[0] <= back_button_x + button_width and \
                   back_button_y <= mouse_pos[1] <= back_button_y + button_height:
                    gt = "menu"
                back_button_pressed = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_x <= mouse_pos[0] <= start_button_x + button_width and \
               start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                start_button_hovered = True
            else:
                start_button_hovered = False
            if guide_button_x <= mouse_pos[0] <= guide_button_x + button_width and \
               guide_button_y <= mouse_pos[1] <= guide_button_y + button_height:
                guide_button_hovered = True
            else:
                guide_button_hovered = False
            if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                quit_button_y <= mouse_pos[1] <= quit_button_y + button_height:
                quit_button_hovered = True
            else:
                quit_button_hovered =False
            if back_button_x <= mouse_pos[0] <= back_button_x + button_width and \
               back_button_y <= mouse_pos[1] <= back_button_y + button_height:
                back_button_hovered = True
            else:
                back_button_hovered = False

    if gt == "menu":
        drawMenu()
    elif gt == "guide":
        drawGuide()

    pygame.display.flip()
