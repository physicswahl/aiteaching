from manim import *

class NeuralNetworkComputation(Scene):
    def construct(self):
        # Student data - Matthew Walker
        student_name = "Matthew Walker"
        x1 = 7.3  # Math performance
        x2 = 4.9  # Reading/Writing performance
        is_eligible = False  # Matthew is not eligible for support
        
        # Network parameters (defaults from two_nodes)
        w1 = 1.4
        w2 = 1.2
        bias = -10.0
        
        # ========== PART 1: Student Selection from Graph ==========
        
        # Title for graph section
        graph_title = Text("Student Performance Data", font_size=36)
        graph_title.to_edge(UP)
        self.add(graph_title)
        
        # Create axes (smaller for 16:9 format)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=5.5,
            y_length=5.5,
            axis_config={"color": GRAY},
            tips=False
        ).shift(DOWN * 0.5)
        
        # Axis labels
        x_label = Text("Math Performance", font_size=20).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Literacy", font_size=20).next_to(axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.4)
        
        # Actual student data from database
        students_data = [
            (2.5, 3.1, True), (8.4, 4.4, False), (6.9, 1.5, False),
            (2.5, 2.3, True), (1.5, 2.8, True), (3.9, 3.9, False),
            (1.3, 4.0, True), (7.4, 2.1, False), (0.4, 0.9, True),
            (8.5, 7.4, False), (1.6, 8.2, False), (3.4, 4.0, False),
            (2.1, 0.7, True), (1.8, 2.4, True), (8.6, 6.7, False),
            (7.1, 8.7, False), (8.5, 7.3, False), (4.2, 6.3, False),
            (0.0, 9.3, True), (6.3, 2.1, False), (6.3, 5.6, True),
            (8.9, 1.9, False), (7.3, 4.9, False), (5.1, 9.5, False),
            (1.7, 4.8, False), (0.6, 0.4, True), (2.0, 6.0, True),
            (5.0, 1.0, True), (2.8, 3.7, True), (1.9, 7.8, False),
            (2.5, 5.5, False), (4.0, 2.9, True), (1.0, 8.3, True)
        ]
        
        # Draw student dots
        dots = VGroup()
        matthew_dot = None
        
        for i, (math, reading, eligible) in enumerate(students_data):
            point = axes.coords_to_point(math, reading)
            color = BLUE if eligible else RED
            dot = Dot(point, radius=0.08, color=color, fill_opacity=0.8)
            dots.add(dot)
            
            # Mark Matthew Walker's dot
            if math == x1 and reading == x2:
                matthew_dot = dot
        
        self.play(FadeIn(dots), run_time=3.0)
        self.wait(2)
        
        # Legend
        legend = VGroup(
            VGroup(
                Dot(color=BLUE, radius=0.08, fill_opacity=0.8),
                Text("Eligible for Support", font_size=18, color=BLUE)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=RED, radius=0.08, fill_opacity=0.8),
                Text("Not Eligible", font_size=18, color=RED)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.5)
        
        self.play(FadeIn(legend))
        self.wait(2)
        
        # Highlight Matthew Walker
        highlight_circle = Circle(radius=0.25, color=YELLOW, stroke_width=4).move_to(matthew_dot.get_center())
        matthew_label = Text(student_name, font_size=22, color=YELLOW).next_to(matthew_dot, UR, buff=0.2)
        
        self.play(
            Create(highlight_circle),
            matthew_dot.animate.scale(1.5),
            Write(matthew_label)
        )
        self.wait(2)
        
        # Show coordinates being read (positioned off-screen initially, will appear on right)
        coord_display = VGroup(
            Text(f"Math Performance (x₁): {x1}", font_size=24, color=WHITE),
            Text(f"Reading/Writing (x₂): {x2}", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
        
        # Draw lines to axes
        vertical_line = DashedLine(
            matthew_dot.get_center(),
            axes.coords_to_point(x1, 0),
            color=YELLOW,
            stroke_width=2
        )
        horizontal_line = DashedLine(
            matthew_dot.get_center(),
            axes.coords_to_point(0, x2),
            color=YELLOW,
            stroke_width=2
        )
        
        x_tick_label = Text(f"{x1}", font_size=16, color=YELLOW).next_to(axes.coords_to_point(x1, 0), DOWN, buff=0.2)
        y_tick_label = Text(f"{x2}", font_size=16, color=YELLOW).next_to(axes.coords_to_point(0, x2), LEFT, buff=0.2)
        
        self.play(
            Create(vertical_line),
            Create(horizontal_line),
            Write(x_tick_label),
            Write(y_tick_label)
        )
        self.wait(2)
        
        # Shift graph to the left and show coordinates on the right
        graph_group = VGroup(
            graph_title, axes, x_label, y_label, dots, legend,
            highlight_circle, matthew_label, vertical_line, horizontal_line,
            x_tick_label, y_tick_label
        )
        
        self.play(
            graph_group.animate.shift(LEFT * 2.5),
            run_time=2
        )
        self.wait(1.0)
        
        # Show coordinates on the right side
        self.play(Write(coord_display))
        self.wait(4)
        
        # Transition to neural network
        self.play(
            FadeOut(graph_group),
            coord_display.animate.to_edge(UP, buff=0.3).to_edge(LEFT)
        )
        self.wait(1.0)
        
        # ========== PART 2: Neural Network Processing ==========
        # (Title removed to avoid overlap with coord_display)
        
        # Draw neural network
        # Input neurons
        input1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + UP * 1)
        input1_label = Text("x₁", font_size=28, color=WHITE).move_to(input1)
        input1_value = Text(f"{x1}", font_size=20, color=YELLOW).next_to(input1, LEFT, buff=0.3)
        
        input2 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + DOWN * 1)
        input2_label = Text("x₂", font_size=28, color=WHITE).move_to(input2)
        input2_value = Text(f"{x2}", font_size=20, color=YELLOW).next_to(input2, LEFT, buff=0.3)
        
        # Output neuron
        output = Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(RIGHT * 2)
        output_label = Text("y", font_size=28, color=WHITE).move_to(output)
        
        # Connections
        conn1 = Line(input1.get_right(), output.get_left(), color=GRAY)
        conn2 = Line(input2.get_right(), output.get_left(), color=GRAY)
        
        # Weight labels
        weight1_label = Text(f"w₁ = {w1}", font_size=24, color=GREEN).next_to(conn1, UP, buff=0.2)
        weight2_label = Text(f"w₂ = {w2}", font_size=24, color=GREEN).next_to(conn2, DOWN, buff=0.2)
        bias_label = Text(f"b = {bias}", font_size=24, color=ORANGE).next_to(output, DOWN, buff=0.5)
        
        # Draw network
        self.play(
            Create(input1), Write(input1_label), Write(input1_value),
            Create(input2), Write(input2_label), Write(input2_value)
        )
        self.wait(1.0)
        
        self.play(Create(conn1), Create(conn2))
        self.play(Write(weight1_label), Write(weight2_label))
        self.wait(1.0)
        
        self.play(Create(output), Write(output_label), Write(bias_label))
        self.wait(2)
        
        # Step 1: Multiply inputs by weights
        calc_title = Text("Step 1: Multiply inputs by weights for each branch", font_size=24, color=YELLOW)
        calc_title.to_edge(DOWN, buff=2)
        self.play(Write(calc_title))
        
        product1 = w1 * x1
        product2 = w2 * x2
        
        calc1 = Text(f"w₁ × x₁ = {w1} × {x1} = {product1:.2f}", font_size=28)
        calc2 = Text(f"w₂ × x₂ = {w2} × {x2} = {product2:.2f}", font_size=28)
        
        calculations = VGroup(calc1, calc2).arrange(DOWN, buff=0.3).next_to(calc_title, DOWN, buff=0.3)
        
        # Highlight first connection
        self.play(conn1.animate.set_color(YELLOW), run_time=1.0)
        self.play(Write(calc1))
        self.play(conn1.animate.set_color(GRAY), run_time=1.0)
        self.wait(1.0)
        
        # Highlight second connection
        self.play(conn2.animate.set_color(YELLOW), run_time=1.0)
        self.play(Write(calc2))
        self.play(conn2.animate.set_color(GRAY), run_time=1.0)
        self.wait(2)
        
        # Step 2: Sum the weighted inputs
        # Move step 1 calculations to the left side
        self.play(
            FadeOut(calc_title),
            calculations.animate.scale(0.8).to_edge(LEFT, buff=0.5).shift(DOWN * 1)
        )
        
        calc_title2 = Text("Step 2: Sum the weighted inputs", font_size=24, color=YELLOW)
        calc_title2.to_edge(DOWN, buff=2)
        self.play(Write(calc_title2))
        
        sum_calc = Text(f"{product1:.2f} + {product2:.2f} = {product1 + product2:.2f}", font_size=32)
        sum_calc.next_to(calc_title2, DOWN, buff=0.3)
        
        # Animate the results from step 1 moving to step 2
        calc1_copy = calc1.copy()
        calc2_copy = calc2.copy()
        
        # Extract just the result values
        result1_text = Text(f"{product1:.2f}", font_size=32, color=GREEN)
        result2_text = Text(f"{product2:.2f}", font_size=32, color=GREEN)
        
        self.play(
            Transform(calc1_copy, result1_text.move_to(sum_calc.get_left() + RIGHT * 0.8)),
            Transform(calc2_copy, result2_text.move_to(sum_calc.get_center() + RIGHT * 1.5)),
            run_time=3.0
        )
        self.wait(1.0)
        
        self.play(
            FadeOut(calc1_copy),
            FadeOut(calc2_copy),
            Write(sum_calc)
        )
        self.wait(3.0)
        
        # Step 3: Subtract the bias
        self.play(FadeOut(calc_title2), FadeOut(sum_calc), FadeOut(calculations))
        
        calc_title3 = Text("Step 3: Subtract the bias", font_size=24, color=YELLOW)
        calc_title3.to_edge(DOWN, buff=2)
        self.play(Write(calc_title3))
        
        weighted_sum = product1 + product2
        result = weighted_sum + bias  # bias is already negative
        
        bias_calc = Text(f"{weighted_sum:.2f} + ({bias}) = {result:.2f}", font_size=32)
        bias_calc.next_to(calc_title3, DOWN, buff=0.3)
        
        self.play(bias_label.animate.set_color(YELLOW), run_time=1.0)
        self.play(Write(bias_calc))
        self.play(bias_label.animate.set_color(ORANGE), run_time=1.0)
        self.wait(3.0)
        
        # Step 4: Classification
        self.play(FadeOut(calc_title3), FadeOut(bias_calc))
        
        calc_title4 = Text("Step 4: Classification", font_size=24, color=YELLOW)
        calc_title4.to_edge(DOWN, buff=1.5)
        self.play(Write(calc_title4))
        
        if result <= 0:
            classification = "Eligible for SEN Support"
            class_color = BLUE
        else:
            classification = "SEN Support is not recommended"
            class_color = RED
        
        class_rule = Text(f"Output = {result:.2f}", font_size=28)
        class_rule.next_to(calc_title4, DOWN, buff=0.2)
        
        class_text = Text(f"Output > 0: {classification}", font_size=26, color=class_color)
        class_text.next_to(class_rule, DOWN, buff=0.4)
        
        self.play(Write(class_rule))
        self.wait(1.0)
        self.play(output.animate.set_fill(class_color, opacity=1), run_time=1.0)
        self.play(Write(class_text))
        self.wait(4)
        
        # Final summary box
        summary = VGroup(
            Text(f"{student_name}", font_size=28, color=WHITE),
            Text(f"Math: {x1}, Reading/Writing: {x2}", font_size=22),
            Text(f"Network Output: {result:.2f}", font_size=22),
            Text(classification, font_size=24, color=class_color, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        
        summary_box = SurroundingRectangle(summary, color=class_color, buff=0.4, corner_radius=0.2)
        summary_group = VGroup(summary_box, summary)
        
        self.play(
            FadeOut(calc_title4),
            FadeOut(class_rule),
            FadeOut(class_text),
            FadeOut(coord_display),
            FadeOut(input1), FadeOut(input1_label), FadeOut(input1_value),
            FadeOut(input2), FadeOut(input2_label), FadeOut(input2_value),
            FadeOut(output), FadeOut(output_label), FadeOut(bias_label),
            FadeOut(conn1), FadeOut(conn2),
            FadeOut(weight1_label), FadeOut(weight2_label)
        )
        
        summary_group.move_to(ORIGIN)
        self.play(FadeIn(summary_group))
        self.wait(6)
