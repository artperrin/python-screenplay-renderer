import re
import logging as lg


def begins_with(string: str, substring: str) -> bool:
    """Checks wether a given string begins with a given substring.

    Args:
        string (str): string that may begin with the substring.
        substring (str): the substring the string may begin with.

    Returns:
        bool: whether the string begins with the substring.
    """
    return string[: len(substring)] == substring


def get_header(line: str) -> str:
    """Checks whether a line is a scene header, a summary, a dialog, a transition, or something else.

    Args:
        line (str): line to be checked.

    Returns:
        str: the line's type.
    """
    if begins_with(line, "\\scene"):
        return "scene"
    elif begins_with(line, "\\summary"):
        return "summary"
    elif begins_with(line, "\\dialog"):
        return "dialog"
    elif begins_with(line, "\\end"):
        return "end"
    elif begins_with(line, "\\dir"):
        return "dir"
    elif begins_with(line, "\\transition"):
        return "transition"
    elif begins_with(line, "<"):
        return "comment"
    else:
        return "action"


def get_scene_info(line: str) -> tuple:
    """Extracts all scene's info from the line.

    Args:
        line (str): scene header.

    Returns:
        tuple: value, location and time of the scene.
    """
    infos = re.findall("(\{[^{}]+\})", line)
    if len(infos) != 3:
        lg.error(f"Wrong infos on the scene! Expected 3, got {len(infos)}.")
        res = ()
    else:
        res = (infos[0][1:-1], infos[1][1:-1], infos[2][1:-1])
    return res

def get_dir_info(line: str) -> tuple:
    """Extracts all direction's info from the line.

    Args:
        line (str): direction header.

    Returns:
        tuple: direction.
    """
    dirs = re.findall("(\{[^{}]+\})", line)
    if len(dirs) != 1:
        lg.error(f"Wrong infos on the scene! Expected 1, got {len(dirs)}.")
        res = ""
    else:
        res = dirs[0][1:-1]
    return res

def get_dialog_info(line: str) -> tuple:
    """Extracts all dialog's info from the line.

    Args:
        line (str): dialog line.

    Returns:
        tuple: speaker, line, direction (if any)
    """
    required = re.findall("(\{[^{}]+\})", line)
    if len(required) != 2:
        lg.error(f"Wrong infos on the dialog! Expected 2, got {len(required)}.")
        res = ()
    else:
        optional = re.findall("\[([^]]+)\]", line)
        if optional:
            res = (required[0][1:-1], required[1][1:-1], optional[0])
        else:
            res = (required[0][1:-1], required[1][1:-1], "")
    return res


def get_summary(line: str) -> str:
    """Extracts the summary from the line.

    Args:
        line (str): summary line.

    Returns:
        str: the summary.
    """
    summary = re.findall("(\{[^{}]+\})", line)
    if len(summary) != 1:
        lg.error(f"Wrong summary! Expected , got {len(summary)}.")
        res = ""
    else:
        res = summary[0][1:-1]
    return res


def get_transition(line: str) -> str:
    """Extracts the transition from the line.

    Args:
        line (str): transition line.

    Returns:
        str: the transition.
    """
    transition = re.findall("(\{[^{}]+\})", line)
    if len(transition) != 1:
        lg.error(f"Wrong summary! Expected , got {len(transition)}.")
        res = ""
    else:
        res = transition[0][1:-1]
    return res
