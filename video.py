from manimlib import *
from numpy import power, right_shift


class PartialSum:
    def nth_term(self, n):
        return Rectangle(self.rectangle_base_size*self.func(n), self.rectangle_base_size).set_stroke(self.accent_color, 2)

    def __init__(self, func, up_to, accent_color, rectangle_base_size=2):
        self.func = func
        self.up_to = up_to
        self.accent_color = accent_color
        self.terms = VGroup()
        self.rectangle_base_size = rectangle_base_size
        self.animations = []

        first_term = Rectangle(rectangle_base_size,
                               rectangle_base_size).set_stroke(accent_color, 2)
        self.terms.add(first_term)
        for n in range(2, up_to + 1):
            term = self.nth_term(n).next_to(
                self.terms.submobjects[n - 2], RIGHT, 0)
            self.terms.add(term)


class first(Scene):
    def construct(self):
        self.accent_color = '#e1fad2'

        def nth_term(n, l=2.5):
            return Rectangle(l/n, l).set_stroke(self.accent_color, 2)

        def h_n(n):
            if n == 1:
                return 1
            else:
                return h_n(n-1) + 1/n

        def create_square_divided_into(n_pieces):
            if n_pieces > 0:
                pieces = VGroup()
                term = nth_term(n_pieces)
                for n in range(n_pieces):
                    piece = term.copy()
                    if len(pieces.submobjects) > 0:
                        piece.next_to(pieces, RIGHT, 0)
                    pieces.add(piece)
                pieces.move_to(ORIGIN)
                return pieces
        
        def fade_out_all_pieces_except_first(division):
            self.play(*(FadeOut(piece) for i, piece in enumerate(division.submobjects) if i > 0))

        square_divided_1 = create_square_divided_into(1)
        square_divided_1.move_to(UP)
        squares_divided = [square_divided_1]
        terms = VGroup(square_divided_1.submobjects[0])
        self.play(ShowCreation(square_divided_1))
        self.wait(3)
        self.play(square_divided_1.submobjects[0].animate.to_corner(LEFT + DOWN))
        for n in range(2, 9):
            fade_out_all_pieces_except_first(squares_divided[n - 2])
            square_divided = create_square_divided_into(n)
            square_divided.move_to(UP)
            pieces_amount_brace = Brace(square_divided, UP)
            pieces_amount_label = Tex(str(n)).next_to(pieces_amount_brace, UP)
            squares_divided.append(square_divided)
            self.play(ShowCreation(square_divided), ShowCreation(pieces_amount_brace), Write(pieces_amount_label))
            self.wait(2/(n**2))
            self.play(square_divided.submobjects[0].animate.next_to(terms, RIGHT, 0), FadeOut(pieces_amount_brace), FadeOut(pieces_amount_label))
            terms.add(square_divided.submobjects[0])
        fade_out_all_pieces_except_first(squares_divided[7])
        self.wait(2)

        first_term = nth_term(1).to_corner(LEFT + DOWN)
        new_terms = VGroup(first_term)
        first_square = Rectangle(2.5, 2.5).set_stroke(self. accent_color, 2).next_to(first_term, UP)
        full_squares = VGroup(first_square)

        trailing_square = Rectangle(0.00001, 2.5)
        always(trailing_square.next_to, full_squares, RIGHT, 0)
        always(trailing_square.set_stroke, self.accent_color, 2)
        animations = [ShowCreation(first_square), ShowCreation(trailing_square)]
        for n in range(2, 33):
            term = nth_term(n).next_to(new_terms, RIGHT, 0)
            new_terms.add(term)
            trailing_square.set_width(2.5 * (h_n(n) % 1), True)
            if math.floor(h_n(n)) - len(full_squares.submobjects) == 1:
                new_full_square = Rectangle(2.5, 2.5).set_stroke(
                    self.accent_color, 2).next_to(full_squares, RIGHT, 0)
                full_squares.add(new_full_square)
                animations.append(ShowCreation(new_full_square))
                trailing_square.next_to(full_squares, RIGHT, 0)
                trailing_square.set_width(2.5 * (h_n(n) % 1), False)
        self.play(*animations, Transform(terms, new_terms))

        size_demonstration = Brace(terms, UP)
        size_demonstration_label = Tex('32')
        size_demonstration_label.next_to(size_demonstration, UP)
        self.play(Write(size_demonstration), Write(size_demonstration_label))
        self.wait(8)
        self.play(FadeOut(size_demonstration), FadeOut(size_demonstration_label))
        self.wait()
        self.play(FadeOut(terms), FadeOut(trailing_square), FadeOut(full_squares))
        giant_text = Text('SÉRIE').scale(10)
        self.play(Write(giant_text))
        self.wait(9)
        self.play(Transform(giant_text, Text('PROVA').scale(9)))
        self.wait(7)
        self.play(FadeOut(giant_text), FadeIn(terms))
        self.play(terms.animate.to_corner(LEFT + UP))
        
        self.wait(2)

        square_divided_2 = create_square_divided_into(2)
        square_divided_2_amount_brace = always_redraw(Brace, square_divided_2, UP)
        square_divided_2_amount_label = Tex('2')
        always(square_divided_2_amount_label.next_to, square_divided_2_amount_brace, UP)

        square_divided_4 = create_square_divided_into(4).next_to(square_divided_2, RIGHT)
        square_divided_4_amount_brace = always_redraw(Brace, square_divided_4, UP)
        square_divided_4_amount_label = Tex('4')
        always(square_divided_4_amount_label.next_to, square_divided_4_amount_brace, UP)

        square_divided_8 = create_square_divided_into(8).next_to(square_divided_4, RIGHT)
        square_divided_8_amount_brace = always_redraw(Brace, square_divided_8, UP)
        square_divided_8_amount_label = Tex('8')
        always(square_divided_8_amount_label.next_to, square_divided_8_amount_brace, UP)

        square_divided_16 = create_square_divided_into(16).next_to(square_divided_8, RIGHT)
        square_divided_16_amount_brace = always_redraw(Brace, square_divided_16, UP)
        square_divided_16_amount_label = Tex('16')
        always(square_divided_16_amount_label.next_to, square_divided_16_amount_brace, UP)

        square_powers_2 = VGroup(square_divided_2, square_divided_4, square_divided_8, square_divided_16)
        square_powers_2_amount_braces = VGroup(square_divided_2_amount_brace, square_divided_4_amount_brace, square_divided_8_amount_brace, square_divided_16_amount_brace)
        square_powers_2_amount_labels = VGroup(square_divided_2_amount_label, square_divided_4_amount_label, square_divided_8_amount_label, square_divided_16_amount_label)
        everything_group = VGroup(square_powers_2, square_powers_2_amount_braces, square_powers_2_amount_labels)
        everything_group.move_to(ORIGIN)
        everything_group.shift(DOWN)
        self.play(ShowCreation(everything_group))
        self.wait(5)
        def create_group_from_first_half_of(power):
            index = power - 1
            result_group = VGroup(
                *(square_powers_2[index].submobjects[i] for i in range(2**index))
            )
            return result_group

        def create_2_times_arrow_from_power_to_next(power):
            index = power - 1
            brace_label = square_powers_2_amount_labels[index]
            next_brace_label = square_powers_2_amount_labels[power]
            arrow = Arrow(brace_label.get_center(), next_brace_label.get_center())
            arrow.next_to(brace_label, RIGHT, 0.125)
            arrow_label = Tex(r'2\times').next_to(arrow, UP)
            return VGroup(arrow, arrow_label)

        arrow_1 = create_2_times_arrow_from_power_to_next(1)
        arrow_2 = create_2_times_arrow_from_power_to_next(2)
        arrow_3 = create_2_times_arrow_from_power_to_next(3)
        arrows = VGroup(arrow_1, arrow_2, arrow_3)
        self.play(ShowCreation(arrows))

        self.play(Indicate(create_group_from_first_half_of(1)), Indicate(create_group_from_first_half_of(2)), Indicate(create_group_from_first_half_of(3)), Indicate(create_group_from_first_half_of(4)))

        self.wait(3)

        def create_size_brace_for_first_half_of(power):
            index = power - 1
            first_half = create_group_from_first_half_of(power)
            brace = Brace(first_half, DOWN)
            brace_label = Tex(str(2 ** index)).next_to(brace, DOWN)
            return VGroup(brace, brace_label)

        size_1_half = create_size_brace_for_first_half_of(1)
        size_2_half = create_size_brace_for_first_half_of(2)
        size_3_half = create_size_brace_for_first_half_of(3)
        size_4_half = create_size_brace_for_first_half_of(4)
        sizes = VGroup(size_1_half, size_2_half, size_3_half, size_4_half)
        self.play(ShowCreation(sizes))
        self.wait(4)
        self.play(Indicate(sizes))
        
        self.wait(17)
        self.play(FadeOut(everything_group), FadeOut(sizes), FadeOut(arrows))

        sum_inverse_powers_of_2 = PartialSum(
            lambda n: 1/(2**math.ceil(math.log2(n))), 32, self.accent_color, 2.5)
        sum_inverse_powers_of_2.terms.next_to(terms, DOWN, aligned_edge=LEFT)
        power_groups = []
        for i, term in enumerate(sum_inverse_powers_of_2.terms):
            if i - 2**math.floor(math.log2(i + 1)) == 0 or i == 0 or i == 1:
                power_groups.append(VGroup(term))
            else:
                power_groups[math.ceil(math.log2(i + 1))].add(term)
            self.play(ShowCreation(term), run_time=8/((i+1)**2))
            # self.add(term)

        self.wait(4)

        def compare_power_group_to_respective_terms(p):
            # Make disappear all the terms that are not in the power group
            animations = []
            for i, term in enumerate(terms):
                if math.ceil(math.log2(i+1)) != p:
                    animations.append(FadeOut(term))

            for i, group in enumerate(power_groups):
                if i != p:
                    animations.append(FadeOut(group))

            self.play(*animations, run_time=2)

            power_group = power_groups[p]
            respective_p_group_terms = VGroup(
                *(terms.submobjects[2 ** p - i - 1] for i in range(len(power_group.submobjects))))
            original_power_group = power_group.copy()
            original_respective_p_group_terms = respective_p_group_terms.copy()
            self.play(power_group.animate.move_to(ORIGIN))
            self.play(respective_p_group_terms.animate.next_to(power_group, UP))
            comparing_group = VGroup(respective_p_group_terms, power_group)
            self.play(comparing_group.animate.move_to(ORIGIN))
            animations = []
            for i, term in enumerate(respective_p_group_terms):
                animations.append(power_group[len(
                    power_group) - i - 1].animate.next_to(term, DOWN, aligned_edge=LEFT))
            self.play(*animations)
            self.wait(2)
            animations = []
            for i, term in enumerate(terms):
                if math.ceil(math.log2(i+1)) != p:
                    animations.append(FadeIn(term))
            for i, group in enumerate(power_groups):
                if i != p:
                    animations.append(FadeIn(group))
            self.play(*animations, run_time=2)
            animations = []
            for i, term in enumerate(respective_p_group_terms):
                animations.append(respective_p_group_terms[i].animate.move_to(original_respective_p_group_terms[i]))
                animations.append(power_group[len(power_group) - i - 1].animate.move_to(original_power_group[len(power_group) - i - 1]))
            self.play(*animations)

        def group_all_power_group_terms(p):
            return VGroup(*(term for term in power_groups[p]))

        self.wait()

        compare_power_group_to_respective_terms(3)
        compare_power_group_to_respective_terms(4)
        compare_power_group_to_respective_terms(5)

        self.wait()
        self.play(Indicate(group_all_power_group_terms(2)), run_time=2)
        self.play(Indicate(group_all_power_group_terms(3)), run_time=2)
        self.play(Indicate(group_all_power_group_terms(4)), run_time=2)
        self.wait()

        self.wait(6)
        harmonic_series = Tex(
            r"\square + \frac{\square}{2} + \frac{\square}{3} + \frac{\square}{4} + \frac{\square}{5} + \frac{\square}{6} + \frac{\square}{7} + \frac{\square}{8} + \cdots")
        harmonic_series.shift(DOWN)
        self.play(FadeOut(sum_inverse_powers_of_2.terms), Write(harmonic_series))
        self.wait(6)
        smaller_harmonic_series = Tex(
            r"\square + \frac{\square}{2} + \frac{\square}{4} + \frac{\square}{4} + \frac{\square}{8} + \frac{\square}{8} + \frac{\square}{8} + \frac{\square}{8} + \cdots")
        smaller_harmonic_series.shift(UP)
        self.play(FadeOut(terms), Write(smaller_harmonic_series))
        self.wait(4)
        goes_to_infinity = Tex(r"\to\infty")
        goes_to_infinity.next_to(harmonic_series, RIGHT)
        self.play(FadeOut(smaller_harmonic_series), Write(goes_to_infinity))
        self.play(VGroup(goes_to_infinity, harmonic_series).animate.move_to(ORIGIN))
        self.wait(6)
        new_harmonic_series = Tex(
            r"1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} + \cdots")
        self.play(TransformMatchingTex(harmonic_series, new_harmonic_series))
        self.wait(4)
