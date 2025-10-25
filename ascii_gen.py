


from PIL import Image
import ascii_magic

path = "/home/aura/Pictures/logos/l.jpeg"

# Resize first with Pillow
img = Image.open(path)
img = img.resize((80, 60))

# Then convert
art = ascii_magic.from_pillow_image(img)
art.to_terminal()
