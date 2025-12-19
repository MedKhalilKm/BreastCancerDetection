# 🩺 Breast Cancer Prediction API (FastAPI)

This project is a **FastAPI-based web service** for **breast cancer classification**.  
It supports prediction using either **numerical tumor features** or **breast cancer images**, from which features are automatically extracted.

The backend uses a **Voting Classifier** trained on normalized data inspired by the **Wisconsin Breast Cancer Diagnostic (WBCD)** feature set.

---

## 🚀 Features

- 🖼️ Upload a breast cancer tumor image
- 🧠 Automatic extraction of **30 tumor features**
- 🔍 Breast cancer prediction (**Benign / Malignant**)
- 📊 Confidence score (if supported by the model)
- 📡 REST API with Swagger documentation
- 🔗 Designed to work with a frontend application

---

## 🧠 Extracted Features (30)

### Mean Values (1–10)
- radius_mean  
- texture_mean  
- perimeter_mean  
- area_mean  
- smoothness_mean  
- compactness_mean  
- concavity_mean  
- concave_points_mean  
- symmetry_mean  
- fractal_dimension_mean  

### Standard Error Values (11–20)
- radius_se  
- texture_se  
- perimeter_se  
- area_se  
- smoothness_se  
- compactness_se  
- concavity_se  
- concave_points_se  
- symmetry_se  
- fractal_dimension_se  

### Worst (Largest) Values (21–30)
- radius_worst  
- texture_worst  
- perimeter_worst  
- area_worst  
- smoothness_worst  
- compactness_worst  
- concavity_worst  
- concave_points_worst  
- symmetry_worst  
- fractal_dimension_worst  

---

## 🖥️ Frontend Application

This API is connected to a **frontend project** that provides a user-friendly interface for interacting with the model.

🔗 **Frontend Repository:**  
https://github.com/your-username/your-frontend-repo

The frontend allows users to:
- Upload breast cancer images
- Send requests to the FastAPI backend
- View predictions and confidence scores
- Display extracted tumor features

---

## 📁 Project Structure

.
├── app.py  
├── model/  
│   └── voting_classifier_model.pkl  
├── requirements.txt  
├── README.md  

---

## 🛠️ Requirements

The project dependencies are listed in `requirements.txt`:

- fastapi  
- uvicorn[standard]  
- numpy  
- joblib  
- opencv-python-headless  
- scikit-image  
- python-multipart  
- pydantic  

---

## ⚙️ Installation

### Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
