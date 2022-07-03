import logging as lg
from fpdf import FPDF

try:
    from modules.screenplay import *
except ModuleNotFoundError:
    from screenplay import *


class PDF(FPDF):
    """Custom PDF class as a screenplay template."""

    BETWEEN_AUTHORS_SPACE = 1
    BETWENN_OTHERS_SPACE = 5

    AFTER_SCENE_HEADER_SPACE = 10
    AFTER_SUMMARY_SPACE = 5
    AFTER_TRANSITION_SPACE = 5
    AFTER_DIALOG_SPACE = 5
    AFTER_ACTION_SPACE = 5
    AFTER_REAL_SPACE = 5

    DEBUG = 0  # draws the cells borders

    def __init__(self) -> None:
        super().__init__()
        self.previous_speaker = ""

    def set_infos(
        self, title: str, authors: list, director: str, date: str, production: str, div: dict = {}
    ) -> None:
        self.title = title
        self.authors = authors
        self.director = director
        self.date = date
        self.production = production
        self.other = div

    def draw_cover(self):
        # draw the title at two-thirds
        self.set_y(65)
        self.set_font("Courier", "", 10)
        self.cell(0, 10, "Screenplay of", self.DEBUG, 0, "C")
        self.set_y(75)
        self.set_font("Courier", "B", 25)
        self.cell(0, 10, self.title.upper(), self.DEBUG, 0, "C")
        # if there is a subtitle, print it
        if "subtitle" in self.other.keys():
            self.set_y(85)
            self.set_font("Courier", "B", 15)
            self.cell(0, 10, self.other["subtitle"].upper(), self.DEBUG, 0, "C")
        # print the authors
        self.set_y(120)
        self.set_font("Courier", "", 10)
        self.cell(0, 10, "Written by", self.DEBUG, 0, "C")
        self.set_y(127)
        self.set_font("Courier", "", 15)
        for author in self.authors:
            self.cell(0, 10, author, self.DEBUG, self.BETWEEN_AUTHORS_SPACE, "C")
        # print the director
        self.set_y(165)
        self.set_font("Courier", "", 10)
        self.cell(0, 10, "Directed by", self.DEBUG, 0, "C")
        self.set_y(172)
        self.set_font("Courier", "", 15)
        self.cell(0, 10, self.director, self.DEBUG, 0, "C")
        # print the production
        self.set_y(185)
        self.set_font("Courier", "", 10)
        self.cell(0, 10, "Produced by", self.DEBUG, 0, "C")
        self.set_y(192)
        self.set_font("Courier", "", 15)
        self.cell(0, 10, self.production, self.DEBUG, 0, "C")
        # print the date
        self.set_y(-50)
        self.set_font("Courier", "", 15)
        self.cell(120)
        self.cell(40, 10, self.date, self.DEBUG, 0, "R")
        # print all the other things that may be here
        if self.other:
            for ii, (key, value) in enumerate(self.other.items()):
                if key == "subtitle":
                    continue
                self.set_y(205 + (ii + 1) * self.BETWENN_OTHERS_SPACE)
                self.set_font("Courier", "", 12)
                self.cell(50, 5, key, self.DEBUG, 0, "L")
                self.set_font("Courier", "I", 12)
                self.cell(0, 5, value, self.DEBUG, 0, "L")

    def header(self):
        # if it is not the cover page
        if self.page_no() != 1:
            # Arial bold 10
            self.set_font("Courier", "", 10)
            # centered title
            self.cell(0, 5, f"Screenplay - {self.title.upper()}", self.DEBUG, 0, "C")
            # Line break
            self.ln(20)

    def footer(self):
        # if it is not the cover page
        if self.page_no() != 1:
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font("Courier", "I", 8)
            # Page number
            self.cell(0, 5, f"Prod. {self.production.upper()}", self.DEBUG, 0, "L")
            self.cell(0, 5, "Page " + str(self.page_no()) + "/{nb}", self.DEBUG, 0, "R")

    def add_action(self, action: Action) -> None:
        """Adds an action paragraph to the pdf.

        Args:
            action (Action): action to append.
        """
        self.set_font("Courier", "", 12)
        self.multi_cell(0, 5, action.text_without_comments, self.DEBUG)
        self.ln(self.AFTER_ACTION_SPACE)

    def add_dialog(self, dialog: Dialog) -> None:
        """Adds a dialog paragraph to the pdf.

        Args:
            action (Action): dialog to append.
        """
        self.set_font("Courier", "", 12)
        # print the character's name
        speaker = dialog.speaker.name.upper()
        if self.previous_speaker == speaker:
            # if the speaker has already spoke, write "cont'd after his name"
            speaker += " (cont'd)"
        self.cell(0, 5, speaker, self.DEBUG, 0, "C")
        self.ln(5)
        self.previous_speaker = dialog.speaker.name.upper()
        # print the direction if any
        if dialog.direction:
            self.set_font("Courier", "I", 10)
            self.cell(40)
            self.multi_cell(95, 5, f"({dialog.direction})", self.DEBUG, "C")
            self.set_font("Courier", "", 12)
        # print the line
        self.cell(40)
        self.multi_cell(95, 5, dialog.text, self.DEBUG, "C")
        self.ln(self.AFTER_DIALOG_SPACE)

    def add_transition(self, transition: Transition) -> None:
        """Adds a transition to the pdf.

        Args:
            transition (Transition): transition to append.
        """
        self.set_font("Courier", "", 12)
        self.cell(80)
        self.multi_cell(85, 5, transition.text.upper(), self.DEBUG, "R")
        self.ln(self.AFTER_TRANSITION_SPACE)

    def add_summary(self, summary: Summary) -> None:
        """Adds a summmary to the pdf.

        Args:
            summmary (Summmary): summmary to append.
        """
        self.set_font("Courier", "", 12)
        self.multi_cell(0, 5, summary.text, 1, "L")
        self.ln(self.AFTER_SUMMARY_SPACE)

    def add_dir(self, dir: Dir) -> None:
        """Adds a direction to the pdf.

        Args:
            dir (Dir): direction to append.
        """
        self.set_font("Courier", "I", 12)
        self.multi_cell(0, 5, dir.text, self.DEBUG, "L")
        self.ln(self.AFTER_REAL_SPACE)

    def add_scene_header(
        self, scene_nb: int, value: str, location: str, time: str
    ) -> None:
        """Prints a scene header.

        Parameters
        ----------
        scene_nb : int
            number of the scene.
        value : str
            value of the scene (INT or EXT).
        location : str
            where the scene takes place.
        time : str
            when the scene takes place.
        """
        self.set_font("Courier", "B", 12)
        self.cell(10, 5, f"{scene_nb}", self.DEBUG, 0, "L")
        self.cell(0, 5, f"{value.upper()}. {location}. {time.upper()}", self.DEBUG, 0, "L")
        self.ln(self.AFTER_SCENE_HEADER_SPACE)
        # reset the speakers
        self.previous_speaker = ""

    def the_end(self) -> None:
        """Prints "the end" at the end of the document."""
        self.ln(10)
        self.set_font("Courier", "B", 25)
        self.cell(0, 15, "The END", self.DEBUG, 0, "C")


def create_pdf(
    title: str,
    authors: list,
    director: str,
    date: str,
    production: str,
    list_of_scenes: list,
    other: dict = {},
) -> PDF:
    """Instantiates the pdf class and sets its attributes.

    Args:
        title (str): title of the document.
        authors (list): list of authors of the document.
        director (str): director of the project.
        date (str): creation date of the document.
        production (str): producer of the document.
        list_of_scenes (list): list of scenes to appear in the pdf.
        other (dict): other informations that might be usefull.

    Returns:
        PDF: created pdf.
    """
    pdf = PDF()
    pdf.set_infos(title, authors, director, date, production, div=other)
    pdf.set_margins(left=25, top=10, right=15)
    pdf.alias_nb_pages()
    # draw the cover page
    pdf.add_page()
    pdf.draw_cover()
    # write the body
    pdf.add_page()
    for scene_nb, scene in enumerate(list_of_scenes):
        pdf.add_scene_header(scene_nb + 1, scene.value, scene.location, scene.time)
        elements = scene.get_elements()
        for element in elements:
            if element.__class__.__name__ == "Action":
                pdf.add_action(element)
            elif element.__class__.__name__ == "Dialog":
                pdf.add_dialog(element)
            elif element.__class__.__name__ == "Transition":
                pdf.add_transition(element)
            elif element.__class__.__name__ == "Summary":
                pdf.add_summary(element)
            elif element.__class__.__name__ == "Dir":
                pdf.add_dir(element)
            else:
                lg.warning(f"Unknown element found: {element.__class__.__name__}. Ignoring it.")
    pdf.the_end()
    return pdf
