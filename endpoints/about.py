import os

path = ""

def main(*args, **kwargs):
    # Load all filenames in assets/frames
    frames = [f'`{x.split(".")[0].lower()}`' for x in os.listdir('assets/frames')]
    frame_list = ", ".join(frames)
    # Replace the final "," with ", or"
    frame_list = ', or'.join(frame_list.rsplit(',', 1))

    return f"""
    # Avatar endpoints
    Use either `avatar.png` or `avatar.svg` to generate an avatar, depending on the format you want.

    ## Parameters
    - colour: The colour of the avatar. Can be one of `purple`, `red`, `black`, `green`, `blue` or `yellow`. Defaults to `purple`.
    - frame: The frame to use. Omit this for no frame. One of {frame_list}. Defaults to `none`.
      - This can only be used with the `circle` shape, otherwise the frame will be ignored.
    - shape: The shape of the avatar. One of `circle` or `square`. Defaults to `circle`.
    - gradient_start: The start colour of the gradient. Defaults to the value needed for colour.
    - gradient_end: The end colour of the gradient. Defaults to the value needed for colour.
    - - Both a start and end point must be specified
    - pineapple_colour: The colour of the pineapple. Defaults to `white`.
    - output_format: The format of the output.
      - `svg` for SVG, and cannot be changed
      - For PNG, either `512` or `2048`. Defaults to `2048`.
    """
