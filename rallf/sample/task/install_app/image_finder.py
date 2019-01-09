import cv2


class ImageFinder:
    def __init__(self, pattern):
        self.pattern = cv2.imread(pattern, 0)

    def match(self, image):
        img = cv2.imread(image, 0)
        # Apply template Matching
        res = cv2.matchTemplate(img, self.pattern, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return {"matches": max_val, "coords": max_loc}
