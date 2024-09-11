# eclipsetools

[![PyPI version](https://badge.fury.io/py/eclipsetools.svg)](https://badge.fury.io/py/eclipsetools)

**eclipsetools** is a toolkit for various features I like having for my projects. Although it's intended to be used by me, it offers utilities that anyone might find useful for inclusion in their projects. It is lightweight and easy to integrate!

## Features

- **Video Tools**: A set of functions like crop, trim, blur, and more for working with video files. All functions that modify files save out a new file and do not alter the original input file.
- **Image Tools**: Provides basic image operations such as resizing, cropping, rotation, and adjustments to contrast, hue, and brightness.
- **File Tools**: File handling operations including copying directories, reading/writing files, and JSON utilities.
- **Task Tools**: Background task management with a tray icon interface for managing long-running or background tasks.

## Examples

**Video Tools:**
```python
from eclipsetools import vt

video_folder_path = "path/to/your/folder"
video_paths = vt.get_videos_in_folder(video_folder_path)

saved_paths = vt.perform_operations(video_paths, [
    vt.Operation.Resize(128, 128, keep_aspect_ratio=True, save_path="*_001"), # the star is the name of the input file
    vt.Operation.Crop(64, 128, save_path="*[_001:_002]"), # this will replace the _001 with _002
    vt.Operation.RotateFlip(90, "h", save_path="*[_002:_final]"), # this will rotate 90 degrees and flip on horizontal axis
])

vt.delete_all_but_last_operation_files(saved_paths) # this will remove all the files that were created besides the final ones
```


**Image Tools:**
Basically the same as video tools but both "**vt**" and "**it**" have different meta functions for getting info from files among other things
```python
from eclipsetools import it

image_folder_path = "path/to/your/folder"
image_paths = it.get_images_in_folder(image_folder_path)

saved_paths = it.perform_operations(image_paths, [
    it.Operation.Resize(128, 128, keep_aspect_ratio=True, save_path="*_001"), # the star is the name of the input file
    it.Operation.Crop(64, 128, save_path="*[_001:_002]"), # this will replace the _001 with _002
    it.Operation.RotateFlip(90, "h", save_path="*[_002:_final]"), # this will rotate 90 degrees and flip on horizontal axis
])

it.delete_all_but_last_operation_files(saved_paths) # this will remove all the files that were created besides the final ones
```

**File Tools:**
```python
from eclipsetools import ft

source_folder = "path/to/your/src_folder"
destination_folder = "path/to/your/dest_folder"

ft.copy_directory(source_folder, destination_folder, renaming=[
    ("_001", "_002"),  # replaces all _001 with _002 in all file and folder names
    ("fancy", "dirty"),  # replaces all fancy with dirty in all file and folder names
], 
ignore=[], # list of absolute paths of files or folders from the source folder to ignore
overwrite_files=True,
ignore_files=False # when true this will only copy over folders, no files
)
```


**Task Tools:**
```python
from eclipsetools import tt


class ExampleTask(tt.BackgroundTask):
    def __init__(self) -> None:
        super().__init__("ExampleTask")

    def start(self):
        print("Start")

    def update(self):
        from random import random
        print(random())

    def end(self):
        print("End")


service = tt.BackgroundService()
service.add_task(ExampleTask())
service.run()
```