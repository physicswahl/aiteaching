from manim import *
import numpy as np
import tensorflow as tf
from tensorflow import keras


class NeuralNetworkVisualization(Scene):
    def construct(self):
        # Load the trained model
        model = keras.models.load_model('species_classifier.keras')
        
        # Tasmanian Devil data
        # Raw values: pop_size=2500, decline_rate=50.0, fragmented=Yes(1)
        animal_name = "Tasmanian Devil"
        pop_size_raw = 2500
        decline_rate_raw = 50.0
        fragmented_raw = 1  # Yes = 1
        
        # Apply same transformations as in training
        # Log transform and normalization (simplified for visualization)
        pop_size_processed = np.log1p(pop_size_raw)
        
        # Normalize (approximate values for visualization)
        pop_size_norm = (pop_size_processed - 7.5) / 2.0  # Approximate normalization
        decline_rate_norm = (decline_rate_raw - 50) / 25.0
        fragmented_norm = fragmented_raw
        
        input_values = np.array([[pop_size_norm, decline_rate_norm, fragmented_norm]])
        
        # Get predictions from each layer
        layer_outputs = []
        temp_input = input_values
        for layer in model.layers:
            if 'dropout' not in layer.name:
                temp_model = keras.Model(inputs=model.input, outputs=layer.output)
                output = temp_model.predict(input_values, verbose=0)
                layer_outputs.append(output[0])
        
        # Title
        title = Text("Neural Network: Predicting Endangered Status", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Animal info
        animal_text = Text(f"Species: {animal_name}", font_size=32, color=YELLOW)
        animal_text.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(animal_text))
        self.wait(0.5)
        
        # Create network structure
        # Input layer (3 neurons)
        input_layer = self.create_layer(3, "Input Layer", LEFT * 5)
        
        # Hidden layer 1 (16 neurons - show 8 for visualization)
        hidden1_layer = self.create_layer(8, "Hidden Layer 1\n(16 neurons)", LEFT * 1.5, scale=0.7)
        
        # Hidden layer 2 (8 neurons - show 6 for visualization)
        hidden2_layer = self.create_layer(6, "Hidden Layer 2\n(8 neurons)", RIGHT * 2, scale=0.7)
        
        # Output layer (1 neuron)
        output_layer = self.create_layer(1, "Output Layer", RIGHT * 5.5)
        
        # Input labels
        input_labels = [
            Text(f"Pop Size\n{pop_size_raw:,}", font_size=18, color=BLUE),
            Text(f"Decline Rate\n{decline_rate_raw}%", font_size=18, color=BLUE),
            Text(f"Fragmented\n{'Yes' if fragmented_raw == 1 else 'No'}", font_size=18, color=BLUE)
        ]
        
        for i, label in enumerate(input_labels):
            label.next_to(input_layer[i], LEFT, buff=0.3)
        
        # Draw network
        self.play(
            *[Create(neuron) for neuron in input_layer],
            *[Write(label) for label in input_labels]
        )
        self.wait(0.3)
        
        self.play(
            *[Create(neuron) for neuron in hidden1_layer],
        )
        self.wait(0.3)
        
        self.play(
            *[Create(neuron) for neuron in hidden2_layer],
        )
        self.wait(0.3)
        
        self.play(
            *[Create(neuron) for neuron in output_layer],
        )
        self.wait(0.5)
        
        # Create connections with animations
        connections = []
        
        # Input to Hidden1
        for input_neuron in input_layer:
            for hidden_neuron in hidden1_layer:
                line = Line(
                    input_neuron.get_center(),
                    hidden_neuron.get_center(),
                    stroke_width=0.5,
                    color=GRAY
                )
                connections.append(line)
        
        self.play(*[Create(conn) for conn in connections], run_time=1)
        self.wait(0.3)
        
        # Hidden1 to Hidden2
        connections2 = []
        for h1_neuron in hidden1_layer:
            for h2_neuron in hidden2_layer:
                line = Line(
                    h1_neuron.get_center(),
                    h2_neuron.get_center(),
                    stroke_width=0.5,
                    color=GRAY
                )
                connections2.append(line)
        
        self.play(*[Create(conn) for conn in connections2], run_time=1)
        self.wait(0.3)
        
        # Hidden2 to Output
        connections3 = []
        for h2_neuron in hidden2_layer:
            for out_neuron in output_layer:
                line = Line(
                    h2_neuron.get_center(),
                    out_neuron.get_center(),
                    stroke_width=0.5,
                    color=GRAY
                )
                connections3.append(line)
        
        self.play(*[Create(conn) for conn in connections3], run_time=1)
        self.wait(1)
        
        # Animate data flow
        # Input activation
        self.play(*[neuron.animate.set_fill(GREEN, opacity=0.8) for neuron in input_layer])
        self.wait(0.5)
        
        # Flow to hidden1
        dots1 = []
        for input_neuron in input_layer:
            for hidden_neuron in hidden1_layer[:5]:  # Animate to first 5 for clarity
                dot = Dot(input_neuron.get_center(), color=YELLOW, radius=0.05)
                dots1.append((dot, hidden_neuron.get_center()))
        
        self.play(*[FadeIn(dot) for dot, _ in dots1])
        self.play(*[dot.animate.move_to(target) for dot, target in dots1], run_time=1)
        self.play(*[FadeOut(dot) for dot, _ in dots1])
        
        # Hidden1 activation
        self.play(*[neuron.animate.set_fill(ORANGE, opacity=0.7) for neuron in hidden1_layer])
        self.wait(0.5)
        
        # Flow to hidden2
        dots2 = []
        for h1_neuron in hidden1_layer[:4]:
            for h2_neuron in hidden2_layer[:4]:
                dot = Dot(h1_neuron.get_center(), color=YELLOW, radius=0.05)
                dots2.append((dot, h2_neuron.get_center()))
        
        self.play(*[FadeIn(dot) for dot, _ in dots2[:12]])  # Limit animations
        self.play(*[dot.animate.move_to(target) for dot, target in dots2[:12]], run_time=1)
        self.play(*[FadeOut(dot) for dot, _ in dots2[:12]])
        
        # Hidden2 activation
        self.play(*[neuron.animate.set_fill(RED, opacity=0.7) for neuron in hidden2_layer])
        self.wait(0.5)
        
        # Flow to output
        dots3 = []
        for h2_neuron in hidden2_layer:
            dot = Dot(h2_neuron.get_center(), color=YELLOW, radius=0.05)
            dots3.append((dot, output_layer[0].get_center()))
        
        self.play(*[FadeIn(dot) for dot, _ in dots3])
        self.play(*[dot.animate.move_to(target) for dot, target in dots3], run_time=1)
        self.play(*[FadeOut(dot) for dot, _ in dots3])
        
        # Output activation
        prediction = model.predict(input_values, verbose=0)[0][0]
        
        self.play(output_layer[0].animate.set_fill(YELLOW, opacity=1))
        self.wait(0.5)
        
        # Show prediction result
        result_text = Text(
            f"Prediction: {'Threatened' if prediction > 0.5 else 'Not Threatened'}",
            font_size=36,
            color=RED if prediction > 0.5 else GREEN
        )
        result_text.next_to(output_layer[0], RIGHT, buff=0.5)
        
        confidence_text = Text(
            f"Confidence: {prediction:.1%}",
            font_size=28,
            color=YELLOW
        )
        confidence_text.next_to(result_text, DOWN, buff=0.3)
        
        self.play(Write(result_text))
        self.play(Write(confidence_text))
        self.wait(2)
        
        # Highlight the result
        result_box = SurroundingRectangle(
            VGroup(result_text, confidence_text),
            color=YELLOW,
            buff=0.2
        )
        self.play(Create(result_box))
        self.wait(2)
    
    def create_layer(self, num_neurons, label, position, scale=1.0):
        """Create a layer of neurons"""
        neurons = VGroup()
        spacing = 0.6 * scale
        total_height = (num_neurons - 1) * spacing
        start_y = total_height / 2
        
        for i in range(num_neurons):
            neuron = Circle(radius=0.2 * scale, color=BLUE, fill_opacity=0.3)
            neuron.move_to(position + UP * (start_y - i * spacing))
            neurons.add(neuron)
        
        # Add label
        layer_label = Text(label, font_size=20 * scale)
        layer_label.next_to(neurons, DOWN, buff=0.3)
        self.add(layer_label)
        
        return neurons
