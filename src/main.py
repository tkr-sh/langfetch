#!/usr/bin/env python

from json import load
from subprocess import run
from .log import logger
from re import search
from .get_ascii_art import get_ascii_art
from .get_params import get_argv
from .print_infos import print_infos
from os.path import isfile, expanduser
from distutils.spawn import find_executable


# Load the language informations from the JSON
if isfile("/".join(__file__.split("/")[:-1]) + "/" + "languages.json"):
    LANGUAGES_JSON = load(open("/".join(__file__.split("/")[:-1]) + "/" + "languages.json", 'r', encoding="utf-8"))
elif isfile("/usr/share/langfetch/languages.json"):
    LANGUAGES_JSON = load(open("/usr/share/langfetch/languages.json", 'r', encoding="utf-8"))
elif isfile("/usr/local/share/langfetch/languages.json"):
    LANGUAGES_JSON = load(open("/usr/local/share/langfetch/languages.json", 'r', encoding="utf-8"))
else:
    logger.error("No languages.json file found")
    exit(127)


# Functions
## Convert hex to list
hex_to_list = lambda s: [str(int(s[1 + i * 2:1 + -~i * 2], 16)) for i in range(3)]
## Convert rgb to ANSI
rgb_to_ansi = lambda s: f"\033[38;2;{';'.join(hex_to_list(s))}m"



# The languages to display
langs = []
main_lang = "Python"
max_popularity = -1
for language, data in LANGUAGES_JSON.items():
    if find_executable(data["path"]) or find_executable("/usr/bin/" + data["path"]) or find_executable("/bin/" + data["path"]):
        langs.append(language)

        if data["popularity"] > max_popularity:
            max_popularity = data["popularity"]
            main_lang = language


# langs = ["Python", "gcc", "Bash", "Perl"]
# main_lang = "Python"

# The output of the languages
lang_out = []

# If it must be aligned
aligned = True

# Aligned to top, center or bottom
align = "center"

# Define the color of the Ascii art
colors = None

# The variable that is here to put color on the name of the language
color_lang = None

# Do we need to sort the languages
sort = None


if isfile(expanduser("~") + "/.config/langfetch/config.json"):
    # Read the default values from the file
    with open(expanduser('~') + "/.config/langfetch/config.json") as config_json:
        data = load(config_json)

        main_lang = data.get("lang", main_lang)
        align = data.get("align", align)
        aligned = data.get("aligned", aligned)
        colors = data.get("colors", colors)
        color_lang = data.get("color", color_lang)
        sort = data.get("sort", sort)
        langs = data.get("langs", langs)



# Get the argv
params = get_argv()

if "lang" in params and params["lang"] is not None:
    main_lang = params["lang"]
if "align" in params and params["align"] is not None:
    align = params["align"]
if "aligned" in params and params["aligned"] is not None:
    aligned = params["aligned"]
if "colors" in params and params["colors"] is not None:
    colors = params["colors"]
if "color" in params and params["color"] is not None:
    color_lang = params["color"]
if "sort" in params and params["sort"] is not None:
    sort = params["sort"]


# Sort the languages
if sort:
    langs.sort(key=lambda c:c.lower())

# For each lang that we want to have the version of
# ==================================================
for lang in langs:
    if lang.lower() in LANGUAGES_JSON:
        # Get the attributes of a lang
        lang_attributes = LANGUAGES_JSON[lang.lower()]
        color = "\033[1m"

        # If there is a color
        if "colors" in lang_attributes and len(lang_attributes["colors"]) > 0 and color_lang is None:
            color = rgb_to_ansi(lang_attributes['colors'][0])
        elif color_lang is not None:
            color = rgb_to_ansi(color_lang)



        # If there is all the correct data
        if "path" in lang_attributes and "regex" in lang_attributes and "version" in lang_attributes:
            # Put the values in some variables
            version, path, regex = lang_attributes["version"], lang_attributes["path"], lang_attributes["regex"]

            # Execute the command to get the version
            sys_version = run([path, version], capture_output=True, text=True)
            # Match it with a regex
            match_regex = search(regex, sys_version.stdout + sys_version.stderr)

            # If there is a match
            if match_regex:
                lang_out.append(f"\033[1m{color}{lang}\033[0m: {match_regex.group(0)}")
            else:
                logger.warning(f"There is a problem with the version of {lang}")
        else:
            logger.warning(f"There is an error with {lang}, missing some fields")
            continue
    else:
        logger.warning(f"{lang} doesn't exist")



# Get the ASCII art
# =================
ascii_art: str = "$1" + get_ascii_art(main_lang)


# Get the colors of the language
if main_lang.lower() in LANGUAGES_JSON and colors is None:
    colors = LANGUAGES_JSON[main_lang.lower()]["colors"]
elif colors is None:
    logger.error("No language with that name")
    exit()


# Restore the color at the start of the line
curr_color = "$1"
for i in range(len(ascii_art)):
    if ascii_art[i] == '$':
        if len(ascii_art) != i - 1 and ascii_art[i + 1].isdigit():
            curr_color = f'${ascii_art[i+1]}'
    elif ascii_art[i] == '\n':
        ascii_art = ascii_art[:i + 1] + curr_color + ascii_art[i + 1:]

for i,color in enumerate(colors):
    ascii_art = ascii_art.replace(f"${i+1}", rgb_to_ansi(color))

ascii_art = ascii_art.split("\n")



# Print it
# ========
print_infos(ascii_art, lang_out, aligned, align=align)
