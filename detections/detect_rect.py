import cv2

MIN_AREA = 1000  # minimum contour area (in pixels) for a rectangle

def find_rectangles(mask):
    """
    Given a binary mask, return a list of (x, y, w, h) of all
    detected quadrilaterals above MIN_AREA.
    """
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    rects = []
    for cnt in contours:
        peri   = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        area   = cv2.contourArea(approx)

        if len(approx) == 4 and area > MIN_AREA:
            x, y, w, h = cv2.boundingRect(approx)
            rects.append((x, y, w, h))

    return rects
