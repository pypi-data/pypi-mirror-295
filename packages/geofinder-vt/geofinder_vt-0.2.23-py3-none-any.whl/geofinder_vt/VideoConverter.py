import os
from moviepy.editor import VideoFileClip
import datetime
import numpy as np
import concurrent.futures
from .gpmf_support import extract_metadata
from moviepy.editor import VideoFileClip

class VideoConverter:
    def __init__(self, video_folder_prefix):
        self.video_folder_prefix = video_folder_prefix

    def video_extract(self, video_file):
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_clip = VideoFileClip(video_file)
        num_frames = int(video_clip.fps * video_clip.duration)
        output_dir = f"{os.path.basename(video_file).split('.')[0]}_{timestamp_str}"
        os.makedirs(output_dir, exist_ok=True)

        metadata_list = extract_metadata(video_file, output_dir)
        if not metadata_list:
            return

        old_indices = np.linspace(0, len(metadata_list) - 1, num=num_frames, endpoint=True)
        new_indices = np.round(old_indices).astype(int)
        frame_metadata_map = {i: metadata_list[new_indices[i]] for i in range(num_frames)}

        def save_frame(count, duration):
            frame_name = frame_metadata_map[count]
            frame_filename = os.path.join(output_dir, f"frame_{frame_name}.jpg")
            video_clip.save_frame(frame_filename, duration)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(save_frame, range(num_frames), np.arange(0, video_clip.duration, 1 / video_clip.fps)))

    def video_extract_folder(self):
        vids = os.listdir(self.video_folder_prefix)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(self.video_extract, [os.path.join(self.video_folder_prefix, vid) for vid in vids if vid.split('.')[-1] in ['mp4', '360', 'MP4']]))

# Example usage
if __name__ == "__main__":
    video_folder = "campus_video_test"
    converter = VideoConverter(video_folder)
    converter.video_extract_folder()
