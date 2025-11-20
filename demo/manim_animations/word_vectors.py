from manim import *
import numpy as np

class WordVectors(ThreeDScene):
    def construct(self):
        # Create 2D axes
        axes = Axes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-1.2, 1.2, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        )
        
        # Axis labels
        x_label = Text("Gender", font_size=28).next_to(axes.coords_to_point(-1.2, 0), LEFT, buff=0.3)
        y_label = Text("Size", font_size=28).next_to(axes.coords_to_point(0, -1.2), DOWN, buff=0.3)
        
        # Gender axis annotations
        masculine_label = Text("Masculine", font_size=20, color=BLUE).next_to(axes.coords_to_point(-1.2, 0), DOWN, buff=0.2)
        feminine_label = Text("Feminine", font_size=20, color=PINK).next_to(axes.coords_to_point(1.2, 0), DOWN, buff=0.2)
        
        # Size axis annotations
        small_label = Text("Small", font_size=20, color=GREEN).next_to(axes.coords_to_point(0, -1.2), RIGHT, buff=0.2)
        large_label = Text("Big", font_size=20, color=ORANGE).next_to(axes.coords_to_point(0, 1.2), RIGHT, buff=0.2)
        
        # Start with just axes
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=4)
        self.play(Write(masculine_label), Write(feminine_label), Write(small_label), Write(large_label), run_time=4)
        self.wait(2)
        
        # Helper function to create word vector
        def create_word_vector(x, y, word, color, axes_obj):
            point = axes_obj.coords_to_point(x, y)
            dot = Dot(point, radius=0.12, color=color, fill_opacity=0.9)
            label = Text(word, font_size=22, color=color).next_to(dot, UR, buff=0.15)
            vector = Arrow(
                axes_obj.coords_to_point(0, 0),
                point,
                color=color,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.15
            )
            return vector, dot, label
        
        # Add adult man
        man_vec, man_dot, man_label = create_word_vector(-1, 1, "adult man", BLUE, axes)
        self.play(GrowArrow(man_vec), FadeIn(man_dot), Write(man_label), run_time=3)
        self.wait(2)
        
        # Add adult woman
        woman_vec, woman_dot, woman_label = create_word_vector(1.0, 1.0, "adult woman", PINK, axes)
        self.play(GrowArrow(woman_vec), FadeIn(woman_dot), Write(woman_label), run_time=3)
        self.wait(2)
        
        # Add girl
        girl_vec, girl_dot, girl_label = create_word_vector(1, -0.97, "girl", PINK, axes)
        self.play(GrowArrow(girl_vec), FadeIn(girl_dot), Write(girl_label), run_time=3)
        self.wait(2)
        
        # Remove size and gender labels
        self.play(FadeOut(masculine_label), FadeOut(feminine_label), 
                  FadeOut(small_label), FadeOut(large_label), run_time=3)
        self.wait(2)
        
        # Add teenage man
        teen_vec, teen_dot, teen_label = create_word_vector(-0.866, 0.5, "teenage man", BLUE, axes)
        self.play(GrowArrow(teen_vec), FadeIn(teen_dot), Write(teen_label), run_time=3)
        self.wait(2)
        
        # Draw angle between teenage man and adult man using Angle class
        angle1 = Angle(man_vec, teen_vec, radius=0.5, color=YELLOW)
        angle_label1 = Text("θ", font_size=32, color=YELLOW).move_to(
            Angle(man_vec, teen_vec, radius=0.7).point_from_proportion(0.5)
        )
        self.play(Create(angle1), Write(angle_label1), run_time=3)
        self.wait(3)
        
        # Remove angle and draw one between adult man and girl
        self.play(FadeOut(angle1), FadeOut(angle_label1), run_time=2)
        angle2 = Angle(man_vec, girl_vec, radius=0.5, color=YELLOW)
        angle_label2 = Text("θ", font_size=32, color=YELLOW).move_to(
            Angle(man_vec, girl_vec, radius=0.7).point_from_proportion(0.5)
        )
        self.play(Create(angle2), Write(angle_label2), run_time=3)
        self.wait(3)
        
        # Remove angle and draw one between adult man and woman
        self.play(FadeOut(angle2), FadeOut(angle_label2), run_time=2)
        angle3 = Angle(man_vec, woman_vec, radius=0.5, color=YELLOW)
        angle_label3 = Text("θ", font_size=32, color=YELLOW).move_to(
            Angle(man_vec, woman_vec, radius=0.7).point_from_proportion(0.5)
        )
        self.play(Create(angle3), Write(angle_label3), run_time=3)
        self.wait(3)
        
        # Remove angle and add "she" vector first
        self.play(FadeOut(angle3), FadeOut(angle_label3), run_time=2)
        she_vec, she_dot, she_label = create_word_vector(1.0, 0, "she", PINK, axes)
        self.play(GrowArrow(she_vec), FadeIn(she_dot), Write(she_label), run_time=3)
        self.wait(2)
        
        # Draw angle towards adult woman
        angle4 = Angle(she_vec, woman_vec, radius=0.5, color=YELLOW)
        angle_label4 = Text("θ", font_size=32, color=YELLOW).move_to(
            Angle(she_vec, woman_vec, radius=0.7).point_from_proportion(0.5)
        )
        self.play(Create(angle4), Write(angle_label4), run_time=3)
        self.wait(3)
        
        # Remove "she" angle and add building vector
        self.play(FadeOut(angle4), FadeOut(angle_label4), run_time=2)
        building_vec, building_dot, building_label = create_word_vector(0, 1.0, "building", ORANGE, axes)
        self.play(GrowArrow(building_vec), FadeIn(building_dot), Write(building_label), run_time=3)
        self.wait(2)
        
        # Draw angle between man and building
        angle5 = Angle(man_vec, building_vec, radius=0.5, color=YELLOW)
        angle_label5 = Text("θ", font_size=32, color=YELLOW).move_to(
            Angle(man_vec, building_vec, radius=0.7).point_from_proportion(0.5)
        )
        self.play(Create(angle5), Write(angle_label5), run_time=3)
        self.wait(3)
        
        # Remove building angle
        self.play(FadeOut(angle5), FadeOut(angle_label5), run_time=2)
        self.wait(2)
        
        # Transition to 3D
        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-1.2, 1.2, 0.5],
            z_range=[-1.2, 1.2, 0.5],
            x_length=7,
            y_length=7,
            z_length=7,
            axis_config={"color": GRAY},
            tips=False
        )
        
        # 3D axis labels
        z_label = Text("Living", font_size=28).next_to(axes_3d.z_axis, OUT, buff=0.3)
        
        # Fade out 2D elements and bring in 3D
        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(man_vec), FadeOut(man_dot), FadeOut(man_label),
            FadeOut(woman_vec), FadeOut(woman_dot), FadeOut(woman_label),
            FadeOut(girl_vec), FadeOut(girl_dot), FadeOut(girl_label),
            FadeOut(teen_vec), FadeOut(teen_dot), FadeOut(teen_label),
            FadeOut(building_vec), FadeOut(building_dot), FadeOut(building_label)
        )
        
        self.add(axes_3d)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=3)
        
        # 3D labels at the end of axes
        x_label_3d = Text("Gender", font_size=20).move_to(axes_3d.coords_to_point(1.4, 0, 0))
        y_label_3d = Text("Size", font_size=20).move_to(axes_3d.coords_to_point(0, 1.4, 0))
        z_label_3d = Text("Living", font_size=20).move_to(axes_3d.coords_to_point(0, 0, 1.4))
        
        self.add_fixed_in_frame_mobjects(x_label_3d, y_label_3d, z_label_3d)
        self.play(Write(x_label_3d), Write(y_label_3d), Write(z_label_3d), run_time=4)
        self.wait(2)
        
        # Add 3D vectors
        # Building: (0, 1.0, -1) - inanimate
        building_point_3d = axes_3d.coords_to_point(0, 1.0, -1)
        building_vec_3d = Arrow3D(
            axes_3d.coords_to_point(0, 0, 0),
            building_point_3d,
            color=ORANGE,
            thickness=0.02
        )
        building_dot_3d = Sphere(radius=0.1, color=ORANGE).move_to(building_point_3d)
        building_label_3d = Text("building", font_size=18, color=ORANGE).next_to(building_dot_3d, OUT)
        
        # Adult man: (-1, 1, 1) - living
        man_point_3d = axes_3d.coords_to_point(-1, 1, 1)
        man_vec_3d = Arrow3D(
            axes_3d.coords_to_point(0, 0, 0),
            man_point_3d,
            color=BLUE,
            thickness=0.02
        )
        man_dot_3d = Sphere(radius=0.1, color=BLUE).move_to(man_point_3d)
        man_label_3d = Text("adult man", font_size=18, color=BLUE).next_to(man_dot_3d, OUT)
        
        # Teenage man: (-0.866, 0.5, 1) - living
        teen_point_3d = axes_3d.coords_to_point(-0.866, 0.5, 1)
        teen_vec_3d = Arrow3D(
            axes_3d.coords_to_point(0, 0, 0),
            teen_point_3d,
            color=BLUE,
            thickness=0.02
        )
        teen_dot_3d = Sphere(radius=0.1, color=BLUE).move_to(teen_point_3d)
        teen_label_3d = Text("teenage man", font_size=18, color=BLUE).next_to(teen_dot_3d, OUT)
        
        # Add all 3D vectors
        self.play(
            Create(building_vec_3d), FadeIn(building_dot_3d), Write(building_label_3d),
            Create(man_vec_3d), FadeIn(man_dot_3d), Write(man_label_3d),
            Create(teen_vec_3d), FadeIn(teen_dot_3d), Write(teen_label_3d),
            run_time=3
        )
        self.wait(1.5)
        
        # Show angle between man and teenager in 3D with connecting line
        # Create a line segment between the two endpoint vectors to show angle
        teen_to_man_line = Line3D(teen_point_3d, man_point_3d, color=YELLOW, thickness=0.015)
        
        angle_text_1 = Text("Angle: man ↔ teenager", font_size=20, color=YELLOW)
        self.add_fixed_in_frame_mobjects(angle_text_1)
        angle_text_1.to_edge(UP)
        self.play(Create(teen_to_man_line), Write(angle_text_1), run_time=2)
        self.wait(3)
        
        # Show angle between building and man in 3D
        self.play(FadeOut(angle_text_1), FadeOut(teen_to_man_line), run_time=1)
        
        building_to_man_line = Line3D(building_point_3d, man_point_3d, color=YELLOW, thickness=0.015)
        
        angle_text_2 = Text("Angle: man ↔ building", font_size=20, color=YELLOW)
        self.add_fixed_in_frame_mobjects(angle_text_2)
        angle_text_2.to_edge(UP)
        self.play(Create(building_to_man_line), Write(angle_text_2), run_time=2)
        self.wait(3)
        
        self.play(FadeOut(angle_text_2), FadeOut(building_to_man_line), run_time=1)
        self.wait(1)

