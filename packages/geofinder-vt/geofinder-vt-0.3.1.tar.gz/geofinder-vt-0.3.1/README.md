# GEOFINDER-VT

This is collaboration with Dr. Junghwan Kim (Department of Geography@Virginia Tech) to create a user friendly Python API that uses geographical video files (captured by GoPro) to extract nearest gps location. The extracted metadata is saved in a CSV file and the image frame renamed with the tagged geolocation is available in the specified folder. 

## Installation
To install this tool from PyPI, use the following command:
```
pip install geofinder-vt
```

## Usage

### VideoConverter Class

The VideoConverter class is used to extract images from video files in a specified folder.

```
from geofinder_vt import VideoConverter

video_folder = "campus_video_test"  # Specify the folder where your video files are stored
converter = VideoConverter(video_folder)
converter.video_extract_folder()
```

#### Methods

`__init__(self, video_folder_prefix)`: Initializes the VideoConverter with the specified folder prefix.

`video_extract(self, video_file)`: Extracts images from a single video file using the extract_video function.

`video_extract_folder(self)`: Extracts images from all video files in the specified folder.


### ImageExtractor Class

The ImageExtractor class is used to process metadata from the extracted images and move relevant files based on geolocation data.

Example Usage
```
from geofinder_vt import ImageExtractor

input_csv = "example.csv"  # Path to your CSV file containing geolocation data
directory_prefix = "GH"  # Directory prefix to filter relevant folders
extractor = ImageExtractor(input_csv, directory_prefix)
destination_path = extractor.run()
print(f"Processed files moved to: {destination_path}")

```

#### Methods

`__init__(self, input_csv, dir_prefix)`: Initializes the ImageExtractor with the specified input CSV and directory prefix.

`list_relevant_folders(self)`: Lists all relevant folders in the base path that start with the specified directory prefix.

`consolidate_files(self, folders)`: Consolidates all files from the relevant folders.

`prepare_dataframe(self, all_files)`: Prepares a DataFrame from the consolidated files, extracting necessary metadata.

`find_closest_coords(self, row, ref_df)`: Finds the closest coordinates for a given row from the reference DataFrame.

`process_files(self, ref_df)`: Processes the files and finds unique files based on the closest coordinates.

`move_files(self, unique_files)`: Moves the unique files to a new destination directory.

`run(self)`: Runs the entire process of listing folders, consolidating files, preparing the DataFrame, processing files, and moving files.

## Dependencies
This tool requires the following dependencies:

`pandas>=2.0.1`

`geopy>=2.3.0`

`moviepy>=1.0.3`

`numpy>=1.24.3`

`xmltodict>=0.13.0`

`gpmf>=0.1`

`gpxpy>=1.5.0`

These packages are installed along with the installation of the geofinder-vt package

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

