# Python screenplay renderer

The aim of this project is to create a simple document parser in Python, to render movie screenplays as a pdf file. Nothing fancy, just a nice cover page and the screenplay.

The screenplay file follows a LaTex-like syntax, and is coupled with a metadata file (containing the project's title, the writers' names, the director's name, _et cetera_).

The Python program ought to be simple and to work with few external libraries.

## Usage

### Installation

To install the program, one needs [Python](https://www.python.org/) (I use [version 3.8.3](https://www.python.org/downloads/release/python-383/)) and all the required dependancies:
```shell
python -m pip install -r requirements.txt
```

### Create a project

A project is a directory containing at least a metadata file and a screenplay file (their exact names are defined as constants in the `render.py` file). The `create-projects.ps1` script helps creating a project.

### Render a project

To render, use the following command:
```shell
python render.py path/to/project/directory/
```
All options are available with the `--help` flag.

Moreover, a demo project has been added to this repository to test the program.

## Screenplay syntax

A screenplay is written as a LaTex document (see the `demo/screenplay.txt` example): `\command{arg1}{arg2}[optional]`. Here are the available commands:

+ `\scene{<int/ext>}{<location>}{<time>}` : begins a new scene ;
+ `\summary{<text>}` : displays a summary of the scene ;
+ `\dialog{<character>}[<direction>]{<speech>}` : write a dialog ;
+ `\dir{<text>}` : displays a direction ;
+ `\transition{<text>}` : displays a transition to the next scene ;
+ `\end` : marks the end of the screenplay.

Text written between the `<` and `>` characters are interpreted as comments and will not be displayed.

All the remaining text is displayed as actions.
