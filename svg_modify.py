import re
import glob
from track_info import SpotifyAPI
from dotenv import load_dotenv
import os


def swap_logo_fill(new_color: str, line: str, old_color: str = "000000"):
    pattern = r"(?<=^\<g\stransform\=\"translate\(20\,20\)\"\>\<path\sfill\=\"\#){}"
    matches = re.findall(pattern.format(old_color), line)
    assert len(matches) == 1, "regex pattern does not have singular match"
    return re.sub(pattern.format(old_color), new_color, line)


def change_svg_logo_color(file_path: str, new_color: str, old_color: str = "000000"):
    with open(file_path, "r") as f:
        lines = f.readlines()

    lines[-2] = swap_logo_fill(new_color, lines[-2], old_color)

    with open(file_path, "w") as f:
        f.writelines(lines)


def get_svg_filepaths(directory: str):
    # Get all .svg files in the specified directory
    return glob.glob(os.path.join(directory, "*.svg"))


def rename_file(file_path: str):

    directory, file_name = os.path.split(file_path)
    file_name = os.path.splitext(file_name)[0]

    # Extract the track ID from the filename
    track_id = file_name.split("-")[1]

    # Get the track info using the track ID
    load_dotenv("secrets.env")
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    track_name, artist_names = spotify.get_track_info(track_id)

    # Ensure the track name is alphanumeric
    track_name = re.sub(r"\W+", "_", track_name)

    # Ensure the artist names are alphanumeric
    artist_names = [re.sub(r"\W+", "_", artist) for artist in artist_names]

    # Create the new filename
    new_filename = f"{track_name}_{'_'.join(artist_names)}.svg"

    # Rename the file
    os.rename(file_path, os.path.join(directory, new_filename))


if __name__ == "__main__":
    svg_filepaths = "downloaded_song_codes"
    for fp in get_svg_filepaths(svg_filepaths):
        change_svg_logo_color(fp, '3d3d3d')
        rename_file(fp)