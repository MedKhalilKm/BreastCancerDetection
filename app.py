from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import cv2
from skimage import measure, filters, morphology
# FIXED: Updated to use 'gray' spelling for newer scikit-image versions
from skimage.feature import graycomatrix, graycoprops
import shutil
import os

# ======================
# Load model (already normalized during training)
# ======================
# Ensure the model path is correct relative to where you run the server
model = joblib.load("model/voting_classifier_model.pkl")

app = FastAPI(
    title="Breast Cancer Prediction API",
    version="1.0"
)

# ======================
# CORS Middleware
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Input Schema
# ======================
class CancerInput(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float

    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float

    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

FEATURE_ORDER = list(CancerInput.model_fields.keys())

# ======================
# Image Processing Features
# ======================
def fractal_dimension(Z):
    """Estimate fractal dimension using box-counting"""
    Z = (Z > 0).astype(int)
    sizes = 2 ** np.arange(1, int(np.log2(min(Z.shape))))
    counts = []
    for size in sizes:
        S = np.add.reduceat(np.add.reduceat(Z, np.arange(0, Z.shape[0], size), axis=0),
                             np.arange(0, Z.shape[1], size), axis=1)
        counts.append(np.sum(S > 0))
    if len(counts) < 2:
        return 0.0
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]

def extract_features(image_path):
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not read image")
    
    # Step 1: Segment tumor
    try:
        thresh_val = filters.threshold_otsu(img)
    except Exception:
        # Fallback if image is uniform
        thresh_val = 128
        
    binary = img > thresh_val
    binary = morphology.remove_small_objects(binary, 50)
    
    # Step 2: Extract regions
    labeled_img = measure.label(binary)
    regions = measure.regionprops(labeled_img, intensity_image=img)
    
    if not regions:
        # Fallback feature values
        return {f: 0.0 for f in FEATURE_ORDER}

    # Take largest region as tumor
    region = max(regions, key=lambda r: r.area)
    
    # Step 3: Compute shape features
    area = region.area
    perimeter = region.perimeter
    radius = np.sqrt(area / np.pi)
    compactness = perimeter**2 / (4*np.pi*area) if area > 0 else 0
    concavity = region.eccentricity
    concave_points = region.extent
    symmetry = region.major_axis_length / (region.minor_axis_length + 1e-5)  # avoid divide by zero
    fractal = fractal_dimension(binary)
    
    # Step 4: Compute texture features
    # FIXED: using graycomatrix/graycoprops with 'a'
    glcm = graycomatrix(img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    texture = graycoprops(glcm, 'contrast')[0,0]
    smoothness = region.mean_intensity
    
    # Combine features into a dictionary
    raw_features = [radius, texture, perimeter, area, smoothness,
                    compactness, concavity, concave_points, symmetry, fractal]
    
    # Compute mean, SE, worst
    features = {}
    feature_names = ['radius','texture','perimeter','area','smoothness',
                     'compactness','concavity','concave_points','symmetry','fractal_dimension']
                     
    for i, name in enumerate(feature_names):
        mean_val = float(raw_features[i])
        se_val = float(raw_features[i] / np.sqrt(region.area)) if region.area > 0 else 0.0
        worst_val = float(raw_features[i])  # approximation
        
        features[f'{name}_mean'] = mean_val
        features[f'{name}_se'] = se_val
        features[f'{name}_worst'] = worst_val
    
    return features

# ======================
# Health check$
#uvicorn app:app --reload
# ======================
@app.get("/")
def health():
    return {"status": "FastAPI is running"}

# ======================
# Prediction endpoint
# ======================
@app.post("/predict")
def predict(data: CancerInput):
    # Convert input to NumPy array (correct order)
    X = np.array([[getattr(data, f) for f in FEATURE_ORDER]])

    prediction = model.predict(X)[0]

    # If your voting classifier supports probabilities
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba(X)[0].max())

    return {
        "prediction": "Malignant" if prediction == 1 else "Benign",
        "confidence": confidence
    }

# ======================
# Image Prediction endpoint
# ======================
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    try:
        # Save uploaded file
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract features
        features_dict = extract_features(temp_file)
        
        # Create input object for prediction
        input_data = CancerInput(**features_dict)
        
        # Get prediction using existing logic
        result = predict(input_data)
        
        # Add features to result
        result["features"] = features_dict
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)