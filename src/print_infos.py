import re


def remove_ansi(text):
    # Matches any ANSI escape sequence
    ansi_escape_pattern = re.compile(r'\x1b[^m]*m')
    # Replaces all matches with an empty string
    return ansi_escape_pattern.sub('', text)



# Print it
# ========
def print_infos(ascii_art: list[str], lang_out: list[str], aligned: bool, align: str="center"):

    """
    A function that prints the info of the language
    with the ASCII art
    """

    first = max((len(ascii_art) - len(lang_out)) // 2, 0)
    second = (len(ascii_art) + len(lang_out)) // 2

    # If there is an horizontal align
    # We need to get the maximum line width
    if aligned:
        max_len: int = len(remove_ansi(max(ascii_art, key=lambda s: len(remove_ansi(s)))))
    else:
        max_len: int = -1


    match align:
        case "top":
            for i in range(max(len(ascii_art), len(lang_out))):
                line: str = ""

                # If it's the end of the ascii art
                # Add a blank line if aligned, else
                # just add nothing
                if i >= len(ascii_art):
                    line = " " * (aligned * max_len)
                    line += " " + lang_out[i]
                else:
                    line = ascii_art[i]

                    if i < len(lang_out):
                        line += " " * (aligned * (max_len - len(remove_ansi(ascii_art[i]))))
                        line += " " + lang_out[i]

                print(line)




        case "center":
            # First, print the language
            for i in range(first):
                print(ascii_art[i])

            for i in range(first, second):
                # If it shouldn't be aligned
                if i < len(ascii_art):
                    if not aligned:
                        print(ascii_art[i], lang_out[i - first])
                    else:
                        print(ascii_art[i],
                            (" " * (max_len - len(remove_ansi(ascii_art[i])))) +
                            lang_out[i - first]
                        )
                else:
                    print(" " * (aligned * -~max_len) + lang_out[i - first])

            for i in range(second, max(len(ascii_art), len(lang_out))):
                if i < len(ascii_art):
                    print(ascii_art[i])
                else:
                    print(" " * (aligned * -~max_len) + lang_out[i])



        case "bottom":
            for i in range(max(len(ascii_art), len(lang_out))):
                line: str = ""

                # If it's the end of the ascii art
                # Add a blank line if aligned, else
                # just add nothing
                if i >= len(ascii_art):
                    line = " " * (aligned * max_len)
                    line += " " + lang_out[i]
                else:
                    line = ascii_art[i]

                    lang_it = i - len(ascii_art) + len(lang_out)

                    if lang_it >= 0:
                        line += " " * (aligned * (max_len - len(remove_ansi(ascii_art[i]))))
                        line += " " + lang_out[i]

                print(line)
