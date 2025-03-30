from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shapes.dinosaur import Dinosaur
from shapes.obstacles import MovingObstacles
from scene.scene import Scene
from utils.utils import keyboard, keyboardUp, iterate
import time

# Game state variables
moving_obstacles = MovingObstacles()  
dinosaur = Dinosaur()
scene = Scene()
pause = False
game_over = False
last_frame_time = time.time()
frame_time = 0

def showScreen():
    global pause, game_over, last_frame_time, frame_time
    
    # Calculate frame time for smooth animation
    current_time = time.time()
    frame_time = current_time - last_frame_time
    last_frame_time = current_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate(scene)

    # Draw background scene
    scene.draw()
    
    # Update game state if not paused or game over
    if not pause and not game_over:
        # Update obstacle positions and speed
        current_speed = moving_obstacles.update()
        
        # Update dinosaur animation and position
        dinosaur.update(current_speed)
        
        # Check for collisions
        if moving_obstacles.detect_collision(dinosaur.x, dinosaur.y):
            game_over = True
    
    # Draw game elements
    moving_obstacles.draw()
    dinosaur.draw()
    
    # Display score
    displayScore()
    
    # Display game over message if needed
    if game_over:
        displayGameOver()

    glutSwapBuffers()

def displayScore():
    """Display the score on the screen."""
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(600, 450)  # Position for the score display
    score_text = f"Score: {moving_obstacles.num_triangles_touched}" 
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def displayGameOver():
    """Display game over message and instructions to restart."""
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(300, 250)  # Center position
    game_over_text = "GAME OVER"
    for char in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
        
    glRasterPos2f(250, 220)
    restart_text = "Press 'R' to restart"
    for char in restart_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def keyboardHandler(key, x, y):
    global pause, game_over
    
    # Handle restart on game over
    if game_over and key == b'r':
        resetGame()
        return
        
    # Don't process other keys if game is over
    if game_over:
        return
        
    # Normal keyboard handling for running game
    pause = keyboard(key, x, y, dinosaur, scene, pause)

def keyboardUpHandler(key, x, y):
    if not game_over:
        keyboardUp(key, x, y, dinosaur)

def resetGame():
    """Reset the game state."""
    global game_over, pause
    moving_obstacles.reset()
    scene.__init__()  # Reset scene
    dinosaur.__init__()  # Reset dinosaur
    game_over = False
    pause = False

# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500)  # window size
glutInitWindowPosition(250, 150)
wind = glutCreateWindow(b"T-Rex Dino Runner")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardHandler)
glutKeyboardUpFunc(keyboardUpHandler)
glutIdleFunc(showScreen)
glutMainLoop()