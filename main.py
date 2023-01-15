import PIL, math
from PIL import Image

def horizontalFlip(img):

    #Pixels will be copied to a new image so it doesn't mirror itself
    manipulated_img = img.copy()

    w, h = img.size

    for row in range(h):
        for col in range(w):

            #Taking the RGB data from the pixel on the opposite side and placing it at the given position in the copied image
            pixel_rgb_data = img.getpixel((-(col + 1), row))
            manipulated_img.putpixel((col, row), pixel_rgb_data)

    manipulated_img.save("horizontalflip.jpg", format = "jpeg")


def verticalFlip(img):

    #Pixels will be copied to a new image so it doesn't mirror itself
    manipulated_img = img.copy()

    w, h = img.size

    for row in range(h):
        for col in range(w):

            #Taking the RGB data from the pixel on the opposite side and placing it at the given position in the copied image
            pixel_rgb_data = img.getpixel((col, -(row + 1)))
            manipulated_img.putpixel((col, row), pixel_rgb_data)

    manipulated_img.save("verticalflip.jpg", format = "jpeg")

def grayscale(img):
    w, h = img.size

    for row in range(h):
        for col in range(w):
            pixel_rgb_data = img.getpixel((col, row))

            #Storing the average RGB value in a new tuple
            grayscale_value = tuple([round((sum(pixel_rgb_data)) / 3)]) * 3
            img.putpixel((col, row), grayscale_value)

    img.save("grayscale.jpg", format = "jpeg")

def colourQuantization(img, CL):
    w, h = img.size

    for row in range(h):
        for col in range(w):

            euclidean_values = []
            pixel_rgb_data = img.getpixel((col, row))

            #Finding the euclidean distance from each value in the colour list for the given pixel
            for rgb_value in CL:
                euclidean_distance = math.sqrt((pixel_rgb_data[0] - rgb_value[0]) ** 2 + (pixel_rgb_data[1] - rgb_value[1]) ** 2 + (pixel_rgb_data[2] - rgb_value[2]) ** 2)
                euclidean_values.append(euclidean_distance)

            euclidean_values.sort()

            #Finding the RGB value with the shortest distance from the original RGB value and changing it accordingly
            for rgb_value in CL: 
                euclidean_distance = math.sqrt((pixel_rgb_data[0] - rgb_value[0]) ** 2 + (pixel_rgb_data[1] - rgb_value[1]) ** 2 + (pixel_rgb_data[2] - rgb_value[2]) ** 2)
                if euclidean_distance == euclidean_values[0]:
                    break

            img.putpixel((col, row), rgb_value)
    
    img.save("colourquantization.jpg", format = "jpeg")
            

def gaussianBlur(img, radius):
    w, h = img.size

    for row in range(h):
        for col in range(w):
            sum_r = 0
            sum_g = 0
            sum_b = 0
            num_pixels_traversed = 0

            #Traversing column by column within each row
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    
                    #Try except block to ignore when the function tries traversing a pixel that doesn't exist
                    try:
                        if j + col < 0 or i + row < 0 or j + col > w or i + row > h:
                            raise IndexError

                        sum_r += (img.getpixel((col + j, row + i)))[0]
                        sum_g += (img.getpixel((col + j, row + i)))[1]
                        sum_b += (img.getpixel((col + j, row + i)))[2] 
                        num_pixels_traversed += 1

                    except IndexError:
                        pass

            average_r = round(sum_r / num_pixels_traversed)
            average_g = round(sum_g / num_pixels_traversed)
            average_b = round(sum_b / num_pixels_traversed)

            blurred_value = tuple([average_r, average_g, average_b])   

            img.putpixel((col, row), blurred_value)
    
    img.save("gaussianblur.jpg", format = "jpeg")


def pixelate(img, threshold):
   w, h = img.size
  
   for row in range(0, h, threshold):
        for col in range(0, w, threshold):
            pixel_rgb_data = img.getpixel((col, row))

            #Traversing column by column within each row
            for i in range(threshold):
                for j in range(threshold):

                    #Try except block to ignore when the function tries traversing a pixel that doesn't exist
                    try:
                        if col + j > w or row + i > h:
                            raise IndexError
                        
                        #Copying the RGB data from the pixel found in the first loop to all pixels within the threshold
                        img.putpixel((col + j, row + i), pixel_rgb_data)

                    except IndexError:
                        pass
  
   img.save("pixelate.jpg", format = "jpeg")

#change the file name if you want to test your own image
filename = "mario.jpg"
img = Image.open(filename)

horizontalFlip(img.copy()) 
verticalFlip(img.copy()) 
grayscale(img.copy()) 

CL = [(0, 0, 0), (255, 255, 255)]
#CL = [(249, 228, 177), (17, 51, 75), (196, 51, 47), (122, 149, 158)]
#CL = [(45,70,82),(79,155,143),(228,196,119),(233,165,108),(217,117,89)]

colourQuantization(img.copy(), CL) 
gaussianBlur(img.copy(), 6) 
pixelate(img.copy(), 13) 