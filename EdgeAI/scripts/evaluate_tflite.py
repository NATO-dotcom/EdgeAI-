"""
Evaluate a TFLite model on a small test set.

Usage:
    python scripts/evaluate_tflite.py --tflite model/edge_model.tflite
"""
import argparse
import numpy as np
import tensorflow as tf

def load_test_data():
    try:
        (_, _), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        x_test = x_test.astype('float32') / 255.0
        return x_test, y_test
    except Exception:
        x_test = np.random.rand(1000,32,32,3).astype('float32')
        y_test = np.random.randint(0,10,size=(1000,1))
        return x_test, y_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tflite', required=True)
    args = parser.parse_args()
    x_test, y_test = load_test_data()

    interpreter = tf.lite.Interpreter(model_path=args.tflite)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    correct = 0
    N = 200
    for i in range(N):
        img = x_test[i:i+1]
        if input_details[0]['dtype'] == np.uint8:
            img_in = (img*255).astype(np.uint8)
        else:
            img_in = img.astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], img_in)
        interpreter.invoke()
        out = interpreter.get_tensor(output_details[0]['index'])
        pred = np.argmax(out, axis=-1)
        if pred[0] == int(y_test[i][0]):
            correct += 1
    print('Accuracy on', N, 'samples:', correct/N)

if __name__ == '__main__':
    main()
