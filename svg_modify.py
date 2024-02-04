import re

def swap_logo_fill(new_color:str, line:str, old_color:str='000000'):
    pattern = r"(?<=^\<g\stransform\=\"translate\(20\,20\)\"\>\<path\sfill\=\"\#){}"
    matches = re.findall(pattern.format(old_color), line)
    assert len(matches)==1, "regex pattern does not have singular match"
    return re.sub(pattern.format(old_color), new_color, line)

def change_svg_logo_color(file_path:str, new_color:str, old_color:str='000000'):
    with open(file_path, "r") as f:
        lines = f.readlines()

    lines[-2] = swap_logo_fill(new_color, lines[-2], old_color)

    with open(file_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    test_filepath = "downloaded_song_codes\spcode-5EFczt9dqrCu60udoD41Yy.svg"
    change_svg_color(test_filepath, '3d3d3d')