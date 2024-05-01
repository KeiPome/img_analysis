import os
import re
import glob
import cv2
import argparse
import datetime

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def create_video_from_images(image_folder, output_folder, fps, segment_duration, start_frame, end_frame):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    images = glob.glob(f"{image_folder}/*.jpg")
    images.sort(key=natural_keys)
    
    images = images[start_frame:end_frame] if end_frame else images[start_frame:]
    
    total_frames = segment_duration * 60 * fps
    segment_index = 0
    img_array = []

    for i, img_path in enumerate(images):
        if i % total_frames == 0 and i != 0:
            save_video(img_array, output_folder, segment_index, fps)
            print(f"Segment {segment_index} video created with {len(img_array)} frames.")
            img_array = []
            segment_index += 1
            
        if i % 100 == 0:  # Every 100 frames, print progress
            print(f"Processing frame {i} of {len(images)}...")
        
        img = cv2.imread(img_path)
        img_array.append(img)
    
    if img_array:
        save_video(img_array, output_folder, segment_index, fps)
        print(f"Segment {segment_index} video created with {len(img_array)} frames. All segments completed.")

def save_video(images, output_folder, index, fps):
    now = datetime.datetime.now()
    output_folder = f"{output_folder}/{now.strftime('%Y-%m-%d')}"
    
    try:
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    except FileExistsError:
        print(f"Folder already exists: {output_folder}")
        pass
    
    height, width, layers = images[0].shape
    size = (width, height)
    video_path = os.path.join(output_folder, f"{index}.mp4")
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    
    for image in images:
        out.write(image)
    out.release()

def main():
    parser = argparse.ArgumentParser(description="Create videos from images.")
    parser.add_argument("image_folder", type=str, help="Directory containing the images.")
    parser.add_argument("output_folder", type=str, help="Directory where videos will be saved.")
    parser.add_argument("--fps", type=int, default=50, help="Frame rate of the video.")
    parser.add_argument("--segment_duration", type=int, default=5, help="Duration of each video segment in minutes.")
    parser.add_argument("--start_frame", type=int, default=0, help="Start frame to begin creating video.")
    parser.add_argument("--end_frame", type=int, default=None, help="End frame to stop creating video.")
    
    args = parser.parse_args()
    
    create_video_from_images(
        args.image_folder, 
        args.output_folder, 
        args.fps, 
        args.segment_duration, 
        args.start_frame, 
        args.end_frame
    )

if __name__ == "__main__":
    main()
