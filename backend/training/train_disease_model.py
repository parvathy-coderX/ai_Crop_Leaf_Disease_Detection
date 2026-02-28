"""
Disease Detection Model Training Script
Trains a CNN model for crop disease classification
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from datetime import datetime

# Configuration
class Config:
    # Paths
    DATA_DIR = '../../datasets/crop_images'
    MODEL_SAVE_PATH = '../models/disease_model.h5'
    CLASS_NAMES_PATH = '../models/disease_classes.pkl'
    LOGS_DIR = '../logs/disease_training'
    
    # Training parameters
    IMG_SIZE = 128
    BATCH_SIZE = 8
    EPOCHS = 3
    LEARNING_RATE = 0.001
    VALIDATION_SPLIT = 0.2
    RANDOM_SEED = 42
    
    # Data augmentation
    ROTATION_RANGE = 20
    ZOOM_RANGE = 0.2
    HORIZONTAL_FLIP = True
    VERTICAL_FLIP = False
    BRIGHTNESS_RANGE = (0.8, 1.2)
    
    # Model parameters
    DROPOUT_RATE = 0.5
    DENSE_UNITS = 256

class DiseaseModelTrainer:
    def __init__(self):
        """Initialize the trainer"""
        self.config = Config()
        self.model = None
        self.train_generator = None
        self.val_generator = None
        self.class_names = []
        self.history = None
        
        # Create directories
        os.makedirs(os.path.dirname(self.config.MODEL_SAVE_PATH), exist_ok=True)
        os.makedirs(self.config.LOGS_DIR, exist_ok=True)
        
        # Set random seeds for reproducibility
        np.random.seed(self.config.RANDOM_SEED)
        tf.random.set_seed(self.config.RANDOM_SEED)
        
        print(f"✅ Trainer initialized with config:")
        print(f"   - Data directory: {self.config.DATA_DIR}")
        print(f"   - Image size: {self.config.IMG_SIZE}x{self.config.IMG_SIZE}")
        print(f"   - Batch size: {self.config.BATCH_SIZE}")
        print(f"   - Epochs: {self.config.EPOCHS}")

    def prepare_data(self):
        """Prepare and augment the dataset"""
        print("\n📁 Preparing dataset...")
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=self.config.ROTATION_RANGE,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=self.config.ZOOM_RANGE,
            horizontal_flip=self.config.HORIZONTAL_FLIP,
            vertical_flip=self.config.VERTICAL_FLIP,
            brightness_range=self.config.BRIGHTNESS_RANGE,
            fill_mode='nearest',
            validation_split=self.config.VALIDATION_SPLIT
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=self.config.VALIDATION_SPLIT
        )
        
        # Load training data
        self.train_generator = train_datagen.flow_from_directory(
            self.config.DATA_DIR,
            target_size=(self.config.IMG_SIZE, self.config.IMG_SIZE),
            batch_size=self.config.BATCH_SIZE,
            class_mode='categorical',
            subset='training',
            shuffle=True,
            seed=self.config.RANDOM_SEED
        )
        
        # Load validation data
        self.val_generator = val_datagen.flow_from_directory(
            self.config.DATA_DIR,
            target_size=(self.config.IMG_SIZE, self.config.IMG_SIZE),
            batch_size=self.config.BATCH_SIZE,
            class_mode='categorical',
            subset='validation',
            shuffle=False,
            seed=self.config.RANDOM_SEED
        )
        
        # Get class names
        self.class_names = list(self.train_generator.class_indices.keys())
        print(f"\n✅ Found {len(self.class_names)} classes:")
        for i, class_name in enumerate(self.class_names):
            print(f"   {i}: {class_name}")
        
        print(f"\n📊 Dataset statistics:")
        print(f"   Training samples: {self.train_generator.samples}")
        print(f"   Validation samples: {self.val_generator.samples}")
        
        # Save class names
        with open(self.config.CLASS_NAMES_PATH, 'wb') as f:
            pickle.dump(self.class_names, f)
        print(f"✅ Class names saved to {self.config.CLASS_NAMES_PATH}")

    def build_model(self):
        """Build the CNN model using transfer learning"""
        print("\n🏗️ Building model...")
        
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            input_shape=(self.config.IMG_SIZE, self.config.IMG_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build the model
        inputs = keras.Input(shape=(self.config.IMG_SIZE, self.config.IMG_SIZE, 3))
        
        # Data augmentation
        x = layers.RandomFlip("horizontal")(inputs)
        x = layers.RandomRotation(0.1)(x)
        x = layers.RandomZoom(0.1)(x)
        
        # Pre-trained base
        x = base_model(x, training=False)
        
        # Global average pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers
        x = layers.Dense(self.config.DENSE_UNITS, activation='relu')(x)
        x = layers.Dropout(self.config.DROPOUT_RATE)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(self.config.DROPOUT_RATE * 0.5)(x)
        
        # Output layer
        outputs = layers.Dense(len(self.class_names), activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        
        print(f"✅ Model built successfully:")
        print(f"   - Total parameters: {self.model.count_params():,}")
        print(f"   - Trainable parameters: {sum([w.shape.num_elements() for w in self.model.trainable_weights]):,}")
        print(f"   - Output classes: {len(self.class_names)}")

    def train_model(self):
        """Train the model"""
        print("\n🎯 Starting training...")
        
        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=self.config.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Callbacks
        callbacks = [
            ModelCheckpoint(
                self.config.MODEL_SAVE_PATH,
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train the model
        start_time = datetime.now()
        self.history = self.model.fit(
            self.train_generator,
            validation_data=self.val_generator,
            epochs=self.config.EPOCHS,
            callbacks=callbacks,
            verbose=1
        )
        training_time = datetime.now() - start_time
        
        print(f"\n✅ Training completed in {training_time}")
        print(f"   Best validation accuracy: {max(self.history.history['val_accuracy']):.4f}")

    def evaluate_model(self):
        """Evaluate the model and plot results"""
        print("\n📊 Evaluating model...")
        
        # Load best model
        self.model = keras.models.load_model(self.config.MODEL_SAVE_PATH)
        
        # Evaluate on validation set
        val_loss, val_accuracy = self.model.evaluate(self.val_generator)
        print(f"\n📈 Validation Results:")
        print(f"   Loss: {val_loss:.4f}")
        print(f"   Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
        
        # Get predictions
        self.val_generator.reset()
        predictions = self.model.predict(self.val_generator)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = self.val_generator.classes
        
        # Classification report
        print("\n📋 Classification Report:")
        report = classification_report(
            true_classes,
            predicted_classes,
            target_names=self.class_names,
            output_dict=True
        )
        
        for class_name, metrics in report.items():
            if class_name not in ['accuracy', 'macro avg', 'weighted avg']:
                print(f"\n   {class_name}:")
                print(f"      Precision: {metrics['precision']:.4f}")
                print(f"      Recall: {metrics['recall']:.4f}")
                print(f"      F1-Score: {metrics['f1-score']:.4f}")
        
        # Plot confusion matrix
        self.plot_confusion_matrix(true_classes, predicted_classes)
        
        # Plot training history
        self.plot_training_history()

    def plot_confusion_matrix(self, true_classes, predicted_classes):
        """Plot confusion matrix"""
        plt.figure(figsize=(12, 10))
        
        cm = confusion_matrix(true_classes, predicted_classes)
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            annot_kws={'size': 8}
        )
        
        plt.title('Confusion Matrix - Disease Detection Model', fontsize=16, fontweight='bold')
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('Actual', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(self.config.LOGS_DIR, 'confusion_matrix.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Confusion matrix saved to {plot_path}")

    def plot_training_history(self):
        """Plot training history"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Train', linewidth=2)
        ax1.plot(self.history.history['val_accuracy'], label='Validation', linewidth=2)
        ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Epoch', fontsize=12)
        ax1.set_ylabel('Accuracy', fontsize=12)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Train', linewidth=2)
        ax2.plot(self.history.history['val_loss'], label='Validation', linewidth=2)
        ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Epoch', fontsize=12)
        ax2.set_ylabel('Loss', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(self.config.LOGS_DIR, 'training_history.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Training history saved to {plot_path}")

    def test_prediction(self):
        """Test the model with a sample prediction"""
        print("\n🧪 Testing sample prediction...")
        
        # Get a sample from validation set
        self.val_generator.reset()
        x_batch, y_batch = next(self.val_generator)
        
        # Make prediction
        predictions = self.model.predict(x_batch[:5])
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y_batch[:5], axis=1)
        
        print("\n📝 Sample predictions:")
        for i in range(min(5, len(predictions))):
            print(f"\n   Image {i+1}:")
            print(f"      True class: {self.class_names[true_classes[i]]}")
            print(f"      Predicted: {self.class_names[predicted_classes[i]]}")
            print(f"      Confidence: {predictions[i][predicted_classes[i]]:.4f} ({predictions[i][predicted_classes[i]]*100:.2f}%)")

    def fine_tune_model(self):
        """Fine-tune the model by unfreezing some layers"""
        print("\n🔧 Fine-tuning model...")
        
        # Unfreeze the top layers of the base model
        self.model.trainable = True
        
        # Fine-tune from this layer onwards
        fine_tune_at = 100
        
        # Freeze all the layers before fine_tune_at
        for layer in self.model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=Adam(learning_rate=self.config.LEARNING_RATE / 10),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"✅ Model prepared for fine-tuning")
        print(f"   Trainable layers: {sum([layer.trainable for layer in self.model.layers])}")
        
        # Continue training
        fine_tune_epochs = 20
        total_epochs = self.config.EPOCHS + fine_tune_epochs
        
        callbacks = [
            ModelCheckpoint(
                self.config.MODEL_SAVE_PATH.replace('.h5', '_finetuned.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            )
        ]
        
        history_fine = self.model.fit(
            self.train_generator,
            validation_data=self.val_generator,
            epochs=fine_tune_epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # Append to history
        for key in self.history.history.keys():
            self.history.history[key].extend(history_fine.history[key])
        
        print("✅ Fine-tuning completed")

    def save_model_summary(self):
        """Save model summary and configuration"""
        summary_path = os.path.join(self.config.LOGS_DIR, 'model_summary.txt')
        
        with open(summary_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("DISEASE DETECTION MODEL SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Configuration:\n")
            f.write(f"  - Image Size: {self.config.IMG_SIZE}x{self.config.IMG_SIZE}\n")
            f.write(f"  - Batch Size: {self.config.BATCH_SIZE}\n")
            f.write(f"  - Epochs: {self.config.EPOCHS}\n")
            f.write(f"  - Learning Rate: {self.config.LEARNING_RATE}\n")
            f.write(f"  - Dropout Rate: {self.config.DROPOUT_RATE}\n\n")
            
            f.write(f"Dataset:\n")
            f.write(f"  - Classes: {len(self.class_names)}\n")
            for i, class_name in enumerate(self.class_names):
                f.write(f"      {i}: {class_name}\n")
            f.write(f"  - Training samples: {self.train_generator.samples}\n")
            f.write(f"  - Validation samples: {self.val_generator.samples}\n\n")
            
            f.write(f"Model Architecture:\n")
            self.model.summary(print_fn=lambda x: f.write(x + '\n'))
            
            f.write(f"\nFinal Performance:\n")
            val_loss, val_accuracy = self.model.evaluate(self.val_generator, verbose=0)
            f.write(f"  - Validation Loss: {val_loss:.4f}\n")
            f.write(f"  - Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)\n")
        
        print(f"✅ Model summary saved to {summary_path}")

    def run(self):
        """Run the complete training pipeline"""
        print("=" * 60)
        print("🌾 DISEASE DETECTION MODEL TRAINING PIPELINE")
        print("=" * 60)
        
        # Step 1: Prepare data
        self.prepare_data()
        
        # Step 2: Build model
        self.build_model()
        
        # Step 3: Train model
        self.train_model()
        
        # Step 4: Evaluate model
        self.evaluate_model()
        
        # Step 5: Test predictions
        self.test_prediction()
        
        # Step 6: Save model summary
        self.save_model_summary()
        
        print("\n" + "=" * 60)
        print("✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📁 Model saved to: {self.config.MODEL_SAVE_PATH}")
        print(f"📁 Class names saved to: {self.config.CLASS_NAMES_PATH}")
        print(f"📁 Logs saved to: {self.config.LOGS_DIR}")

if __name__ == "__main__":
    # Check for GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPU detected: {gpus}")
        # Enable memory growth
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    else:
        print("⚠️ No GPU detected, training on CPU")
    
    # Run training
    trainer = DiseaseModelTrainer()
    trainer.run()