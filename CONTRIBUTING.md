# Contributing to langfetch
## Bugs and suggestions
If you found a bug or you want to add something to langfetch, you can first open an issue or make a pull request

## Adding a language
If you want to add a language there are several things that you need to do:
1) Add informations (path, colors, regex, version) about the language in `languages.json`.
    - **path**: The path to the executable file
    - **colors**: The colors of the language
    - **regex**: The regex that matches the version of the languages
    - **version**: The flag used to get the version of the language
2) Generate the ASCII art.
    - Get a SVG of the logo of the programming language.
    - Put it in the "icons" folder.
    - Run the `convert_svg_to_ascii.py` program
    - Add it to `src/get_ascii_art.py` as a match/case
3) Update the popularity of the languages
    - Run `popularity_language.py` to update the popularity of each languages
