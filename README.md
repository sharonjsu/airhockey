
<img src="docs/header.png" width = "1000">

# airhockey
`airhockey`, a package for passing information back and forth from Airtable for the Behnia lab database.

Sections:
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Structure](#structure)

## Installation

Navigate to the directory containing `pyproject.toml` and type in your CLI:
```
python3 -m pip install .
```
## Getting Started

Add your access token into the config.py file. I'll add instructions later but I believe in you. You can do it.


## Structure


 I will outline what the table structure looks like here later, but you can also just look at the classes yourself.


## TO DO: 
- Current version not robust to arbitrary changes in Airtable column titles
- Actually implement a config parser or something instead of just shoving your token as a global variable in a .py file lmao
- Unit tests
- Fix Stock casefold bug
- Add search function for "all" [just convert everything to a string]
- Think of a system so that people can access their own tables without having to actually hardcode it into anything aside from a config file? 
        - Maybe make generic all the functions 