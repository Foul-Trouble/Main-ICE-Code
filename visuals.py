import platform
if platform.system() == "Linux":
    import cv2


def cameras():
    #   Dual Camera Feed
    top_view = cv2.VideoCapture(0)
    bottom_view = cv2.VideoCapture(1)
    while not end:
        cv2.imshow('Top_View', top_view)
        cv2.imshow('Bottom_View', bottom_view)
