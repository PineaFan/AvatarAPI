from endpoints import list as all_list
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import cairosvg
import os


colour_definitions = {
    "black": ("424242", "8D8D8D"),
    "blue": ("78ECF2", "71AFE5"),
    "green": ("65CC76", "68D49E"),
    "purple": ("6576CC", "8D58B3"),
    "red": ("F27878", "D96B6B"),
    "yellow": ("F2D478", "EDC575"),
}


def make_circle(base_image):
    # Modify the rx property of the first rect element to be 50%
    base_image[0][0].attrib["rx"] = "50%"
    return base_image


def add_frame(base_image, frame):
    frame_svg = ET.parse(f"assets/frames/{frame}.svg").getroot()
    frame_svg = frame_svg[0]
    # Get the path elements inside frame_svg
    frame_svg = frame_svg.findall("{http://www.w3.org/2000/svg}path")

    # Overlay into the base image
    # This involves putting these elements into the base image at the end of the first g element

    base_image[0].extend(frame_svg)
    return base_image


def set_gradient(base_image, start, end):
    # Set the gradient start and end colours
    # These are set within defs/linearGradient
    base_image[1][0][0].attrib["stop-color"] = f"#{start}"
    base_image[1][0][1].attrib["stop-color"] = f"#{end}"
    return base_image


def set_pineapple_colour(base_image, colour):
    # The pineapple is the first path element in the first g element
    # Set the fill colour of this element to the colour

    base_image[0][1].attrib["fill"] = f"#{colour}"
    return base_image


def correct_hex(code):
    code = str(code).strip("#")
    code = "".join([char for char in code.upper() if char in "0123456789ABCDEF"])
    if not code:
        return "000000"

    if len(code) > 6:
        code = code[:6]
    if len(code) == 6:
        return code

    if len(code) == 1:
        return code * 6
    if len(code) == 2:
        return code * 3

    # If 4 characters, assume the last character is the alpha channel, and strip it
    if len(code) == 4:
        code = code[:3]
    if len(code) == 3:
        return "".join([char * 2 for char in code])

    # For 5 characters, it is probable that a leading zero was omitted
    if len(code) == 5:
        code = "0" + code


def save_to_cache(image, name):
    # Save the image to the cache folder
    with open(f"cache/{name}", "wb") as f:
        f.write(image)


def main(
    output_format="svg",  # svg, 512 or 2048
    colour="purple",
    frame=None,
    shape="circle",
    gradient_start=None,
    gradient_end=None,
    pineapple_colour=None,
    **_
):
    allowed = all_list.main(output_format="dict")
    if colour not in allowed["colours"]:
        colour = "purple"
    if frame and frame not in allowed["frames"]:
        frame = None
    if frame and shape != "circle":
        frame = None
    if gradient_start and gradient_end:
        gradient_start, gradient_end = gradient_end, gradient_start
    else:
        gradient_start, gradient_end = colour_definitions[colour]
    gradient_start, gradient_end = correct_hex(gradient_start), correct_hex(gradient_end)

    full_name = f"{output_format}-{gradient_start}{gradient_end}-{frame}{shape}{pineapple_colour}.{'svg' if output_format == 'svg' else 'png'}"
    # Check if the image has already been generated. If it has been, it will be in the cache folder
    if os.path.exists(f"cache/{full_name}"):
        return open(f"cache/{full_name}", "rb").read()

    base_image = ET.parse(f"assets/base.svg").getroot()

    base_image = set_gradient(base_image, gradient_start, gradient_end)

    if pineapple_colour:
        base_image = set_pineapple_colour(base_image, pineapple_colour)

    if frame:
        base_image = add_frame(base_image, frame)

    if shape == "circle":
        base_image = make_circle(base_image)


    if output_format == "svg":
        generated = ET.tostring(base_image)
        save_to_cache(generated, full_name)
        return generated

    # Convert the SVG to a PNG using cairosvg
    image = cairosvg.svg2png(bytestring=ET.tostring(base_image))
    # Convert the PNG to a numpy array
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_UNCHANGED)
    # Resize the image to the correct size
    if output_format == "512":
        image = cv2.resize(image, (512, 512), interpolation=cv2.INTER_AREA)
    elif output_format == "2048":
        image = cv2.resize(image, (2048, 2048), interpolation=cv2.INTER_AREA)
    # Convert the image back to a PNG
    image = cv2.imencode(".png", image)[1].tostring()

    save_to_cache(image, full_name)

    # Return the PNG as a bytestring
    return image
