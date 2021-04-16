from manim import *
import os
import scipy.stats
import scipy.special as sc
import random


class CubePyramid(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        opac = 0.25

        pts = [UP + RIGHT + 2 * OUT, UP + LEFT + 2 * OUT, DOWN + LEFT + 2 * OUT, DOWN + RIGHT + 2 * OUT]
        face1 = Polygon(*pts, fill_color = BLUE, fill_opacity = opac)

        pts = [UP + LEFT + 2 * OUT, DOWN + LEFT + 2 * OUT, 4 * OUT]
        face2 = Polygon(*pts, fill_color = BLUE, fill_opacity = opac)

        pyrgrp = VGroup(face1, face2)
        for i in range(1, 1 + 3):
            temp = face2.copy()
            temp.rotate(i * 90 * DEGREES, axis = OUT, about_point = ORIGIN)
            pyrgrp.add(temp)
        
        invpyrgrp = pyrgrp.copy().rotate(180 * DEGREES, axis = RIGHT, about_point = 2 * OUT)

        hpyrgrp = VGroup()
        pts = [ORIGIN, DOWN, DR, UR, UL, LEFT]
        hpyrgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [2 * OUT, ORIGIN, DOWN]
        hpyrgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [2 * OUT, DOWN, DR]
        hpyrgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [2 * OUT, DR, UR]
        hpyrgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        hpyrgrp.add(hpyrgrp[1].copy().rotate(-90 * DEGREES, axis = OUT, about_point = ORIGIN))
        hpyrgrp.add(hpyrgrp[2].copy().rotate(180 * DEGREES, axis = 2 * OUT + UP, about_point = DOWN).rotate(-90 * DEGREES, axis = OUT, about_point = ORIGIN))
        hpyrgrp.add(hpyrgrp[3].copy().rotate(90 * DEGREES, axis = OUT, about_point = ORIGIN))
        hpyrgrp.shift(UR)

        hgrp = VGroup()
        for i in range(4):
            hgrp.add(hpyrgrp.copy().rotate_about_origin(i * 90 * DEGREES))
        
        rgrp = VGroup()
        pts = [ORIGIN, RIGHT, UR, UP]
        rgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [RIGHT, UR, UR + 2 * OUT]
        rgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [UP, UR, UR + 2 * OUT]
        rgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [ORIGIN, RIGHT, UR + 2 * OUT]
        rgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [ORIGIN, UP, UR + 2 * OUT]
        rgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))

        rpgrp = VGroup()
        for i in range(4):
            rpgrp.add(rgrp.copy().rotate_about_origin(i * 90 * DEGREES))
        
        remgrp = VGroup()
        pts = [DL + 2 * OUT, DR + 2 * OUT, DOWN]
        remgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [DL + 2 * OUT, DR + 2 * OUT, 2 * DOWN]
        remgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [DR + 2 * OUT, DOWN, 2 * DOWN]
        remgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))
        pts = [DR + 2 * OUT, DOWN, 2 * DOWN]
        remgrp.add(Polygon(*pts, fill_color = BLUE, fill_opacity = opac))

        trempgrp = VGroup(remgrp.copy())
        trempgrp.add(remgrp.copy().rotate(180 * DEGREES, about_point = DOWN))

        rempgrp = VGroup()
        for i in range(4):
            rempgrp.add(trempgrp.copy().rotate_about_origin(i * 90 * DEGREES))
        
        VGroup(rempgrp, hgrp, rpgrp, pyrgrp, invpyrgrp).set_stroke(width = 1)
        VGroup(rempgrp, hgrp, rpgrp, pyrgrp, invpyrgrp).shift(-0.75 * OUT)

        logo = ImageMobject("C:/ManimCE/manim-1/CubePyramidFormula/ActOfLearningLogo").scale(1 / 16)
        title = Tex("\\text{Act of Learning}")
        title.to_corner(UR, buff = MED_SMALL_BUFF)
        logo.next_to(title, LEFT, buff = SMALL_BUFF)
        logo.align_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(logo, title)
        #self.add_fixed_orientation_mobjects(logo, title)

        d = 2

        self.set_camera_orientation(phi = 60 * DEGREES, theta = 30 * DEGREES)
        pyrgrp.set_color(GREEN)
        invpyrgrp.set_color(RED_E)
        rpgrp.set_color(GOLD)
        hgrp.set_color(PURPLE_E)
        #rempgrp.set_color(YELLOW_E)

        #self.add(circle, axes, pyrgrp, invpyrgrp, hpyrgrp)
        #self.add(circle, axes, hgrp, rpgrp)
        self.add(title, logo, rempgrp, hgrp, rpgrp, pyrgrp, invpyrgrp)
        self.begin_ambient_camera_rotation(rate = 1 / 2)
        self.wait(1)
        self.play(pyrgrp.animate.shift(d * OUT))
        self.wait(1)
        self.play(VGroup(hgrp[0], rpgrp[0]).animate.shift(d * UR))
        self.play(VGroup(hgrp[1], rpgrp[1]).animate.shift(d * UL))
        self.play(VGroup(hgrp[2], rpgrp[2]).animate.shift(d * DL))
        self.play(VGroup(hgrp[3], rpgrp[3]).animate.shift(d * DR))
        self.wait(1)
        self.play(rempgrp[0].animate.shift(d * DOWN))
        self.play(rempgrp[1].animate.shift(d * RIGHT))
        self.play(rempgrp[2].animate.shift(d * UP))
        self.play(rempgrp[3].animate.shift(d * LEFT))
        self.wait(1)
        self.play(
            rempgrp[0][0].animate.shift(d / 2 * DOWN).set_color(LIGHT_PINK),
            rempgrp[1][0].animate.shift(d / 2 * RIGHT).set_color(LIGHT_PINK),
            rempgrp[2][0].animate.shift(d / 2 * UP).set_color(LIGHT_PINK),
            rempgrp[3][0].animate.shift(d / 2 * LEFT).set_color(LIGHT_PINK)
        )
        self.wait(1)
        self.play(
            rempgrp[0][1].animate.shift(-d * DOWN),
            rempgrp[1][1].animate.shift(-d * RIGHT),
            rempgrp[2][1].animate.shift(-d * UP),
            rempgrp[3][1].animate.shift(-d * LEFT),
        )
        #self.play(rempgrp[0][1].animate.shift(-d * DOWN))
        #self.play(rempgrp[1][1].animate.shift(-d * RIGHT))
        #self.play(rempgrp[2][1].animate.shift(-d * UP))
        #self.play(rempgrp[3][1].animate.shift(-d * LEFT))
        self.wait(1)
        self.play(
            rpgrp[0].animate.shift(-d * UR),
            rpgrp[1].animate.shift(-d * UL),
            rpgrp[2].animate.shift(-d * DL),
            rpgrp[3].animate.shift(-d * DR),
        )
        #self.play(rpgrp[0].animate.shift(-d * UR))
        #self.play(rpgrp[1].animate.shift(-d * UL))
        #self.play(rpgrp[2].animate.shift(-d * DL))
        #self.play(rpgrp[3].animate.shift(-d * DR))
        self.wait(10)
        #self.stop_ambient_camera_rotation()
        #self.move_camera(phi = 75 * DEGREES, theta = 30 * DEGREES)
        #self.wait()

if __name__ == "__main__":
    module_name = os.path.abspath(__file__)
    output_location = "C:\ManimCE\media"
    clear_cmd = "cls"
    #command_A = "manim " + module_name + " " + "CubePyramid" + " " + "-pql -n 0" + " --media_dir " + output_location
    command_A = "manim " + module_name + " " + "CubePyramid" + " " + "-pqk -n 0" + " --media_dir " + output_location
    #command_A = "manim " + module_name + " " + "CubePyramid" + " " + "--format gif" + " --media_dir " + output_location
    #command_A = "manim " + module_name + " --media_dir " + output_location + " -pqh"
    os.system(clear_cmd)
    os.system(command_A)