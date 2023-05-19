import torch
import torchvision
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms

# Load the pre-trained model with the most up-to-date weights
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Load the image using PIL
image = Image.open('image02.png')

# Define the image transformations
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert PIL image to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
])

# Apply the transformations to the image
input_tensor = transform(image)

# Add a batch dimension to the input tensor
input_tensor = input_tensor.unsqueeze(0)

# Pass the input through the model
with torch.no_grad():  # Disable gradient calculation
    output = model(input_tensor)

# Extract the predicted bounding boxes, labels, and masks
boxes = output[0]['boxes']  # Predicted bounding boxes
masks = output[0]['masks']  # Predicted masks


# Rest of the code for visualization
fig, ax = plt.subplots(1)
ax.imshow(input_tensor[0].permute(1, 2, 0).numpy())

for i in range(len(boxes)):
    box = boxes[i].numpy()
    mask = masks[i, 0].numpy()

    # Draw bounding box
    ax.add_patch(plt.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=False, color='red'))
    
    # Apply mask
    masked_image = input_tensor[0].clone()
    mask = mask > 0.5
    for c in range(3):
        masked_image[c][mask] = 1.0

    # Show masked image
    ax.imshow(masked_image.permute(1, 2, 0).numpy(), alpha=0.7)

plt.axis('off')
plt.show()
