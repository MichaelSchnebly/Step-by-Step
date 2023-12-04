import glfw
import OpenGL.GL as gl
from freetype import Face

def load_font(font_file, size):
    face = Face(font_file)
    face.set_char_size(size * 64)
    return face

def render_text(face, text, x, y, scale):
    for char in text:
        face.load_char(char)
        bitmap = face.glyph.bitmap
        # Create texture and render the bitmap here
        # Position the text at (x, y) and apply the scale
        x += face.glyph.advance.x

def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "GLFW Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    gl.glClearColor(1.0, 1.0, 1.0, 1.0)

    # Load font
    face = load_font("fonts/Montserrat-Black.otf", 100)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Render text
        render_text(face, "Hello, World!", 10, 10, 1.0)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()