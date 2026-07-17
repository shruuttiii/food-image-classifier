# 🍽️ FoodLens AI — Food Image Classifier & Nutrition Estimator

A computer vision mini-project that classifies food images into 15 categories using
**transfer learning (MobileNetV2)** and estimates nutrition info, deployed as an
interactive **Streamlit** web app.

## 🎯 Project Overview

| | |
|---|---|
| **Task** | Multi-class food image classification |
| **Classes** | 15 (biryani, pizza, burger, dosa, idli, samosa, sushi, pasta, noodles, and more) |
| **Approach** | Transfer learning with MobileNetV2 (pretrained on ImageNet), fine-tuned |
| **Framework** | TensorFlow / Keras |
| **Deployment** | Streamlit (Streamlit Community Cloud) |
| **Bonus feature** | Calorie & nutrition estimation for the predicted food |

## 🗂️ Repository Structure

```
food-image-classifier/
│── app.py                  
│── food_classifier_model.h5 
│── class_labels.json       
│── nutrition_data.py       
│── requirements.txt        
│── README.md               
│── train_food_classifier.ipynb   
│── .gitignore              
```

## 🧠 Model Approach

1. **Data augmentation** — rotation, zoom, shift, brightness, flips (dataset has
   ~1600 images across 15 classes, so augmentation reduces overfitting)
2. **Stage 1 — Head training** — MobileNetV2 base frozen, custom classification
   head trained on top
3. **Stage 2 — Fine-tuning** — top ~40 layers of MobileNetV2 unfrozen, trained
   at a very low learning rate to adapt features specifically to food images
4. **Evaluation** — accuracy/loss curves, confusion matrix, classification report

## 🥗 Why Nutrition Is Serving-Based, Not Pixel-Measured

A single 2D photo has no depth or scale reference, so no model can determine
exact portion weight from pixels alone (without a reference object or depth
sensor). Instead, once the food is classified, the app shows nutrition for a
**standard serving size**, with a slider to scale the estimate up or down.
This is the same approach used by real-world food-logging apps.

## 🚀 How to Run

### 1. Train the model (Google Colab)
- Open `notebook/train_food_classifier.ipynb` in Colab
- Set runtime to GPU (`Runtime > Change runtime type > GPU`)
- Upload your dataset zip when prompted, run all cells
- Download `food_classifier_model.h5` and `class_labels.json`
- Place both files inside the `app/` folder

### 2. Run the app locally
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

### 3. Deploy on Streamlit Community Cloud
1. Push this repo to GitHub (see `.gitignore` — model file may need Git LFS if >100MB, or host it externally and load via URL)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo, set the main file path to `app/app.py`
4. Deploy 🎉

## 📊 Results

_Add your final validation accuracy, confusion matrix, and sample predictions here after training (screenshots from the notebook)._

## 🛠️ Tech Stack

- **Model:** TensorFlow / Keras, MobileNetV2 (transfer learning)
- **App:** Streamlit, Plotly
- **Language:** Python
