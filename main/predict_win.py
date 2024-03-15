import pandas as pd
import tensorflow as tf


def predict_match_winner(hero_ids):
    model = tf.keras.models.load_model('../models/win_predictor_model.keras')

    features = pd.DataFrame([hero_ids], columns=[f'hero_{i + 1}' for i in range(10)])
    features = features.apply(lambda col: pd.to_numeric(col, downcast='integer').fillna(-1).astype(int))

    predicted_outcome = model.predict(features)
    winner = 'Radiant' if predicted_outcome[0][0] > 0.5 else 'Dire'

    return winner, predicted_outcome[0][0]
