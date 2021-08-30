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

        def nth_term(n, l=2):
            return Rectangle(l/n, l).set_stroke(self.accent_color, 2)

        def h_n(n):
            if n == 1:
                return 1
            else:
                return h_n(n-1) + 1/n

        first_term = Rectangle(3, 3).set_stroke(self.accent_color, 2)
        terms = VGroup(first_term)
        self.play(ShowCreation(first_term))
        self.wait(3)
        self.play(first_term.animate.scale(2/3))
        self.play(first_term.animate.to_edge(LEFT))

        first_square = Rectangle(2, 2).set_stroke(
            self.accent_color, 2).next_to(first_term, UP)
        full_squares = VGroup(first_square)

        trailing_square = Rectangle(0.1, 2)
        always(trailing_square.next_to, full_squares, RIGHT, 0)
        always(trailing_square.set_stroke, self.accent_color, 2)
        self.play(ShowCreation(first_square), ShowCreation(trailing_square))
        for n in range(2, 401):
            term = nth_term(n).next_to(terms.submobjects[n - 2], RIGHT, 0)
            terms.add(term)
            animations = []
            animations.append(ShowCreation(term))
            animations.append(
                trailing_square.animate.set_width(2 * (h_n(n) % 1), True))
            if math.floor(h_n(n)) - len(full_squares.submobjects) == 1:
                new_full_square = Rectangle(2, 2).set_stroke(
                    self.accent_color, 2).next_to(full_squares, RIGHT, 0)
                full_squares.add(new_full_square)
                animations.append(ShowCreation(new_full_square))
                trailing_square.next_to(full_squares, RIGHT, 0)
            self.play(*animations, run_time=8/(n**2))

        self.selected_term_original = None
        self.selected_term_n = None

        def fade_out_terms_except(n):
            animations = []
            for i, term in enumerate(terms):
                if i != n - 1:
                    animations.append(FadeOut(term))
            self.play(*animations, FadeOut(full_squares),
                      FadeOut(trailing_square), run_time=0.5)

        def fade_in_terms_except(n):
            animations = []
            for i, term in enumerate(terms):
                if i != n - 1:
                    animations.append(FadeIn(term))
            self.play(*animations, FadeIn(full_squares),
                      FadeIn(trailing_square), run_time=0.5)

        def select_specific_term(n):
            term_to_select = terms.submobjects[n - 1]
            self.selected_term_original = term_to_select.copy()
            self.selected_term_n = n
            fade_out_terms_except(self.selected_term_n)
            self.play(term_to_select.animate.move_to(ORIGIN))
            self.play(term_to_select.animate.scale(3/2))

        def get_current_selected_term():
            return terms[self.selected_term_n - 1]

        def unselect():
            current_selected_term = get_current_selected_term()
            self.play(current_selected_term.animate.scale(2/3))
            self.play(current_selected_term.animate.move_to(
                self.selected_term_original))
            fade_in_terms_except(self.selected_term_n)
            self.selected_term_original = None
            self.selected_term_n = None

        def make_up_all_pieces(piece, n):
            self.all_pieces = VGroup()
            self.all_pieces.add(piece)
            for pos in range(1, n):
                new_piece = piece.copy()
                self.all_pieces.add(new_piece)
                self.add(new_piece)
                self.play(new_piece.animate.next_to(
                    self.all_pieces.submobjects[pos - 1], RIGHT, 0))
            self.play(self.all_pieces.animate.move_to(ORIGIN))

        def fade_out_pieces_except_for_one():
            animations = []
            for i, piece in enumerate(self.all_pieces):
                if i > 0:
                    animations.append(FadeOut(piece))
            self.play(*animations)

        self.wait()
        # Show that the second term is really a half of the square
        select_specific_term(2)
        make_up_all_pieces(get_current_selected_term(), 2)
        self.wait()
        fade_out_pieces_except_for_one()
        unselect()

        # Show that the third term is really a half of the square
        select_specific_term(3)
        make_up_all_pieces(get_current_selected_term(), 3)
        self.wait()
        fade_out_pieces_except_for_one()
        unselect()

        self.wait()

        sum_inverse_powers_of_2 = PartialSum(
            lambda n: 1/(2**math.ceil(math.log2(n))), 400, self.accent_color)
        sum_inverse_powers_of_2.terms.next_to(terms, DOWN, aligned_edge=LEFT)
        power_groups = []
        for i, term in enumerate(sum_inverse_powers_of_2.terms):
            if i - 2**math.floor(math.log2(i + 1)) == 0 or i == 0 or i == 1:
                power_groups.append(VGroup(term))
            else:
                power_groups[math.ceil(math.log2(i + 1))].add(term)
            self.play(ShowCreation(term), run_time=8/((i+1)**2))
            # self.add(term)
        self.play(
            FadeOut(full_squares),
            FadeOut(trailing_square),
            sum_inverse_powers_of_2.terms.animate.shift(UP),
            terms.animate.shift(UP * 2)
        )

        self.wait()

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
            for i, term in enumerate(respective_p_group_terms):
                self.play(power_group[len(
                    power_group) - i - 1].animate.next_to(term, DOWN, aligned_edge=LEFT))
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

        compare_power_group_to_respective_terms(1)
        compare_power_group_to_respective_terms(2)
        compare_power_group_to_respective_terms(3)
        compare_power_group_to_respective_terms(4)

        self.wait()
        self.play(Indicate(group_all_power_group_terms(1)), run_time=2)
        self.wait(2)
        self.play(Indicate(group_all_power_group_terms(2)), run_time=2)
        self.wait()
        self.play(Indicate(group_all_power_group_terms(3)), run_time=2)
        self.wait()
        self.play(Indicate(group_all_power_group_terms(4)), run_time=2)
        self.wait()
        self.play(Indicate(group_all_power_group_terms(5)), run_time=2)
        self.wait()
        self.play(Indicate(group_all_power_group_terms(6), run_time=2))
        self.wait()
        self.play(Indicate(group_all_power_group_terms(7), run_time=2))
        self.wait()

        size_demonstration = Brace(terms, DOWN)
        size_demonstration_label = Tex('400')
        size_demonstration_label.next_to(size_demonstration, DOWN)
        self.play(ShowCreation(size_demonstration), Write(size_demonstration_label))
        self.wait()
        self.play(FadeOut(size_demonstration), FadeOut(size_demonstration_label))
        self.wait()
        harmonic_series = Tex(
            r"\square + \frac{\square}{2} + \frac{\square}{3} + \frac{\square}{4} + \frac{\square}{5} + \frac{\square}{6} + \frac{\square}{7} + \frac{\square}{8} + \cdots")
        harmonic_series.shift(DOWN)
        self.play(FadeOut(sum_inverse_powers_of_2.terms), Write(harmonic_series))
        self.wait(4)
        smaller_harmonic_series = Tex(
            r"\square + \frac{\square}{2} + \frac{\square}{4} + \frac{\square}{4} + \frac{\square}{8} + \frac{\square}{8} + \frac{\square}{8} + \frac{\square}{8} + \cdots")
        smaller_harmonic_series.shift(UP)
        self.play(FadeOut(terms), Write(smaller_harmonic_series))
        self.wait(3)
        goes_to_infinity = Tex(r"\to\infty")
        goes_to_infinity.next_to(harmonic_series, RIGHT)
        self.play(FadeOut(smaller_harmonic_series), Write(goes_to_infinity))
        self.play(VGroup(goes_to_infinity, harmonic_series).animate.move_to(ORIGIN))
        self.wait(6)
        new_harmonic_series = Tex(
            r"1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} + \cdots")
        self.play(TransformMatchingTex(harmonic_series, new_harmonic_series))
        self.wait(2)
