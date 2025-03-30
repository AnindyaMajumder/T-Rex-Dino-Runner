from OpenGL.GL import *

def keyboard(key, x, y, dinosaur, scene, pause):
    """Handle keyboard input"""
    if key == b' ':  # Spacebar for jump
        dinosaur.jump_press()
    if key == b"d":  # 'd' for day-night toggle
        scene.toggle_day_night()
    if key == b"\x1b":  # Escape key for pause
        pause = not pause
    return pause

def keyboardUp(key, x, y, dinosaur):
    """Handle keyboard key release"""
    if key == b' ':  # Spacebar release
        dinosaur.jump_release()

def iterate(scene):
    """Setup OpenGL viewport and projection"""
    glViewport(0, 0, 800, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    scene.set_clear_color()  # Use scene method to set clear color
    glOrtho(0.0, 800, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()