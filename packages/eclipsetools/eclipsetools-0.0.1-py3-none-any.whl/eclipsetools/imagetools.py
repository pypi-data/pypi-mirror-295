import re
import cv2
import os
from PIL import Image
import numpy as np


class Operation:
    class Resize:
        def __init__(self, width: int = 16, height: int = 16, keep_aspect_ratio: bool = True, save_path: str = None) -> None:
            self.width = width
            self.height = height
            self.keep_aspect_ratio = keep_aspect_ratio
            self.save_path = save_path

    class Crop:
        def __init__(self, width: int, height: int, save_path: str = None) -> None:
            self.width = width
            self.height = height
            self.save_path = save_path

    class RotateFlip:
        def __init__(self, rotation_degrees: int = 0, flip_axis: str = None, save_path: str = None) -> None:
            self.rotation_degrees = rotation_degrees
            self.flip_axis = flip_axis
            self.save_path = save_path

    class HSB:
        def __init__(self, brightness=1.0, saturation=1.0, hue=0, save_path: str = None) -> None:
            self.brightness = brightness
            self.saturation = saturation
            self.hue = hue
            self.save_path = save_path

    class ContrastGamma:
        def __init__(self, contrast=1.0, gamma=1.0, save_path: str = None) -> None:
            self.contrast = contrast
            self.gamma = gamma
            self.save_path = save_path

    class BlurSharpen:
        def __init__(self, blur_strength=0, sharpen_strength=0, save_path: str = None) -> None:
            self.blur_strength = blur_strength
            self.sharpen_strength = sharpen_strength
            self.save_path = save_path

    class ZoomPan:
        def __init__(self, zoom_factor: float, pan_factor_x: int, pan_factor_y: int, save_path: str = None) -> None:
            self.zoom_factor = zoom_factor
            self.pan_factor_x = pan_factor_x
            self.pan_factor_y = pan_factor_y
            self.save_path = save_path


def perform_operations(image_paths: list[str], operations: list, chain: bool = True):
    operation_map = {
        Operation.Resize: resize_image,
        Operation.Crop: crop_image,
        Operation.RotateFlip: rotate_flip_image,
        Operation.HSB: adjust_hsb,
        Operation.ContrastGamma: adjust_contrast_gamma,
        Operation.BlurSharpen: blur_sharpen_image,
        Operation.ZoomPan: zoom_pan_image,
    }

    prev_paths = list(image_paths)
    save_paths = []

    for op in operations:
        operation_func = operation_map.get(type(op), None)
        save_path_op = []
        save_paths.append(save_path_op)

        if operation_func is None:
            print(
                f"Operation type: [{type(op).__name__}] is not a valid operation, skipping.")
            continue

        args = op.__dict__
        for image_path in prev_paths:
            if not args:
                path = operation_func(image_path)
            else:
                path = operation_func(image_path, **args)
            save_path_op.append(path)

        if chain:
            prev_paths = list(save_path_op)

    return save_paths


def delete_all_but_last_operation_files(files: list[list[str]]):
    """
    Deletes all files from the operations except for the last set of files in the list.

    :param files: A list of lists containing file paths created during the operations.
    """
    for i in range(len(files) - 1):
        for file in files[i]:
            try:
                os.remove(file)
                print(f"Successfully removed file: [{file}]")
            except Exception as e:
                print(f"Could not remove file: [{file}]. Error: {e}")


def get_images_in_folder(folder_path: str, image_extensions: dict[str] = {'.png', '.jpeg', '.jpg'}):
    """
    Retrieves all .png, .jpeg, and .jpg image files from the specified folder.

    :param folder_path: Path to the folder where the search for image files will be performed.
    :return: A list of absolute paths to the image files found in the folder, or an empty list if no images are found.
    """
    # List to store the paths of the image files found
    image_files = []

    # Iterate through the files in the specified folder
    try:
        for file_name in os.listdir(folder_path):
            # Get the full path of the file
            file_path = os.path.join(folder_path, file_name)

            # Check if it's a file and if its extension matches the desired image formats
            if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in image_extensions:
                image_files.append(file_path)

    except FileNotFoundError:
        print("The specified folder does not exist.")
    except PermissionError:
        print("Permission denied to access the folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return image_files


def get_save_path(video_path: str, save_path: str = None) -> str:
    base, ext = os.path.splitext(video_path)
    video_folder = os.path.dirname(base)
    video_name = os.path.basename(base)
    if save_path is None:
        save_path = f"{base}_saved{ext}"
        return save_path

    pattern = r'\[[^:\]]*:[^:\]]*\]'

    # Find all matches and create a dictionary mapping
    matches = re.findall(pattern, save_path)

    mapping = {}
    for match in matches:
        # Remove the brackets and split by colon to get the key and value
        key_value = match.strip('[]').split(':')
        if len(key_value) == 2:  # Ensure it has exactly two parts
            first, second = key_value
            mapping[first] = second

    # Remove the [any_substring:any_substring] patterns from the string
    video_name = re.sub(pattern, '', video_name)

    # Replace all instances of the first substring with the second
    for key, value in mapping.items():
        video_name = video_name.replace(key, value)

    save_path = re.sub(pattern, "", save_path)

    save_path = save_path.replace("*", video_name)

    save_path = os.path.join(video_folder, save_path) + ext

    return save_path


def crop_image(image_path: str, width: int, height: int, save_path: str = None):
    """
    Crops an image to the specified width and height from the center of the image.

    :param image_path: Path to the input image file.
    :param width: The desired width of the cropped image.
    :param height: The desired height of the cropped image.
    :param save_path: Optional path to save the cropped image. If None, saves in the same folder as the image with a modified name.
    :return: The path of the saved cropped image.
    """
    if save_path is None:
        save_path = "*_crop"
    save_path = get_save_path(image_path, save_path)

    # Open the image
    image = Image.open(image_path)
    original_width, original_height = image.size

    # Calculate the cropping coordinates
    x_center = original_width // 2
    y_center = original_height // 2
    x_start = max(0, x_center - width // 2)
    y_start = max(0, y_center - height // 2)

    # Crop the image
    cropped_image = image.crop(
        (x_start, y_start, x_start + width, y_start + height))
    cropped_image.save(save_path)

    print(f"Cropped image saved as {save_path}")
    return save_path


def resize_image(image_path: str, width: int, height: int, keep_aspect_ratio: bool = True, save_path: str = None):
    """
    Resizes an image to the specified width and height. By default, the aspect ratio is maintained,
    and padding is added to fit the target size. Optionally, you can disable aspect ratio maintenance
    to force the image to fit the exact dimensions.

    :param image_path: Path to the input image file.
    :param width: The desired width of the resized image.
    :param height: The desired height of the resized image.
    :param keep_aspect_ratio: Whether to maintain the aspect ratio and add padding (default is True).
    :param save_path: Optional path to save the resized image. If None, saves in the same folder as the image.
    :return: The path of the saved resized image.
    """
    if save_path is None:
        save_path = "*_resize"
    save_path = get_save_path(image_path, save_path)

    # Open the image
    image = Image.open(image_path)
    original_width, original_height = image.size

    if keep_aspect_ratio:
        # Calculate aspect ratio of the original image
        aspect_ratio = original_width / original_height

        # Calculate new dimensions while maintaining aspect ratio
        if (width / height) > aspect_ratio:
            new_height = height
            new_width = int(aspect_ratio * height)
        else:
            new_width = width
            new_height = int(width / aspect_ratio)

        # Resize the image
        resized_image = image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new image with the desired dimensions and paste the resized image onto it
        final_image = Image.new("RGB", (width, height))
        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2
        final_image.paste(resized_image, (x_offset, y_offset))
    else:
        # Resize without maintaining aspect ratio
        final_image = image.resize((width, height), Image.Resampling.LANCZOS)

    final_image.save(save_path)
    print(f"Resized image saved as {save_path}")
    return save_path


def rotate_flip_image(image_path: str, rotation_degrees: int = 0, flip_axis: str = None, save_path: str = None):
    """
    Rotates and/or flips an image according to specified codes.

    :param image_path: Path to the input image file.
    :param rotation_degrees: The rotation degrees (e.g., 90, 180, 270) to apply to the image.
    :param flip_axis: Optional flip degrees ('H' for horizontal, 'V' for vertical) to apply. If None, no flip is applied.
    :param save_path: Optional path to save the rotated/flipped image. If None, saves in the same folder as the image.
    :return: The path of the saved rotated/flipped image.
    """
    if save_path is None:
        save_path = "*_rotate_flip"
    save_path = get_save_path(image_path, save_path)

    # Open the image
    image = Image.open(image_path)

    # Rotate the image
    if rotation_degrees == 90:
        image = image.rotate(-90, expand=True)
    elif rotation_degrees == 180:
        image = image.rotate(180, expand=True)
    elif rotation_degrees == 270:
        image = image.rotate(-270, expand=True)

    # Flip the image if flip_code is specified
    flip_axis = flip_axis.lower()
    if flip_axis == 'h':  # Horizontal flip
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_axis == 'v':  # Vertical flip
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Save the processed image
    image.save(save_path)
    print(f"Rotated/Flipped image saved as {save_path}")
    return save_path


def adjust_hsb(image_path: str, brightness=1.0, saturation=1.0, hue=0, save_path: str = None):
    """
    Adjusts the brightness, saturation, and hue of an image using the HSV color space.

    :param image_path: Path to the input image file.
    :param brightness: Factor to adjust brightness (1.0 = no change).
    :param saturation: Factor to adjust saturation (1.0 = no change).
    :param hue: Offset to adjust hue in degrees (-180 to 180).
    :param save_path: Optional path to save the adjusted image. If None, saves in the same folder as the image.
    :return: The path of the saved adjusted image.
    """
    if save_path is None:
        save_path = "*_hsb"
    save_path = get_save_path(image_path, save_path)

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Cannot open the image file.")
        return None

    # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

    # Adjust brightness, saturation, and hue
    hsv_image[..., 2] = np.clip(
        hsv_image[..., 2] * brightness, 0, 255)  # Brightness
    hsv_image[..., 1] = np.clip(
        hsv_image[..., 1] * saturation, 0, 255)  # Saturation
    hsv_image[..., 0] = (hsv_image[..., 0] + hue) % 180  # Hue adjustment

    # Convert back to BGR color space
    adjusted_image = cv2.cvtColor(
        hsv_image.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # Save the adjusted image
    cv2.imwrite(save_path, adjusted_image)
    print(f"HSB-adjusted image saved as {save_path}")
    return save_path


def adjust_contrast_gamma(image_path: str, contrast=1.0, gamma=1.0, save_path: str = None):
    """
    Adjusts the contrast and gamma of an image.

    :param image_path: Path to the input image file.
    :param contrast: Factor to adjust contrast (1.0 = no change).
    :param gamma: Factor to adjust gamma (1.0 = no change).
    :param save_path: Optional path to save the adjusted image. If None, saves in the same folder as the image.
    :return: The path of the saved adjusted image.
    """
    if save_path is None:
        save_path = "*_contrast_gamma"
    save_path = get_save_path(image_path, save_path)

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Cannot open the image file.")
        return None

    # Adjust contrast
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)

    # Adjust gamma
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) *
                     255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted_image = cv2.LUT(image, table)

    # Save the adjusted image
    cv2.imwrite(save_path, adjusted_image)
    print(f"Contrast and gamma-adjusted image saved as {save_path}")
    return save_path


def blur_sharpen_image(image_path: str, blur_strength=0, sharpen_strength=0, save_path: str = None):
    """
    Applies blur and/or sharpen effects to an image.

    :param image_path: Path to the input image file.
    :param blur_strength: Strength of the Gaussian blur effect. A value of 0 means no blur.
    :param sharpen_strength: Strength of the sharpening effect. A value of 0 means no sharpening.
    :param save_path: Optional path to save the blurred/sharpened image. If None, saves in the same folder as the image.
    :return: The path of the saved blurred/sharpened image.
    """
    if save_path is None:
        save_path = "*_blur_sharpen"
    save_path = get_save_path(image_path, save_path)

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Cannot open the image file.")
        return None

    # Apply blur if specified
    if blur_strength > 0:
        image = cv2.GaussianBlur(
            image, (blur_strength * 2 + 1, blur_strength * 2 + 1), 0)

    # Apply sharpen if specified
    if sharpen_strength > 0:
        kernel = np.array([[0, -sharpen_strength, 0],
                           [-sharpen_strength, 1 + 4 *
                               sharpen_strength, -sharpen_strength],
                           [0, -sharpen_strength, 0]])
        image = cv2.filter2D(image, -1, kernel)

    # Save the processed image
    cv2.imwrite(save_path, image)
    print(f"Blurred/Sharpened image saved as {save_path}")
    return save_path


def zoom_pan_image(image_path: str, zoom_factor: float, pan_factor_x: int, pan_factor_y: int, save_path: str = None):
    """
    Applies a zoom and pan effect to an image.

    :param image_path: Path to the input image file.
    :param zoom_factor: The factor by which to zoom the image.
    :param pan_factor_x: The number of pixels to pan horizontally.
    :param pan_factor_y: The number of pixels to pan vertically.
    :param save_path: Optional path to save the zoomed/panned image. If None, saves in the same folder as the image.
    :return: The path of the saved zoomed/panned image.
    """
    if save_path is None:
        save_path = "*_zoom_pan"
    save_path = get_save_path(image_path, save_path)

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Cannot open the image file.")
        return None

    original_height, original_width = image.shape[:2]

    # Calculate new dimensions after zoom
    new_width = int(original_width / zoom_factor)
    new_height = int(original_height / zoom_factor)

    # Crop the image to the new zoomed dimensions
    x_start = max(0, pan_factor_x)
    y_start = max(0, pan_factor_y)

    # Ensure the crop area does not go outside the image bounds
    x_end = min(x_start + new_width, original_width)
    y_end = min(y_start + new_height, original_height)

    cropped_image = image[y_start:y_end, x_start:x_end]

    # Resize the cropped image back to the original dimensions
    zoomed_image = cv2.resize(cropped_image, (original_width, original_height))

    # Save the zoomed and panned image
    cv2.imwrite(save_path, zoomed_image)
    print(f"Zoomed/Panned image saved as {save_path}")
    return save_path


def concatenate_images(image_paths: list, save_path: str = None):
    """
    Concatenates multiple image files into a single video.

    :param image_paths: List of paths to the image files to concatenate.
    :param save_path: Optional path to save the concatenated video. If None, saves in the same folder as the first image.
    :return: The path of the saved concatenated video.
    """
    if not image_paths:
        print("Error: No images provided for concatenation.")
        return None

    if save_path is None:
        save_path = "*_concatenated"
    save_path = get_save_path(image_paths[0], save_path)
    base, ext = os.path.splitext(save_path)
    save_path = base + ".mp4"

    # Read the first image to get the dimensions
    first_image = cv2.imread(image_paths[0])
    if first_image is None:
        print("Error: Cannot open the first image file.")
        return None

    height, width, _ = first_image.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1  # You can adjust the frame rate as needed

    # Create VideoWriter object
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # Add each image to the video
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Cannot open image file: {
                  image_path}. Skipping this image.")
            continue

        # Resize image to match the first image dimensions if necessary
        resized_image = cv2.resize(image, (width, height))
        out.write(resized_image)

    out.release()
    print(f"Concatenated video saved as {save_path}")
    return save_path


def load_image_as_array(image_path: str) -> np.ndarray:
    """
    Loads an image from the specified path and converts it to a NumPy array.

    :param image_path: Path to the input image file.
    :return: NumPy array representing the image.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Cannot open the image file.")
        return None

    # Convert the image to a NumPy array
    image_array = np.array(image)

    return image_array


def save_array_as_image(image_array: np.ndarray, save_path: str = None):
    """
    Saves a NumPy array as an image file using the specified save path methodology.

    :param image_array: NumPy array representing the image.
    :param save_path: Optional path to save the image. If None, saves with default naming.
    :return: The path of the saved image.
    """
    # Check if the array is valid for saving as an image
    if image_array is None or image_array.size == 0:
        print("Error: Invalid image array.")
        return None

    # Save the array as an image
    success = cv2.imwrite(save_path, image_array)
    if not success:
        print("Error: Unable to save the image file.")
        return None

    print(f"Image saved as {save_path}")
    return save_path
