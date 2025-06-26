
import json
import numpy as np
from utils.evaluate_ego4d_nlq import evaluate_nlq_performance

# Toggle whether to use Google Drive (True) or local files (False)
GDrive = False

if(GDrive == True):
    from google.colab import drive
    drive.mount('/content/drive')

if GDrive:
    # Load data
    with open('/content/drive/MyDrive/Colab Notebooks/Egocentric Vision/BEST QUERIES/IOU/val.json', 'r') as f:
        val_data = json.load(f)
    with open('/content/drive/MyDrive/Colab Notebooks/Egocentric Vision/BEST QUERIES/IOU/vslnet_9_3230_preds.json', 'r') as f:
        pred_data = json.load(f)
    with open('/content/drive/MyDrive/Colab Notebooks/Egocentric Vision/BEST QUERIES/IOU/nlq_val.json', 'r') as f:
        nlq_val_data = json.load(f)
else:
    with open('inputs/val.json', 'r') as f:
        val_data = json.load(f)
    with open('inputs/vslnet_9_3230_preds.json', 'r') as f:
        pred_data = json.load(f)
    with open('inputs/nlq_val.json', 'r') as f:
        nlq_val_data = json.load(f)

# 3️⃣ Compute Metrics & Detailed Per-Query Results
thresholds = [0.01, 0.3, 0.5]
topK = [1, 3, 5]

# Correct unpacking based on the actual function signature
metrics, mIoU = evaluate_nlq_performance(
    predictions=pred_data["results"],
    ground_truth=nlq_val_data,
    thresholds=thresholds,
    topK=topK
)

print("===== Overall Metrics (Tensorboard Style) =====")
for i, thr in enumerate(thresholds):
    for j, k in enumerate(topK):
        print(f"R@{k} IoU={thr}: {metrics[i, j]:.4f}")
print(f"mIoU across all queries: {mIoU:.4f}")

# Function to calculate IoU for two intervals
def calculate_iou(pred, gt):
    inter_start = max(pred[0], gt[0])
    inter_end = min(pred[1], gt[1])
    if inter_start >= inter_end:
        return 0.0
    inter = inter_end - inter_start
    union = max(pred[1], gt[1]) - min(pred[0], gt[0])
    return inter / union

# Build mappings
clip_to_video_map = {}
clip_video_times = {}
for video in nlq_val_data['videos']:
    video_uid = video.get('video_uid', 'unknown')
    for clip in video.get('clips', []):
        clip_uid = clip.get('clip_uid', 'unknown')
        clip_to_video_map[clip_uid] = video_uid
        clip_video_times[clip_uid] = {
            "video_start_sec": clip.get("video_start_sec", 0.0),
            "video_end_sec": clip.get("video_end_sec", 0.0)
        }

# Build detailed_results
detailed_results = []
for pred in pred_data["results"]:
    clip_uid = pred["clip_uid"]
    query_idx = pred["query_idx"]
    predicted_times = pred["predicted_times"]

    # Ground truth
    gt_clip = val_data[clip_uid]
    gt_segment = gt_clip["exact_times"][query_idx]
    sentence = gt_clip["sentences"][query_idx]

    # Compute IoUs for top-5 predictions
    iou_per_pred = []
    for p_time in predicted_times[:5]:
        iou = calculate_iou(p_time, gt_segment)
        iou_per_pred.append(iou)

    video_times = clip_video_times.get(clip_uid, {"video_start_sec": 0.0, "video_end_sec": 0.0})

    detailed_results.append({
        "clip_uid": clip_uid,
        "query_idx": query_idx,
        "video_uid": clip_to_video_map.get(clip_uid, "unknown"),
        "sentence": sentence,
        "gt_segment": gt_segment,
        "predicted_segments": predicted_times[:5],
        "iou_per_pred": iou_per_pred,
        "avg_iou": np.mean(iou_per_pred) if iou_per_pred else 0.0,
        "video_start_sec": video_times["video_start_sec"],
        "video_end_sec": video_times["video_end_sec"]
    })

# Save detailed results
detailed_path = ('/content/drive/MyDrive/Colab Notebooks/Egocentric Vision/BEST QUERIES/IOU/detailed_eval_results.json' if GDrive else 'detailed_eval_results.json')
with open(detailed_path, 'w') as f:
    json.dump(detailed_results, f, indent=4)
print(f"Saved detailed evaluation results to {detailed_path}")

# 6️⃣ Extract and Save Top 50 Queries by Average IoU
for query in detailed_results:
    ious = query["iou_per_pred"]
    predicted_segments = query["predicted_segments"]

    best_idx = np.argmax(ious)
    best_pred_segment = predicted_segments[best_idx]

    query["best_predicted_segment"] = best_pred_segment
    query["best_iou"] = ious[best_idx] if ious else 0.0

top_50_queries = sorted(detailed_results, key=lambda x: x["avg_iou"], reverse=True)[:50]
top_50_path = ('/content/drive/MyDrive/Colab Notebooks/Egocentric Vision/BEST QUERIES/IOU/top_50_queries.json' if GDrive else 'inputs/top_50_queries.json')

with open(top_50_path, 'w') as f:
    json.dump(top_50_queries, f, indent=4)
print(f"Saved Top-50 queries to {top_50_path}")