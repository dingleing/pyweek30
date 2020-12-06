from PIL import Image
from numpy import asarray
# load the image
image = Image.open('assets/another_map.png')
# convert image to numpy array
data = asarray(image)
# summarize shape
print(data.shape)

# create Pillow image
final_map = ""
for line in data:
    for color in line:
        if color[0] == 0 and color[1] == 0 and color[2] == 0:
            final_map += "1"
        elif color[0] == 255 and color[1] == 0 and color[2] == 0:
            final_map += "2"
        elif color[0] == 0 and color[1] == 255 and color[2] == 0:
            final_map += "3"
        elif color[0] == 0 and color[1] == 0 and color[2] == 255:
            final_map += "4"
        elif color[0] == 255 and color[1] == 255 and color[2] == 0:
            final_map += "5"
        elif color[0] == 0 and color[1] == 100 and color[2] == 0:
            final_map += "7"
        elif color[0] == 100 and color[1] == 0 and color[2] == 0:
            final_map += "6"
        elif color[0] == 0 and color[1] == 0 and color[2] == 100:
            final_map += "9"
        elif color[0] == 200 and color[1] == 0 and color[2] == 0:
            final_map += "a"
        elif color[0] == 200 and color[1] == 200 and color[2] == 0:
            final_map += "b"
        elif color[0] == 255 and color[1] == 255 and color[2] == 200:
            final_map += "c"
        else:
            final_map += "0"
    final_map += "\n"

file = open("assets/the_map.txt", "w")
print(final_map)
file.write(final_map)
file.close()
