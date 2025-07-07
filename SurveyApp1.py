import csv
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

# Change this if your tablet's documents folder is elsewhere
DOCUMENTS_PATH = os.path.expanduser("~/Documents")
QUESTIONS_FILE = "questions.csv"
RESULTS_FILE = os.path.join(DOCUMENTS_PATH, "SurveyResults.csv")


class QuestionWidget(BoxLayout):
    def __init__(self, question, answer_type, options=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.question = question
        self.answer_type = answer_type
        self.options = options
        self.answer = None

        self.label = Label(text=question, size_hint_y=None, height=40)
        self.add_widget(self.label)

        if answer_type == 'data_entry':
            self.input_widget = TextInput(multiline=False, size_hint_y=None, height=40)
            self.input_widget.bind(text=self.on_text)
            self.add_widget(self.input_widget)

        elif answer_type == 'multiple_choice':
            self.input_widget = Spinner(text='Select an option', values=options, size_hint_y=None, height=40)
            self.input_widget.bind(text=self.on_select)
            self.add_widget(self.input_widget)

    def on_text(self, instance, value):
        self.answer = value.strip()

    def on_select(self, instance, value):
        self.answer = value


class SurveyApp(App):
    def build(self):
        self.title = "Dynamic Survey"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.questions = []
        self.answers = {}

        # Load questions from CSV
        self.load_questions()

        # Add submit button
        submit_btn = Button(text='Submit Survey', size_hint_y=None, height=50)
        submit_btn.bind(on_press=self.save_results)
        self.root.add_widget(submit_btn)

        return self.root

    def load_questions(self):
        self.all_questions = []
        with open(QUESTIONS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.all_questions.append(row)

        self.displayed_questions = {}
        self.display_questions()

    def display_questions(self):
        # Clear previous
        self.root.clear_widgets()

        # Show questions that have no parent or whose parent condition matches
        for q in self.all_questions:
            parent_id = q['parent_id'].strip()
            parent_answer = q['parent_answer'].strip()
            if parent_id == '' or (parent_id in self.answers and self.answers[parent_id] == parent_answer):
                # Parse options for multiple choice
                options = q['options'].split(';') if q['options'] else None
                qw = QuestionWidget(q['question'], q['type'], options)
                self.questions.append((q['id'], qw))
                self.root.add_widget(qw)

                # Track widget for updates if needed
                self.displayed_questions[q['id']] = qw

                # Listen for multiple choice changes to refresh questions (for conditional logic)
                if q['type'] == 'multiple_choice':
                    qw.input_widget.bind(text=self.on_answer_change)

        # Add submit button at bottom
        submit_btn = Button(text='Submit Survey', size_hint_y=None, height=50)
        submit_btn.bind(on_press=self.save_results)
        self.root.add_widget(submit_btn)

    def on_answer_change(self, spinner, new_value):
        # Update answer
        for qid, qw in self.questions:
            if qw.input_widget == spinner:
                self.answers[qid] = new_value
                break
        # Refresh visible questions based on new answers
        self.questions.clear()
        self.display_questions()

    def save_results(self, instance):
        # Gather all answers
        for qid, qw in self.questions:
            self.answers[qid] = qw.answer if qw.answer is not None else ''

        # Save to CSV
        file_exists = os.path.exists(RESULTS_FILE)
        with open(RESULTS_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [q['id'] for q in self.all_questions]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            # Write answers as a row keyed by question ids
            writer.writerow(self.answers)

        self.root.clear_widgets()
        self.root.add_widget(Label(text="Thank you! Survey submitted."))


if __name__ == '__main__':
    SurveyApp().run()
