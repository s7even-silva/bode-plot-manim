from manim import *

#config.media_width = "75%"
#config.verbosity = "WARNING"

import numpy as np
from scipy import signal

gain_10_color = BLUE
s_term_color = GREEN
s_plus_1_color = PURPLE
s_over_10_color = ORANGE
s_over_20_color = RED

letter_size = 0.5

class BodeApproximation(Scene):
    def construct(self):

        # H(s) = 10 * s * (s + 1) / ((s / 10 + 1) * ((s / 20)^2 + s / 20 + 1))
        transferf = MathTex(r"H(s) = \frac{10 \cdot s \cdot (s + 1)}{\left(\frac{s}{10} + 1\right) \cdot \left(\frac{s^2}{400} + \frac{s}{20} + 1\right)}", color = WHITE).scale(letter_size+0.2)

        # fransfer function
        num = [40000, 40000, 0]   # Numerador: 40000 * s * (s + 1)
        den = [1, 30, 500, 4000]  # Denominador: (s + 10) * (s^2 + 20s + 400)
        system = signal.TransferFunction(num, den)
        
        # 10
        gain_10 = MathTex(r"10", color = gain_10_color).scale(letter_size).to_edge(UP)

        num_gain_10 = [10]
        den_gain_10 = [1]
        gain_10_system = signal.TransferFunction(num_gain_10, den_gain_10)
        
        # s
        s_term = MathTex(r"s", color = s_term_color).scale(letter_size).next_to(gain_10, RIGHT, buff=0.5)

        num_s_term = [1,0]
        den_s_term = [1]
        s_term_system = signal.TransferFunction(num_s_term, den_s_term)
        
        # (s + 1)
        s_plus_1 = MathTex(r"(s + 1)", color = s_plus_1_color).scale(letter_size).next_to(s_term, DOWN, buff=0.5)

        num_s_plus_1 = [1, 1]
        den_s_plus_1 = [1]
        s_plus_1_system = signal.TransferFunction(num_s_plus_1, den_s_plus_1)
        
        # (s / 10 + 1)
        s_over_10_plus_1 = MathTex(r"\left(\frac{s}{10} + 1\right)", color = s_over_10_color).scale(letter_size).next_to(s_plus_1, LEFT, buff=0.5)

        num_s_over_10 = [1]
        den_s_over_10 = [0.1, 1]
        s_over_10_system = signal.TransferFunction(num_s_over_10, den_s_over_10)
        
        # ((s / 20)^2 + s / 20 + 1)
        s_over_20_sq = MathTex(r"\left(\left(\frac{s}{20}\right)^2 + \frac{s}{20} + 1\right)", color = s_over_20_color).scale(letter_size).next_to(s_over_10_plus_1, DOWN, buff=0.5)

        num_s_over_20_sq = [1]
        den_s_over_20_sq = [0.0025, 0.05, 1]
        s_over_20_sq_system = signal.TransferFunction(num_s_over_20_sq, den_s_over_20_sq)

        # x axis range
        range_min = -2
        range_max = 3

        frequencies = np.logspace(range_min, range_max, 500)  # Rango de frecuencias (0.1 a 1000 rad/s)
                
        w, mag_db, phase_deg = signal.bode(system, frequencies)
        w_gain_10, mag_gain_10, phase_gain_10 = signal.bode(gain_10_system, frequencies)
        w_s_term, mag_s_term, phase_s_term = signal.bode(s_term_system, frequencies)
        w_s_plus_1, mag_s_plus_1, phase_s_plus_1 = signal.bode(s_plus_1_system, frequencies)
        w_s_over_10, mag_s_over_10, phase_s_over_10 = signal.bode(s_over_10_system, frequencies)
        w_s_over_20_sq, mag_s_over_20_sq, phase_s_over_20_sq = signal.bode(s_over_20_sq_system, frequencies)
        


        mag_axes = Axes(
            x_range=[range_min, range_max, 1],  
            y_range=[-40, 80, 20], 
            axis_config={"include_tip": False, "numbers_to_exclude": [0]},
            x_axis_config={"label_direction": DOWN, "scaling": LogBase(10)},
            y_axis_config={"label_direction": LEFT}
        ).add_coordinates()

        
        mag_axes_labels = mag_axes.get_axis_labels(x_label="rad/s", y_label="dB")
        
        mag_plot = mag_axes.plot_line_graph(w, mag_db, line_color=WHITE, add_vertex_dots=False)

        gain_10_mag_plot = mag_axes.plot_line_graph(w_gain_10, mag_gain_10, line_color=gain_10_color, add_vertex_dots=False)
        s_term_mag_plot = mag_axes.plot_line_graph(w_s_term, mag_s_term, line_color=s_term_color, add_vertex_dots=False)
        s_plus_1_mag_plot = mag_axes.plot_line_graph(w_s_plus_1, mag_s_plus_1, line_color=s_plus_1_color, add_vertex_dots=False)
        s_over_10_mag_plot = mag_axes.plot_line_graph(w_s_over_10, mag_s_over_10, line_color=s_over_10_color, add_vertex_dots=False)
        s_over_20_sq_mag_plot = mag_axes.plot_line_graph(w_s_over_20_sq, mag_s_over_20_sq, line_color=s_over_20_color, add_vertex_dots=False)

        
        self.play( Write(transferf) )

        self.play(Indicate(transferf[0][5:15]) )
        self.play(Indicate(transferf[0][16:40]) )
        
        self.play( Write(mag_axes), Write(mag_axes_labels))
        self.play( transferf.animate.to_edge(UP) )
        
        self.play( Create(gain_10_mag_plot), transferf[0][5:7].animate.set_fill(color=gain_10_color))
        self.play( Create(s_term_mag_plot), transferf[0][8].animate.set_fill(color=s_term_color))
        self.play( Create(s_plus_1_mag_plot), transferf[0][10:15].animate.set_fill(color=s_plus_1_color))
        self.play( Create(s_over_10_mag_plot), transferf[0][16:24].animate.set_fill(color=s_over_10_color))
        self.play( Create(s_over_20_sq_mag_plot), transferf[0][25:40].animate.set_fill(color=s_over_20_color))
        
        self.play( Create(mag_plot) )
        self.wait(2)


        
        phase_axes = Axes(
            x_range=[range_min, range_max, 1],  
            y_range=[-180, 100, 45],  
            axis_config={"include_tip": False, "numbers_to_exclude": [0]},
            x_axis_config={"label_direction": DOWN, "scaling": LogBase(10)},
            y_axis_config={"label_direction": LEFT}
        ).add_coordinates()

        phase_axes_labels = phase_axes.get_axis_labels(x_label="rad/s", y_label="Fase")


        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [mag_axes, mag_axes_labels, transferf]] # idk why the transfer functions still vanishes
        )

        self.play( transferf.animate.to_edge(DOWN) )

        self.play(
            Transform(mag_axes, phase_axes),
            Transform(mag_axes_labels, phase_axes_labels)
        )

        
        phase_plot = phase_axes.plot_line_graph(w, mag_db, line_color=WHITE, add_vertex_dots=False)

        gain_10_phase_plot = phase_axes.plot_line_graph(w_gain_10, phase_gain_10, line_color=gain_10_color, add_vertex_dots=False)
        s_term_phase_plot = phase_axes.plot_line_graph(w_s_term, phase_s_term, line_color=s_term_color, add_vertex_dots=False)
        s_plus_1_phase_plot = phase_axes.plot_line_graph(w_s_plus_1, phase_s_plus_1, line_color=s_plus_1_color, add_vertex_dots=False)
        s_over_10_phase_plot = phase_axes.plot_line_graph(w_s_over_10, phase_s_over_10, line_color=s_over_10_color, add_vertex_dots=False)
        s_over_20_sq_phase_plot = phase_axes.plot_line_graph(w_s_over_20_sq, phase_s_over_20_sq, line_color=s_over_20_color, add_vertex_dots=False)
    
        self.play(Create(gain_10_phase_plot))
        self.wait(1)
        self.play(Create(s_term_phase_plot))
        self.wait(1)
        self.play(Create(s_plus_1_phase_plot))
        self.wait(1)
        self.play(Create(s_over_10_phase_plot))
        self.wait(1)
        self.play(Create(s_over_20_sq_phase_plot))
        self.wait(1)
        self.play( Create(phase_plot) )
        self.wait(10)
