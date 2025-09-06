import sys
from PIL import Image
import os
import shutil


def folder_size(folder):
    total = 0
    for fileName in os.listdir(folder):
        path = os.path.join(folder, fileName)
        if os.path.isfile(path):
            total += os.path.getsize(path)
    return total


while True:
    # User input
    input_folder = input("Enter the path of the texture folder: ").strip()
    if input_folder.lower() == "exit":
        print("exiting program ...".title())
        sys.exit()

    max_size_input = input("Enter the maximum size (px) (leave empty for default 512): ").strip()

    # Settings
    MAX_SIZE = int(max_size_input) if max_size_input else 512

    # Base output folder
    base_output_folder = os.path.join(os.path.dirname(input_folder), "Output Textures")
    output_folder_original = os.path.join(base_output_folder, "Resized Textures")
    output_folder_webp = os.path.join(base_output_folder, "WebP Textures")

    os.makedirs(output_folder_original, exist_ok=True)
    os.makedirs(output_folder_webp, exist_ok=True)

    print(f"\nInput folder: {input_folder}")
    print(f"Maximum resolution: {MAX_SIZE} px\n")

    # Process images
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            aspect_ratio = img.width / img.height

            # Resize if larger than MAX_SIZE
            if img.width > MAX_SIZE or img.height > MAX_SIZE:
                if aspect_ratio > 1:  # Landscape
                    new_width = MAX_SIZE
                    new_height = int(MAX_SIZE / aspect_ratio)
                else:  # Portrait or square
                    new_height = MAX_SIZE
                    new_width = int(MAX_SIZE * aspect_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                # If smaller, just copy the original image
                shutil.copy(img_path, os.path.join(output_folder_original, filename))
                name_wo_ext = os.path.splitext(filename)[0]
                webp_path = os.path.join(output_folder_webp, f"{name_wo_ext}.webp")
                img.save(webp_path, "WEBP", quality=90)
                continue  # Skip further processing

            # Save resized image in original format
            img.save(os.path.join(output_folder_original, filename))

            # Save WebP version
            name_wo_ext = os.path.splitext(filename)[0]
            webp_path = os.path.join(output_folder_webp, f"{name_wo_ext}.webp")
            img.save(webp_path, "WEBP", quality=90)

    # Calculate folder sizes
    size_original = folder_size(output_folder_original) / (1024 * 1024)
    size_webp = folder_size(output_folder_webp) / (1024 * 1024)

    print(f"\nProcessing completed!")
    print(f"Size of resized folder: {size_original:.2f} MB")
    print(f"Size of WebP folder: {size_webp:.2f} MB")
    print(f"All output saved inside: {base_output_folder}")
    print("\n" * 2)
