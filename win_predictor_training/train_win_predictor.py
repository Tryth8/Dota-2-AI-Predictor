import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers

NUM_HEROES = 138
EMBEDDING_DIM = 10


data = pd.read_csv('data/training_dataset.csv', header=None)
data = data.fillna(-1)

X = data.iloc[:, :10]
y = data.iloc[:, 10]

X = X.apply(lambda col: pd.to_numeric(col, downcast='integer').fillna(-1).astype(int))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

model = tf.keras.Sequential([
    layers.Embedding(input_dim=NUM_HEROES + 1, output_dim=EMBEDDING_DIM, mask_zero=True),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=6, batch_size=128, validation_split=0.2)

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)
print('\nTest accuracy:', test_accuracy)

model.save('../../models/win_predictor_model.keras')
