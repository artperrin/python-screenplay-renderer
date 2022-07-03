from typing import Union


### FUNCTIONS ###


def remove_multiple_spaces(string: str) -> str:
    """Removes multiple spaces from a string (and keeps whitespaces).

    Args:
        string (str): string to remove the spaces from.

    Returns:
        str: string without multiple spaces
    """
    return "\n".join(" ".join(line.split()) for line in string.splitlines())


### CLASSES ###

class Dir:
    """Object that represents directions elements."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = None

    def set_pos(self, pos: int) -> None:
        self.pos = pos


class Transition:
    """Object that represents a transition."""

    def __init__(self, text: str) -> None:
        self.text = text


class Summary:
    """Object that represents a summary."""

    def __init__(self, text: str) -> None:
        self.text = text


class Character:
    """Object that represents a character."""

    def __init__(self, name: str, actor: str = "") -> None:
        self.name = name
        self.actor = actor


class Action:
    """Object that represents an action."""

    def _remove_comments(self, text: str) -> tuple:
        """Remove the comments from the text.

        Args:
            text (str): text with comments.

        Returns:
            tuple: (str) text without comments, (list) (start,end) indices of comments.
        """
        no_comments = ""
        indices = []
        inside = False
        for pos, char in enumerate(text):
            if char == "<":
                inside = True
                start = pos
            elif inside and char == ">":
                inside = False
                end = pos
                indices.append((start, end))
            else:
                if not inside:
                    no_comments += char
        return remove_multiple_spaces(no_comments), indices

    def __init__(self, text: str) -> None:
        self.pos = None
        self.text_with_comments = text
        self.text_without_comments, self.comments_pos = self._remove_comments(text)

    def set_pos(self, pos: int) -> None:
        """Sets the position of the action in the scene.

        Args:
            pos (int): position in the scene.
        """
        self.pos = pos


class Dialog:
    """Object that represents a dialog."""

    def __init__(self, speaker: Character, text: str, direction: str = "") -> None:
        self.pos = None
        self.speaker = speaker
        self.text = text
        self.direction = direction

    def set_pos(self, pos: int) -> None:
        """Sets the position of the dialog in the scene.

        Args:
            pos (int): position in the scene.
        """
        self.pos = pos


class Scene:
    """Object that represents a scene."""

    def __init__(self, value: str, location: str, time: str) -> None:
        """Initializes the scene.

        Args:
            value (str): INT or EXT.
            location (str): where the scene takes place.
            time (str): when the scene takes place (DAY, NIGHT, ...).
        """
        self.value = value.upper()
        self.location = location
        self.time = time
        self.actions = []
        self.dirs = []
        self.dialogs = []
        self.transition = ""
        self.summary = ""
        self.pos = 0

    def add_action(self, action: Action) -> None:
        action.set_pos(self.pos)
        self.pos += 1
        self.actions.append(action)

    def add_dialog(self, dialog: Dialog) -> None:
        dialog.set_pos(self.pos)
        self.pos += 1
        self.dialogs.append(dialog)

    def add_dir(self, dir: Dir) -> None:
        dir.set_pos(self.pos)
        self.pos += 1
        self.dirs.append(dir)

    def set_transition(self, transition: Transition) -> None:
        self.transition = transition

    def set_summary(self, summary: Summary) -> None:
        self.summary = summary

    def get_elements(self) -> list:
        """Returns all elements by order

        Returns:
            list: ordered list of all elements.
        """
        res = [None for _ in range(self.pos)]
        for action in self.actions:
            res[action.pos] = action
        for dialog in self.dialogs:
            res[dialog.pos] = dialog
        for dir in self.dirs:
            res[dir.pos] = dir
        if self.summary:
            res = [self.summary] + res
        if self.transition:
            res += [self.transition]
        return res


class Screenplay:
    """General object to represent a screenplay."""

    def __init__(
        self, title: str, authors: Union[list, str], director: str, date: str, production: str, other: dict = {}
    ) -> None:
        """Initializes the screenplay.

        Args:
            title (str): title of the screenplay.
            authors (list | str): list of authors or the single author as str.
            director: name of the director.
            date (str): creation date (format dd/MM/yyy).
            production (str): production name.
            other (dict): other informations that might be usefull
            . Defaults to {}.
        """
        self.title = title
        if type(authors) is list:
            self.authors = authors
        else:
            self.authors = [authors]
        self.director = director
        self.date = date
        self.production = production
        self.other = other
        self.scenes = []

    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)
