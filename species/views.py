from django.shortcuts import render
from django.http import JsonResponse
from .models import Species
import numpy as np
import os

# Cache the model and scalers to avoid reloading on every request
_cached_model = None
_cached_scaler1 = None
_cached_scaler2 = None

def load_model_and_scalers():
    """Load model and scalers once and cache them"""
    global _cached_model, _cached_scaler1, _cached_scaler2
    
    if _cached_model is None:
        import tensorflow as tf
        from tensorflow import keras
        import pickle
        
        model_path = 'species_classifier.keras'
        if not os.path.exists(model_path):
            raise FileNotFoundError('Model not found. Please train the model first.')
        
        _cached_model = keras.models.load_model(model_path)
        
        # Load scalers
        try:
            with open('species_scaler1.pkl', 'rb') as f:
                _cached_scaler1 = pickle.load(f)
            with open('species_scaler2.pkl', 'rb') as f:
                _cached_scaler2 = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError('Scalers not found. Please retrain the model.')
    
    return _cached_model, _cached_scaler1, _cached_scaler2


def get_full_status_name(status_code):
    """Convert status code to full name"""
    status_map = {
        'CR': 'Critically Endangered',
        'EN': 'Endangered',
        'VU': 'Vulnerable',
        'NT': 'Near Threatened',
        'LC': 'Least Concern'
    }
    return status_map.get(status_code, status_code)


def network_visualization(request):
    """Display the neural network visualization page"""
    # Get species with complete data
    all_species = Species.objects.exclude(
        pop_size__isnull=True
    ).exclude(
        decline_rate__isnull=True
    ).exclude(
        fragmented__isnull=True
    ).order_by('animal_name')
    
    # Filter out species with unparseable population data
    species_list = []
    for species in all_species:
        if parse_population(species.pop_size) is not None:
            species_list.append(species)
    
    context = {
        'species_list': species_list,
    }
    return render(request, 'species/network_visualization_new.html', context)


def predict_species(request, species_id):
    """API endpoint to get prediction for a specific species"""
    try:
        import tensorflow as tf
        
        species = Species.objects.get(id=species_id)
        
        # Parse population size
        pop_size = parse_population(species.pop_size)
        if pop_size is None:
            return JsonResponse({'error': 'Invalid population data'}, status=400)
        
        # Get other features
        decline_rate = species.decline_rate
        fragmented = 1 if species.fragmented == 'Yes' else 0
        
        # Load cached model and scalers
        try:
            model, scaler1, scaler2 = load_model_and_scalers()
        except FileNotFoundError as e:
            return JsonResponse({'error': str(e)}, status=404)
        
        # Prepare input - must match training process exactly
        input_raw = np.array([[pop_size, decline_rate, fragmented]])
        
        # Step 1: Apply first scaler
        input_scaled = scaler1.transform(input_raw)
        
        # Step 2: Log transform population (first column)
        input_scaled[:, 0] = np.log1p(np.abs(input_raw[:, 0]))
        
        # Step 3: Apply second scaler
        input_final = scaler2.transform(input_scaled)
        
        # Get prediction (now returns 5 probabilities)
        predictions = model.predict(input_final, verbose=0)[0]
        
        # Map to status names
        status_names = ['CR', 'EN', 'VU', 'NT', 'LC']
        predicted_class_idx = np.argmax(predictions)
        predicted_status = status_names[predicted_class_idx]
        confidence = float(predictions[predicted_class_idx])
        
        # Create probabilities dictionary
        class_probabilities = {status_names[i]: float(predictions[i]) for i in range(5)}

        # Compute layer outputs by running a manual forward pass through layers
        # This avoids relying on layer tensors like model.input which may be undefined
        layer_outputs = []
        try:
            import tensorflow as tf
            x = tf.convert_to_tensor(input_final, dtype=tf.float32)
            
            # Add input layer activations
            layer_outputs.append({
                'layer_name': 'input',
                'values': x.numpy().flatten().tolist()
            })
            
            for layer in model.layers:
                # call the layer; for Dropout, set training=False
                x = layer(x, training=False)
                if 'dropout' in layer.name:
                    # skip recording dropout activations
                    continue
                # extract numpy values
                try:
                    vals = x.numpy().flatten().tolist()
                except Exception:
                    # fallback to converting via tf.make_ndarray
                    vals = tf.make_ndarray(x).flatten().tolist()
                layer_outputs.append({
                    'layer_name': layer.name,
                    'values': vals
                })
        except Exception as e:
            # If something goes wrong computing intermediates, continue without them
            layer_outputs = []
        
        return JsonResponse({
            'species_name': species.animal_name,
            'actual_status': species.get_status_display(),
            'prediction': predicted_status,
            'full_status': get_full_status_name(predicted_status),
            'confidence': confidence,
            'features': {
                'population': pop_size,
                'decline_rate': decline_rate,
                'fragmented': fragmented == 1
            },
            'class_probabilities': class_probabilities,
            'layer_outputs': layer_outputs
        })
        
    except Species.DoesNotExist:
        return JsonResponse({'error': 'Species not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def parse_population(pop_str):
    """Convert population string to numeric value"""
    if not pop_str or str(pop_str).strip().lower() in ['unknown', 'nan', 'declining', 'increasing', 'varies']:
        return None

    import re
    s = str(pop_str).lower()
    
    # Handle special cases
    if 'million' in s:
        # Extract number before 'million'
        match = re.search(r'(\d+(?:\.\d+)?)', s)
        if match:
            return float(match.group(1)) * 1000000
        # If just "millions" with no number, use a default
        return 2000000.0
    
    if 'thousand' in s:
        # Extract number before 'thousand'
        match = re.search(r'(\d+(?:\.\d+)?)', s)
        if match:
            return float(match.group(1)) * 1000
        # If just "few thousand" with no number, use a conservative estimate
        return 5000.0
    
    # Remove common words and punctuation
    s = s.replace(',', '')
    s = s.replace('~', '')
    s = s.replace('+', '')
    s = s.replace('>', '')
    s = s.replace('<', '')
    s = s.replace('over', '')
    s = s.replace('more than', '')
    s = s.replace('approximately', '')

    # If it's a range like '2,500-3,000' or '2500 - 3000', take the average
    range_match = re.search(r"(\d+[\d,]*)\s*-\s*(\d+[\d,]*)", s)
    if range_match:
        a = float(range_match.group(1).replace(',', ''))
        b = float(range_match.group(2).replace(',', ''))
        return (a + b) / 2.0

    # Find all numbers in the string
    nums = re.findall(r"\d+[\d,]*", s)
    if not nums:
        return None

    # Convert found numbers to floats and return the largest (conservative)
    try:
        vals = [float(n.replace(',', '')) for n in nums]
        return max(vals)
    except:
        return None

