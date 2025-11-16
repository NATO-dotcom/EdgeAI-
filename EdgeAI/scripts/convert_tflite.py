"""
Convert a saved Keras model to TensorFlow Lite with optional int8 quantization.

Usage:
    python scripts/convert_tflite.py --keras model/edge_model.h5 --tflite model/edge_model.tflite
"""
import argparse
import tensorflow as tf
import numpy as np

def representative_data_gen():
    # representative data for quantization calibration
    for i in range(100):
        yield [np.random.rand(1,32,32,3).astype('float32')]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keras', required=True)
    parser.add_argument('--tflite', required=True)
    args = parser.parse_args()

    model = tf.keras.models.load_model(args.keras)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_data_gen
    try:
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
    except Exception:
        pass
    tflite_model = converter.convert()
    with open(args.tflite, 'wb') as f:
        f.write(tflite_model)
    print('Saved TFLite model to', args.tflite)

if __name__ == '__main__':
    main()
