import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Step 1: Generate synthetic images
def generate_synthetic_dataset(base_dir="train_data", img_size=(32, 32), fonts=None, count=10):
    letters = ['H', 'S', 'U', 'A', 'B', 'Z']  # H/S/U are targets, others are distractors
    os.makedirs(base_dir, exist_ok=True)

    if fonts is None:
        fonts = ["/Library/Fonts/Arial.ttf", "/Library/Fonts/Times New Roman.ttf"]

    for letter in letters:
        letter_dir = os.path.join(base_dir, letter)
        os.makedirs(letter_dir, exist_ok=True)

        for i in range(count):
            img = Image.new("L", img_size, 255)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(np.random.choice(fonts), 24)

            # Updated line:
            bbox = font.getbbox(letter)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            draw.text(((img_size[0] - w) / 2, (img_size[1] - h) / 2), letter, font=font, fill=0)
            img.save(os.path.join(letter_dir, f"{letter}_{i}.png"))

# Step 2: Load data and preprocess
def load_dataset(data_dir="train_data"):
    X, y = [], []
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        for fname in os.listdir(label_dir):
            img_path = os.path.join(label_dir, fname)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
            resized = cv2.resize(thresh, (32, 32))
            X.append(resized.flatten())
            y.append(label)
    return np.array(X), np.array(y)

# Step 3: Train a simple classifier
def train_knn(X, y):
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)
    return model

# Step 4: Test on an image with synthetic letters
def detect_letters_in_image(img, model):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:
            roi = binary[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (32, 32)).flatten()
            pred = model.predict([roi_resized])[0]
            if pred in ['H', 'S', 'U']:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, pred, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    return img

# Generate dataset
generate_synthetic_dataset()

# Load and train
X, y = load_dataset()
model = train_knn(X, y)

# Save the model and example usage
print("Model trained. You can now use `detect_letters_in_image(image, model)` on real or synthetic images.")
