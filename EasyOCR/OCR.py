import easyocr
import cv2
import numpy as np
import PIL
from PIL import Image, ImageDraw
from utils import base64_to_np

class OCR:
    MAX_IMG_SIZE = 2000
    
    def __init__(self, language="pt", debug=False):
        # for debug
        self.output = "result.jpg"
        self.debug = debug

        self.reader = easyocr.Reader(
            [language]
        )  # this needs to run only once to load the model into memory

    def draw_boxes(self, image, bounds, color="yellow", width=2):
        draw = ImageDraw.Draw(image)
        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
        return image

    # sort by y0
    def sortFunction(self, prediction):
        return prediction[0][3][1]

    def distance(self, a, b):
        return np.sqrt(np.pow(a[0] - b[0], 2) + np.pow(a[1] - b[1], 2))

    def merge_next_word(self, current_word, result, space):
        bMergedOnce = False
        while True:
            bMerged = False
            # to the left
            minIndex_left = -1
            minDistance_left = np.inf
            # to the right
            minIndex_right = -1
            minDistance_right = np.inf
            for index, r in enumerate(result):
                # distance between end and start < space
                d_left = self.distance(current_word[3], r[4])
                d_right = self.distance(current_word[4], r[3])
                # to the left
                if d_left < space:
                    if d_left < minDistance_left:
                        minDistance_left = d_left
                        minIndex_left = index
                # to the right
                if d_right < space:
                    if d_right < minDistance_right:
                        minDistance_right = d_right
                        minIndex_right = index
            # if found a word to the left next to the current one:
            if minIndex_left > -1:
                r = result[minIndex_left]
                current_word[0][0] = r[0][0]
                current_word[0][3] = r[0][3]
                current_word[1] = r[1] + " " + current_word[1]
                current_word[3] = r[3]
                result.pop(minIndex_left)
                # result list was shifted
                if minIndex_left < minIndex_right:
                    minIndex_right -= 1
                bMerged = True
                bMergedOnce = True
            # if found a word to the right next to the current one:
            if minIndex_right > -1:
                r = result[minIndex_right]
                current_word[0][1] = r[0][1]
                current_word[0][2] = r[0][2]
                current_word[1] += " " + r[1]
                current_word[4] = r[4]
                result.pop(minIndex_right)
                bMerged = True
                bMergedOnce = True
            # if didnt find any word to merge, break loop (need new line)
            if not bMerged:
                break
        return current_word, result, bMergedOnce

    def start_end_points(self, result):
        new_result = []
        for r in result:
            r = list(r)
            start = [(r[0][0][0] + r[0][3][0]) / 2, (r[0][0][1] + r[0][3][1]) / 2]
            end = [(r[0][1][0] + r[0][2][0]) / 2, (r[0][1][1] + r[0][2][1]) / 2]
            r.append(start)
            r.append(end)
            new_result.append(r)
        return new_result

    def process_lines(self, result):
        # add start and end points
        result = self.start_end_points(result)
        # need to sort before
        result = sorted(result, key=self.sortFunction)
        new_result = []
        while True:
            bMergedOnce = False
            # while there is a word not processed...
            while len(result) > 0:
                # get the word
                current_word = result.pop(0)
                # get the threshold distance to the next word
                space = 2 * (current_word[0][2][1] - current_word[0][1][1]) / 3
                # merge with next word
                current_word, result, bMerged = self.merge_next_word(
                    current_word, result, space
                )
                # append new word to new resultts
                new_result.append(current_word)
                # update bMerged
                bMergedOnce = bMergedOnce or bMerged
            # if didnt merged at least one time, break
            if not bMergedOnce:
                break

            # update vars to continue the loop
            result = new_result
            new_result = []
        # return new word bounds
        return new_result

    def get_image(self, base64_image, is_base64):
        if is_base64:
            # read data
            image = base64_to_np(base64_image)
        else:
            # read data
            image = cv2.imread(base64_image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # image must be between 0-255
        if np.max(image) < 1.1:
            image *= 255.0

        # CROP
        im = Image.fromarray(image.astype(np.uint8))

        # debug
        if self.debug:
            im.save("EasyOCR/input.png")

        width, height = im.size  # Get dimensions
        max_dim = max(width, height)
        scale = self.MAX_IMG_SIZE / max_dim
        im = im.resize((int(scale * width), int(scale * height)))

        # debug
        if self.debug:
            im.save("EasyOCR/resized.png")

        return np.asarray(im)

    # run OCR
    def __call__(self, base64_image, is_base64=True):
        # preprocess the image
        image_rgb = self.get_image(base64_image, is_base64=is_base64)

        result = self.reader.readtext(image_rgb)
        # process the words into lines
        result = self.process_lines(result)

        # (optional for debug) save the bounding boxes
        if self.debug and not is_base64:
            im = PIL.Image.open(base64_image)
            self.draw_boxes(im, result)
            im.save(self.output)

        # join the lines
        lines = []
        for r in result:
            lines.append(r[1])
        text = " ".join(lines)

        if self.debug:
            print(text)
            
        # return the text of the page
        return text
