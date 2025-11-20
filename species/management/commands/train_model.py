import os
import re
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from species.models import Species
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class Command(BaseCommand):
    help = 'Train a neural network to predict endangered status'

    def parse_population(self, pop_str):
        """Convert population string to numeric value"""
        if pd.isna(pop_str) or pop_str == 'Unknown':
            return np.nan
        
        # Remove commas
        pop_str = str(pop_str).replace(',', '')
        
        # Handle ranges (take average)
        if '-' in pop_str:
            parts = pop_str.split('-')
            try:
                return (float(parts[0].replace('~', '')) + float(parts[1].replace('~', ''))) / 2
            except:
                return np.nan
        
        # Handle approximate values
        pop_str = pop_str.replace('~', '').replace('<', '').replace('>', '')
        
        try:
            return float(pop_str)
        except:
            return np.nan

    def handle(self, *args, **options):
        self.stdout.write('Loading species data...')
        
        # Get all species data
        species = Species.objects.all().order_by('id')
        data = []
        
        for s in species:
            data.append({
                'animal_name': s.animal_name,
                'status': s.status,
                'pop_size': s.pop_size,
                'decline_rate': s.decline_rate,
                'fragmented': s.fragmented
            })
        
        df = pd.DataFrame(data)
        self.stdout.write(f'Total species: {len(df)}')
        
        # Convert pop_size to numeric
        df['pop_size_numeric'] = df['pop_size'].apply(self.parse_population)
        
        # Convert fragmented to binary (Yes=1, No=0)
        df['fragmented_binary'] = df['fragmented'].map({'Yes': 1, 'No': 0})
        
        # Drop rows with missing values in our features
        df_clean = df.dropna(subset=['pop_size_numeric', 'decline_rate', 'fragmented_binary'])
        
        self.stdout.write(f'Species with complete data: {len(df_clean)}')
        
        # Filter to only include the 5 main statuses
        df_clean = df_clean[df_clean['status'].isin(['CR', 'EN', 'VU', 'NT', 'LC'])]
        self.stdout.write(f'Species with CR/EN/VU/NT/LC status: {len(df_clean)}')
        
        # Create multi-class target variable
        status_map = {'CR': 0, 'EN': 1, 'VU': 2, 'NT': 3, 'LC': 4}
        df_clean['status_encoded'] = df_clean['status'].map(status_map)
        
        self.stdout.write(f"\nStatus distribution:")
        for status, code in status_map.items():
            count = (df_clean['status_encoded'] == code).sum()
            self.stdout.write(f"  {status}: {count}")
        
        # Prepare features
        X = df_clean[['pop_size_numeric', 'decline_rate', 'fragmented_binary']].values
        y = df_clean['status_encoded'].values
        
        # Convert to one-hot encoding for multi-class
        y_onehot = keras.utils.to_categorical(y, num_classes=5)
        
        # Split data: first 55 for training, rest for testing
        if len(df_clean) < 55:
            self.stdout.write(self.style.WARNING(
                f'Only {len(df_clean)} species available. Using first {int(len(df_clean)*0.8)} for training.'
            ))
            train_size = int(len(df_clean) * 0.8)
        else:
            train_size = 55
        
        X_train = X[:train_size]
        y_train = y_onehot[:train_size]
        X_test = X[train_size:]
        y_test = y_onehot[train_size:]
        y_test_labels = y[train_size:]  # Keep original labels for display
        
        # Store test animal names for later
        test_animals = df_clean.iloc[train_size:]['animal_name'].values
        test_statuses = df_clean.iloc[train_size:]['status'].values
        
        self.stdout.write(f'\nTraining set size: {len(X_train)}')
        self.stdout.write(f'Test set size: {len(X_test)}')
        
        # Normalize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Log transform population size (after scaling) to handle large range
        # Take log of absolute values to handle the scale difference
        X_train_scaled[:, 0] = np.log1p(np.abs(X_train[:, 0]))
        X_test_scaled[:, 0] = np.log1p(np.abs(X_test[:, 0]))
        
        # Re-scale after log transform
        scaler2 = StandardScaler()
        X_train_scaled = scaler2.fit_transform(X_train_scaled)
        X_test_scaled = scaler2.transform(X_test_scaled)
        
        # Build neural network for multi-class classification
        self.stdout.write('\nBuilding neural network...')
        model = keras.Sequential([
            layers.Input(shape=(3,)),
            layers.Dense(16, activation='relu'),
            layers.Dense(8, activation='relu'),
            layers.Dense(5, activation='softmax')  # 5 output neurons with softmax
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.stdout.write('\nModel architecture:')
        model.summary(print_fn=lambda x: self.stdout.write(x))
        
        # Train model
        self.stdout.write('\nTraining model...')
        history = model.fit(
            X_train_scaled, y_train,
            epochs=500,
            batch_size=4,
            validation_split=0.15,
            verbose=0
        )
        
        # Evaluate on training set
        train_loss, train_acc = model.evaluate(X_train_scaled, y_train, verbose=0)
        self.stdout.write(f'\nTraining accuracy: {train_acc:.4f}')
        
        # Evaluate on test set
        if len(X_test) > 0:
            test_loss, test_acc = model.evaluate(X_test_scaled, y_test, verbose=0)
            self.stdout.write(f'Test accuracy (out-of-sample): {test_acc:.4f}')
            
            # Make predictions
            predictions = model.predict(X_test_scaled, verbose=0)
            predicted_classes = np.argmax(predictions, axis=1)
            
            status_names = ['CR', 'EN', 'VU', 'NT', 'LC']
            
            self.stdout.write('\n' + '='*80)
            self.stdout.write('OUT-OF-SAMPLE PREDICTIONS:')
            self.stdout.write('='*80)
            
            for i, animal in enumerate(test_animals):
                actual_status = test_statuses[i]
                predicted_status = status_names[predicted_classes[i]]
                confidence = predictions[i][predicted_classes[i]]
                correct = '✓' if predicted_status == actual_status else '✗'
                
                # Show all class probabilities
                probs = ' | '.join([f'{status}: {predictions[i][j]:.1%}' for j, status in enumerate(status_names)])
                
                self.stdout.write(
                    f'{correct} {animal:40s} | Actual: {actual_status:2s} | '
                    f'Predicted: {predicted_status:2s} ({confidence:.1%})'
                )
                self.stdout.write(f'   Probabilities: {probs}')
        else:
            self.stdout.write(self.style.WARNING('No test data available'))
        
        # Save model
        model_path = 'species_classifier.keras'
        model.save(model_path)
        self.stdout.write(f'\nModel saved to {model_path}')
        
        # Save scalers for prediction
        import pickle
        with open('species_scaler1.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        with open('species_scaler2.pkl', 'wb') as f:
            pickle.dump(scaler2, f)
        self.stdout.write('Scalers saved to species_scaler1.pkl and species_scaler2.pkl')
        
        # Show feature importance (weights from first layer)
        self.stdout.write('\n' + '='*80)
        self.stdout.write('FEATURE ANALYSIS:')
        self.stdout.write('='*80)
        weights = model.layers[0].get_weights()[0]
        features = ['Population Size', 'Decline Rate', 'Fragmented']
        
        avg_weights = np.abs(weights).mean(axis=1)
        for feat, weight in zip(features, avg_weights):
            self.stdout.write(f'{feat:20s}: {weight:.4f}')
