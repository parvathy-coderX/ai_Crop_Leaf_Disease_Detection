"""
Weather-Based Disease Risk Model Training Script
Trains a machine learning model to predict disease risk based on weather conditions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score,
                           roc_curve, auc, roc_auc_score)
import warnings
warnings.filterwarnings('ignore')

# Configuration
class Config:
    # Paths
    DATA_PATH = '../../datasets/weather_data/Weather Data in India from 1901 to 2017.csv'
    MODEL_SAVE_PATH = '../models/weather_model.pkl'
    SCALER_SAVE_PATH = '../models/weather_scaler.pkl'
    FEATURES_SAVE_PATH = '../models/weather_features.pkl'
    LOGS_DIR = '../logs/weather_training'
    
    # Training parameters
    TEST_SIZE = 0.2
    RANDOM_SEED = 42
    CV_FOLDS = 5
    
    # Model parameters
    RF_N_ESTIMATORS = 100
    RF_MAX_DEPTH = 10
    GB_N_ESTIMATORS = 100
    GB_LEARNING_RATE = 0.1

class WeatherModelTrainer:
    def __init__(self):
        """Initialize the trainer"""
        self.config = Config()
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.models = {}
        self.best_model = None
        self.feature_names = []
        self.label_encoder = LabelEncoder()
        
        # Create directories - FIXED: changed exist-ok=True to exist_ok=True
        os.makedirs(os.path.dirname(self.config.MODEL_SAVE_PATH), exist_ok=True)
        os.makedirs(self.config.LOGS_DIR, exist_ok=True)  # ✅ Corrected: underscore instead of hyphen
        
        # Set random seed
        np.random.seed(self.config.RANDOM_SEED)
        
        print(f"✅ Trainer initialized with config:")
        print(f"   - Data path: {self.config.DATA_PATH}")
        print(f"   - Test size: {self.config.TEST_SIZE}")
        print(f"   - CV folds: {self.config.CV_FOLDS}")

    def load_and_prepare_data(self):
        """Load and prepare the weather dataset"""
        print("\n📁 Loading and preparing dataset...")
        
        try:
            # Try to load real dataset
            self.df = pd.read_csv(self.config.DATA_PATH)
            print(f"✅ Loaded {len(self.df)} samples from dataset")
            
            # Display basic info about the actual dataset structure
            print(f"\n📊 Dataset shape: {self.df.shape}")
            print(f"\nColumn names: {list(self.df.columns)}")
            print(f"\nFirst few rows:")
            print(self.df.head())
            
            print(f"\nDataset info:")
            print(self.df.info())
            
            print(f"\nBasic statistics:")
            print(self.df.describe())
            
            # Transform the dataset to the required format
            self.transform_weather_data()
            
        except FileNotFoundError:
            print("⚠️ Real dataset not found. Generating synthetic data...")
            self.df = self.generate_synthetic_data()

    def transform_weather_data(self):
        """Transform the weather dataset to the required format"""
        print("\n🔄 Transforming weather data to required format...")
        
        # Melt the dataframe to have monthly data as rows
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        
        # Season mapping
        season_map = {
            'JAN': 1, 'FEB': 1,  # Winter
            'MAR': 2, 'APR': 2, 'MAY': 2,  # Spring/Summer transition
            'JUN': 3, 'JUL': 3, 'AUG': 3,  # Summer/Monsoon
            'SEP': 4, 'OCT': 4, 'NOV': 4,  # Autumn/Post-monsoon
            'DEC': 5  # Early Winter
        }
        
        # Create expanded dataset
        expanded_data = []
        
        for _, row in self.df.iterrows():
            year = row['YEAR']
            for month in months:
                temperature = row[month]
                
                # Determine season based on month
                season = season_map[month]
                
                # Generate correlated features based on temperature
                # This is a simplified approach - in production, you'd want real humidity/rainfall data
                if season == 1:  # Winter
                    humidity = np.random.normal(60, 10)
                    rainfall = np.random.exponential(5)
                    wind_speed = np.random.normal(10, 3)
                    pressure = np.random.normal(1015, 5)
                elif season == 2:  # Spring
                    humidity = np.random.normal(65, 8)
                    rainfall = np.random.exponential(15)
                    wind_speed = np.random.normal(12, 4)
                    pressure = np.random.normal(1012, 4)
                elif season == 3:  # Summer/Monsoon
                    humidity = np.random.normal(80, 10)
                    rainfall = np.random.exponential(30)
                    wind_speed = np.random.normal(18, 6)
                    pressure = np.random.normal(1008, 5)
                elif season == 4:  # Autumn
                    humidity = np.random.normal(70, 8)
                    rainfall = np.random.exponential(20)
                    wind_speed = np.random.normal(14, 4)
                    pressure = np.random.normal(1010, 4)
                else:  # Early Winter
                    humidity = np.random.normal(65, 8)
                    rainfall = np.random.exponential(8)
                    wind_speed = np.random.normal(11, 3)
                    pressure = np.random.normal(1013, 4)
                
                # Add some correlation with temperature
                humidity = max(20, min(100, humidity + (temperature - 25) * 0.5))
                
                # Random crop type for each sample
                crop_type = np.random.choice([1, 2, 3, 4, 5, 6])
                
                expanded_data.append({
                    'year': year,
                    'month': month,
                    'season': season,
                    'crop_type': crop_type,
                    'temperature': temperature,
                    'humidity': humidity,
                    'rainfall': rainfall,
                    'wind_speed': wind_speed,
                    'pressure': pressure
                })
        
        self.df = pd.DataFrame(expanded_data)
        
        print(f"✅ Transformed data: {len(self.df)} samples")
        print(f"   Columns: {list(self.df.columns)}")
        print(f"\nSample of transformed data:")
        print(self.df.head())
        
        # Calculate risk levels for the transformed data
        self.calculate_risk_levels()

    def calculate_risk_levels(self):
        """Calculate risk levels based on weather conditions"""
        print("\n📊 Calculating risk levels...")
        
        def calculate_risk(row):
            risk_score = 0
            
            # Temperature effects (using actual temperature from data)
            if row['temperature'] > 35:
                risk_score += 30
            elif row['temperature'] > 32:
                risk_score += 20
            elif row['temperature'] < 15:
                risk_score += 25
            elif row['temperature'] < 20:
                risk_score += 10
            
            # Humidity effects
            if row['humidity'] > 85:
                risk_score += 40
            elif row['humidity'] > 75:
                risk_score += 25
            elif row['humidity'] > 65:
                risk_score += 10
            
            # Rainfall effects
            if row['rainfall'] > 50:
                risk_score += 35
            elif row['rainfall'] > 25:
                risk_score += 20
            elif row['rainfall'] > 10:
                risk_score += 5
            
            # Wind speed effects
            if row['wind_speed'] > 30:
                risk_score += 20
            elif row['wind_speed'] > 20:
                risk_score += 10
            
            # Pressure effects
            if row['pressure'] < 1000:
                risk_score += 15
            
            # Season-based adjustments
            if row['season'] == 3:  # Monsoon season
                risk_score += 15
            elif row['season'] == 1:  # Winter
                risk_score -= 5
            
            # Crop-specific adjustments
            crop_factors = {1: 1.2, 2: 0.8, 3: 1.1, 4: 1.0, 5: 1.3, 6: 0.9}
            risk_score *= crop_factors.get(row['crop_type'], 1.0)
            
            # Add small random noise
            risk_score += np.random.normal(0, 3)
            
            # Determine risk level
            if risk_score >= 70:
                return 2  # High
            elif risk_score >= 40:
                return 1  # Medium
            else:
                return 0  # Low
        
        # Apply risk calculation
        self.df['risk_level'] = self.df.apply(calculate_risk, axis=1)
        
        # Display risk distribution
        risk_counts = self.df['risk_level'].value_counts().sort_index()
        print(f"\nRisk level distribution:")
        print(f"   Low (0): {risk_counts.get(0, 0)} samples")
        print(f"   Medium (1): {risk_counts.get(1, 0)} samples")
        print(f"   High (2): {risk_counts.get(2, 0)} samples")

    def generate_synthetic_data(self):
        """Generate synthetic weather data for training"""
        print("Generating synthetic weather data...")
        
        n_samples = 10000
        
        # Seasons (1: Winter, 2: Spring, 3: Summer, 4: Monsoon, 5: Autumn)
        seasons = np.random.choice([1, 2, 3, 4, 5], n_samples)
        
        # Crop types (1: Rice, 2: Wheat, 3: Cotton, 4: Sugarcane, 5: Banana, 6: Coconut)
        crop_types = np.random.choice([1, 2, 3, 4, 5, 6], n_samples)
        
        # Generate weather parameters
        temperature = []
        humidity = []
        rainfall = []
        wind_speed = []
        pressure = []
        
        for season in seasons:
            if season == 1:  # Winter
                temp = np.random.normal(18, 5)
                hum = np.random.normal(60, 10)
                rain = np.random.exponential(5)
                wind = np.random.normal(10, 3)
                pres = np.random.normal(1015, 5)
            elif season == 2:  # Spring
                temp = np.random.normal(25, 4)
                hum = np.random.normal(65, 8)
                rain = np.random.exponential(15)
                wind = np.random.normal(12, 4)
                pres = np.random.normal(1012, 4)
            elif season == 3:  # Summer
                temp = np.random.normal(35, 5)
                hum = np.random.normal(55, 12)
                rain = np.random.exponential(8)
                wind = np.random.normal(15, 5)
                pres = np.random.normal(1008, 6)
            elif season == 4:  # Monsoon
                temp = np.random.normal(30, 3)
                hum = np.random.normal(85, 8)
                rain = np.random.exponential(40)
                wind = np.random.normal(20, 7)
                pres = np.random.normal(1005, 5)
            else:  # Autumn
                temp = np.random.normal(28, 4)
                hum = np.random.normal(70, 10)
                rain = np.random.exponential(20)
                wind = np.random.normal(13, 4)
                pres = np.random.normal(1010, 4)
            
            temperature.append(max(5, min(50, temp)))
            humidity.append(max(20, min(100, hum)))
            rainfall.append(max(0, min(200, rain)))
            wind_speed.append(max(0, wind))
            pressure.append(max(990, min(1030, pres)))
        
        df = pd.DataFrame({
            'season': seasons,
            'crop_type': crop_types,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'wind_speed': wind_speed,
            'pressure': pressure
        })
        
        # Calculate risk level
        def calculate_risk(row):
            risk_score = 0
            
            # Temperature effects
            if row['temperature'] > 35:
                risk_score += 30
            elif row['temperature'] > 32:
                risk_score += 20
            elif row['temperature'] < 15:
                risk_score += 25
            
            # Humidity effects
            if row['humidity'] > 85:
                risk_score += 40
            elif row['humidity'] > 75:
                risk_score += 25
            elif row['humidity'] > 65:
                risk_score += 10
            
            # Rainfall effects
            if row['rainfall'] > 50:
                risk_score += 35
            elif row['rainfall'] > 25:
                risk_score += 20
            elif row['rainfall'] > 10:
                risk_score += 5
            
            # Wind speed effects
            if row['wind_speed'] > 30:
                risk_score += 20
            elif row['wind_speed'] > 20:
                risk_score += 10
            
            # Pressure effects
            if row['pressure'] < 1000:
                risk_score += 15
            
            # Season-based adjustments
            if row['season'] == 4:  # Monsoon
                risk_score += 15
            
            # Crop-specific adjustments
            crop_factors = {1: 1.2, 2: 0.8, 3: 1.1, 4: 1.0, 5: 1.3, 6: 0.9}
            risk_score *= crop_factors.get(row['crop_type'], 1.0)
            
            # Add noise
            risk_score += np.random.normal(0, 5)
            
            # Determine risk level
            if risk_score >= 70:
                return 2  # High
            elif risk_score >= 40:
                return 1  # Medium
            else:
                return 0  # Low
        
        df['risk_level'] = df.apply(calculate_risk, axis=1)
        
        print(f"✅ Generated {len(df)} synthetic samples")
        return df

    def engineer_features(self):
        """Create additional features"""
        print("\n🔧 Engineering features...")
        
        # Verify required columns exist
        required_cols = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'pressure']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            print(f"⚠️ Missing columns: {missing_cols}")
            print("   Skipping feature engineering for these columns")
        
        # Create interaction terms only if columns exist
        if all(col in self.df.columns for col in ['temperature', 'humidity']):
            self.df['temp_humidity_interaction'] = self.df['temperature'] * self.df['humidity'] / 100
        
        if all(col in self.df.columns for col in ['temperature', 'rainfall']):
            self.df['temp_rain_interaction'] = self.df['temperature'] * self.df['rainfall'] / 50
        
        if 'humidity' in self.df.columns:
            self.df['humidity_squared'] = self.df['humidity'] ** 2 / 100
        
        if 'temperature' in self.df.columns:
            self.df['temp_squared'] = self.df['temperature'] ** 2 / 100
        
        # Create dummy variables for categorical features
        if 'season' in self.df.columns:
            season_dummies = pd.get_dummies(self.df['season'], prefix='season', drop_first=True)
        else:
            season_dummies = pd.DataFrame()
        
        if 'crop_type' in self.df.columns:
            crop_dummies = pd.get_dummies(self.df['crop_type'], prefix='crop', drop_first=True)
        else:
            crop_dummies = pd.DataFrame()
        
        # Select base feature columns that exist
        base_features = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'pressure']
        existing_base = [col for col in base_features if col in self.df.columns]
        
        # Select interaction features that exist
        interaction_features = ['temp_humidity_interaction', 'temp_rain_interaction', 
                               'humidity_squared', 'temp_squared']
        existing_interaction = [col for col in interaction_features if col in self.df.columns]
        
        # Combine all features
        feature_columns = existing_base + existing_interaction
        
        if feature_columns:
            X_base = self.df[feature_columns]
        else:
            X_base = pd.DataFrame()
        
        # Combine with dummy variables
        if not X_base.empty and not season_dummies.empty and not crop_dummies.empty:
            self.X = pd.concat([X_base, season_dummies, crop_dummies], axis=1)
        elif not X_base.empty and not season_dummies.empty:
            self.X = pd.concat([X_base, season_dummies], axis=1)
        elif not X_base.empty and not crop_dummies.empty:
            self.X = pd.concat([X_base, crop_dummies], axis=1)
        elif not X_base.empty:
            self.X = X_base
        else:
            # Fallback to using only season and crop dummies
            self.X = pd.concat([season_dummies, crop_dummies], axis=1)
        
        self.y = self.df['risk_level']
        self.feature_names = self.X.columns.tolist()
        
        print(f"✅ Created {self.X.shape[1]} features")
        print(f"   Features: {self.feature_names[:5]}... (showing first 5)")

    def split_and_scale_data(self):
        """Split data and scale features"""
        print("\n✂️ Splitting and scaling data...")
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_SEED, stratify=self.y
        )
        
        print(f"   Training set: {len(self.X_train)} samples")
        print(f"   Test set: {len(self.X_test)} samples")
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✅ Data split and scaled successfully")

    def train_models(self):
        """Train multiple models and compare"""
        print("\n🎯 Training multiple models...")
        
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=self.config.RANDOM_SEED
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=self.config.RF_N_ESTIMATORS,
                max_depth=self.config.RF_MAX_DEPTH,
                random_state=self.config.RANDOM_SEED,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=self.config.GB_N_ESTIMATORS,
                learning_rate=self.config.GB_LEARNING_RATE,
                random_state=self.config.RANDOM_SEED
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=self.config.RANDOM_SEED
            )
        }
        
        # Train and evaluate each model
        results = []
        for name, model in models.items():
            print(f"\n📌 Training {name}...")
            
            try:
                # Train
                model.fit(self.X_train_scaled, self.y_train)
                
                # Predict
                y_pred = model.predict(self.X_test_scaled)
                accuracy = accuracy_score(self.y_test, y_pred)
                
                # Cross-validation
                cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train,
                                           cv=self.config.CV_FOLDS)
                
                print(f"   Accuracy: {accuracy:.4f}")
                print(f"   CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
                
                # Store model and results
                self.models[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'predictions': y_pred
                }
                
                results.append({
                    'Model': name,
                    'Accuracy': accuracy,
                    'CV Mean': cv_scores.mean(),
                    'CV Std': cv_scores.std()
                })
            except Exception as e:
                print(f"   ❌ Error training {name}: {str(e)}")
        
        if results:
            # Create comparison dataframe
            comparison_df = pd.DataFrame(results)
            comparison_df = comparison_df.sort_values('Accuracy', ascending=False)
            
            print("\n📊 Model Performance Comparison:")
            print(comparison_df.to_string(index=False))
            
            # Select best model
            best_model_name = comparison_df.iloc[0]['Model']
            self.best_model = self.models[best_model_name]['model']
            print(f"\n🏆 Best model: {best_model_name}")

    def hyperparameter_tuning(self):
        """Tune hyperparameters of the best model"""
        if self.best_model is None:
            print("\n⚠️ No best model selected, skipping hyperparameter tuning")
            return
        
        print("\n🔧 Performing hyperparameter tuning...")
        
        # Define parameter grids
        param_grids = {
            'Random Forest': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            },
            'Gradient Boosting': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5],
                'min_samples_split': [2, 5]
            },
            'Logistic Regression': {
                'C': [0.1, 1, 10],
                'solver': ['lbfgs', 'liblinear'],
                'max_iter': [1000]
            },
            'SVM': {
                'C': [0.1, 1, 10],
                'gamma': ['scale', 'auto'],
                'kernel': ['rbf']
            }
        }
        
        # Find model type
        model_type = type(self.best_model).__name__
        for model_name in param_grids.keys():
            if model_name in model_type:
                param_grid = param_grids[model_name]
                print(f"   Tuning {model_name}...")
                
                try:
                    # Perform grid search
                    grid_search = GridSearchCV(
                        self.best_model, param_grid,
                        cv=min(self.config.CV_FOLDS, 3),  # Use smaller CV for speed
                        scoring='accuracy',
                        n_jobs=-1,
                        verbose=0
                    )
                    
                    grid_search.fit(self.X_train_scaled, self.y_train)
                    
                    print(f"\n✅ Best parameters: {grid_search.best_params_}")
                    print(f"   Best CV score: {grid_search.best_score_:.4f}")
                    
                    # Update best model
                    self.best_model = grid_search.best_estimator_
                    
                    # Evaluate on test set
                    y_pred = self.best_model.predict(self.X_test_scaled)
                    accuracy = accuracy_score(self.y_test, y_pred)
                    print(f"   Test accuracy after tuning: {accuracy:.4f}")
                    
                except Exception as e:
                    print(f"   ❌ Error during tuning: {str(e)}")
                
                break

    def evaluate_model(self):
        """Detailed model evaluation"""
        if self.best_model is None:
            print("\n⚠️ No best model selected, skipping evaluation")
            return
        
        print("\n📊 Evaluating best model...")
        
        try:
            # Make predictions
            y_pred = self.best_model.predict(self.X_test_scaled)
            
            if hasattr(self.best_model, 'predict_proba'):
                y_pred_proba = self.best_model.predict_proba(self.X_test_scaled)
            else:
                y_pred_proba = None
            
            # Accuracy
            accuracy = accuracy_score(self.y_test, y_pred)
            print(f"\n📈 Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            
            # Classification report
            print("\n📋 Classification Report:")
            target_names = ['Low Risk', 'Medium Risk', 'High Risk']
            print(classification_report(self.y_test, y_pred, target_names=target_names))
            
            # Confusion Matrix
            self.plot_confusion_matrix(self.y_test, y_pred, target_names)
            
            # ROC Curves (if probabilities available)
            if y_pred_proba is not None:
                self.plot_roc_curves(self.y_test, y_pred_proba, target_names)
            
        except Exception as e:
            print(f"   ❌ Error during evaluation: {str(e)}")

    def plot_confusion_matrix(self, y_true, y_pred, target_names):
        """Plot confusion matrix"""
        try:
            plt.figure(figsize=(8, 6))
            
            cm = confusion_matrix(y_true, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=target_names,
                       yticklabels=target_names,
                       annot_kws={'size': 14})
            
            plt.title('Confusion Matrix - Weather Risk Model', fontsize=16, fontweight='bold')
            plt.xlabel('Predicted', fontsize=12)
            plt.ylabel('Actual', fontsize=12)
            
            # Save plot
            plot_path = os.path.join(self.config.LOGS_DIR, 'confusion_matrix.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.show()
            print(f"✅ Confusion matrix saved to {plot_path}")
        except Exception as e:
            print(f"   ❌ Error plotting confusion matrix: {str(e)}")

    def plot_roc_curves(self, y_true, y_pred_proba, target_names):
        """Plot ROC curves for each class"""
        try:
            plt.figure(figsize=(10, 8))
            
            # Binarize the output
            from sklearn.preprocessing import label_binarize
            y_true_bin = label_binarize(y_true, classes=[0, 1, 2])
            
            # Compute ROC curve and ROC area for each class
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            
            colors = ['green', 'orange', 'red']
            
            for i in range(3):
                if y_pred_proba.shape[1] > i:
                    fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_pred_proba[:, i])
                    roc_auc[i] = auc(fpr[i], tpr[i])
                    
                    plt.plot(fpr[i], tpr[i], color=colors[i], lw=2,
                            label=f'{target_names[i]} (AUC = {roc_auc[i]:.2f})')
            
            plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('ROC Curves - Weather Risk Model', fontsize=16, fontweight='bold')
            plt.legend(loc="lower right", fontsize=10)
            plt.grid(True, alpha=0.3)
            
            # Save plot
            plot_path = os.path.join(self.config.LOGS_DIR, 'roc_curves.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.show()
            print(f"✅ ROC curves saved to {plot_path}")
        except Exception as e:
            print(f"   ❌ Error plotting ROC curves: {str(e)}")

    def plot_feature_importance(self):
        """Plot feature importance for tree-based models"""
        if self.best_model is None:
            return
            
        if hasattr(self.best_model, 'feature_importances_'):
            try:
                plt.figure(figsize=(12, 8))
                
                importances = self.best_model.feature_importances_
                indices = np.argsort(importances)[::-1]
                
                # Plot top 15 features
                n_features = min(15, len(importances))
                plt.bar(range(n_features), importances[indices[:n_features]])
                plt.xticks(range(n_features),
                          [self.feature_names[i] for i in indices[:n_features]],
                          rotation=45, ha='right')
                
                plt.title('Top 15 Feature Importances', fontsize=16, fontweight='bold')
                plt.xlabel('Features', fontsize=12)
                plt.ylabel('Importance', fontsize=12)
                plt.tight_layout()
                
                # Save plot
                plot_path = os.path.join(self.config.LOGS_DIR, 'feature_importance.png')
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.show()
                print(f"✅ Feature importance plot saved to {plot_path}")
                
                # Print top features
                print("\n🔝 Top 10 Most Important Features:")
                for i in range(min(10, len(importances))):
                    print(f"   {i+1}. {self.feature_names[indices[i]]}: {importances[indices[i]]:.4f}")
            except Exception as e:
                print(f"   ❌ Error plotting feature importance: {str(e)}")

    def test_realistic_scenarios(self):
        """Test model on realistic weather scenarios"""
        if self.best_model is None or self.scaler is None:
            print("\n⚠️ No best model or scaler available, skipping scenario testing")
            return
        
        print("\n🧪 Testing realistic scenarios...")
        
        scenarios = [
            {
                'name': 'Monsoon - Rice',
                'features': {
                    'temperature': 28, 'humidity': 90, 'rainfall': 45,
                    'wind_speed': 18, 'pressure': 1002, 'season': 4, 'crop_type': 1
                },
                'expected': 'HIGH'
            },
            {
                'name': 'Summer - Wheat',
                'features': {
                    'temperature': 38, 'humidity': 45, 'rainfall': 5,
                    'wind_speed': 12, 'pressure': 1005, 'season': 3, 'crop_type': 2
                },
                'expected': 'MEDIUM'
            },
            {
                'name': 'Optimal - Coconut',
                'features': {
                    'temperature': 28, 'humidity': 70, 'rainfall': 20,
                    'wind_speed': 10, 'pressure': 1012, 'season': 2, 'crop_type': 6
                },
                'expected': 'LOW'
            }
        ]
        
        risk_map = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
        
        for scenario in scenarios:
            try:
                # Create feature vector
                feat = scenario['features']
                
                # Create feature dictionary based on available features
                feat_dict = {}
                
                # Add base features
                if 'temperature' in self.feature_names:
                    feat_dict['temperature'] = feat['temperature']
                if 'humidity' in self.feature_names:
                    feat_dict['humidity'] = feat['humidity']
                if 'rainfall' in self.feature_names:
                    feat_dict['rainfall'] = feat['rainfall']
                if 'wind_speed' in self.feature_names:
                    feat_dict['wind_speed'] = feat['wind_speed']
                if 'pressure' in self.feature_names:
                    feat_dict['pressure'] = feat['pressure']
                
                # Add interaction terms if they exist in feature_names
                if 'temp_humidity_interaction' in self.feature_names:
                    feat_dict['temp_humidity_interaction'] = feat['temperature'] * feat['humidity'] / 100
                if 'temp_rain_interaction' in self.feature_names:
                    feat_dict['temp_rain_interaction'] = feat['temperature'] * feat['rainfall'] / 50
                if 'humidity_squared' in self.feature_names:
                    feat_dict['humidity_squared'] = feat['humidity'] ** 2 / 100
                if 'temp_squared' in self.feature_names:
                    feat_dict['temp_squared'] = feat['temperature'] ** 2 / 100
                
                # Add season dummies
                for i in range(2, 6):
                    col = f'season_{i}'
                    if col in self.feature_names:
                        feat_dict[col] = 1 if feat['season'] == i else 0
                
                # Add crop dummies
                for i in range(2, 7):
                    col = f'crop_{i}'
                    if col in self.feature_names:
                        feat_dict[col] = 1 if feat['crop_type'] == i else 0
                
                # Create dataframe and ensure column order
                feat_df = pd.DataFrame([feat_dict])
                feat_df = feat_df.reindex(columns=self.feature_names, fill_value=0)
                
                # Scale and predict
                feat_scaled = self.scaler.transform(feat_df)
                pred = self.best_model.predict(feat_scaled)[0]
                
                if hasattr(self.best_model, 'predict_proba'):
                    proba = self.best_model.predict_proba(feat_scaled)[0]
                else:
                    proba = [0, 0, 0]
                
                predicted_risk = risk_map[pred]
                
                print(f"\n📌 {scenario['name']}:")
                print(f"   Weather: {feat['temperature']}°C, {feat['humidity']}% humidity, {feat['rainfall']}mm rain")
                print(f"   Predicted: {predicted_risk} (Expected: {scenario['expected']})")
                if len(proba) >= 3:
                    print(f"   Confidence: Low={proba[0]:.2f}, Medium={proba[1]:.2f}, High={proba[2]:.2f}")
                
                if predicted_risk == scenario['expected']:
                    print("   ✅ Correct prediction")
                else:
                    print("   ❌ Incorrect prediction")
                    
            except Exception as e:
                print(f"\n📌 {scenario['name']}: ❌ Error - {str(e)}")

    def save_model(self):
        """Save the trained model and associated files"""
        if self.best_model is None:
            print("\n⚠️ No best model to save")
            return
            
        print("\n💾 Saving model...")
        
        try:
            # Save model
            with open(self.config.MODEL_SAVE_PATH, 'wb') as f:
                pickle.dump(self.best_model, f)
            
            # Save scaler
            with open(self.config.SCALER_SAVE_PATH, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Save feature names
            with open(self.config.FEATURES_SAVE_PATH, 'wb') as f:
                pickle.dump(self.feature_names, f)
            
            print(f"✅ Model saved to {self.config.MODEL_SAVE_PATH}")
            print(f"✅ Scaler saved to {self.config.SCALER_SAVE_PATH}")
            print(f"✅ Feature names saved to {self.config.FEATURES_SAVE_PATH}")
        except Exception as e:
            print(f"❌ Error saving model: {str(e)}")

    def save_training_summary(self):
        """Save training summary to file"""
        if self.best_model is None:
            return
            
        summary_path = os.path.join(self.config.LOGS_DIR, 'training_summary.txt')
        
        try:
            with open(summary_path, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("WEATHER RISK MODEL - TRAINING SUMMARY\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("Dataset Information:\n")
                f.write(f"  - Total samples: {len(self.df)}\n")
                f.write(f"  - Features: {self.X.shape[1] if self.X is not None else 0}\n")
                f.write(f"  - Classes: 3 (Low, Medium, High)\n\n")
                
                f.write("Training Configuration:\n")
                f.write(f"  - Test size: {self.config.TEST_SIZE}\n")
                f.write(f"  - CV folds: {self.config.CV_FOLDS}\n")
                f.write(f"  - Random seed: {self.config.RANDOM_SEED}\n\n")
                
                f.write("Model Performance:\n")
                y_pred = self.best_model.predict(self.X_test_scaled)
                accuracy = accuracy_score(self.y_test, y_pred)
                f.write(f"  - Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n\n")
                
                f.write("Classification Report:\n")
                target_names = ['Low Risk', 'Medium Risk', 'High Risk']
                report = classification_report(self.y_test, y_pred,
                                             target_names=target_names,
                                             output_dict=True)
                
                for class_name in target_names:
                    if class_name in report:
                        metrics = report[class_name]
                        f.write(f"\n  {class_name}:\n")
                        f.write(f"    Precision: {metrics['precision']:.4f}\n")
                        f.write(f"    Recall: {metrics['recall']:.4f}\n")
                        f.write(f"    F1-Score: {metrics['f1-score']:.4f}\n")
            
            print(f"✅ Training summary saved to {summary_path}")
        except Exception as e:
            print(f"❌ Error saving training summary: {str(e)}")

    def run(self):
        """Run the complete training pipeline"""
        print("=" * 60)
        print("🌤️ WEATHER RISK MODEL TRAINING PIPELINE")
        print("=" * 60)
        
        # Step 1: Load and prepare data
        self.load_and_prepare_data()
        
        # Step 2: Engineer features
        self.engineer_features()
        
        # Step 3: Split and scale data
        self.split_and_scale_data()
        
        # Step 4: Train models
        self.train_models()
        
        # Step 5: Hyperparameter tuning (if models were trained)
        if self.models:
            self.hyperparameter_tuning()
        
        # Step 6: Evaluate model (if best model exists)
        if self.best_model:
            self.evaluate_model()
            
            # Step 7: Feature importance (if applicable)
            self.plot_feature_importance()
            
            # Step 8: Test realistic scenarios
            self.test_realistic_scenarios()
            
            # Step 9: Save model
            self.save_model()
            
            # Step 10: Save training summary
            self.save_training_summary()
        else:
            print("\n❌ No models were successfully trained. Please check the data and try again.")
        
        print("\n" + "=" * 60)
        print("✅ TRAINING PIPELINE COMPLETED!")
        print("=" * 60)

if __name__ == "__main__":
    # Run training
    trainer = WeatherModelTrainer()
    trainer.run()