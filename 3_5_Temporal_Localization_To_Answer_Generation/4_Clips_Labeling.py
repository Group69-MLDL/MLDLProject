import json
import os

# Load the top_50_queries.json file
with open('inputs/top_50_queries.json', 'r') as f:
    top_50_queries = json.load(f)

# Path for the labeled file
labeled_file = 'outputs/labeled_top_50_queries.json'

# If the labeled file already exists, load it; otherwise, start with top_50_queries
if os.path.exists(labeled_file):
    with open(labeled_file, 'r') as f:
        labeled_queries = json.load(f)
else:
    # Create a copy of the top_50_queries with modifications
    labeled_queries = []
    for query in top_50_queries:
        new_query = query.copy()
        # Rename 'sentence' to 'question' if it exists
        if 'sentence' in new_query:
            new_query['question'] = new_query.pop('sentence')
        # Add an empty 'answer' field if it doesn't exist
        if 'answer' not in new_query:
            new_query['answer'] = ''
        labeled_queries.append(new_query)
    # Save the new labeled file right away
    with open(labeled_file, 'w') as f:
        json.dump(labeled_queries, f, indent=4)


# Loop over each query and prompt for answer if empty
for idx, query in enumerate(labeled_queries, start=1):
    clip_uid = query.get('clip_uid', 'unknown')
    question = query.get('question', '')
    query_idx = query.get('query_idx', 'unknown')

    # Skip if 'answer' already exists and is not empty
    if 'answer' in query and query['answer']:
        print(f"[{idx}] Clip UID: {clip_uid} — Question already answered. Skipping.")
        continue

    print(f"\n[{idx}] Clip UID: {clip_uid} — Query Index: {query_idx}")
    print(f"Question: {question}")
    answer = input("Enter your answer (or press Enter to skip): ").strip()
    
    # Only update if user provides an answer
    if answer:
        query['answer'] = answer

    # Save the updated file after each entry to ensure progress is saved
    with open(labeled_file, 'w') as f:
        json.dump(labeled_queries, f, indent=4)

print("\n✅ All questions labeled and saved to labeled_top_50_queries.json!")