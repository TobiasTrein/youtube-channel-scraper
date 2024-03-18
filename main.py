import os
import config
import yt_dlp
import cv2

def process_video(url, video_number):
    ydl_opts = {}
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(url, download=False)

    output_dir = os.path.join("output", f"video{video_number}")
    os.makedirs(output_dir, exist_ok=True)

    formats = info_dict.get('formats', None)
    for f in formats:
        if f.get('format_note', None) == config.video_quality:
            video_url = f.get('url', None)
            cap = cv2.VideoCapture(video_url)
            frame_count = 0
            
            video_dir = os.path.join("output", f"video{i+1}")
            os.makedirs(video_dir, exist_ok=True)

            while True:
                # Set the frame position to read the next frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

                # Read the next frame
                ret, frame = cap.read()
                if not ret:
                    break

                # Process the frame (e.g., display, save, etc.)
                filename = os.path.join(video_dir, f"frame{frame_count}.png")
                cv2.imwrite(filename, frame)

                # Skip frames according to the specified pattern
                frame_count += 300  # Skip 300 frames

            cap.release()
            cv2.destroyAllWindows()
            break

def get_channel_videos(channel_id):
    url = f'https://www.youtube.com/{channel_id}/{config.type}'
    ydl_opts = {
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        channel_videos = ydl.extract_info(url, download=False)
        return [video['url'] for video in channel_videos['entries']]

videos = get_channel_videos(config.channel_id)
for i, video_url in enumerate(videos, start=1):
    process_video(video_url, i)
    