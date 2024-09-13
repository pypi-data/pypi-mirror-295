import os
import shutil
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic
import concurrent.futures
import heapq

class ImageExtractor:
    def __init__(self, input_csv, dir_prefix):
        self.input_csv = input_csv
        self.dir_prefix = dir_prefix
        self.df = pd.read_csv(input_csv)
        self.base_path = "."

    def list_relevant_folders(self):
        return [item for item in os.listdir(self.base_path) 
                if os.path.isdir(os.path.join(self.base_path, item)) and item.startswith(self.dir_prefix)]

    def consolidate_files(self, folders):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            all_files = list(executor.map(self._get_files_in_folder, folders))
        return sum(all_files, [])

    def _get_files_in_folder(self, folder):
        full_folder_path = os.path.join(self.base_path, folder)
        return [f"{folder}/{file}" for file in os.listdir(full_folder_path) if 'metadata' not in file]

    def prepare_dataframe(self, all_files):
        df = pd.DataFrame(all_files, columns=["filename"])
        df[["folder", "fname"]] = df["filename"].str.split('/', expand=True)
        df[["dummy", "timestamp", "latitude", "longitude"]] = df['fname'].str.split('_', expand=True)
        df['longitude'] = df['longitude'].str.replace('.jpg', '')
        df = df[df['latitude'].notna()]
        return df

    def find_closest_coords(self, row, ref_df):
        min_heap = []
        for _, row_df in ref_df.iterrows():
            distance = geodesic((float(row_df['latitude']), float(row_df['longitude'])), 
                                (float(row['lat']), float(row['lon']))).kilometers
            if distance < 0.02:
                heapq.heappush(min_heap, (distance, row_df['filename']))
        return [heapq.heappop(min_heap)[1]] if min_heap else [None]

    def process_files(self, ref_df):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            print(self.df.itertuples,ref_df)
            closest_coords = list(executor.map(lambda row: self.find_closest_coords(row, ref_df), self.df.itertuples()))
        unique_files = set(sum(closest_coords, []))
        return unique_files - {None}

    def move_files(self, unique_files):
        destination_path = f"results_{datetime.now().timestamp()}"
        os.mkdir(destination_path)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(lambda file: shutil.copy(file, destination_path), unique_files))
        return destination_path
    
    def individual_coords(self, input_tuple, ref_df):
        row = {'lat':input_tuple['Latitude'],'lon':input_tuple['Longitude']}
        closest_coords = self.find_closest_coords(row, ref_df), self.df.itertuples()
        return closest_coords

    def run(self):
        folders = self.list_relevant_folders()
        all_files = self.consolidate_files(folders)
        ref_df = self.prepare_dataframe(all_files)
        unique_files = self.process_files(ref_df)
        destination = self.move_files(unique_files)
        self.df.to_csv('prelim_output.csv')
        return destination
