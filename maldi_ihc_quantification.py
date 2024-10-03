from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the three images
image_paths = ["CD68.png", "ki67.png", "CD8a.png"]
images = [Image.open(path) for path in image_paths]

# Define the colors for each image
image_colors = ['cyan', 'purple', 'yellow']

# Set the threshold value (adjust as needed)
threshold = 0  # Example threshold value

# Initialize lists to store the percentages for each image
percentages_black = []
percentages_non_black = []

for img in images:
    # Convert the image to grayscale
    img_gray = img.convert("L")

    # Convert the grayscale image to a numpy array
    img_array = np.array(img_gray)

    # Apply the threshold to distinguish black from dark colors
    img_thresholded = np.where(img_array <= threshold, 0, img_array)

    # Calculate the total number of pixels in the image
    total_pixels = img_thresholded.size

    # Calculate the percentage of black pixels (0)
    percentage_black = (np.sum(img_thresholded == 0) / total_pixels) * 100
    percentages_black.append(percentage_black)

    # Calculate the percentage of non-black pixels
    percentage_non_black = 100 - percentage_black
    percentages_non_black.append(percentage_non_black)

# Normalize the percentages for each image
normalized_percentages = []

for i in range(len(images)):
    total_percentage = percentages_black[i] + percentages_non_black[i]
    normalized_black = (percentages_black[i] / total_percentage) * 100
    normalized_non_black = 100 - normalized_black
    normalized_percentages.append({"Black": normalized_black, "Non-Black": normalized_non_black})

# Create a bar chart to visualize the normalized percentages for each image with specified colors
categories = ['CD68', 'ki67', 'CD8a']
values_black = [p["Black"] for p in normalized_percentages]
values_non_black = [p["Non-Black"] for p in normalized_percentages]

bar_width = 0.5
index = np.arange(len(categories))

# Specify colors for each bar
colors = [image_colors[i] for i in range(len(images))]

# Invert the order of plotting (Black on top of Non-Black)
plt.bar(index, values_non_black, bar_width, label='Non-Black', color=colors)
plt.bar(index, values_black, bar_width, label='Black', color='black', bottom=values_non_black)

plt.xlabel('Images')
plt.ylabel('Percentage')
plt.title('Black and Non-Black Percentages')
plt.xticks(index, categories)

plt.legend()
plt.show()

# Print the normalized percentages for each image
for i, category in enumerate(categories):
    print(f"{category}:")
    print(f"Black: {values_black[i]:.2f}%")
    print(f"Non-Black: {values_non_black[i]:.2f}%")
    print()
