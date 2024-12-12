import sys  # Import the sys module to access system-specific parameters and functions

# Import necessary modules and classes from PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices, QPixmap, QPainter, QTransform, QFont
from PyQt5.QtCore import QUrl

# Define the main application class inheriting from QWidget
class SearchApp(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the base class

        self.initUI()  # Initialize the user interface
        self.open_windows = []  # Keep track of open windows

    def initUI(self):
        # Initialize the main layout as a vertical box layout
        self.layout = QVBoxLayout()

        # Create the top bar layout as a horizontal box layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with styles and connect its click event
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with styles and connect its text change event
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretch to push the search bar to the right
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout as a grid layout
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(20)  # Set spacing between buttons

        # Define the categories and their positions in the grid layout
        self.categories = ["Study Guides", "School Resources", "Miscellaneous Info", "Health Check-Up"]
        self.buttons = []
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # Define button positions

        # Create buttons for each category with styles and connect their click events
        for position, category in zip(positions, self.categories):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set button size policy
            button.setMinimumSize(150, 100)  # Set minimum size

            # Set different styles for each category
            if category == "Study Guides":
                button.setStyleSheet("background-color: #480CA8; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "School Resources":
                button.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "Miscellaneous Info":
                button.setStyleSheet("background-color: #3F37C9; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "Health Check-Up":
                button.setStyleSheet("background-color: #B5179E; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")

            # Connect button click to open a new window corresponding to the category
            button.clicked.connect(lambda checked, cat=category: self.open_new_window(cat))
            self.buttonLayout.addWidget(button, *position)  # Add button to the grid layout
            self.buttons.append(button)  # Add button to the list of buttons

        # Add the buttons layout to the main layout
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)  # Set the main layout

        self.setWindowTitle("Main Menu")  # Set the window title
        self.setGeometry(100, 100, 800, 600)  # Set the window size and position
        self.setStyleSheet("background-color: #121212;")  # Set the background color

        self.ascending = True  # Set the initial sort order to ascending

    def keyPressEvent(self, event):
        # Override the key press event to set focus on the search bar when any key is pressed
        if event.text():
            self.searchBar.setFocus()

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()  # Show button if it matches the search text
            else:
                button.hide()  # Hide button if it doesn't match the search text

    def toggle_sort_order(self):
        # Toggle the sort order between ascending and descending
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")  # Update button text
        self.sort_buttons()  # Sort the buttons

    def sort_buttons(self):
        # Sort buttons by their text in the specified order
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)
        for i, button in enumerate(self.buttons):
            self.buttonLayout.addWidget(button, i // 2, i % 2)  # Reposition buttons in the grid layout

    def open_new_window(self, category):
        # Open a new window corresponding to the selected category
        if category == "Study Guides":
            self.new_window = StudyGuidesWindow(self)
        elif category == "School Resources":
            self.new_window = SchoolResourcesWindow(self)
        elif category == "Miscellaneous Info":
            self.new_window = MiscellaneousInfoWindow(self)
        elif category == "Health Check-Up":
            self.new_window = HealthCheckUpWindow(self)

        self.new_window.show()  # Show the new window
        self.open_windows.append(self.new_window)  # Add the new window to the list of open windows

    def closeEvent(self, event):
        # Override the close event to close all open windows before closing the main window
        for window in self.open_windows:
            window.close()
        event.accept()  # Accept the close event


class StudyGuidesWindow(QWidget):
    def __init__(self, main_window):
        """
        Initialize the StudyGuidesWindow.

        :param main_window: Reference to the main window that manages this window.
        """
        super().__init__()  # Call the base class constructor
        self.main_window = main_window  # Store reference to the main window
        self.initUI()  # Initialize the user interface

    def initUI(self):
        """
        Set up the user interface for the StudyGuidesWindow.
        """
        # Create the main vertical layout for the window
        self.layout = QVBoxLayout()

        # Create a horizontal layout for the top bar
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button to sort categories
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet(
            "background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)  # Connect button click to toggle_sort_order method

        # Create a search bar for filtering categories
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")  # Placeholder text when the search bar is empty
        self.searchBar.textChanged.connect(self.on_search)  # Connect text change to on_search method
        self.searchBar.setStyleSheet(
            "background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add the toggle button and search bar to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)  # Add button aligned to the left
        topLayout.addStretch()  # Add a stretchable space to push the search bar to the right
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)  # Add search bar aligned to the right

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create a grid layout for the main buttons
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(20)  # Set spacing between buttons

        # Define categories and button positions
        self.categories = ["Exam Techniques", "Note Taking Tips", "Revision Techniques", "Music", "Bored?",
                           "Study Guide Videos"]
        self.buttons = []  # List to hold button references
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]  # Button positions in the grid

        # Create and configure buttons for each category
        for position, category in zip(positions, self.categories):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow button to expand
            button.setMinimumSize(150, 100)  # Set minimum size of the button
            button.setStyleSheet("background-color: #480CA8; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")

            # Connect button clicks to the appropriate method based on the category
            if category == "Exam Techniques":
                button.clicked.connect(self.open_exam_techniques)
            elif category == "Note Taking Tips":
                button.clicked.connect(self.open_note_taking_tips)
            elif category == "Revision Techniques":
                button.clicked.connect(self.open_revision_techniques)
            elif category == "Bored?":
                button.clicked.connect(self.Bored)
            elif category == "Study Guide Videos":
                button.clicked.connect(self.Study_Guide_Videos)
            elif category == "Music":
                button.clicked.connect(self.Music)

            # Add button to the grid layout at the specified position
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)  # Keep track of button references

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Create a horizontal layout for navigation buttons
        navLayout = QHBoxLayout()

        # Create the "Previous" navigation button
        self.prevButton = QPushButton("⬅", self)
        self.prevButton.setStyleSheet(
            "background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.prevButton.clicked.connect(self.navigate_left)  # Connect button click to navigate_left method

        # Create the "Next" navigation button
        self.nextButton = QPushButton("➡", self)
        self.nextButton.setStyleSheet(
            "background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.nextButton.clicked.connect(self.navigate_right)  # Connect button click to navigate_right method

        # Add navigation buttons to the navigation layout
        navLayout.addWidget(self.prevButton, alignment=Qt.AlignLeft)  # Add "Previous" button aligned to the left
        navLayout.addStretch()  # Add stretchable space between buttons
        navLayout.addWidget(self.nextButton, alignment=Qt.AlignRight)  # Add "Next" button aligned to the right

        # Add the navigation layout to the main layout
        self.layout.addLayout(navLayout)

        # Set the final layout for the window
        self.setLayout(self.layout)
        self.setWindowTitle("Study Guides")  # Set window title
        self.setGeometry(200, 200, 800, 600)  # Set window size and position
        self.setStyleSheet("background-color: #121212;")  # Set window background color

        # Initialize sort order for category buttons
        self.ascending = True

    def on_search(self):
        """
        Handles search functionality for filtering category buttons based on user input.

        Hides buttons that do not match the search text and shows those that do.
        The search is case-insensitive.
        """
        # Get the search text from the search bar and convert it to lowercase
        search_text = self.searchBar.text().lower()

        # Iterate through each button in the list of buttons
        for button in self.buttons:
            # Check if the search text is in the button's text (case-insensitive)
            if search_text in button.text().lower():
                button.show()  # Show the button if it matches the search text
            else:
                button.hide()  # Hide the button if it does not match the search text

    def toggle_sort_order(self):
        """
        Toggles the sort order of the category buttons between ascending and descending.

        Updates the text of the sort button and re-sorts the buttons accordingly.
        """
        # Toggle the sort order
        self.ascending = not self.ascending

        # Update the text of the sort button based on the current sort order
        self.azButton.setText("A - Z" if self.ascending else "Z - A")

        # Re-sort the buttons based on the new sort order
        self.sort_buttons()

    def sort_buttons(self):
        """
        Sorts the category buttons based on the current sort order and arranges them in the grid layout.

        Buttons are sorted alphabetically, and the order is determined by the `ascending` attribute.
        """
        # Sort the buttons alphabetically based on their text
        # If `ascending` is True, sort in ascending order; otherwise, sort in descending order
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)

        # Re-add the buttons to the grid layout according to the sorted order
        for i, button in enumerate(self.buttons):
            # Calculate the position of the button in the grid layout
            self.buttonLayout.addWidget(button, i // 2, i % 2)

    def keyPressEvent(self, event):
        """
        Handles key press events.

        Sets focus to the search bar if any key is pressed.

        :param event: The key press event.
        """
        # Check if the key press event has text (i.e., it's a character key)
        if event.text():
            # Set focus to the search bar
            self.searchBar.setFocus()

    def navigate_left(self):
        """
        Navigates to the "Health Check-Up" window.

        Closes the current window and opens the specified new window in the main window.
        """
        self.close()  # Close the current window
        self.main_window.open_new_window("Health Check-Up")  # Open the "Health Check-Up" window in the main window

    def navigate_right(self):
        """
        Navigates to the "School Resources" window.

        Closes the current window and opens the specified new window in the main window.
        """
        self.close()  # Close the current window
        self.main_window.open_new_window("School Resources")  # Open the "School Resources" window in the main window

    def open_exam_techniques(self):
        """
        Opens the "Exam Techniques" window.

        Creates an instance of the ExamTechniquesWindow, shows it, and adds it to the list of open windows in the main window.
        """
        # Create an instance of the ExamTechniquesWindow
        self.exam_techniques_window = ExamTechniquesWindow(self)
        # Show the new window
        self.exam_techniques_window.show()
        # Add the new window to the list of open windows in the main window
        self.main_window.open_windows.append(self.exam_techniques_window)

    def open_note_taking_tips(self):
        """
        Opens a web page with note-taking tips in the default web browser.
        """
        # URL of the note-taking tips page
        url = "https://students.unimelb.edu.au/academic-skills/resources/reading,-writing-and-referencing/reading-and-note-taking/note-taking"
        # Open the URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def open_revision_techniques(self):
        """
        Opens the "Revision Techniques" window.

        Creates an instance of the RevisionTechniquesWindow, shows it, and adds it to the list of open windows in the main window.
        """
        # Create an instance of the RevisionTechniquesWindow
        self.revision_techniques_window = RevisionTechniquesWindow(self)
        # Show the new window
        self.revision_techniques_window.show()
        # Add the new window to the list of open windows in the main window
        self.main_window.open_windows.append(self.revision_techniques_window)

    def Music(self):
        """
        Opens the "Music" window.

        Creates an instance of the Music window, shows it, and adds it to the list of open windows in the main window.
        """
        # Create an instance of the Music window
        self.Music = Music(self)
        # Show the new window
        self.Music.show()
        # Add the new window to the list of open windows in the main window
        self.main_window.open_windows.append(self.Music)

    def Bored(self):
        """
        Opens a web page to a site for entertainment in the default web browser.
        """
        # URL of the entertainment site
        url = "http://mentalfloss.com/"
        # Open the URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def Study_Guide_Videos(self):
        """
        Opens a YouTube playlist with study guide videos in the default web browser.
        """
        # URL of the YouTube playlist
        url = "https://www.youtube.com/watch?v=eAj8AC5RmSg&list=PLSjrnIOGvOq36-ESQSyO-gK6B0gCSm6Hg&pp=iAQB"
        # Open the URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))


class Music(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # Store the reference to the main window
        self.main_window = main_window
        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Create the main vertical layout
        self.layout = QVBoxLayout()

        # Create the top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with style and connect its signal to the toggle_sort_order method
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with placeholder text and connect its signal to the on_search method
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretchable space between widgets
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout (grid layout) with spacing
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(20)

        # Define the categories and initialize the buttons list
        self.categories = ["Classical Music Playlist Online", "Download Classical Music", "Ambient Music Playlist Online", "Download Ambient Music", "Facts About Music"]
        self.buttons = []

        # Define positions for the buttons in a grid layout
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)]  # Adjust button positions in a grid layout

        # Create buttons for each category and add them to the grid layout
        for position, category in zip(positions, self.categories):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 100)
            button.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)

        # Connect the buttons to their respective methods
        self.buttons[0].clicked.connect(self.open_classical_playlist)
        self.buttons[1].clicked.connect(self.open_download_classical_music)
        self.buttons[2].clicked.connect(self.open_ambient_playlist)
        self.buttons[3].clicked.connect(self.open_download_Ambient_music)
        self.buttons[4].clicked.connect(self.open_facts_classical_music)

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Set the window title, geometry, and background color
        self.setWindowTitle("Music")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #121212;")

        # Initialize sorting order flag
        self.ascending = True

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()
            else:
                button.hide()

    def toggle_sort_order(self):
        # Toggle the sorting order and update the button text
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")
        self.sort_buttons()

    def sort_buttons(self):
        # Sort buttons based on their text
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)
        # Reposition the sorted buttons in the grid layout
        for i, button in enumerate(self.buttons):
            self.buttonLayout.addWidget(button, i // 2, i % 2)

    def keyPressEvent(self, event):
        # Set focus to the search bar when a key is pressed
        if event.text():
            self.searchBar.setFocus()

    def open_classical_playlist(self):
        # Open the Classical Music Playlist URL
        url = QUrl("https://open.spotify.com/playlist/37i9dQZF1EIgLoMVUd9oTU?si=277772aacf784ef9")
        QDesktopServices.openUrl(url)

    def open_download_classical_music(self):
        # Open the Download Classical Music URL
        url = QUrl("https://drive.google.com/file/d/15B4AxAbCoicKXOWRczpRS2yQP0e1ngN6/view?usp=sharing")
        QDesktopServices.openUrl(url)

    def open_ambient_playlist(self):
        # Open the Ambient Music Playlist URL
        url = QUrl("https://open.spotify.com/playlist/5iPjgCLzMr8r5VYmUOV6tp?si=92945c48a4a14a53")
        QDesktopServices.openUrl(url)

    def open_facts_classical_music(self):
        # Open the Facts About Music URL
        url = QUrl("https://www.healthline.com/health/does-music-help-you-study")
        QDesktopServices.openUrl(url)

    def open_download_Ambient_music(self):
        # Open the Download Ambient Music URL
        url = QUrl("https://drive.google.com/file/d/19QvmzaxXLTB-ZpznusOm7B-WShBpeJmu/view?usp=sharing")
        QDesktopServices.openUrl(url)

class RevisionTechniquesWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        # Store the reference to the parent window
        self.parent_window = parent_window
        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Create the main vertical layout
        self.layout = QVBoxLayout()

        # Create the top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with style and connect its signal to the toggle_sort_order method
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with placeholder text and connect its signal to the on_search method
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretchable space between widgets
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout (grid layout) with spacing
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(10)  # Adjust spacing between cells

        # Define the categories and initialize the buttons list
        self.categories = ["UK nidirect", "Iglu Guide"]
        self.buttons = []

        # Define positions for the buttons in a grid layout
        positions = [(0, 1), (2, 0)]  # Define button positions in a grid layout

        # Create buttons for each category and add them to the grid layout
        for position, category in zip(positions, self.categories):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumSize(400, 400)  # Set maximum size for the buttons

            # Apply different styles based on the category
            if category == "UK nidirect":
                button.setStyleSheet("background-color: #560BAD; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "Iglu Guide":
                button.setStyleSheet("background-color: #3F37C9; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")

            # Connect the button click to the open_new_window method
            button.clicked.connect(lambda checked, cat=category: self.open_new_window(cat))
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)

        # Add image labels
        self.imageLabel1 = QLabel(self)
        pixmap1 = QPixmap("stressed_student.png")
        scaled_pixmap1 = pixmap1.scaled(400, 400, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageLabel1.setPixmap(scaled_pixmap1)
        self.imageLabel1.setAlignment(Qt.AlignCenter)
        self.imageLabel1.setMaximumSize(400, 400)  # Set maximum size for the image label
        self.buttonLayout.addWidget(self.imageLabel1, 0, 0, 2, 1, Qt.AlignCenter)  # Align center within its cell and span 2 rows

        self.imageLabel2 = QLabel(self)
        pixmap2 = QPixmap("happy_student.jpg")
        scaled_pixmap2 = pixmap2.scaled(400, 400, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageLabel2.setPixmap(scaled_pixmap2)
        self.imageLabel2.setAlignment(Qt.AlignCenter)
        self.imageLabel2.setMaximumSize(400, 400)  # Set maximum size for the image label
        self.buttonLayout.addWidget(self.imageLabel2, 2, 1, 1, 1, Qt.AlignCenter)  # Align center within its cell

        # Adjust cell spacing and margins for closer alignment
        self.buttonLayout.setContentsMargins(10, 10, 10, 10)
        self.buttonLayout.setHorizontalSpacing(10)
        self.buttonLayout.setVerticalSpacing(10)

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Set the window title, geometry, and background color
        self.setWindowTitle("Revision Techniques")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212;")

        # Initialize sorting order flag
        self.ascending = True

    def keyPressEvent(self, event):
        # Set focus to the search bar when a key is pressed
        if event.text():
            self.searchBar.setFocus()

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()
            else:
                button.hide()

    def toggle_sort_order(self):
        # Toggle the sorting order and update the button text
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")
        # No sorting action performed

    def open_new_window(self, category):
        # Open a new window based on the category
        if category == "UK nidirect":
            QDesktopServices.openUrl(QUrl("https://www.nidirect.gov.uk/articles/revision-tips-preparing-exams"))
        elif category == "Iglu Guide":
            QDesktopServices.openUrl(QUrl("https://iglu.com.au/best-revision-techniques/"))

class ExamTechniquesWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        # Store the reference to the parent window
        self.parent_window = parent_window
        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Create the main vertical layout
        self.layout = QVBoxLayout()

        # Create the top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with style and connect its signal to the toggle_sort_order method
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with placeholder text and connect its signal to the on_search method
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretchable space between widgets
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout (grid layout) with spacing
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(10)  # Adjust spacing between cells

        # Define the categories and initialize the buttons list
        self.categories = ["Western Australia Uni", "Self Help Website", "The StudySpace"]
        self.buttons = []

        # Define positions for the buttons in a grid layout
        positions = [(0, 0), (1, 0), (2, 0)]  # Define button positions in a grid layout

        # Create buttons for each category and add them to the grid layout
        for position, category in zip(positions, self.categories):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 100)  # Set minimum size for the buttons

            # Apply different styles based on the category
            if category == "Western Australia Uni":
                button.setStyleSheet("background-color: #560BAD; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "Self Help Website":
                button.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            elif category == "The StudySpace":
                button.setStyleSheet("background-color: #3F37C9; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")

            # Connect the button click to the open_new_window method
            button.clicked.connect(lambda checked, cat=category: self.open_new_window(cat))
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)

        # Add image labels
        self.imageLabel1 = QLabel(self)
        pixmap1 = QPixmap("perfection.jpg")
        scaled_pixmap1 = pixmap1.scaled(400, 500, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageLabel1.setPixmap(scaled_pixmap1)
        self.imageLabel1.setAlignment(Qt.AlignCenter)
        self.imageLabel1.setMaximumSize(400, 500)  # Set maximum size for the image label
        self.buttonLayout.addWidget(self.imageLabel1, 0, 1, 2, 1, Qt.AlignCenter)  # Align center within its cell and span 2 rows

        self.imageLabel2 = QLabel(self)
        pixmap2 = QPixmap("harvard_student.jpg")
        scaled_pixmap2 = pixmap2.scaled(400, 400, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageLabel2.setPixmap(scaled_pixmap2)
        self.imageLabel2.setAlignment(Qt.AlignCenter)
        self.imageLabel2.setMaximumSize(400, 400)  # Set minimum size for the image label
        self.buttonLayout.addWidget(self.imageLabel2, 2, 1, 1, 1, Qt.AlignCenter)  # Align center within its cell

        # Adjust cell spacing and margins for closer alignment
        self.buttonLayout.setContentsMargins(10, 10, 10, 10)
        self.buttonLayout.setHorizontalSpacing(10)
        self.buttonLayout.setVerticalSpacing(10)

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Set the window title, geometry, and background color
        self.setWindowTitle("Exam Techniques")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212;")

        # Initialize sorting order flag
        self.ascending = True

    def keyPressEvent(self, event):
        # Set focus to the search bar when a key is pressed
        if event.text():
            self.searchBar.setFocus()

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()
            else:
                button.hide()

    def toggle_sort_order(self):
        # Toggle the sorting order and update the button text
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")
        # Call sort_buttons method to reorder the buttons
        self.sort_buttons()

    def sort_buttons(self):
        # Sort the buttons based on their text
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)
        # Re-add buttons to the layout in the new order
        for i, button in enumerate(self.buttons):
            self.buttonLayout.addWidget(button, i, 0)

    def open_new_window(self, category):
        # Open a new window based on the category
        if category == "Western Australia Uni":
            QDesktopServices.openUrl(QUrl("https://www.uwa.edu.au/seek-wisdom/seekers-space/study/study-tips/2023/09/7-exam-tips-to-help-you-succeed"))
        elif category == "Self Help Website":
            QDesktopServices.openUrl(QUrl("https://www.wikihow.com/Main-Page"))
        elif category == "The StudySpace":
            QDesktopServices.openUrl(QUrl("https://www.thestudyspace.com/page/exam-techniques/"))

class SchoolResourcesWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # Store the reference to the main window
        self.main_window = main_window
        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Create the main vertical layout
        self.layout = QVBoxLayout()

        # Create the top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with style and connect its signal to the toggle_sort_order method
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with placeholder text and connect its signal to the on_search method
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretchable space between widgets
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout (grid layout) with spacing
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(20)

        # Define the categories and their URLs
        self.categories = {
            "Student Portal": "https://portal.education.nsw.gov.au/",
            "School Library": "https://oliver-10.library.det.nsw.edu.au/3/home/news",
            "Adobe Suite": "https://www.adobe.com/apps/all/desktop",
            "Sentral": "https://carlingfordhs.sentral.com.au/s-vQamQe/portal/#!/student/1305",
            "Academic Resources": "https://oliver-10.library.det.nsw.edu.au/3/learnpath/guide/ResearchDatabases",
            "Microsoft Suite": "https://login.microsoftonline.com/login.srf?wa=wsignin1.0&whr=det.nsw.edu.au&wreply=https:%2f%2fportal.office.com"
        }
        self.buttons = []
        # Define positions for the buttons in a grid layout
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

        # Create buttons for each category and add them to the grid layout
        for position, (category, url) in zip(positions, self.categories.items()):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 100)  # Set minimum size for the buttons
            button.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            # Connect the button click to the open_url method with the respective URL
            button.clicked.connect(lambda _, url=url: self.open_url(url))
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Create the navigation buttons layout
        navLayout = QHBoxLayout()
        # Create the previous navigation button with style and connect its signal to the navigate_left method
        self.prevButton = QPushButton("⬅", self)
        self.prevButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.prevButton.clicked.connect(self.navigate_left)
        # Create the next navigation button with style and connect its signal to the navigate_right method
        self.nextButton = QPushButton("➡", self)
        self.nextButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.nextButton.clicked.connect(self.navigate_right)

        # Add navigation buttons to the navigation layout
        navLayout.addWidget(self.prevButton, alignment=Qt.AlignLeft)
        navLayout.addStretch()  # Add stretchable space between buttons
        navLayout.addWidget(self.nextButton, alignment=Qt.AlignRight)

        # Add the navigation layout to the main layout
        self.layout.addLayout(navLayout)
        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Set the window title, geometry, and background color
        self.setWindowTitle("School Resources")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #121212;")

        # Initialize sorting order flag
        self.ascending = True

    def open_url(self, url):
        # Open the given URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()
            else:
                button.hide()

    def toggle_sort_order(self):
        # Toggle the sorting order and update the button text
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")
        # Call sort_buttons method to reorder the buttons
        self.sort_buttons()

    def sort_buttons(self):
        # Sort the buttons based on their text
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)
        # Re-add buttons to the layout in the new order
        for i, button in enumerate(self.buttons):
            self.buttonLayout.addWidget(button, i // 2, i % 2)

    def keyPressEvent(self, event):
        # Set focus to the search bar when a key is pressed
        if event.text():
            self.searchBar.setFocus()

    def navigate_left(self):
        # Close the current window and open the "Study Guides" window
        self.close()
        self.main_window.open_new_window("Study Guides")

    def navigate_right(self):
        # Close the current window and open the "Miscellaneous Info" window
        self.close()
        self.main_window.open_new_window("Miscellaneous Info")

class MiscellaneousInfoWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # Store the reference to the main window
        self.main_window = main_window
        # Initialize the UI
        self.initUI()

    def initUI(self):
        # Create the main vertical layout
        self.layout = QVBoxLayout()

        # Create the top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button with style and connect its signal to the toggle_sort_order method
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)

        # Create the search bar with placeholder text and connect its signal to the on_search method
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)
        topLayout.addStretch()  # Add stretchable space between widgets
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Create the main buttons layout (grid layout) with spacing
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(20)

        # Define the categories and their URLs
        self.categories = {
            "Eating Habits": "https://www.betterhealth.vic.gov.au/health/healthyliving/healthy-eating",
            "School Calendar": "https://carlingfordhs.sentral.com.au/webcal/calendar/19",
            "E-Books": "https://soraapp.com/",
            "Physical Habits": "https://nutritionsource.hsph.harvard.edu/2013/11/04/making-exercise-a-daily-habit-10-tips/",
            "School Intranet": "https://sites.google.com/education.nsw.gov.au/carlingfordhs-student-intranet/home",
            "Online Safety": "https://kidshelpline.com.au/teens/issues/staying-safe-online"
        }
        self.buttons = []
        # Define positions for the buttons in a grid layout
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

        # Create buttons for each category and add them to the grid layout
        for position, (category, url) in zip(positions, self.categories.items()):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 100)  # Set minimum size for the buttons
            button.setStyleSheet(
                "background-color: #3F37C9; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            # Connect the button click to the open_url method with the respective URL
            button.clicked.connect(lambda _, url=url: self.open_url(url))
            self.buttonLayout.addWidget(button, *position)
            self.buttons.append(button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.buttonLayout)

        # Create the navigation buttons layout
        navLayout = QHBoxLayout()
        # Create the previous navigation button with style and connect its signal to the navigate_left method
        self.prevButton = QPushButton("⬅", self)
        self.prevButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.prevButton.clicked.connect(self.navigate_left)
        # Create the next navigation button with style and connect its signal to the navigate_right method
        self.nextButton = QPushButton("➡", self)
        self.nextButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.nextButton.clicked.connect(self.navigate_right)

        # Add navigation buttons to the navigation layout
        navLayout.addWidget(self.prevButton, alignment=Qt.AlignLeft)
        navLayout.addStretch()  # Add stretchable space between buttons
        navLayout.addWidget(self.nextButton, alignment=Qt.AlignRight)

        # Add the navigation layout to the main layout
        self.layout.addLayout(navLayout)
        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Set the window title, geometry, and background color
        self.setWindowTitle("Miscellaneous Info")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #121212;")

        # Initialize sorting order flag
        self.ascending = True

    def on_search(self):
        # Filter buttons based on the search text
        search_text = self.searchBar.text().lower()
        for button in self.buttons:
            if search_text in button.text().lower():
                button.show()
            else:
                button.hide()

    def toggle_sort_order(self):
        # Toggle the sorting order and update the button text
        self.ascending = not self.ascending
        self.azButton.setText("A - Z" if self.ascending else "Z - A")
        # Call sort_buttons method to reorder the buttons
        self.sort_buttons()

    def sort_buttons(self):
        # Sort the buttons based on their text
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)
        # Re-add buttons to the layout in the new order
        for i, button in enumerate(self.buttons):
            self.buttonLayout.addWidget(button, i // 2, i % 2)

    def keyPressEvent(self, event):
        # Set focus to the search bar when a key is pressed
        if event.text():
            self.searchBar.setFocus()

    def navigate_left(self):
        # Close the current window and open the "School Resources" window
        self.close()
        self.main_window.open_new_window("School Resources")

    def navigate_right(self):
        # Close the current window and open the "Health Check-Up" window
        self.close()
        self.main_window.open_new_window("Health Check-Up")

    def open_url(self, url):
        # Open the given URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

class HealthCheckUpWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to the main window
        self.initUI()  # Initialize the UI

    def initUI(self):
        self.layout = QVBoxLayout()  # Main layout of the window

        # Top bar layout
        topLayout = QHBoxLayout()

        # Create the "A-Z" toggle button
        self.azButton = QPushButton("A - Z", self)
        self.azButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")
        self.azButton.clicked.connect(self.toggle_sort_order)  # Connect button to toggle_sort_order method

        # Create the search bar
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")  # Placeholder text for the search bar
        self.searchBar.textChanged.connect(self.on_search)  # Connect text change to on_search method
        self.searchBar.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 16pt; padding: 16px;")

        # Add widgets to the top bar layout
        topLayout.addWidget(self.azButton, alignment=Qt.AlignLeft)  # Add A-Z button aligned left
        topLayout.addStretch()  # Add stretch to push search bar to the right
        topLayout.addWidget(self.searchBar, alignment=Qt.AlignRight)  # Add search bar aligned right

        # Add the top bar layout to the main layout
        self.layout.addLayout(topLayout)

        # Main buttons layout
        self.buttonLayout = QGridLayout()  # Grid layout for the category buttons
        self.buttonLayout.setSpacing(20)  # Set spacing between buttons

        # Categories buttons with links
        self.categories = {
            "Eating Habits": "https://www.nhs.uk/live-well/eat-well/how-to-eat-a-balanced-diet/eight-tips-for-healthy-eating/",
            "Coping With Stress": "https://www.helpguide.org/articles/stress/stress-management.htm",
            "Mental Health Quiz": "https://www.headtohealth.gov.au/quiz",
            "Physical Habits": "https://nutritionsource.hsph.harvard.edu/2013/11/04/making-exercise-a-daily-habit-10-tips/",
            "Mental Health Fact Sheet": "https://www.blackdoginstitute.org.au/resources-support/fact-sheets/",
            "Get Better Sleep": "https://www.blackdoginstitute.org.au/resources-support/digital-tools-apps/sleep-ninja/"
        }
        self.buttons = []  # List to store the buttons
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]  # Define button positions in a grid layout

        # Create and add buttons for each category
        for position, (category, url) in zip(positions, self.categories.items()):
            button = QPushButton(category, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make button expandable
            button.setMinimumSize(150, 100)  # Set minimum size for the button
            button.setStyleSheet("background-color: #B5179E; color: #f8f9fa; font-family: Helvetica; font-size: 26pt;")
            button.clicked.connect(lambda _, url=url: self.open_url(url))  # Connect button click to open_url method
            self.buttonLayout.addWidget(button, *position)  # Add button to the grid layout at the specified position
            self.buttons.append(button)  # Add button to the list of buttons

        self.layout.addLayout(self.buttonLayout)  # Add the button layout to the main layout

        # Navigation buttons at the bottom
        navLayout = QHBoxLayout()  # Horizontal layout for navigation buttons
        self.prevButton = QPushButton("⬅", self)
        self.prevButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.prevButton.clicked.connect(self.navigate_left)  # Connect button click to navigate_left method

        self.nextButton = QPushButton("➡", self)
        self.nextButton.setStyleSheet("background-color: #4895EF; color: #f8f9fa; font-family: Helvetica; font-size: 30pt; padding: 20px;")
        self.nextButton.clicked.connect(self.navigate_right)  # Connect button click to navigate_right method

        navLayout.addWidget(self.prevButton, alignment=Qt.AlignLeft)  # Add previous button aligned left
        navLayout.addStretch()  # Add stretch to push next button to the right
        navLayout.addWidget(self.nextButton, alignment=Qt.AlignRight)  # Add next button aligned right

        self.layout.addLayout(navLayout)  # Add the navigation layout to the main layout
        self.setLayout(self.layout)  # Set the main layout for the window

        self.setWindowTitle("Health Check-Up")  # Set window title
        self.setGeometry(200, 200, 800, 600)  # Set window size and position
        self.setStyleSheet("background-color: #121212;")  # Set background color

        self.ascending = True  # Flag to track sort order

    def on_search(self):
        search_text = self.searchBar.text().lower()  # Get the search text in lower case
        for button in self.buttons:  # Iterate through all buttons
            if search_text in button.text().lower():  # If the search text is in the button text
                button.show()  # Show the button
            else:
                button.hide()  # Hide the button

    def toggle_sort_order(self):
        self.ascending = not self.ascending  # Toggle the sort order flag
        self.azButton.setText("A - Z" if self.ascending else "Z - A")  # Update button text
        self.sort_buttons()  # Sort the buttons

    def sort_buttons(self):
        self.buttons.sort(key=lambda btn: btn.text(), reverse=not self.ascending)  # Sort buttons by text
        for i, button in enumerate(self.buttons):  # Iterate through sorted buttons
            self.buttonLayout.addWidget(button, i // 2, i % 2)  # Re-add buttons to the grid layout

    def keyPressEvent(self, event):
        if event.text():  # If a key is pressed
            self.searchBar.setFocus()  # Focus the search bar

    def navigate_left(self):
        self.close()  # Close the current window
        self.main_window.open_new_window("Miscellaneous Info")  # Open the previous window

    def navigate_right(self):
        self.close()  # Close the current window
        self.main_window.open_new_window("Study Guides")  # Open the next window

    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))  # Open the URL in the default web browser

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchApp()  # Create the main application window
    ex.show()  # Show the main application window
    sys.exit(app.exec_())  # Start the application event loop
