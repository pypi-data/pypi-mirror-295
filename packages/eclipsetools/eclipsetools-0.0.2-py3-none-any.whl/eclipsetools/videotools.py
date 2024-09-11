import re
import cv2
import os
from PIL import Image
import numpy as np

log_functions: bool = True


def print_et(value):
    if log_functions:
        print(value)


class Operation:
    class Resize:
        def __init__(self, width: int = 16, height: int = 16, keep_aspect_ratio: bool = True, save_path: str = None) -> None:
            self.width = width
            self.height = height
            self.keep_aspect_ratio = keep_aspect_ratio
            self.save_path = save_path

    class Trim:
        def __init__(self, start_frame: int, end_frame: int, save_path: str = None) -> None:
            self.start_frame = start_frame
            self.end_frame = end_frame
            self.save_path = save_path

    class Crop:
        def __init__(self, width: int, height: int, save_path: str = None) -> None:
            self.width = width
            self.height = height
            self.save_path = save_path

    class Speed:
        def __init__(self, speed_factor: float, save_path: str = None) -> None:
            self.speed_factor = speed_factor
            self.save_path = save_path

    class RotateFlip:
        def __init__(self, rotation_degrees, flip_axis=None, save_path: str = None) -> None:
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

    class RemoveChatter:
        def __init__(self, buffer_size: int = 5, save_path: str = None) -> None:
            self.buffer_size = buffer_size
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

    class Reverse:
        def __init__(self, save_path: str = None) -> None:
            self.save_path = save_path


def perform_operations(video_paths: list[str], operations: list, chain: bool = True):
    operation_map = {
        Operation.Trim: trim_video,
        Operation.Crop: crop_video,
        Operation.Resize: resize_video,
        Operation.Speed: change_video_speed,
        Operation.RotateFlip: rotate_flip_video,
        Operation.HSB: adjust_hsb,
        Operation.ContrastGamma: adjust_contrast_gamma,
        Operation.RemoveChatter: remove_chatter,
        Operation.BlurSharpen: blur_sharpen_video,
        Operation.ZoomPan: zoom_pan_video,
        Operation.Reverse: reverse_video,
    }

    prev_paths = list(video_paths)

    save_paths = []
    for op in operations:
        operation_func = operation_map.get(type(op), None)
        save_path_op = []
        save_paths.append(save_path_op)
        if operation_func is None:
            print_et(
                f"Operation type: [{op["type"]}] is not a valid operation, skipping")

        args = op.__dict__
        for video_path in prev_paths:
            if not args:
                path = operation_func(video_path)
                save_path_op.append(path)
            else:
                path = operation_func(video_path, **args)
                save_path_op.append(path)

        if chain:
            prev_paths = list(save_path_op)

    return save_paths


def delete_all_but_last_operation_files(files: list[list[str]]):
    for i in range(len(files) - 1):
        for file in files[i]:
            try:
                os.remove(file)
                print_et(f"Successfully removed file: [{file}]")
            except:
                print_et(f"Could not remove file: [{file}]")


def get_videos_in_folder(folder_path: str, video_extensions: dict[str] = {'.mp4', '.mov'}):
    """
    Retrieves all .mp4 and .mov video files from the specified folder.

    :param folder_path: Path to the folder where the search for video files will be performed.
    :return: A list of absolute paths to the .mp4 and .mov video files found in the folder,
             or an empty list if no video files are found or if an error occurs.
    """

    # List to store the paths of the video files found
    video_files = []

    # Iterate through the files in the specified folder
    try:
        for file_name in os.listdir(folder_path):
            # Get the full path of the file
            file_path = os.path.join(folder_path, file_name)

            # Check if it's a file and if its extension matches the desired video formats
            if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in video_extensions:
                video_files.append(file_path)

    except FileNotFoundError:
        print_et("The specified folder does not exist.")
    except PermissionError:
        print_et("Permission denied to access the folder.")
    except Exception as e:
        print_et(f"An error occurred: {e}")

    return video_files


def get_total_frames(video_path: str):
    """
    Returns the total number of frames in the given video file.

    :param video_path: Path to the video file.
    :return: Total number of frames in the video, or -1 if the video cannot be opened.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return -1

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames


def get_frame_rate(video_path: str) -> float:
    """
    Returns the frame rate (FPS) of the given video file.

    :param video_path: Path to the video file.
    :return: Frame rate (FPS) of the video, or -1 if the video cannot be opened.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return -1

    # Get the frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Release the video capture object
    cap.release()

    return fps


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


def save_frame(video_path: str, frame_index: int, save_path: str = None):
    """
    Saves a specified frame as a PNG image from the video file. If the frame index is out of range,
    saves a black image of the same width and height as the video.

    :param video_path: Path to the video file.
    :param frame_index: Index of the frame to save (0-based).
    :param save_path: Optional path to save the image. If None, saves in the same folder as the video.
    :return: The path of the saved image.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = f"*_frame_{frame_index}"
    save_path = get_save_path(video_path, save_path)
    base, ext = os.path.splitext(save_path)
    save_path = base + ".png"

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Check if the frame index is within valid range
    if frame_index < 0 or frame_index >= total_frames:
        print_et(f"Frame index {
            frame_index} is out of range. Saving a black image instead.")
        # Create a black image of the same size
        black_image = Image.fromarray(
            np.zeros((height, width, 3), dtype=np.uint8))
        black_image.save(save_path, "PNG")
        cap.release()
        return save_path

    # Set the position to the specified frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    # Read the frame
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print_et(f"Error: Cannot read the frame at index {
            frame_index}. Saving a black image instead.")
        cap.release()
        return None

    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    image = Image.fromarray(frame_rgb)

    # Save as PNG
    image.save(save_path, "PNG")

    # Release the video capture object
    cap.release()
    print_et(f"Frame {frame_index} saved as {save_path}")
    return save_path


def trim_video(video_path: str, start_frame: int, end_frame: int, save_path: str = None):
    """
    Creates a trimmed version of the video from a specified start to end frame index.
    If the specified frame range is outside the available frames in the video, black frames
    will be added to fill the missing frames.

    :param video_path: Path to the input video file.
    :param start_frame: The starting frame index of the trim range (0-based).
    :param end_frame: The ending frame index of the trim range (0-based, inclusive).
    :param save_path: Optional path to save the trimmed video. If None, saves in the same folder as the video.
    :return: The path of the saved trimmed video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_trim"
    save_path = get_save_path(video_path, save_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Validate start and end frames
    if start_frame < 0:
        start_frame = 0
    if end_frame >= total_frames:
        end_frame = total_frames - 1

    # Create VideoWriter object to save the new video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # Add frames from start to end, including black frames if outside the range
    for i in range(start_frame, end_frame + 1):
        if 0 <= i < total_frames:
            # Set the position to the specified frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                # If reading the frame fails, write a black frame
                black_frame = np.zeros((height, width, 3), dtype=np.uint8)
                out.write(black_frame)
        else:
            # Add black frames for out-of-range indices
            black_frame = np.zeros((height, width, 3), dtype=np.uint8)
            out.write(black_frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    print_et(f"Trimmed video saved as {save_path}")
    return save_path


def crop_video(video_path: str, width: int, height: int, save_path: str = None):
    """
    Crops a video to the specified width and height from the center of each frame.
    If the crop size is larger than the original frame, black pixels are added to fill the extra space.

    :param video_path: Path to the input video file.
    :param width: The desired width of the cropped video.
    :param height: The desired height of the cropped video.
    :param save_path: Optional path to save the cropped video. If None, saves in the same folder as the video with a modified name.
    :return: The path of the saved cropped video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_crop"
    save_path = get_save_path(video_path, save_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    # Get video properties
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create VideoWriter object to save the cropped video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # Calculate the cropping coordinates
    x_center = original_width // 2
    y_center = original_height // 2
    x_start = max(0, x_center - width // 2)
    y_start = max(0, y_center - height // 2)

    for _ in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Create a black background for the output frame
        cropped_frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate where to place the cropped part of the original frame
        x_offset = max(0, (width - original_width) // 2)
        y_offset = max(0, (height - original_height) // 2)

        # Define the region of the original frame to copy into the cropped frame
        frame_crop = frame[y_start:y_start + min(height, original_height),
                           x_start:x_start + min(width, original_width)]

        # Place the cropped section of the frame into the center of the black background
        cropped_frame[y_offset:y_offset + frame_crop.shape[0],
                      x_offset:x_offset + frame_crop.shape[1]] = frame_crop

        # Write the cropped frame to the output video
        out.write(cropped_frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    print_et(f"Cropped video saved as {save_path}")
    return save_path


def resize_video(video_path: str, width: int, height: int, keep_aspect_ratio: bool = True, save_path: str = None):
    """
    Resizes a video to the specified width and height. By default, the aspect ratio is maintained,
    and padding is added to fit the target size. Optionally, you can disable aspect ratio maintenance
    to force the video to fit the exact dimensions.

    :param video_path: Path to the input video file.
    :param width: The desired width of the resized video.
    :param height: The desired height of the resized video.
    :param keep_aspect_ratio: Whether to maintain the aspect ratio and add padding (default is True).
    :param save_path: Optional path to save the resized video. If None, saves in the same folder as the video.
    :return: The path of the saved resized video.
    """
    # Generate the output path using get_save_path
    if save_path is None:
        save_path = "*_resize"
    save_path = get_save_path(video_path, save_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    # Get video properties
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object to save the resized video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if keep_aspect_ratio:
            # Calculate aspect ratio of the original frame
            aspect_ratio = original_width / original_height

            # Calculate new dimensions while maintaining aspect ratio
            if (width / height) > aspect_ratio:
                new_height = height
                new_width = int(aspect_ratio * height)
            else:
                new_width = width
                new_height = int(width / aspect_ratio)

            # Resize the frame
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Create a black background and center the resized frame on it
            padded_frame = np.zeros((height, width, 3), dtype=np.uint8)
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            padded_frame[y_offset:y_offset + new_height,
                         x_offset:x_offset + new_width] = resized_frame
        else:
            # Force resize to exact dimensions
            padded_frame = cv2.resize(frame, (width, height))

        # Write the resized (or padded) frame to the output video
        out.write(padded_frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    print_et(f"Resized video saved as {save_path}")
    return save_path


def change_video_speed(video_path: str, speed_factor: float, save_path: str = None):
    """
    Changes the playback speed of a video by adjusting the frame rate.

    :param video_path: Path to the input video file.
    :param speed_factor: The factor by which to adjust the speed. Values greater than 1.0 speed up the video, and values less than 1.0 slow it down.
    :param save_path: Optional path to save the speed-adjusted video. If None, saves in the same folder as the video with a modified name.
    :return: The path of the saved speed-adjusted video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_speed"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    save_fps = fps * speed_factor

    # Create VideoWriter object with adjusted frame rate
    out = cv2.VideoWriter(save_path, fourcc, save_fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print_et(f"Video saved with adjusted speed as {save_path}")
    return save_path


def rotate_flip_video(video_path: str, rotation_degrees: int = 0, flip_axis: str = None, save_path: str = None):
    """
    Rotates and/or flips a video according to specified codes.

    :param video_path: Path to the input video file.
    :param rotation_degrees: The rotation degrees (e.g., 90, 180, 270) to apply to the video.
    :param flip_axis: Optional flip axis ('H' for horizontal, 'V' for vertical) to apply. If None, no flip is applied.
    :param save_path: Optional path to save the rotated/flipped video. If None, saves in the same folder as the video.
    :return: The path of the saved rotated/flipped video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_rotate_flip"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Determine the new width and height if rotation requires a change
    if rotation_degrees in [90, 270]:
        out_width, out_height = height, width
    else:
        out_width, out_height = width, height

    # Create VideoWriter object to save the rotated/flipped video
    out = cv2.VideoWriter(save_path, fourcc, fps, (out_width, out_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate the frame
        if rotation_degrees == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation_degrees == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotation_degrees == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Flip the frame if flip_axis is specified
        if flip_axis:
            flip_axis = flip_axis.lower()
            if flip_axis == 'h':  # Horizontal flip
                frame = cv2.flip(frame, 1)
            elif flip_axis == 'v':  # Vertical flip
                frame = cv2.flip(frame, 0)

        # Write the processed frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print_et(f"Rotated/flipped video saved as {save_path}")
    return save_path


def adjust_hsb(video_path: str, brightness=1.0, saturation=1.0, hue=0, save_path: str = None):
    """
    Adjusts the brightness, saturation, and hue of a video using the HSV color space.

    :param video_path: Path to the input video file.
    :param brightness: Factor to adjust brightness (1.0 = no change).
    :param saturation: Factor to adjust saturation (1.0 = no change).
    :param hue: Offset to adjust hue in degrees (-180 to 180).
    :param save_path: Optional path to save the adjusted video. If None, saves in the same folder as the video.
    :return: The path of the saved adjusted video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_hsb"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object to save the adjusted video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Adjust the HSB values
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv_frame[..., 2] = np.clip(
            hsv_frame[..., 2] * brightness, 0, 255)  # Brightness
        hsv_frame[..., 1] = np.clip(
            hsv_frame[..., 1] * saturation, 0, 255)  # Saturation
        hsv_frame[..., 0] = (hsv_frame[..., 0] + hue) % 180  # Hue
        adjusted_frame = cv2.cvtColor(
            hsv_frame.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # Write the adjusted frame to the output video
        out.write(adjusted_frame)

    # Release resources
    cap.release()
    out.release()
    print_et(f"HSB-adjusted video saved as {save_path}")
    return save_path


def adjust_contrast_gamma(video_path: str, contrast=1.0, gamma=1.0, save_path: str = None):
    """
    Adjusts the contrast and gamma of a video.

    :param video_path: Path to the input video file.
    :param contrast: Factor to adjust contrast (1.0 = no change).
    :param gamma: Factor to adjust gamma (1.0 = no change).
    :param save_path: Optional path to save the adjusted video. If None, saves in the same folder as the video.
    :return: The path of the saved adjusted video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_contrast_gamma"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object to save the adjusted video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # Create a lookup table for gamma correction
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma *
                     255 for i in np.arange(0, 256)]).astype("uint8")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Adjust contrast
        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=0)

        # Apply gamma correction using the lookup table
        adjusted_frame = cv2.LUT(frame, table)

        # Write the adjusted frame to the output video
        out.write(adjusted_frame)

    # Release resources
    cap.release()
    out.release()
    print_et(f"Contrast and gamma-adjusted video saved as {save_path}")
    return save_path


def remove_chatter(video_path: str, buffer_size: int = 5, save_path: str = None):
    """
    Remove chatter (minor, inconsistent movements) from a video using temporal filtering.

    :param video_path: Path to the input video file.
    :param buffer_size: Number of frames to average for smoothing. Default is 5.
    :param save_path: Path to save the output video. If None, saves in the same location
                      as the input video with a suffix. If a simple filename
                      is provided, it saves in the input video folder with the same extension.
    :param suffix: Suffix to add to the filename if save_path is None. Defaults to '_saved'.
    """
    # Get the save path based on input parameters
    if save_path is None:
        save_path = "*_remove_chatter"
    save_path = get_save_path(video_path, save_path)

    # Extract video file information
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

    # Initialize buffer to hold frames for averaging
    frame_buffer = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Add the current frame to the buffer
        frame_buffer.append(frame)

        # Ensure buffer doesn't exceed the defined size
        if len(frame_buffer) > buffer_size:
            frame_buffer.pop(0)

        # Calculate the average frame
        avg_frame = np.mean(frame_buffer, axis=0).astype(np.uint8)

        # Write the averaged frame to the output video
        out.write(avg_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print_et(f"Processed video saved at: {save_path}")
    return save_path


def blur_sharpen_video(video_path: str, blur_strength=0, sharpen_strength=0, save_path: str = None):
    """
    Applies blur and/or sharpen effects to a video.

    :param video_path: Path to the input video file.
    :param blur_strength: Strength of the Gaussian blur effect. A value of 0 means no blur.
    :param sharpen_strength: Strength of the sharpening effect. A value of 0 means no sharpening.
    :param save_path: Optional path to save the blurred/sharpened video. If None, saves in the same folder as the video.
    :return: The path of the saved blurred/sharpened video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_blur_sharpen"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object to save the blurred/sharpened video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Apply blur if specified
        if blur_strength > 0:
            frame = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
        # Apply sharpen if specified
        if sharpen_strength > 0:
            kernel = np.array([[0, -sharpen_strength, 0],
                               [-sharpen_strength, 1 + 4 *
                                   sharpen_strength, -sharpen_strength],
                               [0, -sharpen_strength, 0]])
            frame = cv2.filter2D(frame, -1, kernel)
        # Write the processed frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print_et(f"Blurred/Sharpened video saved as {save_path}")
    return save_path


def zoom_pan_video(video_path: str, zoom_factor: float, pan_factor_x: int, pan_factor_y: int, save_path: str = None):
    """
    Applies a zoom and pan effect to a video.

    :param video_path: Path to the input video file.
    :param zoom_factor: The factor by which to zoom the video.
    :param pan_factor_x: The number of pixels to pan horizontally.
    :param pan_factor_y: The number of pixels to pan vertically.
    :param save_path: Optional path to save the zoomed/panned video. If None, saves in the same folder as the video.
    :return: The path of the saved zoomed/panned video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_zoom_pan"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Calculate new dimensions after zoom
    width = int(original_width / zoom_factor)
    height = int(original_height / zoom_factor)

    # Create VideoWriter object to save the zoomed/panned video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Calculate the starting points for the pan effect
        x_start = pan_factor_x
        y_start = pan_factor_y
        # Apply zoom and pan by cropping the frame
        frame = frame[y_start:y_start + height, x_start:x_start + width]
        # Write the processed frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print_et(f"Zoomed/Panned video saved as {save_path}")
    return save_path


def reverse_video(video_path: str, save_path: str = None):
    """
    Reverses the playback of a video.

    :param video_path: Path to the input video file.
    :param save_path: Optional path to save the reversed video. If None, saves in the same folder as the video.
    :return: The path of the saved reversed video.
    """
    # Use get_save_path to determine the output path
    if save_path is None:
        save_path = "*_reverse"
    save_path = get_save_path(video_path, save_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print_et("Error: Cannot open the video file.")
        return None

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object to save the reversed video
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # Write frames in reverse order
    for frame in reversed(frames):
        out.write(frame)

    out.release()
    print_et(f"Reversed video saved as {save_path}")
    return save_path


def concatenate_videos(video_paths: list, save_path: str = None):
    """
    Concatenates multiple video files into a single video.

    :param video_paths: List of paths to the video files to concatenate.
    :param save_path: Optional path to save the concatenated video. If None, saves in the same folder as the first video.
    :return: The path of the saved concatenated video.
    """

    if not video_paths:
        print_et("Error: No videos provided for concatenation.")
        return None

    cap_list = [cv2.VideoCapture(p) for p in video_paths]

    if any(not cap.isOpened() for cap in cap_list):
        print_et("Error: One or more video files cannot be opened.")
        return None

    fps = int(cap_list[0].get(cv2.CAP_PROP_FPS))
    width = int(cap_list[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap_list[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap_list[0].get(cv2.CAP_PROP_FOURCC))

    video_folder = os.path.dirname(
        video_paths[0]) if save_path is None else save_path
    video_name = "concatenated_video"
    output_path = os.path.join(video_folder, f"{video_name}.mp4")

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for cap in cap_list:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()

    out.release()
    print_et(f"Concatenated video saved as {output_path}")
    return output_path
