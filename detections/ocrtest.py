import cv2
from ocr_train_and_detect import detect_letters_in_image, model

img = cv2.imread("/Users/bzhou/Downloads/CompetitionProgramming/CRC-A-2025-1/detections/test_wall_letters.jpg")  # your test image
result = detect_letters_in_image(img, model)

cv2.imshow("Detected H/S/U", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
