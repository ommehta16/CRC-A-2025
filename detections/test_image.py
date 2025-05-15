import cv2
from detect_multicolor import detect_colored_rectangles

img = cv2.imread('/Users/bzhou/Downloads/CompetitionProgramming/CRC-A-2025-1/detections/multicolor.jpg')  # replace with your test image
if img is None:
    raise FileNotFoundError("Image not found or failed to load.")

dets = detect_colored_rectangles(img)
for d in dets:
    x, y, w, h = d['position']
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, d['color'], (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("Detections", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
