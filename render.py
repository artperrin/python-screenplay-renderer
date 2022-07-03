from pathlib import Path
import argparse
import logging as lg
import json

from modules.screenplay import *
from modules.utils import *
from modules.pdf_handler import *


### CONSTANTS ###


DEFAULT_OUTPUT_PATH = Path("render.pdf")
DEFAULT_SCREENPLAY_NAME = Path("screenplay.txt")
DEFAULT_METADATA_NAME = Path("metadata.json")


### FUNCTIONS ###


def read_screenplay_file(path_to_file: Path) -> list:
    """Reads the screenplay file to a string.

    Args:
        path_to_file (Path): path to the screenplay file.

    Returns:
        list: list containing the screenplay file's content.
    """
    if not path_to_file.is_file():
        lg.error(f"Path '{path_to_file}' is not valid!")
        data = []
    else:
        with open(str(path_to_file), mode="r", encoding="utf-8") as screenplay_file:
            data = [line[:-1] for line in screenplay_file.readlines()]
    return data


def read_metadata(path_to_metadata: Path) -> dict:
    """Reads the .json metadata file to a dict.

    Args:
        path_to_metadata (Path): path to the .json metadata file.

    Returns:
        dict: dictionary containing the .json's content.
    """
    if not (path_to_metadata.is_file() and path_to_metadata.suffix == ".json"):
        lg.error(f"Path {path_to_metadata} is not valid!")
        data = {}
    else:
        with open(str(path_to_metadata), mode="r", encoding="utf-8") as metadata_file:
            data = json.load(metadata_file)
    return data


def doc_to_scenes(document: list) -> list:
    """Parses the document to obtain all the scenes.

    Args:
        document (list): list of strings from the screenplay file.

    Returns:
        list: list of all scenes of the document.
    """
    scenes = []
    doc_copy = document.copy()
    in_scene = False
    in_action = False
    new_action_txt = ""
    line_type = ""
    # look at each element
    line_nb = 1
    while doc_copy:
        line = doc_copy.pop(0)
        try:
            # if the previous line was a summary or a new scene, no need for newline
            if line_type in {"scene", "summary"} and line == "\n":
                continue
            line_type = get_header(line)
            if line_type == "comment":
                continue
            # first, if we were in an action and it is now finished, append the cached action to the scene
            if in_action and line_type != "action":
                in_action = False
                if begins_with(new_action_txt, "\n"):
                    new_action_txt = new_action_txt[1:]
                if new_action_txt.endswith("\n"):
                    new_action_txt = new_action_txt[:-1]
                new_action = Action(new_action_txt)
                new_action_txt = ""
                new_scene.add_action(new_action)
            # next, check the actual type
            if line_type == "scene":
                if in_scene:  # if we were in a scene, it is a new one, so append the previous to the set
                    scenes.append(new_scene)
                in_scene = True  # create a new scene
                value, location, time = get_scene_info(line)
                new_scene = Scene(value, location, time)
            # if it is an action, cache it for later
            elif line_type == "action" and line:
                if in_action:
                    line = "\n" + line
                in_action = True
                new_action_txt += line
            elif line_type == "dialog":
                speaker, speech, direction = get_dialog_info(line)
                new_dialog = Dialog(Character(speaker), speech, direction)
                new_scene.add_dialog(new_dialog)
            elif line_type == "summary":
                new_scene.set_summary(Summary(get_summary(line)))
            elif line_type == "dir":
                dir_txt = get_dir_info(line)
                new_scene.add_dir(Dir(dir_txt))
            elif line_type == "transition":
                new_scene.set_transition(Transition(get_transition(line)))
            elif line_type == "comment":
                continue
            # if we see the end marker, break the loop
            elif line_type == "end":
                scenes.append(new_scene)
                break
        except Exception as ex:
            print(f"Exception at line {line_nb}: {ex}")
        line_nb += 1
    return scenes


def get_screenplay_args(metadata: dict) -> tuple:
    """Formats the metadata from dict to a tuple.

    Parameters
    ----------
    metadata : dict
        metadata dictionary.

    Returns
    -------
    tuple
        tuple containing all the ordered informations.
    """
    meta_copy = metadata.copy()
    return (
        meta_copy.pop("name"),
        meta_copy.pop("authors"),
        meta_copy.pop("director"),
        meta_copy.pop("creation-date"),
        meta_copy.pop("production"),
        meta_copy,
    )


def doc_to_screenplay(metadata: dict, document: list) -> Screenplay:
    """Parses the screenplay file's content to obtain a screenplay.

    Args:
        metadata (dict): dictionary containing the project's metadata.
        document (list): list of strings from the screenplay file.

    Returns:
        Screenplay: the screenplay object.
    """
    args = get_screenplay_args(metadata)
    screenplay = Screenplay(*args)
    scenes = doc_to_scenes(document)
    for scene in scenes:
        screenplay.add_scene(scene)
    return screenplay


def screenplay_to_pdf(screenplay: Screenplay, output_path: Path) -> None:
    """Writes the screenplay into a .pdf file.

    Args:
        screenplay (Screenplay): screenplay to be written.
        output_path (Path): path to the output.
    """
    pdf = create_pdf(
        screenplay.title,
        screenplay.authors,
        screenplay.director,
        screenplay.date,
        screenplay.production,
        screenplay.scenes,
        other=screenplay.other,
    )
    pdf.output(output_path)


def main(path_to_folder: Path, output_path: Path = None) -> None:
    # explore the directory
    lg.info(f"Reading directory '{path_to_folder}'...")
    if not path_to_folder.is_dir():
        lg.error(f"The path '{path_to_folder}' is not a directory!")
        return
    if not output_path:
        output_path = path_to_folder / DEFAULT_OUTPUT_PATH
        lg.info(f"Defined output path at '{output_path}'...")
    # find the metadata file
    metadata_file_path = path_to_folder / DEFAULT_METADATA_NAME
    screenplay_file_path = path_to_folder / DEFAULT_SCREENPLAY_NAME
    if not screenplay_file_path.is_file():
        lg.error(f"Screenplay file not found at '{screenplay_file_path}'!")
        return
    if not metadata_file_path.is_file():
        lg.error(f"Metadata file not found at '{metadata_file_path}'!")
        return
    # generate the screenplay
    lg.info(f"Reading screenplay content...")
    screen_content = read_screenplay_file(screenplay_file_path)
    lg.info(f"Reading metadata content...")
    meta_content = read_metadata(metadata_file_path)
    lg.info("Converting raw content to screenplay object...")
    screenplay = doc_to_screenplay(meta_content, screen_content)
    lg.info(f"Rendering the screenplay object to '{output_path}'...")
    screenplay_to_pdf(screenplay, output_path)


### SCRIPT ###


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Renders the screenplay to a .pdf file."
    )
    parser.add_argument(
        "project",
        type=str,
        help=f"path to the project's directory (must contain the screenplay file '{DEFAULT_SCREENPLAY_NAME}' and the metadata file '{DEFAULT_METADATA_NAME}').",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default=None,
        help=f"path to the rendered pdf. By default, it will be rendered in the project directory as '{DEFAULT_OUTPUT_PATH}'.",
    )
    args = parser.parse_args()
    lg.root.setLevel(lg.INFO)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = None
    main(Path(args.project), output_path)
