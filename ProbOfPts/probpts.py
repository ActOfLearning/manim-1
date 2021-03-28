#!/usr/bin/env python

from manim import *
import os
import scipy.stats
import scipy.special as sc
import random

CMARK_TEX = "\\text{\\ding{51}}"
XMARK_TEX = "\\text{\\ding{55}}"

COIN_COLOR_MAP = {
    "H": BLUE_E,
    "W": BLUE_E,
    "T": RED_E,
    "L": RED_E,
    "D": YELLOW_E
}

# To watch one of these scenes, run the following:
# python --quality m manim example_scenes.py SquareToCircle -p
#
# Use the flag --quality l for a faster rendering at a lower quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have preview of the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the nth animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)

def get_random_process(choices, shuffle_time=2, total_time=3, change_rate=0.1,
                       h_buff=0.1, v_buff=0.1):
    content = choices[0]

    container = Square()
    container.set_opacity(0)
    container.stretch_to_fit_width(content.width + 2 * h_buff)
    container.stretch_to_fit_height(content.height + 2 * v_buff)
    container.move_to(content)
    container.add(content)
    container.time = 0
    container.last_change_time = 0

    def update(container, dt):
        container.time += dt

        t = container.time
        change = all([
            (t % total_time) < shuffle_time,
            container.time - container.last_change_time > change_rate
        ])
        if change:
            mob = container.submobjects[0]
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            new_mob.move_to(container, DL)
            new_mob.shift(2 * np.random.random() * h_buff * RIGHT)
            new_mob.shift(2 * np.random.random() * v_buff * UP)
            #container.set_submobjects([new_mob])
            container.submobjects = [new_mob]
            container.last_change_time = container.time

    container.add_updater(update)
    return container


# Coins
def get_coin(symbol, color=None):
    if color is None:
        color = COIN_COLOR_MAP.get(symbol, GREY_E)
    coin = VGroup()
    circ = Circle()
    circ.set_fill(color, 1)
    circ.set_stroke(WHITE, 1)
    circ.height = 1
    label = Tex(symbol)
    label.height = 0.5 * circ.height
    label.move_to(circ)
    coin.add(circ, label)
    coin.symbol = symbol
    return coin


def get_random_coin(**kwargs):
    return get_random_process([get_coin("H"), get_coin("T")], **kwargs)


def TextPosition(obj, color = YELLOW, scale = 1 / 2):
    pos = 0
    res = VGroup()            
    for letter in obj:
        temp = Tex(f"{pos}").scale(scale).set_color(color)
        temp.move_to(letter.get_top())
        pos += 1
        res.add(temp)
    return res 


def TextReplace(tex, obj, subtext):
    temp = tex.get_part_by_tex(subtext)
    obj.replace(temp)
    tex[tex.index_of_part(temp)].become(obj)


class Introduction(Scene):
    def construct(self):
        players = VGroup(Tex("Player A"), Tex("Player B"))
        for text in players:
            text.scale(2)
        
        players[0].to_edge(LEFT, buff = LARGE_BUFF)
        players[1].to_edge(RIGHT, buff = LARGE_BUFF)

        for i in range(2):
            self.play(Write(players[i]))
            self.play(players[i].animate.to_edge(UP + (2 * i - 1) * RIGHT, buff = LARGE_BUFF))
        
        counts = VGroup()
        headsupdate = Integer(0).set_color(BLUE)
        tailsupdate = Integer(0).set_color(RED)
        counts.add(headsupdate, tailsupdate)
        for i in range(2):
            counts[i].height = 1
            counts[i].next_to(players[i], DOWN, buff = 0.65)
        self.play(Write(counts))
        self.add(counts)
        self.wait()

        buff = 1 * RIGHT
        currpos = 7 * LEFT
        rand_process = 2 * [True] + 3 * [False] + 3 * [True] + 2 * [False] + 3 * [True] + 2 * [False]
        num_heads, num_tails = 0, 0
        random.shuffle(rand_process)
        coingrp = VGroup()
        for boolean in rand_process:
            temp = get_random_coin(shuffle_time=2, total_time=2)
            self.add(temp)
            self.wait(2)
            curr_coin = get_coin("H") if boolean else get_coin("T")
            curr_coin.move_to(temp)
            self.add(curr_coin)
            self.remove(temp)
            coingrp.add(curr_coin)
            counterupdate = 1 if boolean else 0
            anim_list = [curr_coin.animate.move_to(currpos + 2 * DOWN).scale_in_place(0.75)]
            if boolean:
                num_heads += 1
                anim_list += [headsupdate.animate.set_value(num_heads)]
            else:
                num_tails += 1   
                anim_list += [tailsupdate.animate.set_value(num_tails)]
            self.play(*anim_list)
            currpos += buff
            self.wait(0.5)

        anims = [FadeOutAndShift(obj, DOWN) for obj in coingrp]
        self.play(LaggedStart(*anims), run_time = 2)
        self.wait()

        svgimage = SVGMobject("C:/ManimCE/manim-1/ProbOfPts/assets/trophy5").shift(DOWN)
        #prfund = Tex("10,000 USD").scale(1.5)
        #prfund.next_to(svgimage, DOWN)
        #self.play(ShowCreation(svgimage), Write(prfund))
        self.play(ShowCreation(svgimage))
        self.wait()
        #self.play(FadeOut(svgimage), FadeOut(prfund))
        self.play(FadeOut(svgimage))
        self.wait()

        self.play(*[GrowFromCenter(obj) for obj in coingrp])
        anims = [obj.animate.shift(DOWN) for obj in coingrp]
        self.play(LaggedStart(*anims), run_time = 2)
        self.wait()

        self.play(
            VGroup(players[0], headsupdate).animate.shift(0.5 * RIGHT),
            VGroup(players[1], tailsupdate).animate.shift(0.5 * LEFT)
        )

        byfifteen = VGroup(MathTex("\\over"), MathTex("15"), MathTex("\\times"), svgimage.scale_in_place(0.25))
        byfifteen.scale(2)
        byfifteen[1].next_to(byfifteen[0], DOWN)
        byfifteen[2].next_to(byfifteen[0], RIGHT)
        byfifteen[3].next_to(byfifteen[2], RIGHT)

        byfifteen.move_to(headsupdate.get_bottom() + byfifteen.get_center() - byfifteen[0].get_top() + DOWN / 8)
        self.play(Write(byfifteen))
        byfifcpy = byfifteen.copy()
        self.play(byfifcpy.animate.move_to(tailsupdate.get_bottom() + byfifcpy.get_center() - byfifcpy[0].get_top() + DOWN / 8))
        self.wait(3)


class NotACasualPuzzle(Scene):
    def construct(self):
        caspuz = Tex("Not just a casual puzzle..").scale(2)
        self.play(Write(caspuz))
        self.wait()
        self.play(Transform(caspuz, Tex("Probability").scale(2).set_color(YELLOW)))
        self.play(caspuz.animate.to_edge(UP))

        caspuzl = Underline(caspuz)
        self.play(ShowCreation(caspuzl))
        self.wait()

        pascal = ImageMobject("C:/ManimCE/manim-1/ProbOfPts/assets/Pascal").shift(3 * LEFT + 0.5 * DOWN)
        fermat = ImageMobject("C:/ManimCE/manim-1/ProbOfPts/assets/Fermat").shift(3 * RIGHT + 0.5 * DOWN)
        for img in [pascal, fermat]:
            img.height = 5
        self.play(
            GrowFromCenter(pascal),
            GrowFromCenter(fermat),
        )
        self.wait()
        self.play(
            FadeOutAndShift(pascal, LEFT),
            FadeOutAndShift(fermat, RIGHT)
        )
        self.wait()

        trophy = SVGMobject("C:/ManimCE/manim-1/ProbOfPts/assets/trophy5")
        trcpy = trophy.copy().to_edge(LEFT, buff = LARGE_BUFF)
        propto = VGroup(MathTex("\propto"), MathTex("\mathbb{P}("), Tex("Winning the match"), MathTex(")"))
        propto.scale(2)
        propto.arrange(RIGHT)
        propto.next_to(trcpy)
        self.play(GrowFromCenter(trophy))
        self.play(
            trophy.animate.to_edge(LEFT, buff = LARGE_BUFF),
            Write(propto)
        )
        self.wait()
        self.play(
            FadeOut(VGroup(trophy, propto))
        )
        self.wait(3)


class WinningProbability(Scene):
    def construct(self):
        caspuz = Tex("Probability").scale(2).set_color(YELLOW)
        caspuz.to_edge(UP)
        caspuzl = Underline(caspuz)
        self.add(caspuz, caspuzl)

        rand_process = 2 * [True] + 3 * [False] + 3 * [True] + 2 * [False] + 3 * [True] + 2 * [False]
        random.shuffle(rand_process)
        coingrp = VGroup()
        for boolean in rand_process:
            if boolean:
                coingrp.add(get_coin("H").scale(2 / 3))
            else:
                coingrp.add(get_coin("T").scale(2 / 3))
        coingrp.arrange(RIGHT)
        coingrp.shift(1.75 * UP)
        
        gameprob = VGroup(MathTex("\mathbb{P}(\\text{A wins})=p"), MathTex("\mathbb{P}(\\text{B wins})=q"))
        sumtoone = VGroup(MathTex("p + q = 1")).scale_in_place(1.5).shift(1 * DOWN)
        for txt in gameprob:
            txt.scale_in_place(1.5)
        gameprob[0].shift(3.5 * LEFT)
        gameprob[1].shift(3.5 * RIGHT)
        gameprob.shift(0.5 * UP)
        self.play(Write(gameprob))
        self.wait()
        self.play(Write(sumtoone))
        self.wait()

        self.play(
            FadeOutAndShift(sumtoone, DOWN),
            *[GrowFromCenter(obj) for obj in coingrp]
        )
        self.wait()

        Arem = VGroup(*[get_coin("H") for i in range(2)])
        Brem = VGroup(*[get_coin("T") for i in range(3)])
        for obj in Arem + Brem:
            obj.scale_in_place(2 / 3)
        Arem.arrange(RIGHT)
        Brem.arrange(RIGHT)
        Arem.next_to(gameprob[0], DOWN)
        Brem.next_to(gameprob[1], DOWN)
        self.play(Write(Arem), Write(Brem))
        self.wait()

        fourmore = VGroup(*[get_coin("", color = GREY) for i in range(4)])
        fourmore.arrange(RIGHT)
        fourmore.shift(2.5 * DOWN)
        for obj in fourmore:
            obj.rotate_in_place(90 * DEGREES, axis = UP)
        anims = [obj.animate.rotate_in_place(-90 * DEGREES, axis = UP) for obj in fourmore]
        self.play(
            LaggedStart(*anims, run_time = 2, lag_ratio = 0.5)
        )
        self.wait()

        hcoins = VGroup(*[get_coin("H") for i in range(2)])
        fwdanim, rseanim = [], []
        for tcoin, k in zip(hcoins, [0, -1]):
            tcoin.move_to(fourmore[k])
            rseanim += [RotatingFadeOutAndShift(tcoin, DOWN), RotatingFadeInFrom(fourmore[k], UP)]
            fwdanim += [RotatingFadeOutAndShift(fourmore[k], DOWN), RotatingFadeInFrom(tcoin, UP)]
        self.play(*fwdanim)
        self.wait(0.5)
        self.play(*rseanim)
        self.wait()

        tcoins = VGroup(*[get_coin("T") for i in range(3)])
        fwdanim, rseanim = [], []
        for tcoin, k in zip(tcoins, [0, 2, 3]):
            tcoin.move_to(fourmore[k])
            rseanim += [RotatingFadeOutAndShift(tcoin, DOWN), RotatingFadeInFrom(fourmore[k], UP)]
            fwdanim += [RotatingFadeOutAndShift(fourmore[k], DOWN), RotatingFadeInFrom(tcoin, UP)]
        self.play(*fwdanim)
        self.wait(0.5)
        self.play(*rseanim)
        self.wait()

        self.wait(3)


class WinRatio(Scene):
    def construct(self):
        samspace = VGroup()
        n, a, b = 4, 2, 3
        cnts = [VGroup() for i in range(n + 1)]
        for k in range(1 << n):
            kk = k
            tgrp = VGroup()
            jcnt = 0
            for i in range(n):
                j = kk % 2
                jcnt += j
                if j:
                    tgrp.add(get_coin("H").scale(1 / 2))
                else:
                    tgrp.add(get_coin("T").scale(1 / 2))
                kk >>= 1
            tgrp.arrange(RIGHT, buff = -0.125)
            samspace.add(tgrp.copy())
            cnts[jcnt].add(tgrp.copy())

        Group(
            *[
                Group(*samspace[i : i + n]).arrange(DOWN)
                for i in range(0, 1 << n, n)
            ]
        ).arrange(RIGHT, buff = 1)

        for obj in cnts:
            obj.scale(7 / 8)
            Group(*obj).arrange(DOWN, buff = -0.05)

        self.play(LaggedStart(*[GrowFromCenter(obj) for obj in samspace]))
        self.wait()
        self.play(samspace.animate.shift(2.25 * UP))
        boundbox = SurroundingRectangle(samspace, buff = MED_SMALL_BUFF)
        self.play(ShowCreation(boundbox))
        self.wait()

        playerlables = VGroup(
            MathTex("\\mathbb{P}(\\text{A Wins})=").scale(1.375),
            MathTex("\\mathbb{P}(\\text{B Wins})=").scale(1.375),
        )

        labels = VGroup(
            MathTex(r"\binom{4}{4}q^4"),
            MathTex(r"\binom{4}{3}q^3p"),
            MathTex(r"\binom{4}{2}p^2q^2"),
            MathTex(r"\binom{4}{3}p^3q"),
            MathTex(r"\binom{4}{4}p^4")
        )
        for obj in cnts:
            obj.shift(1 * DOWN)
        for obj, k in zip(cnts, range(-2, 2 + 1)):
            obj.shift(k * 2 * RIGHT)
        for k in range(n + 1):
            labels[k].next_to(cnts[k], DOWN)
        playerlables[0].next_to(cnts[2], LEFT)

        self.play(Write(playerlables[0]))
        self.wait()
        for k in range(a, n + 1):
            self.play(TransformFromCopy(samspace, cnts[k]), Write(labels[k]))
            self.wait()
        self.wait()

        self.play(
            FadeOutAndShift(boundbox, UP),
            FadeOutAndShift(samspace, UP),
            VGroup(playerlables[0], *labels[2:], *cnts[2:]).animate.shift(3 * UP)
        )

        playerlables[1].move_to(playerlables[0]).shift(3 * DOWN)
        cnts[1].next_to(playerlables[1], RIGHT)
        cnts[0].match_y(cnts[1]).match_x(cnts[3])

        psign = VGroup(MathTex("+"), MathTex("+"), MathTex("+"))
        psign[0].move_to((cnts[2].get_center() + cnts[3].get_center()) / 2)
        psign[1].move_to((cnts[3].get_center() + cnts[4].get_center()) / 2)
        psign[-1].move_to((cnts[0].get_center() + cnts[1].get_center()) / 2)

        self.play(
            *[Write(obj) for obj in [playerlables[1], psign[:2]]],
            *[txt.animate.scale_in_place(7 / 8).move_to(obj) for txt, obj in zip(labels[2:], cnts[2:])],
            *[FadeOut(obj) for obj in cnts[2:]]
        )
        self.play(Write(cnts[1]), Write(cnts[0]))
        self.wait()

        for txt, obj in zip(labels[:2], cnts[:2]):
            txt.scale_in_place(7 / 8)
            txt.move_to(obj)

        self.play(
            *[FadeOut(obj) for obj in cnts[:2]],
            *[Write(obj) for obj in labels[:2]],
            Write(psign[2])
        )
        self.wait()

        for txt, obj in zip(labels, cnts):
            obj.move_to(txt)
        self.play(
            *[FadeIn(obj) for obj in cnts],
            FadeOut(labels)
        )

        self.wait(3)


class ThreeOutcomes(Scene):
    def construct(self):
        h, t, d = get_coin("W"), get_coin("L"), get_coin("D")
        for obj in [h, t, d]:
            obj.scale(2)
        h.shift(3 * LEFT)
        t.shift(3 * RIGHT)
        self.play(
            RotatingFadeInFrom(h, UP),
            RotatingFadeInFrom(t, UP)
        )
        self.wait()

        self.play(RotatingFadeInFrom(d, DOWN))
        self.wait()

        self.play(FadeOutAndShift(VGroup(h, t, d)))
        self.wait()

        randomresult = VGroup()
        rows, cols = 6, 10
        for k in range(rows * cols):
            r = random.random()
            if r < 1 / 3:
                res = "W"
            elif r < 2 / 3:
                res = "D"
            else:
                res = "L"
            randomresult.add(get_coin(res).scale(2 / 3))
        randomresult.arrange_in_grid(rows, cols)
        rperm = np.random.permutation(rows * cols)

        anims = []
        for k in rperm:
            anims += [RotatingFadeInFrom(randomresult[k], UP)]

        self.play(LaggedStart(*anims, run_time = 2))
        self.wait()
        self.play(FadeOut(randomresult))
        self.wait()

        gameprobs = VGroup(
            MathTex("\\mathbb{P}(\\text{A wins game})=p"),
            Tex(","),
            MathTex("\\mathbb{P}(\\text{B wins game})=q"),
            Tex(","),
            MathTex("\\mathbb{P}(\\text{draw})=r")
        )
        gameprobs.arrange(RIGHT)
        gameprobs.to_edge(UP)
        gamehist = VGroup(
            Tex("A needs $a$ more wins"),
            Tex("and"),
            Tex("B needs $b$ more wins"),
        )
        gamehist.arrange(RIGHT)
        gamehist.next_to(gameprobs, DOWN, buff = LARGE_BUFF)
        Asprob = MathTex("\\mathbb{P}(\\text{A wins}) = \\sum_{l=0}^{b-1}\\sum_{d=0}^\\infty \\binom{a-1+d+l}{a-1,d,l}p^aq^lr^d").scale(1.25)
        Asprob.move_to(DOWN)

        for k in [2, 22, 29, 37, 38]:
            Asprob[0][k].set_color(BLUE)
        for k in [9, 13, 28, 35, 39, 40]:
            Asprob[0][k].set_color(RED)
        for k in [18, 26, 33, 41, 42]:
            Asprob[0][k].set_color(YELLOW)
        for k in [2, 13]:
            gameprobs[0][0][k].set_color(BLUE)
            gameprobs[2][0][k].set_color(RED)
        gameprobs[4][0][8].set_color(YELLOW)
        for k in [0, 6]:
            gamehist[0][0][k].set_color(BLUE)
            gamehist[2][0][k].set_color(RED)

        for txt in [gameprobs, gamehist, Asprob]:
            self.play(Write(txt))
            self.wait()
        
        dontwant = Cross(Asprob).scale_in_place(7 / 8).rotate_in_place(5 * DEGREES)
        self.play(Write(dontwant))

        self.wait()


class PreviousCase(Scene):
    def construct(self):
        gameprobs = VGroup(
            MathTex("\\mathbb{P}(\\text{A wins game})=p"),
            Tex(","),
            MathTex("\\mathbb{P}(\\text{B wins game})=q"),
        )
        gameprobs.arrange(RIGHT)
        gameprobs.shift(3 * UP)
        matchlabels = VGroup(
            MathTex("\\mathbb{P}(A\\text{ wins match})="),
            MathTex("\\mathbb{P}(B\\text{ wins match})="),
        )
        matchlabels.arrange(RIGHT)
        matchlabels.shift(1.5 * UP)
        matchprobs = VGroup(
            MathTex("\\sum_{k=0}^{b-1}\\binom{a+k-1}{k}p^aq^k"),
            MathTex("+"),
            MathTex("\\sum_{k=0}^{a-1}\\binom{b+k-1}{k}q^bp^k"),
            MathTex("="),
            MathTex("1")
        )

        acolor, bcolor = BLUE, RED
        for k in [2, 13]:
            gameprobs[0][0][k].set_color(acolor)
            gameprobs[2][0][k].set_color(bcolor)
        matchlabels[0][0][2].set_color(acolor)
        matchlabels[1][0][2].set_color(bcolor)
        for k in [8, 15, 16]:
            matchprobs[0][0][k].set_color(acolor)
            matchprobs[2][0][k].set_color(bcolor)
        for k in [0, 17, 18]:
            matchprobs[0][0][k].set_color(bcolor)
            matchprobs[2][0][k].set_color(acolor)

        Awingp = VGroup(matchlabels[0], matchprobs[0].copy())
        Awingp.scale_in_place(1.25)
        Awingp.arrange(RIGHT)
        Awingp.shift(2 * UP)
        Bwingp = VGroup(matchlabels[1], matchprobs[2].copy())
        Bwingp.scale_in_place(1.25)
        Bwingp.arrange(RIGHT)
        Bwingp.shift(2 * DOWN)
        self.play(Write(Awingp), Write(Bwingp), run_time = 2)
        self.wait()

        for txt in matchprobs:
            txt.scale_in_place(1.1875)
        matchprobs.arrange(RIGHT)

        self.play(
            FadeOut(matchlabels),
            ReplacementTransform(VGroup(Awingp[1], Bwingp[1]), matchprobs)
        )
        self.wait()

        sumtoone = VGroup(
            Tex("as long as "),
            MathTex("p+q=1"),
        )
        sumtoone.arrange(RIGHT)
        sumtoone[1][0][0].set_color(acolor)
        sumtoone[1][0][2].set_color(bcolor)
        sumtoone.shift(2 * DOWN)
        self.play(Write(sumtoone))
        self.wait()
        self.play(
            matchprobs.animate.shift(2 * UP),
            sumtoone.animate.shift(2 * UP),
        )
        self.wait()

        evenif = Tex("...even if $p$ and $q$ are negative or greater than 1!").scale(1.125).shift(2 * DOWN)
        evenif[0][9].set_color(BLUE)
        evenif[0][13].set_color(RED)
        self.play(Write(evenif))
        self.wait()

        '''tempgrp = VGroup()
        for grp in [gameprobs, matchlabels, matchprobs]:
            for txt in grp:
                tempgrp.add(TextPosition(txt[0]))
        self.add(tempgrp)'''

        self.play(FadeOut(evenif), FadeOut(sumtoone), FadeOut(matchprobs))
        self.wait()

        aspers = Tex("Player A's perspective..").scale(1.5)
        aspers[0][6].set_color(BLUE)
        aspersline = Underline(aspers)
        aspergp = VGroup(aspers, aspersline)
        self.play(Write(aspergp))
        self.play(aspergp.animate.to_edge(UP))
        self.wait()

        aprobs = VGroup(
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=p"),
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=q"),
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=r")
        )
        for txt in aprobs:
            txt.scale_in_place(1.5)
        aprobs.arrange(RIGHT, buff = 1.5)

        coins = VGroup(get_coin("W"), get_coin("L"), get_coin("D"))
        for k in range(3):
            coins[k].scale(15 / 20)
            coins[k].move_to((aprobs[k][0][1].get_center() + aprobs[k][0][2].get_center()) / 2)
            aprobs.add(coins[k])
        aprobs.shift(1.5 * UP)
        self.play(Write(aprobs))
        self.wait()

        steps = VGroup(
            MathTex("p + q + r = 1"),
            MathTex("p + q = 1 - r"),
            MathTex("\\frac{p}{1-r}", "+", "\\frac{q}{1-r}", "=1")
        )
        for txt in steps:
            txt.scale(1.5)
        steps.shift(DOWN)
        
        self.play(Write(steps[0]))
        self.wait()
        self.play(FadeOut(steps[0]), FadeIn(steps[1]))
        self.wait()
        self.play(FadeOutAndShift(steps[1], RIGHT), FadeIn(steps[2]))
        self.wait()

        surrrects = VGroup(
            SurroundingRectangle(steps[2][0]),
            SurroundingRectangle(steps[2][2]),
        )
        self.play(ShowCreation(surrrects))
        self.wait()

        self.play(
            FadeOutAndShift(aspergp, UP),
            FadeOutAndShift(aprobs, UP),
            FadeOutAndShift(steps[2], DOWN),
            FadeOutAndShift(surrrects, DOWN)
        )

        modimatchprobs = VGroup(
            MathTex("\\mathbb{P}(A\\text{ wins match})=\\sum_{k=0}^{b-1}\\binom{a+k-1}{k}\\left(\\frac{p}{1-r}\\right)^a\\left(\\frac{q}{1-r}\\right)^k"),
            MathTex("\\mathbb{P}(B\\text{ wins match})=\\sum_{k=0}^{a-1}\\binom{b+k-1}{k}\\left(\\frac{q}{1-r}\\right)^b\\left(\\frac{p}{1-r}\\right)^k"),
        )
        modimatchprobs.arrange(DOWN, buff = 2.5)

        for k in [2, 22, 30, 36]:
            modimatchprobs[0][0][k].set_color(BLUE)
            modimatchprobs[1][0][k].set_color(RED)
        for k in [14, 38]:
            modimatchprobs[0][0][k].set_color(RED)
            modimatchprobs[1][0][k].set_color(BLUE)
        for k in [34, 42]:
            modimatchprobs[0][0][k].set_color(YELLOW)
            modimatchprobs[1][0][k].set_color(YELLOW)
        
        anims = []
        coingp = VGroup()
        for k in range(17):
            r = random.random()
            if r < 1 / 3:
                res = "W"
            elif r < 2 / 3:
                res = "D"
            else:
                res = "L"
            tempcoin = get_coin(res).scale(2 / 3)
            coingp.add(tempcoin)
            if r < 1 / 3:
                #anims += [RotatingFadeInFrom(tempcoin, UP)]
                anims += [GrowFromCenter(tempcoin)]
            elif r < 2 / 3:
                anims += [GrowFromCenter(tempcoin)]
            else:
                #anims += [RotatingFadeInFrom(tempcoin, DOWN)]
                anims += [GrowFromCenter(tempcoin)]
        coinlist = [obj for obj in coingp]
        random.shuffle(coinlist)
        coingp.add(*coinlist)
        coingp.arrange(RIGHT)

        self.play(
            Write(modimatchprobs),
            LaggedStart(*anims, run_time = 2)
        )
        self.wait()

        self.play(
            FadeOutAndShift(modimatchprobs[0], UP),
            FadeOutAndShift(modimatchprobs[1], DOWN),
            FadeOut(coingp)
        )
        self.wait()

        amodprob = steps[2][0]
        amodprob.move_to(ORIGIN)
        amodprob[0].set_color(BLUE)
        amodprob[-1].set_color(YELLOW)
        self.play(Write(amodprob))
        self.play(amodprob.animate.to_corner(UL))
        self.wait()
        seriesform = MathTex("=p+rp+r^2p+r^3p+r^4p+\\cdots").scale(1.5)
        seriesform.next_to(amodprob, RIGHT)
        for k in [1, 4, 8, 12, 16]:
            seriesform[0][k].set_color(BLUE)
        for k in [3, 6, 10, 14]:
            seriesform[0][k].set_color(YELLOW)
        self.play(Write(seriesform))
        self.wait()

        coinscale = 2 / 3
        modiprobgp = VGroup(VGroup(get_coin("W").scale(coinscale).shift(1.75 * UP)))
        p = 0
        #animlist = [FadeInFrom(modiprobgp[0], UP)]
        animlist = [FadeInFrom(modiprobgp[0], RIGHT)]
        for k in range(1, 8 + 1):
            tempgp = VGroup()
            for j in range(k):
                tempgp.add(get_coin("D").scale(coinscale))
            tempgp.add(get_coin("W").scale(coinscale))
            tempgp.arrange(RIGHT)
            tempgp.move_to(modiprobgp[k - 1].get_center())
            tempgp.shift(0.75 * DOWN)
            #animlist += [FadeInFrom(tempgp, UP)]
            p = 1 - p
            animlist += [FadeInFrom(tempgp, LEFT if p else RIGHT)]
            modiprobgp.add(tempgp)
        self.play(LaggedStart(*animlist, lag_ratio = 0.5))
        self.wait(5)


class WhatIfWeDont(Scene):
    def construct(self):
        aprobs = VGroup(
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=", "p"),
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=", "q"),
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=", "r")
        )
        for txt in aprobs:
            txt.scale_in_place(1.5)
        aprobs.arrange(RIGHT, buff = 1.5)

        coins = VGroup(get_coin("W"), get_coin("L"), get_coin("D"))
        for k in range(3):
            coins[k].scale(15 / 20)
            coins[k].move_to((aprobs[k][0][1].get_center() + aprobs[k][0][2].get_center()) / 2)
            aprobs.add(coins[k])
        aprobs.shift(1.5 * UP)
        self.play(Write(aprobs))
        self.wait()

        quesmark = MathTex("?").scale_in_place(1.5)
        anims = []
        for k in range(3):
            anims += [Transform(aprobs[k][-1], quesmark.copy().next_to(aprobs[k][0]))]
        self.play(*anims)
        self.wait()

        def dirichrect(w, d, l):
            dirirect = VGroup()
            for dim, col in zip([w, d, l], [BLUE, YELLOW, RED]):
                rect = Rectangle(color = col, fill_opacity = 0.5)
                rect.stretch_to_fit_height(1 / 3)
                rect.stretch_to_fit_width(dim)
                dirirect.add(rect)
            #dirirect.stretch_to_fit_width(3)
            dirirect.scale(3)
            dirirect.arrange(RIGHT, buff = 1 / 30)
            dirirect.move_to(ORIGIN).shift(2 * DOWN)
            return dirirect
        
        def get_dirichlet(shuffle_time = 2, total_time = 3, change_rate = 0.05, h_buff = 0.1, v_buff = 0.1):
            res = VGroup(get_coin("W"), dirichrect(1, 1, 1).shift(2 * DOWN))
            res.time = 0
            res.lctime = 0
            
            def update(res, dt):
                res.time += dt
                t = res.time
                change = all([
                    (t % total_time) < shuffle_time,
                    res.time - res.lctime > change_rate])
                if change:
                    old_rectgp = res[1]
                    params = []
                    for obj in old_rectgp:
                        params += [obj.width]
                    dvar = np.random.dirichlet(params)
                    r = random.random()
                    print(params, dvar, r)
                    newcoin = get_coin("W") if r < dvar[0] else (get_coin("D") if r < dvar[0] + dvar[1] else get_coin("L"))
                    if r < dvar[0]:
                        params[0] += 1
                    elif r < dvar[0] + dvar[1]:
                        params[1] += 1
                    else:
                        params[2] += 1
                    newrect = dirichrect(*params).stretch_to_fit_width(3).shift(2 * DOWN)
                    newrrect = dirichrect(*params).stretch_to_fit_width(1)
                    res[0].become(newcoin)
                    res[1].become(newrect)
                    res.lctime = res.time
            res.add_updater(update)
            return res
        
        wwid = ValueTracker(1)
        dwid = ValueTracker(1)

        def update(obj):
            ww = (0.2 + random.random() * 0.3) * np.cos(np.sqrt(17 * wwid.get_value()))
            dd = (0.3 + random.random() * 0.2) * np.sin(np.sqrt(13 * dwid.get_value()))
            newobj = dirichrect(1 + ww, 1 + dd, 1 - ww - dd)
            obj.become(newobj)
        
        drect = dirichrect(1, 1, 1)
        coincpy = VGroup(MathTex("p"), MathTex("r"), MathTex("q"))
        for k in range(3):
            coincpy[k].scale(2)
            coincpy[k].next_to(drect[k], UP)
        self.play(Write(drect), Write(coincpy))

        self.play(
            wwid.animate.set_value(1234),
            dwid.animate.set_value(4321),
            UpdateFromFunc(drect, update),
            rate_func = linear, run_time = 10
        )

        self.wait()


class ProbabilityDensity(Scene):
    def construct(self):
        aprobs = VGroup(
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=", "p"),
            MathTex("\\mathbb{P}(\\hspace{0.25cm})=", "q"),
        )
        for txt in aprobs:
            txt.scale_in_place(1.5)
        aprobs.arrange(RIGHT, buff = 2)
        for k in range(2):
            aprobs[k][1].set_color(RED if k else BLUE)

        coins = VGroup(get_coin("W"), get_coin("L"))
        for k in range(2):
            coins[k].scale(15 / 20)
            coins[k].move_to((aprobs[k][0][1].get_center() + aprobs[k][0][2].get_center()) / 2)
            aprobs.add(coins[k])
        aprobs.shift(2 * UP)
        self.play(Write(aprobs))
        self.wait()

        randvars = VGroup(
            MathTex("0 \\leq"),
            MathTex("P,Q"),
            MathTex("\\leq 1"),
            Tex(" and "),
            MathTex("P+Q=1")
        )
        randvars[1][0][0].set_color(BLUE)
        randvars[1][0][2].set_color(RED)
        randvars[4][0][0].set_color(BLUE)
        randvars[4][0][2].set_color(RED)
        for txt in randvars:
            txt.scale(1.25)
        randvars.arrange(RIGHT)
        self.play(
            *[Write(randvars[k]) for k in [0, 2, 3, 4]],
            TransformFromCopy(VGroup(aprobs[0][1], aprobs[1][1]), randvars[1])
        )
        self.wait()

        densityfunc = VGroup(MathTex("f_{P,Q}(p,q)"), MathTex("="), MathTex("1"))
        for txt in densityfunc:
            txt.scale(1.25)
        densityfunc.arrange(RIGHT)
        densityfunc.shift(2 * DOWN)
        densityfunc[0][0][1].set_color(BLUE)
        densityfunc[0][0][5].set_color(BLUE)
        densityfunc[0][0][3].set_color(RED)
        densityfunc[0][0][7].set_color(RED)
        self.play(Write(densityfunc))
        self.wait()

        self.play(
            FadeOut(aprobs),
            FadeOut(randvars),
            densityfunc.animate.shift(4.5 * UP))
        self.wait()

        fwinprob = VGroup(MathTex("\\mathbb{P}(\\hspace{0.25cm}|p,q)=p").scale(1.5), get_coin("W").scale(1 / 2))
        fwin = get_coin("W")
        fwinprob.move_to(densityfunc).shift(2 * DOWN)
        fwin.move_to(fwinprob).shift(5 * LEFT)
        fwinprob[1].next_to(fwinprob[0][0][1], RIGHT, buff = -0)
        fwinprob[0][0][3].set_color(BLUE)
        fwinprob[0][0][5].set_color(RED)
        fwinprob[0][0][8].set_color(BLUE)
        self.play(RotatingFadeInFrom(fwin, UP), Write(fwinprob)) 
        self.wait()

        bayes1 = VGroup(
            MathTex("f_{P,Q}(p,q|00)", tex_to_color_map={"00": WHITE}),
            MathTex("="),
            MathTex("\\mathbb{P}(00|p,q)", tex_to_color_map={"00": WHITE}),
            MathTex("f_{P,Q}(p,q)"),
            MathTex("\\mathbb{P}(00)", tex_to_color_map={"00": WHITE})
        )
        bayes1[0][0][1].set_color(BLUE)
        bayes1[0][0][5].set_color(BLUE)
        bayes1[0][0][3].set_color(RED)
        bayes1[0][0][7].set_color(RED)
        bayes1[2][2][1].set_color(BLUE)
        bayes1[2][2][3].set_color(RED)
        bayes1[3][0][1].set_color(BLUE)
        bayes1[3][0][5].set_color(BLUE)
        bayes1[3][0][3].set_color(RED)
        bayes1[3][0][7].set_color(RED)
        for txt in bayes1:
            txt.scale(1.25)
        for k in [0, 2, 4]:
            tex = bayes1[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        bayes1[:-1].arrange(RIGHT)
        bayes1.move_to(fwinprob).shift(2 * DOWN)
        bayes1[-1].move_to((bayes1[2].get_center() + bayes1[3].get_center()) / 2)
        bayes1[-1].shift(1 * DOWN)
        denomline = Line(bayes1[2].get_left(), bayes1[3].get_right()).shift(0.5 * DOWN)
        self.play(Write(bayes1), Write(denomline))
        self.wait()

        surecdenom = SurroundingRectangle(bayes1[-1])
        for k in range(5):
            self.play(ShowCreationThenDestruction(surecdenom))
            self.wait(0.5)
        self.wait(0.5)

        propto = MathTex("\\propto").scale(1.25).move_to(bayes1[1])

        self.play(
            FadeOut(VGroup(denomline, bayes1[-1])),
            Transform(bayes1[1], propto)
        )

        arrows = VGroup(
            Arrow(fwinprob[0][0][-1].get_bottom(), bayes1[2].get_top()),
            CurvedArrow(densityfunc.get_right(), bayes1[3].get_top(), angle = -90 * DEGREES)
        )
        self.play(FadeIn(arrows))
        self.wait()

        ndenfuncrhs = VGroup(fwinprob[0][0][-1].copy().move_to(bayes1[2]), densityfunc[-1].copy().move_to(bayes1[3]))
        self.play(
            FadeOut(bayes1[2]),
            FadeOut(bayes1[3]),
            FadeIn(ndenfuncrhs)
        )
        self.wait()

        upddenfunc = VGroup(bayes1[0], bayes1[1], ndenfuncrhs[0])
        self.play(
            *[FadeOut(obj) for obj in [arrows, ndenfuncrhs[-1], fwinprob, densityfunc, fwin]],
            upddenfunc.animate.arrange(RIGHT)
        )

        self.wait(5)


class BWinsSecond(Scene):
    def construct(self):
        firstdensity = VGroup(
            MathTex("f_{P,Q}(p,q|00)", tex_to_color_map={"00": WHITE}),
            MathTex("\\propto"),
            MathTex("p"),
        )
        firstdensity[0][0][1].set_color(BLUE)
        firstdensity[0][0][5].set_color(BLUE)
        firstdensity[0][0][3].set_color(RED)
        firstdensity[0][0][7].set_color(RED)
        firstdensity[-1].set_color(BLUE)
        for txt in firstdensity:
            txt.scale(1.25)
        for k in [0]:
            tex = firstdensity[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        firstdensity.arrange(RIGHT)
        self.add(firstdensity)

        self.play(firstdensity.animate.shift(3 * UP))
        self.wait()

        bayes = VGroup(
            MathTex("f_{P,Q}(p,q|0022)", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("\\propto"),
            MathTex("f_{P,Q}(22|p,q,00)", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("f_{P,Q}(p,q|00)", tex_to_color_map = {"00": BLUE, "22": RED}),
        )
        for txt in bayes:
            txt.scale(1.25)
        bayes[0][0][1].set_color(BLUE)
        bayes[0][0][5].set_color(BLUE)
        bayes[0][0][3].set_color(RED)
        bayes[0][0][7].set_color(RED)
        bayes[2][0][1].set_color(BLUE)
        bayes[2][-3][1].set_color(BLUE)
        bayes[2][0][3].set_color(RED)
        bayes[2][-3][3].set_color(RED)
        bayes[3][0][1].set_color(BLUE)
        bayes[3][0][5].set_color(BLUE)
        bayes[3][0][3].set_color(RED)
        bayes[3][0][7].set_color(RED)
        bayes.arrange(RIGHT)

        for k in [0, 2, 3]:
            tex = bayes[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0, 2]:
            tex = bayes[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        
        '''for txt in bayes:
            self.add(TextPosition(txt[0]))'''

        self.play(Write(bayes))
        self.wait()

        bayesrhs = VGroup(
            MathTex("q").scale(1.25).move_to(bayes[2]).set_color(RED),
            MathTex("p").scale(1.25).move_to(bayes[3]).set_color(BLUE),
        )
        self.play(Transform(bayes[2], bayesrhs[0]))
        self.wait()
        self.play(Transform(bayes[3], bayesrhs[1]))
        self.wait()
        self.play(bayes.animate.arrange(RIGHT))
        self.wait()
        self.play(bayes.animate.shift(1 * UP))
        self.wait()

        goeson = MathTex("\\vdots").scale(1.5).shift(0.25 * DOWN)
        self.play(Write(goeson))
        self.wait()

        arrows = VGroup(
            CurvedArrow(firstdensity[0][1].get_bottom() + 0.1 * DOWN, firstdensity[2].get_bottom()).set_color(BLUE),
            CurvedArrow(bayes[0][-1].get_bottom() + 0.25 * LEFT, bayes[2].get_bottom()).set_color(RED)
        )
        self.play(ShowCreation(arrows[0]))
        self.wait()
        self.play(ShowCreation(arrows[1]))
        self.wait()

        ngamesdensity = VGroup(
            MathTex("f_{P,Q}(p,q|00^k22^{n-k})", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("\\propto"),
            MathTex("p^kq^{n-k}")
        )
        ngamesdensity[0][0][1].set_color(BLUE)
        ngamesdensity[0][0][5].set_color(BLUE)
        ngamesdensity[0][0][3].set_color(RED)
        ngamesdensity[0][0][7].set_color(RED)
        ngamesdensity[2][0][0].set_color(BLUE)
        ngamesdensity[2][0][2].set_color(RED)
        for txt in ngamesdensity:
            txt.scale(1.25)
        ngamesdensity.arrange(RIGHT)
        ngamesdensity.next_to(goeson, DOWN, buff = LARGE_BUFF)

        for k in [0]:
            tex = ngamesdensity[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = ngamesdensity[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)

        self.play(Write(ngamesdensity))
        self.wait()

        '''for txt in ngamesdensity:
            self.add(TextPosition(txt[0]))'''

        self.play(
            *[FadeOut(obj) for obj in [firstdensity, bayes, goeson, arrows]],
            ngamesdensity.animate.move_to(ORIGIN),
        )
        self.play(ngamesdensity.animate.scale(1.75 / 1.25))

        self.wait(3)


class BetaDistribution(Scene):
    def construct(self):
        ngamesdensity = VGroup(
            MathTex("f_{P,Q}(p,q|00^k22^{n-k})", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("\\propto"),
            MathTex("p^kq^{n-k}")
        )
        ngamesdensity[0][0][1].set_color(BLUE)
        ngamesdensity[0][0][5].set_color(BLUE)
        ngamesdensity[0][0][3].set_color(RED)
        ngamesdensity[0][0][7].set_color(RED)
        ngamesdensity[2][0][0].set_color(BLUE)
        ngamesdensity[2][0][2].set_color(RED)
        for txt in ngamesdensity:
            txt.scale(1.75)
        ngamesdensity.arrange(RIGHT)

        for k in [0]:
            tex = ngamesdensity[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = ngamesdensity[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        
        self.add(ngamesdensity)

        betalabel = VGroup(MathTex("\\text{Beta Distribution}").scale(2))
        uline = Underline(betalabel[0])
        betalabel.add(uline)
        betalabel.to_edge(UP)

        self.play(Write(betalabel))
        self.wait()
        self.play(FadeOutAndShift(ngamesdensity, DOWN))
        self.wait()

        betadensity = VGroup(
            MathTex("X,Y\\sim \\text{Beta}(\\alpha, \\beta)"),
            MathTex(";"),
            MathTex("f_{X,Y}(x,y)=\\frac{1}{\\text{B}(\\alpha,\\beta)}x^{\\alpha - 1} y^{\\beta - 1}")
        )
        betadensity.arrange(RIGHT)
        betadensity[0][0][0].set_color(BLUE)
        betadensity[0][0][9].set_color(BLUE)
        betadensity[0][0][2].set_color(RED)
        betadensity[0][0][11].set_color(RED)
        for k in [1, 5, 14, 18, 19]:
            betadensity[2][0][k].set_color(BLUE)
        for k in [3, 7, 16, 20, 21]:
            betadensity[2][0][k].set_color(RED)
        self.play(Write(betadensity))
        self.wait()
        
        rel = MathTex("X+Y=1").scale(1.25)
        rel[0][0].set_color(BLUE)
        rel[0][2].set_color(RED)
        rel.next_to(betadensity, DOWN, buff = 1)
        self.play(Write(rel))
        self.wait()

        singlevar = VGroup(
            MathTex("X\\sim \\text{Beta}(\\alpha, \\beta)"),
            MathTex("f_X(x)=\\frac{1}{\\text{B}(\\alpha,\\beta)}x^{\\alpha - 1} (1-x)^{\\beta - 1}")
        )
        singlevar[0][0][0].set_color(BLUE)
        singlevar[0][0][7].set_color(BLUE)
        singlevar[0][0][9].set_color(RED)
        singlevar[0].move_to(betadensity[0])
        singlevar[1].move_to(betadensity[2])

        for k in [1, 3, 10, 14, 15, 21]:
            singlevar[1][0][k].set_color(BLUE)
        for k in [12, 23]:
            singlevar[1][0][k].set_color(RED)
        
        self.play(
            Transform(betadensity[0], singlevar[0]),
            Transform(betadensity[2], singlevar[1]),
        )
        self.play(betadensity.animate.arrange(RIGHT))
        self.wait()
        self.play(
            betadensity.animate.next_to(betalabel, DOWN, buff = 0.5),
            FadeOut(rel)
        )

        alp, bet = ValueTracker(1), ValueTracker(2)
        alpval, betval = DecimalNumber(alp.get_value()).set_color(BLUE_E), DecimalNumber(bet.get_value()).set_color(RED_E)
        alpgrp = VGroup(MathTex("\\alpha").set_color(BLUE), MathTex("="), alpval)
        for txt in alpgrp:
            txt.scale(1.25)
        alpgrp.arrange(RIGHT)
        betgrp = VGroup(MathTex("\\beta").set_color(RED), MathTex("="), betval)
        for txt in betgrp:
            txt.scale(1.25)
        betgrp.arrange(RIGHT)
        betgrp.next_to(alpgrp, DOWN)
        vargrp = VGroup(alpgrp, betgrp)
        vargrp.shift(1.25 * DOWN + 4 * RIGHT)
        grphframe = Square(side_length = 4)
        grphaxes = VGroup()
        grphlabels = VGroup(
            MathTex("0"),
            MathTex("1"),
            MathTex("0"),
            MathTex("1"),
            MathTex("2"),
            MathTex("f_X(x)"),
        )
        grphlabels[5].rotate(90 * DEGREES)
        for k in [1, 3]:
            grphlabels[5][0][k].set_color(BLUE)
        for k in range(1, 4):
            grphaxes.add(DashedLine(ORIGIN, 4 * UP).fade(0.875).shift(k * RIGHT))
            grphaxes.add(DashedLine(ORIGIN, 4 * RIGHT).fade(0.875).shift(k * UP))
        grphframe.set_color(GREY)
        grphframe.shift(1.25 * DOWN)
        grphaxes.move_to(grphframe)
        grphlabels[0].next_to(grphframe.get_corner(DL), DOWN, buff = SMALL_BUFF)
        grphlabels[1].next_to(grphframe.get_corner(DR), DOWN, buff = SMALL_BUFF)
        grphlabels[2].next_to(grphframe.get_corner(DL), LEFT, buff = SMALL_BUFF)
        grphlabels[3].next_to(grphframe.get_left(), LEFT, buff = SMALL_BUFF)
        grphlabels[4].next_to(grphframe.get_corner(UL), LEFT, buff = SMALL_BUFF)
        grphlabels[5].next_to(grphlabels[3].get_left(), LEFT, buff = MED_SMALL_BUFF)

        def betacreator(m, n, col = RED):
            gr = ParametricFunction(lambda t: np.array([t, min(2, t ** (m - 1) * (1 - t) ** (n - 1) / sc.beta(m, n)) / 2, 0]), t_min = 0.001, t_max = 1 - 0.001, color = col, step_size = 0.01 / 8)
            gr.scale_about_point(4, ORIGIN)
            gr.shift(1.25 * DOWN + 2 * DL)
            res = VGroup(grphaxes, grphlabels, gr, grphframe)
            return res

        def betaupdater(obj):
            newobj = betacreator(alp.get_value(), bet.get_value())
            obj.become(newobj)
        
        betacurve = betacreator(alp.get_value(), bet.get_value())
        self.play(ShowCreation(betacurve), Write(vargrp))
        self.wait()

        for a, b, col in zip([2, 5, 1 / 2, 1], [2, 3 / 2, 1 / 2, 1], [GREEN, PINK, YELLOW, WHITE]):
            self.play(
                betacurve.animate.become(betacreator(a, b, col)),
                #Transform(betacurve, betacreator(a, b, col)),
                ChangeDecimalToValue(alpval, a), ChangeDecimalToValue(betval, b),
            )
            self.wait()

        self.wait(3)


class MatchHistWithBeta(Scene):
    def construct(self):
        txtsc = 1.5
        titles = VGroup(
            MathTex("\\text{Match}"),
            MathTex("\\text{density function}"),
            MathTex("\\text{Beta}"),
        )
        for txt in titles:
            txt.scale(1.5)
        titles[1].to_edge(UP)
        titles[0].move_to(titles[1]).to_edge(LEFT)
        titles[2].move_to(titles[1]).to_edge(RIGHT)
        titles[0].shift(0.5 * RIGHT)
        titles[2].shift(1 * LEFT)
        
        self.play(Write(titles))
        self.wait()

        densities = VGroup(
            MathTex("f(p,q)=1"),
            MathTex("f(p,q| 00 ) \\propto p", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("f(p,q| 00 22 ) \\propto pq", tex_to_color_map = {"00": BLUE, "22": RED}),
            MathTex("\\vdots")
        )
        for txt in densities:
            txt.scale(txtsc)
        densities.arrange(DOWN, buff = LARGE_BUFF)
        densities.shift(0.75 * DOWN)
        densities[0][0][2].set_color(BLUE)
        densities[0][0][4].set_color(RED)
        densities[1][0][2].set_color(BLUE)
        densities[1][-1][-1].set_color(BLUE)
        densities[1][0][4].set_color(RED)
        densities[2][0][2].set_color(BLUE)
        densities[2][0][4].set_color(RED)
        densities[2][-1][-2].set_color(BLUE)
        densities[2][-1][-1].set_color(RED)
        for k in [1, 2]:
            tex = densities[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [2]:
            tex = densities[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)

        betas = VGroup(
            MathTex("B(1, 1)"),
            MathTex("B(2, 1)"),
            MathTex("B(2, 2)"),
            MathTex("\\vdots")
        )
        
        for k in range(3):
            betas[k][0][2].set_color(BLUE)
            betas[k][0][-2].set_color(RED)

        for k in range(4):
            betas[k].scale(txtsc)
            betas[k].match_y(densities[k])
            betas[k].match_x(titles[2])

        matchhist = VGroup(
            MathTex("\\text{START}"),
            VGroup(get_coin("W")),
            VGroup(get_coin("W"), get_coin("L")),
            MathTex("\\vdots")
        )
        matchhist[3].scale(txtsc)
        matchhist[2].arrange(RIGHT)
        
        for k in range(4):
            matchhist[k].match_y(densities[k])
            matchhist[k].match_x(titles[0])
        
        grids = VGroup(
            Line(7 * LEFT, 7 * RIGHT).shift((densities[0].get_top() + titles[1].get_bottom()) / 2),
            Line(10 * UP, 10 * DOWN).shift((titles[0].get_right() + titles[1].get_left()) / 2),
            Line(10 * UP, 10 * DOWN).shift((titles[2].get_left() + titles[1].get_right()) / 2),
        )
        self.play(ShowCreation(grids))
        self.wait()

        for k in range(4):
            self.play(Write(matchhist[k]), Write(densities[k]), Write(betas[k]))
            self.wait()
        
        densurr = VGroup()
        for txt in densities:
            densurr.add(SurroundingRectangle(txt))
        betasurr = VGroup()
        for txt in betas:
            betasurr.add(SurroundingRectangle(txt))
        
        self.play(ShowCreation(densurr[0]), ShowCreation(betasurr[0]))
        self.wait()
        self.play(
            ReplacementTransform(densurr[0], densurr[1]),
            ReplacementTransform(betasurr[0], betasurr[1]),
        )
        self.wait()
        self.play(
            ReplacementTransform(densurr[1], densurr[2]),
            ReplacementTransform(betasurr[1], betasurr[2]),
        )

        self.wait(3)


class AandBPlaysngames(Scene):
    def construct(self):
        coingp = VGroup()
        for k in range(15):
            t = np.random.random()
            if 2 * t <= 1:
                coingp.add(get_coin("W"))
            else:
                coingp.add(get_coin("L"))
        coingp.arrange(RIGHT)
        coingp.shift(3 * UP)
        anims = []
        for coin in coingp:
            anims += [RotatingFadeInFrom(coin, DOWN)]

        self.play(LaggedStart(*anims, run_time = 2))
        self.wait()

        ngames = VGroup(MathTex("\\text{A wins }k\\text{ games}"), MathTex("\\text{B wins }n-k\\text{ games}"))
        ngames.arrange(RIGHT, buff = 2)
        ngames.next_to(coingp, DOWN)

        self.play(Write(ngames))
        self.wait()

        pqdistribution = MathTex("P,Q \\sim \\text{Beta}(k+1,n-k+1)").scale(1.5)
        pqdistribution[0][0].set_color(BLUE)
        pqdistribution[0][2].set_color(RED)
        density = MathTex("f_P(p)=\\frac{1}{B(k+1,n-k+1)}p^k (1-p)^{n-k}")
        for k in [1, 3, 20, 25]:
            density[0][k].set_color(BLUE)
        density.next_to(pqdistribution, DOWN)
        self.play(Write(pqdistribution))
        self.wait()

        self.play(Write(density))
        self.play(
            FadeOutAndShift(ngames[0], LEFT),
            FadeOutAndShift(ngames[1], RIGHT),
            pqdistribution.animate.shift(1.5 * UP),
            density.animate.shift(1.5 * UP),
        )
        self.wait()

        Awinsnextgame = VGroup(
            MathTex("\\mathbb{P}( 00 | 33 ^k 22 ^{n-k})", tex_to_color_map = {"00": BLUE, "22": RED, "33": BLUE}),
            MathTex("="),
            MathTex("\\int\\limits_0^1"),
            MathTex("P").set_color(BLUE),
            MathTex("f_P(p)\\,dp")
        )
        for txt in Awinsnextgame:
            txt.scale(1.5)
        Awinsnextgame[4][0][1].set_color(BLUE)
        Awinsnextgame[4][0][3].set_color(BLUE)
        for k in [0]:
            tex = Awinsnextgame[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = Awinsnextgame[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("33")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = Awinsnextgame[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        Awinsnextgame.arrange(RIGHT)
        Awinsnextgame.shift(2 * DOWN)

        self.play(
            Write(Awinsnextgame[0]),
            Write(Awinsnextgame[1]),
            Write(Awinsnextgame[3])
        )
        self.wait()

        self.play(
            Transform(Awinsnextgame[3], MathTex("p").scale(1.5).move_to(Awinsnextgame[3]).set_color(BLUE)),
            *[FadeIn(Awinsnextgame[k]) for k in [2, 4]]
        )
        self.wait()

        self.play(
            FadeOut(density),
            Awinsnextgame.animate.shift(1.0 * UP),
        )
        self.wait()

        rhs = MathTex("{k+1}\\over{n+2}").scale(1.5)
        bayes = Tex("Bayes' Billiards Argument").to_corner(DR).set_color(YELLOW)
        rhs.next_to(Awinsnextgame[1], RIGHT)
        self.play(
            FadeOutAndShift(Awinsnextgame[2:]),
            FadeInFrom(rhs),
            Write(bayes)
        )

        self.wait(5)


class DirichletDistribution(Scene):
    def construct(self):
        title = Tex("Dirichlet Distribution").scale(1.5)
        uline = Underline(title)
        self.play(Write(VGroup(title, uline)))
        self.play(
            VGroup(title, uline).animate.to_edge(UP)
        )
        self.wait()

        coingp = VGroup(get_coin("W"), get_coin("D"), get_coin("L"))
        coingp.arrange(RIGHT, buff = 2)
        self.play(*[GrowFromCenter(obj) for obj in coingp])
        self.wait()
        self.play(coingp.animate.shift(2 * UP))
        self.wait()

        w, d, l = Integer(1).set_color(BLUE), Integer(1).set_color(YELLOW), Integer(1).set_color(RED)
        dirich = VGroup(
            MathTex("\\text{Dir}("),
            w,
            MathTex(";"),
            d,
            MathTex(";"),
            l,
            MathTex(")")
        )
        for obj in dirich:
            obj.scale(2)
        dirich.arrange(RIGHT)
        dirich.shift(2 * DOWN)
        self.play(Write(dirich))
        self.wait()
        
        cnts = [1, 1, 1]
        for t in [0, 1, 2, 2, 1, 1, 0, 0, 0, 2]:
            coin = get_coin("W") if t == 0 else (get_coin("D") if t == 1 else get_coin("L"))
            self.play(RotatingFadeInFrom(coin, RIGHT))
            cnts[t] += 1
            self.play(
                ChangeDecimalToValue(w, cnts[0]),
                ChangeDecimalToValue(d, cnts[1]),
                ChangeDecimalToValue(l, cnts[2]),
            )
            self.play(RotatingFadeOutAndShift(coin, LEFT))
            self.wait()
        self.play(
            FadeOut(dirich),
            FadeOut(coingp[1]),
            FadeOutAndShift(coingp[0], LEFT),
            FadeOutAndShift(coingp[2], RIGHT),
        )
        self.wait()

        gamehist = VGroup(MathTex("00 ^{10} 22 ^{20} 33 ^{15}", tex_to_color_map = {"00": BLUE, "22": YELLOW, "33": RED}).scale(2))
        for k in [0]:
            tex = gamehist[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = gamehist[k]
            coin = get_coin("D")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = gamehist[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("33")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        self.play(Write(gamehist))
        self.wait()

        dirichhist = MathTex("\\text{Dir}(1 + 10, 1 + 20, 1 + 15)").scale(1.25).shift(2 * DOWN)
        self.play(Write(dirichhist))
        self.wait()

        newdiri = MathTex("W,D,L \\sim \\text{Dir}(11, 21, 16)").scale(1.5).shift(2 * UP)
        newdiri[0][0].set_color(BLUE)
        newdiri[0][2].set_color(YELLOW)
        newdiri[0][4].set_color(RED)
        newdiri[0][10:12].set_color(BLUE)
        newdiri[0][13:15].set_color(YELLOW)
        newdiri[0][16:18].set_color(RED)
        density = MathTex("f(w,d,l)=\\frac{1}{\\text{Dir}(11,21,16)}w^{11-1}d^{21-1}l^{16-1},w+d+l=1")
        density.scale(0.875)
        for k in [2, 15, 16, 24, 25, 26, 40]:
            density[0][k].set_color(BLUE)
        for k in [4, 18, 19, 29, 30, 31, 42]:
            density[0][k].set_color(YELLOW)
        for k in [6, 21, 22, 34, 35, 36, 44]:
            density[0][k].set_color(RED)
        self.play(
            FadeOut(gamehist),
            Transform(dirichhist, newdiri)
        )
        self.wait()
        density.next_to(newdiri, DOWN)
        self.play(Write(density))
        self.wait()

        Awins = VGroup(
            MathTex("\\mathbb{P}(00 | 22 ^{10} 33 ^{20} 44 ^{15})", tex_to_color_map = {"00": BLUE, "22": BLUE, "33": YELLOW, "44": RED}),
            MathTex("=\\int w\\cdot f(w,d,l)\\,dwdl"),
            MathTex("=\\frac{11}{11+21+16}"),
        )
        for txt in Awins:
            txt.scale(1.375)
        Awins[:2].arrange(RIGHT)
        Awins[2].next_to(Awins[0], RIGHT)
        Awins[2][0][1:3].set_color(BLUE)
        Awins[2][0][4:6].set_color(BLUE)
        Awins[2][0][7:9].set_color(YELLOW)
        Awins[2][0][10:].set_color(RED)
        for k in [0]:
            tex = Awins[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = Awins[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = Awins[k]
            coin = get_coin("D")
            temp = tex.get_part_by_tex("33")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = Awins[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("44")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        Awins.shift(1.5 * (DOWN))
        self.play(Write(Awins[:2]))
        self.wait()
        self.play(
            FadeOutAndShift(Awins[1], RIGHT),
            FadeInFrom(Awins[2], DOWN)
        )
        self.wait()
        self.play(FadeOut(Awins[0]), FadeOut(Awins[2]))
        self.wait()

        twodraws = VGroup(
            MathTex("\\mathbb{P}(00 55 | 22 ^{10} 33 ^{20} 44 ^{15})", tex_to_color_map = {"00": YELLOW, "22": BLUE, "33": YELLOW, "44": RED, "55": YELLOW}),
            MathTex("=\\frac{21}{11+21+16}\\cdot \\frac{22}{11+22+16}"),
        )
        for txt in twodraws:
            txt.scale(1.125)
        twodraws.arrange(RIGHT)
        for k in [0]:
            tex = twodraws[k]
            coin = get_coin("D")
            temp = tex.get_part_by_tex("00")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = twodraws[k]
            coin = get_coin("W")
            temp = tex.get_part_by_tex("22")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = twodraws[k]
            coin = get_coin("D")
            temp = tex.get_part_by_tex("33")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = twodraws[k]
            coin = get_coin("L")
            temp = tex.get_part_by_tex("44")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [0]:
            tex = twodraws[k]
            coin = get_coin("D")
            temp = tex.get_part_by_tex("55")
            coin.replace(temp)
            tex[tex.index_of_part(temp)].become(coin)
        for k in [1, 2, 7, 8, 13, 14, 19, 20]:
            twodraws[1][0][k].set_color(YELLOW)
        for k in [4, 5, 16, 17]:
            twodraws[1][0][k].set_color(BLUE)
        for k in [10, 11, 22, 23]:
            twodraws[1][0][k].set_color(RED)
        twodraws.shift(1.5 * DOWN)
        self.play(Write(twodraws))
        self.wait()

        upddirich = MathTex("\\text{Dir}(11, 22, 16)").move_to(twodraws[1]).shift(1.5 * DOWN)
        upddirich[0][4:6].set_color(BLUE)
        upddirich[0][7:9].set_color(YELLOW)
        upddirich[0][10:12].set_color(RED)
        arrowgp = VGroup(
            Arrow(twodraws[1][0][7].get_bottom(), upddirich.get_top() + 0.25 * LEFT, preserve_tip_size_when_scaling = False),
            Arrow(upddirich.get_top() + 0.25 * RIGHT, twodraws[1][0][20].get_bottom(), preserve_tip_size_when_scaling = False),
        )
        self.play(Write(arrowgp[0]), Write(upddirich))
        self.wait()
        self.play(Write(arrowgp[1]))

        self.wait(5)


class RealCase(Scene):
    def construct(self):
        title = Tex("Real Life case").scale(1.5)
        uline = Underline(title)
        self.play(Write(VGroup(title, uline)))
        self.play(
            VGroup(title, uline).animate.to_edge(UP)
        )
        self.wait()

        matchstats = VGroup(
            Tex("A won $3$ games"),
            Tex("$40$ draws"),
            Tex("B won $5$ games"),
            Tex("First to win $6$ games wins the match"),
            Tex("Neither player gets a point in a draw"),
        )
        for txt in matchstats[3:]:
            txt.scale(1.25)
        matchstats[:3].shift(2 * UP)
        matchstats[0].shift(4 * LEFT)
        matchstats[2].shift(4 * RIGHT)
        matchstats[4].shift(2 * DOWN)

        self.play(Write(matchstats[:3]))
        self.wait()
        self.play(Write(matchstats[3]))
        self.play(Write(matchstats[4]))
        self.wait()

        density = VGroup(
            MathTex("W,D,L \\sim \\text{Dir}(4,41,6)").scale(1.5),
            MathTex("f(w,d,l)=\\frac{1}{\\text{Dir}(4, 41, 6)}w^{4-1}d^{41-1}l^{6-1}").scale(0.875)
        )
        for k in [0, 10]:
            density[0][0][k].set_color(BLUE)
        for k in [2, 12, 13]:
            density[0][0][k].set_color(YELLOW)
        for k in [4, 15]:
            density[0][0][k].set_color(RED)
        for k in [2, 15, 22, 23]:
            density[1][0][k].set_color(BLUE)
        for k in [4, 17, 18, 26, 27, 28]:
            density[1][0][k].set_color(YELLOW)
        for k in [6, 20, 31, 32]:
            density[1][0][k].set_color(RED)
        density.arrange(DOWN)
        self.play(
            FadeOutAndShift(matchstats[3], RIGHT),
            FadeOutAndShift(matchstats[4], LEFT),
        )
        self.play(Write(density))
        #self.add(TextPosition(density[0][0]), TextPosition(density[1][0]))
        self.wait()

        self.play(ShowPassingFlashAround(matchstats[2]))
        self.play(ShowPassingFlashAround(matchstats[2]))
        self.wait()

        self.play(
            FadeOut(matchstats[:3]),
            density.animate.shift(UP)
        )
        self.wait()

        seqdraws = VGroup()
        for k in range(3):
            seqdraws.add(get_coin("D").scale(0.75))
        seqdraws.add(MathTex("\\cdots").scale(0.75))
        seqdraws.add(get_coin("W").scale(0.75))
        seqdraws.arrange(RIGHT)

        seqgp = VGroup()
        for k in range(3):
            seqgp.add(seqdraws.copy())
        seqgp[1].next_to(seqgp[0], RIGHT)
        seqgp[2].next_to(seqgp[1], RIGHT)
        seqgp.move_to(ORIGIN)
        seqgp.shift(DOWN)

        for k in range(3):
            self.play(Write(seqgp[k]))
            self.wait()
        
        seqfactor = MathTex("(1+D+D^2+\\cdots)W").scale(0.875)
        for k in [1, 3, 5]:
            seqfactor[0][k].set_color(YELLOW)
        seqfactor[0][12].set_color(BLUE)
        factorgp = VGroup()
        for k in range(3):
            factorgp.add(seqfactor.copy())
        factorgp[1].next_to(factorgp[0], RIGHT)
        factorgp[2].next_to(factorgp[1], RIGHT)
        factorgp.move_to(seqgp).shift(1.5 * DOWN)

        for k in range(3):
            self.play(Write(factorgp[k]))
            self.wait()
        
        modseq = MathTex("\\frac{W^3}{(1-D)^3}").scale(0.875)
        modseq[0][0].set_color(BLUE)
        modseq[0][-3].set_color(YELLOW)
        modseq.move_to(factorgp[1])
        self.play(
            FadeOutAndShift(factorgp[0], RIGHT),
            FadeOutAndShift(factorgp[2], LEFT),
            Transform(factorgp[1], modseq)
        )
        self.wait()

        winintegral = MathTex("\\mathbb{P}(A \\text{ wins match})=\\int \\frac{w^3}{(1-d)^3}f(w,d,l)\\,dwdl").scale(1.25)
        winintegral.move_to(seqgp).shift(0.5 * DOWN)
        for k in [2, 15, 26, 33]:
            winintegral[0][k].set_color(BLUE)
        for k in [21, 28]:
            winintegral[0][k].set_color(YELLOW)
        for k in [30, 35]:
            winintegral[0][k].set_color(RED)

        self.play(
            FadeOut(factorgp[1]),
            FadeOut(seqgp),
        )
        self.play(Write(winintegral))
        #self.add(TextPosition(winintegral[0]))
        self.wait()

        surrect = SurroundingRectangle(winintegral)
        self.play(ShowCreation(surrect))
        self.wait()

        crossgp = VGroup(
            Cross(density[0][0][2]), Cross(density[0][0][-5:-3])
        )
        self.play(FadeInFromLarge(crossgp))
        self.wait()

        betadens = VGroup(
            MathTex("W,L \\sim \\text{B}(4,6)").scale(1.5),
            MathTex("f(w,l)=\\frac{1}{\\text{B}(4, 6)}w^{4-1}l^{6-1}").scale(0.875)
        )
        betadens.arrange(DOWN)
        betadens.move_to(density)
        for k in [0, -4]:
            betadens[0][0][k].set_color(BLUE)
        for k in [2, -2]:
            betadens[0][0][k].set_color(RED)
        for k in [2, 11, 15, 16]:
            betadens[1][0][k].set_color(BLUE)
        for k in [4, 13, 19, 20]:
            betadens[1][0][k].set_color(RED)
        self.play(
            FadeOut(crossgp),
            FadeOutAndShift(surrect, DOWN),
            FadeOutAndShift(winintegral, DOWN),
            ReplacementTransform(density, betadens)
        )

        threegames = VGroup(get_coin("W"), get_coin("W"), get_coin("W"))
        threegames.shift(1.5 * DOWN)
        threegames[0].shift(3 * LEFT)
        threegames[2].shift(3 * RIGHT)
        self.play(Write(threegames))
        self.wait()

        threebetas = VGroup(MathTex("B(4, 6)"), MathTex("B(5, 6)"), MathTex("B(6, 6)"))
        for k in range(3):
            threebetas[k][0][2].set_color(BLUE)
        for k in range(3):
            threebetas[k][0][-2].set_color(RED)
        threeprobs = VGroup(MathTex("\\frac{4}{4+6}"), MathTex("\\frac{5}{5 + 6}"), MathTex("\\frac{6}{6+6}"))
        for k in range(3):
            threeprobs[k][0][0].set_color(BLUE)
            threeprobs[k][0][2].set_color(BLUE)
        for k in range(3):
            threeprobs[k][0][-1].set_color(RED)
        for txt in threeprobs:
            txt.scale(1.25)
        for k in range(3):
            threebetas[k].next_to(threegames[k], UP)
            threeprobs[k].next_to(threegames[k], DOWN, buff = MED_SMALL_BUFF)
        arrgp = VGroup(Arrow(threebetas[0].get_right(), threebetas[1].get_left()), Arrow(threebetas[1].get_right(), threebetas[2].get_left()))
        arrgp.set_color(YELLOW)
        mulsym = VGroup(MathTex("\\times").scale(1.25), MathTex("\\times").scale(1.25))
        mulsym[0].move_to((threeprobs[0].get_center() + threeprobs[1].get_center()) / 2)
        mulsym[1].move_to((threeprobs[1].get_center() + threeprobs[2].get_center()) / 2)
        fprob = MathTex("=\\frac{1}{11}").scale(1.25)
        fprob.next_to(threeprobs[2], RIGHT)

        self.play(Write(threebetas[0]), Write(threeprobs[0]), FadeOut(betadens[1]))
        self.play(Write(arrgp[0]), Write(threebetas[1]), Write(threeprobs[1]), Write(mulsym[0]))
        self.play(Write(arrgp[1]), Write(threebetas[2]), Write(threeprobs[2]), Write(mulsym[1]))
        self.wait()
        self.play(Write(fprob))
        self.wait()

        results = VGroup(
            MathTex("\\mathbb{P}(A\\text{ wins match})=\\frac{1}{11}").scale(1.5),
            MathTex("\\mathbb{P}(B\\text{ wins match})=\\frac{10}{11}").scale(1.5),
        )
        results[0][0][2:7].set_color(BLUE)
        results[1][0][2:7].set_color(RED)
        results.arrange(DOWN, buff = LARGE_BUFF)
        self.play(
            *[FadeOut(obj) for obj in [betadens[0], threegames, threeprobs, threebetas, mulsym, arrgp, fprob]],
        )
        self.play(Write(results))

        self.wait(5)


class RotatingFadeInFrom(Transform):
    def __init__(
        self, mobject: "Mobject", direction: np.ndarray = DOWN, **kwargs
    ) -> None:
        self.direction = direction
        super().__init__(mobject, **kwargs)

    def create_target(self) -> "Mobject":
        return self.mobject.copy()

    def begin(self) -> None:
        super().begin()
        self.starting_mobject.shift(self.direction)
        self.starting_mobject.rotate_in_place(180 * DEGREES, axis = UP)
        self.starting_mobject.fade(1)


class RotatingFadeOutAndShift(FadeOut):
    def __init__(
        self, mobject: "Mobject", direction: np.ndarray = DOWN, **kwargs
    ) -> None:
        self.direction = direction
        super().__init__(mobject, **kwargs)

    def create_target(self) -> "Mobject":
        target = super().create_target()
        target.shift(self.direction)
        target.rotate_in_place(180 * DEGREES, axis = UP)
        return target


if __name__ == "__main__":
    module_name = os.path.abspath(__file__)
    output_location = "C:\ManimCE\media"
    clear_cmd = "cls"
    #command_A = "manim " + module_name + " " + "RealCase" + " " + "-pql -n 42" + " --media_dir " + output_location
    command_A = "manim " + module_name + " --media_dir " + output_location + " -pqh"
    os.system(clear_cmd)
    os.system(command_A)
