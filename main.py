from cgitb import text
from logging import root
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner


from game_info import Course, Player, Game


current_game = None

# Each screen of the app
class MainMenu(Screen):
    pass


class PlayerName(Screen):
    def __init__(self, **kwargs):
        super(PlayerName, self).__init__(**kwargs)

    def on_enter(self, *args):
        layout = GridLayout()
        layout.cols = 2
        global current_game
        num_players = current_game.player_count
        layout.rows = num_players + 1
        self.labels = [Label(text=f"Player {x + 1}:") for x in range(num_players)]
        self.inputs = [TextInput(multiline=False) for _ in range(num_players)]

        for i in range(num_players):
            layout.add_widget(self.labels[i])
            layout.add_widget(self.inputs[i])

        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.press)
        layout.add_widget(self.submit)

        self.add_widget(layout)
        return super().on_enter(*args)

    def press(self, instance):

        global current_game

        for input_box in self.inputs:
            new_player = Player(input_box.text, current_game.course.basket_count)
            current_game.players.append(new_player)

        self.parent.current = "set_par"


class MakeGame(Screen):
    def __init__(self, **kwargs):
        super(MakeGame, self).__init__(**kwargs)

        layout = GridLayout()
        layout.cols = 2
        layout.rows = 4

        layout.add_widget(Label(text="Course Name: ", font_size=32))
        self.course_name_input = TextInput(multiline=False)
        layout.add_widget(self.course_name_input)

        layout.add_widget(Label(text="Number of Baskets: ", font_size=32))
        self.basket_number_input = TextInput(multiline=False)
        layout.add_widget(self.basket_number_input)

        layout.add_widget(Label(text="Number of Players: ", font_size=32))
        self.player_number_input = TextInput(multiline=False)
        layout.add_widget(self.player_number_input)

        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.press)
        layout.add_widget(self.submit)
        self.add_widget(layout)

    def press(self, instance):

        if (
            self.basket_number_input.text.isdigit()
            and self.player_number_input.text.isdigit()
        ):
            course_name = self.course_name_input.text
            basket_number = int(self.basket_number_input.text)
            player_count = int(self.player_number_input.text)

            course = Course(course_name, basket_number)
            global current_game
            current_game = Game(course, player_count)
            self.parent.current = "name_players"
        else:
            if not self.basket_number_input.text.isdigit():
                self.basket_number_input.text = ""
                self.basket_number_input.background_color = (
                    234 / 255,
                    53 / 255,
                    70 / 255,
                    1,
                )
            else:
                self.basket_number_input.background_color = (1, 1, 1, 1)

            if not self.player_number_input.text.isdigit():
                self.player_number_input.text = ""
                self.player_number_input.background_color = (
                    234 / 255,
                    53 / 255,
                    70 / 255,
                    1,
                )
            else:
                self.player_number_input.background_color = (1, 1, 1, 1)


class SetPar(Screen):
    def __init__(self, **kwargs):
        super(SetPar, self).__init__(**kwargs)

    def on_enter(self, *args):
        global current_game
        self.layout = GridLayout()
        self.layout.rows = 3
        self.layout.cols = current_game.course.basket_count + 1
        self.layout.add_widget(Label(text="Hole #: "))
        self.inputs = []

        for x in range(current_game.course.basket_count):
            self.layout.add_widget(Label(text=f"{x + 1}"))

        self.layout.add_widget(Label(text="Par: "))

        for x in range(current_game.course.basket_count):

            text_in = TextInput(
                text=f"{current_game.course.pars[x]}",
                multiline=False,
                size_hint=(0.1, 0.1),
            )
            self.layout.add_widget(text_in)
            self.inputs.append(text_in)

        submit = Button(text="Submit")
        submit.bind(on_press=self.press)
        self.layout.add_widget(submit)

        self.add_widget(self.layout)
        return super().on_enter(*args)

    def press(self, instance):
        global current_game
        all_digit = True
        for input_box in self.inputs:
            if not input_box.text.isdigit():
                input_box.background_color = (
                    234 / 255,
                    53 / 255,
                    70 / 255,
                    1,
                )
                all_digit = False
            else:
                input_box.background_color = (1, 1, 1, 1)

        if all_digit:
            for i, input_box in enumerate(self.inputs):
                current_game.course.pars[i] = int(input_box.text)
            self.parent.current = "score_card"


class ScoreCard(Screen):
    def __init__(self, **kwargs):
        super(ScoreCard, self).__init__(**kwargs)

    def on_leave(self, *args):
        self.clear_widgets()
        return super().on_leave(*args)

    def on_enter(self, *args):

        global current_game
        self.layout = BoxLayout(orientation="vertical")
        self.layout.clear_widgets()
        self.header = StackLayout(size_hint=(1, 0.2))
        self.header.clear_widgets()
        self.score = GridLayout()
        self.score.clear_widgets()

        # Rectangle(pos=(0, 0), size=(5000, 5000), color=(0, 0, 0, 0))

        player_select = Spinner(
            text=current_game.players[0].name,
            values=(x.name for x in current_game.players),
            size_hint=(None, None),
            size=(200, 44),
        )

        player_select.bind(text=self.show_selected_value)

        course_label = Label(
            text=current_game.course.name, size_hint=(None, None), size=(250, 50)
        )

        current_hole = Label(
            text=f"Current Hole: {current_game.current_hole}",
            size_hint=(None, None),
            size=(250, 50),
        )

        score_button = Button(text="Score Hole", size=(200, 50), size_hint=(None, None))
        score_button.bind(on_press=self.press)

        self.header.add_widget(player_select)
        self.header.add_widget(course_label)
        self.header.add_widget(score_button)
        self.header.add_widget(current_hole)

        self.score.cols = current_game.course.basket_count + 2
        self.score.rows = 4

        self.score.add_widget(Label(text="Hole #: "))
        for x in range(current_game.course.basket_count):
            self.score.add_widget(Label(text=f"{x + 1}"))
        self.score.add_widget(Label(text="Totals"))

        self.score.add_widget(Label(text="Par: "))
        total_par = sum(current_game.course.pars)
        for x in range(current_game.course.basket_count):
            self.score.add_widget(Label(text=f"{current_game.course.pars[x]}"))
        self.score.add_widget(Label(text=f"{total_par}", color=(0, 0, 1, 1)))

        self.score.add_widget(Label(text="Shots: "))
        current_p = None
        for p in current_game.players:
            if player_select.text == p.name:
                current_p = p

        for x in current_p.scores:
            self.score.add_widget(Label(text=f"{x}"))

        total_player_score = sum(current_p.scores)
        player_color = (1, 0, 0, 1) if total_player_score > total_par else (0, 1, 0, 1)
        if total_player_score == total_par:
            player_color = (0, 0, 1, 1)
        self.score.add_widget(Label(text=f"{total_player_score}", color=player_color))

        total_score = 0
        score_color = (1, 1, 1, 1)
        self.score.add_widget(Label(text="Score: "))
        for i in range(current_game.course.basket_count):
            shots_taken = current_p.scores[i]
            if shots_taken == 0:
                self.score.add_widget(Label(text=f"", color=score_color))
                continue

            par = current_game.course.pars[i]
            score = shots_taken - par
            total_score += score
            if score < 0:
                score_color = (0, 1, 0, 1)

            if score > 0:
                score_color = (1, 0, 0, 1)

            self.score.add_widget(Label(text=f"{score}", color=score_color))

        if total_score < 0:
            score_color = (0, 1, 0, 1)

        if total_score > 0:
            score_color = (1, 0, 0, 1)

        if total_score == 0:
            score_color = (1, 1, 1, 1)

        self.score.add_widget(Label(text=f"{total_score}", color=score_color))

        self.layout.add_widget(self.header)
        self.layout.add_widget(self.score)

        self.add_widget(self.layout)
        print("entered")
        return super().on_enter(*args)

    def show_selected_value(self, spinner, text):
        self.update(text)

    def update(self, current_player_text):
        self.score.clear_widgets()
        self.score.add_widget(Label(text="Hole #: "))
        for x in range(current_game.course.basket_count):
            self.score.add_widget(Label(text=f"{x + 1}"))
        self.score.add_widget(Label(text="Totals"))

        self.score.add_widget(Label(text="Par: "))
        total_par = sum(current_game.course.pars)
        for x in range(current_game.course.basket_count):
            self.score.add_widget(Label(text=f"{current_game.course.pars[x]}"))
        self.score.add_widget(Label(text=f"{total_par}", color=(0, 0, 1, 1)))

        self.score.add_widget(Label(text="Shots: "))
        current_p = None
        for p in current_game.players:
            if current_player_text == p.name:
                current_p = p

        for x in current_p.scores:
            self.score.add_widget(Label(text=f"{x}"))

        total_player_score = sum(current_p.scores)
        player_color = (1, 0, 0, 1) if total_player_score > total_par else (0, 1, 0, 1)
        if total_player_score == total_par:
            player_color = (0, 0, 1, 1)
        self.score.add_widget(Label(text=f"{total_player_score}", color=player_color))

        total_score = 0
        score_color = (1, 1, 1, 1)
        self.score.add_widget(Label(text="Score: "))
        for i in range(current_game.course.basket_count):
            shots_taken = current_p.scores[i]
            if shots_taken == 0:
                self.score.add_widget(Label(text=f"", color=score_color))
                continue

            par = current_game.course.pars[i]
            score = shots_taken - par
            total_score += score
            if score < 0:
                score_color = (0, 1, 0, 1)

            if score > 0:
                score_color = (1, 0, 0, 1)

            self.score.add_widget(Label(text=f"{score}", color=score_color))

        if total_score < 0:
            score_color = (0, 1, 0, 1)

        if total_score > 0:
            score_color = (1, 0, 0, 1)

        if total_score == 0:
            score_color = (1, 1, 1, 1)

        self.score.add_widget(Label(text=f"{total_score}", color=score_color))
        print("updated")

    def press(self, instance):
        self.parent.current = "score_hole"


class ScoreHole(Screen):
    def __init__(self, **kwargs):
        super(ScoreHole, self).__init__(**kwargs)

    def on_enter(self, *args):
        global current_game

        layout = GridLayout()
        layout.cols = 2
        layout.rows = current_game.player_count + 3
        self.inputs = []

        layout.add_widget(Label(text="Hole #: "))
        self.hole_submit = TextInput(text=f"{current_game.current_hole}")
        layout.add_widget(self.hole_submit)

        for i, player in enumerate(current_game.players):
            layout.add_widget(Label(text=f"{player.name}"))
            in_box = TextInput()
            if player.scores[current_game.current_hole] != 0:
                in_box.text = player.scores[current_game.current_hole]

            self.inputs.append(in_box)
            layout.add_widget(in_box)

        submit = Button(text="Submit")
        back = Button(text="Return")

        layout.add_widget(submit)
        layout.add_widget(back)

        submit.bind(on_press=self.submit)
        back.bind(on_press=self.back)

        self.add_widget(layout)

        return super().on_enter(*args)

    def submit(self, instance):

        submit = True
        self.hole_submit.background_color = (1, 1, 1, 1)
        if not self.hole_submit.text.isdigit():
            self.hole_submit.background_color = (
                234 / 255,
                53 / 255,
                70 / 255,
                1,
            )
            submit = False

        for text_box in self.inputs:
            text_box.background_color = (1, 1, 1, 1)
            if not text_box.text.isdigit():
                text_box.background_color = (
                    234 / 255,
                    53 / 255,
                    70 / 255,
                    1,
                )
                submit = False

        if submit:
            scored_hole = int(self.hole_submit.text)
            if scored_hole == current_game.current_hole:
                current_game.current_hole += 1

            for i, player_score in enumerate(self.inputs):
                number = int(player_score.text)
                current_game.players[i].scores[scored_hole - 1] = number

            self.parent.current = "score_card"

    def back(self, instance):
        self.parent.current = "score_card"


class WindowManager(ScreenManager):
    pass


class DiscGolfScoreKeeper(App):
    def build(self):
        return kv


# design file located here
kv = Builder.load_file("disc_golf_app.kv")

if __name__ == "__main__":
    DiscGolfScoreKeeper().run()
