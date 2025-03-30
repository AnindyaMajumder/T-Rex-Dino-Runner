from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shapes.dinosaur import Dinosaur
from shapes.obstacles import MovingObstacles
from scene.scene import Scene
from scene.intro import IntroScene
from utils.utils import keyboard, keyboardUp, iterate
from logics.score_manager import ScoreManager
import time
import sys

# Game state variables
score_manager = ScoreManager()
moving_obstacles = MovingObstacles()  
dinosaur = Dinosaur()
scene = Scene()
intro_scene = IntroScene()
game_state = "intro"  # intro, playing, paused, game_over
pause = False
game_over = False
last_frame_time = time.time()
frame_time = 0
current_score = 0
mouse_x, mouse_y = 0, 0

high_score = score_manager.get_high_score()
intro_scene.set_high_score(high_score)


def showScreen():
    global pause, game_over, last_frame_time, frame_time, game_state, current_score, high_score
    
    # Calculate frame time for smooth animation
    current_time = time.time()
    frame_time = current_time - last_frame_time
    last_frame_time = current_time
    
    if game_state == "intro":
        # Draw intro screen
        intro_scene.update()
        intro_scene.draw(pause, current_score, scene.is_day)
        # Draw high score history
        intro_scene.draw_high_scores(score_manager.get_score_history(), 600, 350)
    elif game_state == "game_over":
        # Draw game over screen
        intro_scene.update()
        intro_scene.draw_game_over(current_score, high_score, scene.is_day)
    else:
        # Main game rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate(scene)

        # Draw background scene
        scene.draw()
        
        # Update game state if not paused or game over
        if game_state == "playing":
            # Update obstacle positions and speed
            current_speed = moving_obstacles.update()
            
            # Update dinosaur animation and position
            dinosaur.update(current_speed)
            
            # Update current score
            current_score = moving_obstacles.num_triangles_touched
            
            # Check for collisions
            try:
                if moving_obstacles.detect_collision(dinosaur.x, dinosaur.y):
                    game_state = "game_over"
                    # Update high score
                    high_score = max(high_score, current_score)
                    intro_scene.set_high_score(high_score)
                    # Save both the high score and the current score to history
                    try:
                        score_manager.save_score(current_score)
                        
                        # If this was a high score, save immediately
                        if current_score >= high_score:
                            score_manager.save_high_score(high_score, force=True)
                    except Exception as e:
                        print(f"Error saving score: {e}")
            except Exception as e:
                print(f"Error in collision detection: {e}")
        
        # Draw game elements
        moving_obstacles.draw()
        dinosaur.draw()
        
        # Display score
        displayScore()

    glutSwapBuffers()


def displayScore():
    """Display the score on the screen."""
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(600, 450)  # Position for the score display
    score_text = f"Score: {moving_obstacles.num_triangles_touched}" 
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    
    # Also display high score
    glRasterPos2f(400, 450)
    high_score_text = f"High: {high_score}"
    for char in high_score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


def keyboardHandler(key, x, y):
    global game_state, pause, game_over, current_score
    
    # Handle quit key (Q)
    if key == b'q':
        closeHandler()
        sys.exit(0)
    
    # Handle intro screen keys
    if game_state == "intro":
        if key == b' ':  # Space to start
            if pause:
                # Resume the game if paused
                game_state = "playing"
                pause = False
            else:
                # Start a new game
                resetGame()
                game_state = "playing"
        elif key == b'1' and pause:  # 1 to resume
            game_state = "playing"
            pause = False
        elif key == b'2' and pause:  # 2 to start new
            resetGame()
            game_state = "playing"
        return
    
    # Handle game over state
    elif game_state == "game_over":
        try:
            # Draw game over screen
            intro_scene.update()
            intro_scene.draw_game_over(current_score, high_score, scene.is_day)
        except Exception as e:
            print(f"Error drawing game over screen: {e}")
            # Fallback to a simple game over message
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glColor3f(1.0, 0.0, 0.0)
            glRasterPos2f(350, 250)
            for char in "GAME OVER":
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    
    # Handle pause toggle
    if key == b'\x1b':  # Escape key
        if game_state == "playing":
            game_state = "paused"
            pause = True
            intro_scene.set_high_score(high_score)  # Update high score in intro
            # Show the intro screen with pause menu
            game_state = "intro"
            return
        elif game_state == "paused":
            game_state = "playing"
            pause = False
            return
    
    # Normal gameplay keys
    if game_state == "playing":
        if key == b' ':  # Space to jump
            dinosaur.jump_press()
        elif key == b'd':  # D for day/night
            scene.toggle_day_night()


def keyboardUpHandler(key, x, y):
    if game_state == "playing" and key == b' ':
        dinosaur.jump_release()


def mouseHandler(button, state, x, y):
    global game_state, pause
    
    # Only process left mouse button clicks
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
        
    # Check for button clicks in intro screen
    if game_state == "intro":
        action = intro_scene.check_button_click(x, y)
        if action == "start":
            if pause:
                # Resume the game if paused
                game_state = "playing"
                pause = False
            else:
                # Start a new game
                resetGame()
                game_state = "playing"
    
    # Check for button clicks in game over screen
    elif game_state == "game_over":
        action = intro_scene.check_button_click(x, y)
        if action == "restart":
            resetGame()
        elif action == "menu":
            game_state = "intro"


def passiveMouseMotionHandler(x, y):
    global mouse_x, mouse_y
    
    mouse_x, mouse_y = x, y
    
    # Check for hover in intro screen
    if game_state == "intro" or game_state == "game_over":
        intro_scene.check_button_hover(x, y)


def resetGame():
    """Reset the game state."""
    global game_state, pause, game_over, current_score
    moving_obstacles.reset()
    scene.__init__()  # Reset scene
    dinosaur.__init__()  # Reset dinosaur
    game_state = "playing"
    game_over = False
    pause = False
    current_score = 0


def closeHandler():
    """Save high score when window is closed"""
    # Always save the high score when closing
    score_manager.save_high_score(high_score, force=True)
    
    # If we're in the middle of a game, save that score too
    if game_state == "playing" and current_score > 0:
        score_manager.save_score(current_score)
        
    print("Game closed. High scores saved.")


# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500)  # window size
glutInitWindowPosition(250, 150)
wind = glutCreateWindow(b"T-Rex Dino Runner")  # window name
glClearColor(0.529, 0.808, 0.922, 1.0)  # Set default clear color to light blue
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardHandler)
glutKeyboardUpFunc(keyboardUpHandler)
glutMouseFunc(mouseHandler)
glutPassiveMotionFunc(passiveMouseMotionHandler)
glutIdleFunc(showScreen)
glutCloseFunc(closeHandler)  # Register close handler
glutMainLoop()