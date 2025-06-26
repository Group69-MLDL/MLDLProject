
import json
import os
import subprocess

# Directories
VIDEO_DIR = 'videos'
CLIP_DIR = 'clips'
RE_CLIP_DIR = 'outputs/re_clips'
os.makedirs(CLIP_DIR, exist_ok=True)
os.makedirs(RE_CLIP_DIR, exist_ok=True)

# Load top 50 queries
with open('inputs/top_50_queries.json', 'r') as f:
    top_50_queries = json.load(f)

# Process each query
for idx, query in enumerate(top_50_queries, start=1):
    video_uid = query["video_uid"]
    start_time = query["video_start_sec"]
    end_time = query["video_end_sec"]

    video_path = os.path.join(VIDEO_DIR, f"{video_uid}.mp4")
    clip_uid = query["clip_uid"]
    clip_path = os.path.join(CLIP_DIR, f"{clip_uid}.mp4")

    if not os.path.exists(video_path):
        print(f"[{idx}] Video file not found: {video_path}. Skipping.")
        continue

    if os.path.exists(clip_path):
        print(f"[{idx}] Clip already exists: {clip_path}. Skipping.")
        continue

    ffmpeg_cmd = [
        'ffmpeg',
        '-ss', str(start_time),  # Accurate trimming
        '-to', str(end_time),
        '-i', video_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',  # Compatibility for some ffmpeg builds
        clip_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"[{idx}] Created clip: {clip_path} from {start_time:.2f}s to {end_time:.2f}s of video {video_uid}")

print("✅ All clips created successfully!")

# ⚠️ Second phase: Clip again based on best_predicted_segment
for idx, query in enumerate(top_50_queries, start=1):
    clip_uid = query["clip_uid"]
    query_idx = query["query_idx"]
    best_start, best_end = query["best_predicted_segment"]

    input_clip_path = os.path.join(CLIP_DIR, f"{clip_uid}.mp4")
    output_clip_path = os.path.join(RE_CLIP_DIR, f"{clip_uid}_{query_idx}.mp4")

    if not os.path.exists(input_clip_path):
        print(f"[{idx}] Input clip not found: {input_clip_path}. Skipping.")
        continue

    if os.path.exists(output_clip_path):
        print(f"[{idx}] Best clip already exists: {output_clip_path}. Skipping.")
        continue

    ffmpeg_cmd = [
        'ffmpeg',
        '-ss', str(best_start),
        '-to', str(best_end),
        '-i', input_clip_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_clip_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"[{idx}] Created best-predicted clip: {output_clip_path} from {best_start:.2f}s to {best_end:.2f}s")

print("✅ All best-predicted clips created successfully!")