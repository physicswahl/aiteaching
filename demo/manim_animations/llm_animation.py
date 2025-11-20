from manim import *
import numpy as np

class LLMAnimation(Scene):
    def construct(self):
        # Define positions
        input_y_positions = [1.5, 0.5]
        hidden_y_positions = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]
        output_y_positions = [1.5, 0.5, -0.5]
        
        input_x = -4
        hidden_x = 0
        output_x = 4
        
        # Create initial input layer
        input_labels = ["the", "dog"]
        input_nodes = VGroup()
        input_texts = VGroup()
        
        for i, label in enumerate(input_labels):
            node = Circle(radius=0.3, color=BLUE, fill_opacity=0.3)
            node.move_to([input_x, input_y_positions[i], 0])
            text = Text(label, font_size=20).next_to(node, LEFT, buff=0.2)
            input_nodes.add(node)
            input_texts.add(text)
        
        # Create hidden layer
        hidden_nodes = VGroup()
        for i in range(6):
            node = Circle(radius=0.25, color=GREEN, fill_opacity=0.3)
            node.move_to([hidden_x, hidden_y_positions[i], 0])
            hidden_nodes.add(node)
        
        # Create initial output layer
        output_labels = ["eats", "loves", "sleeps"]
        output_nodes = VGroup()
        output_texts = VGroup()
        
        for i, label in enumerate(output_labels):
            node = Circle(radius=0.3, color=RED, fill_opacity=0.3)
            node.move_to([output_x, output_y_positions[i], 0])
            text = Text(label, font_size=18).next_to(node, RIGHT, buff=0.2)
            output_nodes.add(node)
            output_texts.add(text)
        
        # Create connections input -> hidden
        input_to_hidden = VGroup()
        for input_node in input_nodes:
            for hidden_node in hidden_nodes:
                line = Line(input_node.get_center(), hidden_node.get_center(), 
                           stroke_width=1, color=GRAY, stroke_opacity=0.3)
                input_to_hidden.add(line)
        
        # Create connections hidden -> output
        hidden_to_output = VGroup()
        for hidden_node in hidden_nodes:
            for output_node in output_nodes:
                line = Line(hidden_node.get_center(), output_node.get_center(),
                           stroke_width=1, color=GRAY, stroke_opacity=0.3)
                hidden_to_output.add(line)
        
        # Show initial network
        self.play(
            Create(input_to_hidden),
            Create(hidden_to_output),
            Create(input_nodes),
            Create(hidden_nodes),
            Create(output_nodes),
            Write(input_texts),
            Write(output_texts),
            run_time=3
        )
        self.wait(2)
        
        # Create new input nodes (not connected yet)
        new_input_labels = ["{concepts similar\nto outdoors}", "{concepts similar\nto enjoyment}"]
        new_input_y_positions = [-0.5, -1.5]
        new_input_nodes = VGroup()
        new_input_texts = VGroup()
        
        for i, label in enumerate(new_input_labels):
            node = Circle(radius=0.3, color=BLUE, fill_opacity=0.3)
            node.move_to([input_x, new_input_y_positions[i], 0])
            text = Text(label, font_size=16, line_spacing=0.8).next_to(node, LEFT, buff=0.2)
            new_input_nodes.add(node)
            new_input_texts.add(text)
        
        # Show new input nodes appearing
        self.play(
            Create(new_input_nodes),
            Write(new_input_texts),
            run_time=2
        )
        self.wait(1)
        
        # Connect new inputs to hidden layer
        new_input_to_hidden = VGroup()
        for new_node in new_input_nodes:
            for hidden_node in hidden_nodes:
                line = Line(new_node.get_center(), hidden_node.get_center(),
                           stroke_width=1, color=GRAY, stroke_opacity=0.3)
                new_input_to_hidden.add(line)
        
        self.play(Create(new_input_to_hidden), run_time=2)
        self.wait(1)
        
        # Simulate calculation process - flash edges from all inputs to hidden layer
        # Flash from all current input nodes to hidden layer
        all_input_nodes = VGroup(*input_nodes, *new_input_nodes)
        
        # Create flashing edges from all inputs to all hidden nodes
        flash_input_to_hidden = VGroup()
        for input_node in all_input_nodes:
            for hidden_node in hidden_nodes:
                edge = Line(input_node.get_center(), hidden_node.get_center(),
                           stroke_width=3, color=YELLOW)
                flash_input_to_hidden.add(edge)
        
        # Flash input to hidden connections
        self.play(Create(flash_input_to_hidden), run_time=1.5)
        self.play(FadeOut(flash_input_to_hidden), run_time=0.5)
        self.wait(0.5)
        
        # Flash from hidden layer to all output nodes
        flash_hidden_to_output = VGroup()
        for hidden_node in hidden_nodes:
            for output_node in output_nodes:
                edge = Line(hidden_node.get_center(), output_node.get_center(),
                           stroke_width=3, color=YELLOW)
                flash_hidden_to_output.add(edge)
        
        # Flash hidden to output connections
        self.play(Create(flash_hidden_to_output), run_time=1.5)
        self.play(FadeOut(flash_hidden_to_output), run_time=0.5)
        self.wait(0.5)
        
        # Highlight the winning node "loves" (second output node)
        loves_highlight = output_nodes[1].copy().set_color(YELLOW).set_fill(opacity=0.7)
        self.play(Transform(output_nodes[1], loves_highlight), run_time=1.5)
        self.wait(2)
        
        # Move "loves" to become an input node
        loves_node = output_nodes[1].copy()
        loves_text = output_texts[1].copy()
        
        # Position for new input node
        loves_input_pos = [input_x, -2.5, 0]
        
        # Create new text positioned to the left
        loves_text_left = Text("loves", font_size=18).next_to(
            Circle(radius=0.3).move_to(loves_input_pos), LEFT, buff=0.2
        )
        
        self.play(
            loves_node.animate.move_to(loves_input_pos),
            Transform(loves_text, loves_text_left),
            run_time=2
        )
        self.wait(1)
        
        # Revert the "loves" output node back to red before changing outputs
        loves_revert = output_nodes[1].copy().set_color(RED).set_fill(opacity=0.3)
        self.play(Transform(output_nodes[1], loves_revert), run_time=0.5)
        
        # Connect "loves" input to hidden layer
        loves_to_hidden = VGroup()
        for hidden_node in hidden_nodes:
            line = Line(loves_input_pos, hidden_node.get_center(),
                       stroke_width=1, color=GRAY, stroke_opacity=0.3)
            loves_to_hidden.add(line)
        
        self.play(Create(loves_to_hidden), run_time=1.5)
        self.wait(1)
        
        # Fade out old output texts first
        self.play(FadeOut(output_texts), run_time=1)
        self.wait(0.5)
        
        # Change output nodes to new labels
        new_output_labels = ["to run in\nthe park", "to eat\nleftovers", "to scratch\nits ear"]
        
        # Create new output texts positioned to the right of nodes
        new_output_texts = VGroup()
        for i, label in enumerate(new_output_labels):
            text = Text(label, font_size=14, line_spacing=0.8).next_to(output_nodes[i], RIGHT, buff=0.2)
            new_output_texts.add(text)
        
        self.play(Write(new_output_texts), run_time=2)
        self.wait(1)
        
        # Rerun the calculation animation with all inputs (including "loves")
        all_current_inputs = VGroup(*input_nodes, *new_input_nodes, loves_node)
        
        # Flash from all inputs to hidden layer
        flash_input_to_hidden_2 = VGroup()
        for input_node in all_current_inputs:
            for hidden_node in hidden_nodes:
                edge = Line(input_node.get_center(), hidden_node.get_center(),
                           stroke_width=3, color=YELLOW)
                flash_input_to_hidden_2.add(edge)
        
        self.play(Create(flash_input_to_hidden_2), run_time=1.5)
        self.play(FadeOut(flash_input_to_hidden_2), run_time=0.5)
        self.wait(0.5)
        
        # Flash from hidden layer to output nodes
        flash_hidden_to_output_2 = VGroup()
        for hidden_node in hidden_nodes:
            for output_node in output_nodes:
                edge = Line(hidden_node.get_center(), output_node.get_center(),
                           stroke_width=3, color=YELLOW)
                flash_hidden_to_output_2.add(edge)
        
        self.play(Create(flash_hidden_to_output_2), run_time=1.5)
        self.play(FadeOut(flash_hidden_to_output_2), run_time=0.5)
        self.wait(0.5)
        
        # Highlight "run in the park" (first output node) as the winner
        park_highlight = output_nodes[0].copy().set_color(YELLOW).set_fill(opacity=0.7)
        self.play(Transform(output_nodes[0], park_highlight), run_time=1.5)
        self.wait(3)
