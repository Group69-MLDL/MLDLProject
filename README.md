# MLDLProject: From Query-Based Segment Retrieval to Answer Generation in Egocentric Videos

This repository contains the full implementation for "From Query-Based Segment Retrieval to Answer Generation in Egocentric
 Videos". The codebase includes model training notebooks, architecture experiments, video segment processing scripts, answer generation pipelines, and evaluation metrics, corresponding to sections of the final project report.

---

## 📁 Repository Structure

- `3_3_Temporal_Localization_Models/`:  
  Temporal localization with VSLBase and VSLNet using EgoVLP and Omnivore features. Includes Colab-compatible notebooks for Section 3.3.

- `3_4_Architectural_Variants_VSLNet/`:  
  Contains experiments with GLoVE and BERT Non-Shared Encoder variants of VSLNet. Also runnable on free-tier Colab. Linked to Section 3.4.

- `3_5_Temporal_Localization_To_Answer_Generation/`:  
  Local-only scripts for downloading, trimming, and annotating clips using Selenium and ffmpeg. Corresponds to Section 3.5.

- `3_6_Answer_Generation_VideoQA_Models/`:  
  Answer generation with LLaVA-NeXT, CogVLM2, and InternVideo2.5. Requires high-end GPU (e.g., A100). Covered in Section 3.6.

- `4_5_NLP_Metrics.ipynb`:  
  Notebook for computing BLEU and ROUGE metrics on generated answers. Linked to Section 4.5.

- `Report/`:  
  Contains LaTeX source files, assets, and compiled report PDF.

---

## ⚙️ Environment Setup

### General Dependencies

All the dependencies will be solved during each notebook's run.

## ⚙️ Section-Specific Dependencies

### `3_5_Temporal_Localization_To_Answer_Generation/`

```bash
pip install selenium
sudo apt install ffmpeg # if on Linux. On Windows download the installer from official website.
# ChromeDriver should match your Chrome version
```

### `3_6_Answer_Generation_VideoQA_Models/`

- ⚠️ Requires: A100 GPU or Colab Pro+ instance
- ⏳ Estimated Required Colab Units: ~100 Google Colab compute units

## 💻 Hardware Requirements

| Section                                              | Platform         | Notes                                                  |
|------------------------------------------------------|------------------|--------------------------------------------------------|
| `3_3_Temporal_Localization_Models`                   | Google Colab     | Free-tier compatible                                   |
| `3_4_Architectural_Variants_VSLNet`                  | Google Colab     | Free-tier compatible                                   |
| `3_5_Temporal_Localization_To_Answer_Generation`     | Local machine     | Requires ffmpeg, Selenium, and manual labeling         |
| `3_6_Answer_Generation_VideoQA_Models`               | A100 / Colab Pro | Very high memory/compute requirements                  |
| `4_5_NLP_Metrics.ipynb`                              | Any              | Lightweight metric evaluation                          |

## 🚀 How to Run

### `3_3_Temporal_Localization_Models/`

- Open notebooks in Google Colab
- Select between EgoVLP or Omnivore variants
- Execute all cells
- Outputs will be saved in the `runs/` directory

### `3_4_Architectural_Variants_VSLNet/`

- Navigate to either `GLoVE/` or `NonSharedEncoder/` subdirectories
- Run the notebooks in Google Colab
- Uses default hyperparameters
- Choose between EgoVLP or Omnivore features as input

### `3_5_Temporal_Localization_To_Answer_Generation/`

- Execute Python scripts locally (not compatible with Colab)
- Video clips will be downloaded using Selenium from Ego4D Visualizer
- Requirements:
  - Install `ffmpeg` and add it to system PATH
  - Install `selenium` Python package
  - Manually watch and label `[clip_uid]_[query_idx].mp4` files inside the `clips/` directory

### `3_6_Answer_Generation_VideoQA_Models/`

- Use notebooks located in the `NoteBook/` directory
- Place prepared input files in `input/` directory
- Generated outputs will be saved in `output/`
- Supported models:
  - LLaVA-NeXT
  - CogVLM2
  - InternVideo2.5
- ⚠️ This section is highly resource-intensive and requires an A100 GPU or equivalent (e.g., Colab Pro with high memory runtime)

### `4_5_NLP_Metrics.ipynb`

- Run this notebook after generating answer predictions from VLMs
- Calculates evaluation metrics:
  - BLEU-1, BLEU-2, BLEU-4
  - ROUGE-1, ROUGE-L
- Outputs average scores across all evaluated queries

## 📄 Report

The `Report/` folder includes:

- Full LaTeX source code
- Tables, images, and bibliography
- Code section references aligned with the report structure
