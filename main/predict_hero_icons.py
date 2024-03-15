from pathlib import Path

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from hero_data.hero_list import hero_names_alphabetically


def prepare_image(img_path, target_size=(224, 224)):
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    return img_array


def predict_teams(output_dir):
    output_dir = Path(output_dir)
    model = load_model('../models/dota_heroes_classifier.keras')
    predicted_teams = []

    for i in range(1, 11):
        img_path = output_dir / f"hero_{i}.jpg"
        prepared_img = prepare_image(img_path)
        predictions = model.predict(prepared_img)
        predicted_class_index = np.argmax(predictions, axis=1)
        predicted_class_name = hero_names_alphabetically[predicted_class_index[0]]

        predicted_teams.append(predicted_class_name)

    return predicted_teams
