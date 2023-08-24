import os
import pandas as pd

# Define the path to your main image directory
main_image_directory = 'images'  # Change this to your main image directory path

# Create a list to store image filenames and labels
image_data = []

# Recursively iterate through the main image directory and its subdirectories
for root, dirs, files in os.walk(main_image_directory):
    for filename in files:
        if filename.endswith(".jpg"):  # Change the file extension as needed
            image_path = os.path.join(root, filename)
            label = os.path.basename(root)  # Use the subdirectory name as the label
            image_data.append({'image_filename': filename, 'label': label})

# Create a DataFrame from the image data list
image_df = pd.DataFrame(image_data)

# Save the DataFrame to a CSV file
csv_filename = 'test_image_metadata.csv'  # Change this to your desired CSV filename
image_df.to_csv(csv_filename, index=False)

print("Image dataset and metadata CSV created successfully!")
