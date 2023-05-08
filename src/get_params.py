from sys import argv


def get_argv():

    """
    Get the ARGV
    """

    # Define variables
    lang = align = aligned = colors = color = sort = None


    # If the user want some help
    if "--help" in argv or "-h" in argv:
        print("""Langfetch is a CLI system information tool written in Python3. Langfetch displays information about the programming languages on your system and their version.
    --lang, -l   Which language should be displayed in ASCII art
    --align      Vertical align ("top", "center", "bottom")
    --aligned    Should it be aligned or not (true, false)
    --colors     Colors that should be used by the ascii art
    --color      The colors of the name of the languages
    --sort       Should the languages be sorted by name or not (true, false)""")
        exit(0)

    # Get the lang
    if "--lang" in argv or "-l" in argv:
        lang_index = (argv.index("-l") if "-l" in argv else argv.index("--lang")) + 1
        if lang_index < len(argv):
            lang = argv[lang_index]


    # Where should it be aligned
    if "--align" in argv:
        align_index = argv.index("--align") + 1
        if align_index < len(argv):
            align = argv[align_index]

    # Should it be aligned horizontally
    if "--aligned" in argv:
        aligned_index = argv.index("--aligned") + 1
        if aligned_index < len(argv):
            aligned = argv[aligned_index]

    # Add the colors if the user wants to
    if "--colors" in argv:
        index_colors = argv.index("--colors") + 1
        colors = []
        while index_colors < len(argv) and argv[index_colors][0] != '-':
            colors.append('#' + argv[index_colors])
            index_colors += 1


    # Get the color
    if "--color" in argv:
        color_index = argv.index("--color") + 1
        if color_index < len(argv):
            color = "#" + argv[color_index]


    # If it should be sorted
    if "--sort" in argv:
        sort_index = argv.index("--sort") + 1
        if sort_index < len(argv):
            sort = argv[sort_index] == "true"





    return {
        "lang": lang,
        "align": align,
        "aligned": aligned,
        "colors": colors,
        "color": color,
        "sort": sort,
    }
