"""
Train a small CNN on CIFAR-10 (or synthetic data) and save Keras model.

Usage:
    python scripts/train.py --epochs 10
"""
import argparse
import os
import numpy as np
import tensorflow as tf

IMG_SIZE = 32
NUM_CLASSES = 10
BATCH_SIZE = 64

def get_data():
    try:
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        return x_train, y_train, x_test, y_test
    except Exception as e:
        print('Could not load CIFAR-10, creating synthetic data:', e)
        x_train = np.random.rand(5000, IMG_SIZE, IMG_SIZE, 3).astype('float32')
        y_train = np.random.randint(0, NUM_CLASSES, size=(5000,1))
        x_test = np.random.rand(1000, IMG_SIZE, IMG_SIZE, 3).astype('float32')
        y_test = np.random.randint(0, NUM_CLASSES, size=(1000,1))
        return x_train, y_train, x_test, y_test

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, activation='relu', padding='same', input_shape=(IMG_SIZE,IMG_SIZE,3)),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    return model

def main(args):
    x_train, y_train, x_test, y_test = get_data()
    model = build_model()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, validation_split=0.1, epochs=args.epochs, batch_size=BATCH_SIZE)
    os.makedirs('model', exist_ok=True)
    model.save('model/edge_model.h5')
    print('Model saved to model/edge_model.h5')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=10)
    args = parser.parse_args()
    main(args)
