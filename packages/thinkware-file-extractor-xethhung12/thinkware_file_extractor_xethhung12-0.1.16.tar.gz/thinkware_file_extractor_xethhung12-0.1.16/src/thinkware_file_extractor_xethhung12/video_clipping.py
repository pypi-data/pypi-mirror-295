import os
import re
import sys

import cv2
from pytesseract import pytesseract
from dataclasses import dataclass

@dataclass
class VideoClipping:
    date: str
    hour: str
    corresponding_timestamp: str

def extract_time_list(p):
    l = []
    vidcap = cv2.VideoCapture(p)
    # width=thinkware_file_extractor_xethhung12.utils_tools.mp4view(p).get_width()
    # height=thinkware_file_extractor_xethhung12.utils_tools.mp4view(p).get_height()
    # print(width)
    # print(height)
    # out_path = os.path.abspath("../../data-image-clipping")
    # os.popen(f"mkdir -p {out_path}").read()
    # os.popen(f"rm -f {out_path}/*").read()
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    fc = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    # os.popen(f"rm -f {out_path}/*")

    # A text file is created and flushed
    # file = open(f"{out_path}/recognized.txt", "w+")
    # file.write("")
    # file.close()
    found=None
    i = 0
    index=0
    pc = None
    while True:
        index+=1
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, image = vidcap.read()
        i += (fps * 30)

        if success:
            time_image = image[1400:1430, 430:600]
            # cv2.imwrite(f"../../data-image-clipping/video-{index:06d}-crop.jpg", time_image)
            gray_time_image = cv2.cvtColor(time_image, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite(f"../../data-image-clipping/video-{index:06d}-crop-gray.jpg", gray_time_image)
            ret, thresh1 = cv2.threshold(gray_time_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
            dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

            # Finding contours
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_NONE)

            # Creating a copy of image
            im2 = gray_time_image.copy()


            # Looping through the identified contours
            # Then rectangular part is cropped and passed on
            # to pytesseract for extracting text from it
            # Extracted text is then written into the text file
            for cnt in contours:

                x, y, w, h = cv2.boundingRect(cnt)

                # Drawing a rectangle on copied image
                rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Cropping the text block for giving input to OCR
                cropped = im2[y:y + h, x:x + w]

                # Open the file in append mode
                # file = open(f"{out_path}/recognized.txt", "a")

                # Apply OCR on the cropped image
                text = pytesseract.image_to_string(cropped)
                text = text if not text.endswith('\x0c') else text[0:-1]
                text = text if not text.endswith('\n') else text[0:-1]

                res = re.match("\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}", text)

                if res is not None:
                    if found is None or res[0][0:13] != found[0:13]:
                        found = res[0]
                    else:
                        continue
                else:
                    continue

                sec = int(vidcap.get(cv2.CAP_PROP_POS_MSEC)/1000)
                h = int(sec/3600)
                m = int(sec/60) % 60
                s = sec % 60

                # Appending the text into file
                l.append(VideoClipping(
                    text[0:10].replace(".","-"),
                    text[11:13],
                    f"{h:02d}:{m:02d}:{s:02d}"
                ))
                # t = f"{h:02d}:{m:02d}:{s:02d} -> {text}"
                # file.write(t)
                # file.write("\n")

                # Close the file
                # file.close()

        else:
            break

        if pc is None or (not int(i/fc*100) == pc):
            pc = int(i/fc*100)
            sys.stderr.write(f"{i}/{fc} - {pc} %\n")
            # print(f"{i}/{fc} - {pc} %")

    return l
