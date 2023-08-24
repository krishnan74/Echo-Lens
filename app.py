import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load metadata
metadata_path = '../python/test_image_metadata.csv'  # Update with your CSV file path
metadata = pd.read_csv(metadata_path)

# Load pre-trained MobileNetV2 model without classification layers
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)

# Load and preprocess an uploaded image
def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Get feature vector for an image
def get_feature_vector(image_path):
    img_array = preprocess_image(image_path)
    features = model.predict(img_array)
    return features.flatten()

# Your route definitions go here...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')

@app.route('/identify')
def identify():
    return render_template('identify.html')

@app.route('/identify', methods=['GET', 'POST'])
def identify():
    try:
        if request.method == 'POST':
            # Path to uploaded image
            uploaded_image_path = 'uploads/uploaded_image.jpg'  # Update with your uploaded image path
            uploaded_image_features = get_feature_vector(uploaded_image_path)

            # Calculate feature vectors for dataset images and add to metadata
            image_directory = 'testimages'  # Update with your image directory path
            metadata['feature_vector'] = metadata['image_filename'].apply(
                lambda filename: get_feature_vector(os.path.join(image_directory, filename))
            )

            # Calculate cosine similarity between uploaded image and dataset images
            cosine_similarities = cosine_similarity([uploaded_image_features], metadata['feature_vector'].tolist())
            most_similar_index = np.argmax(cosine_similarities)

            # Retrieve all details for the most similar image
            most_similar_image_details = metadata.loc[most_similar_index]
            print("Generated Details:")
            print(most_similar_image_details)

            return jsonify({'result': 'Identification successful'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5500)
