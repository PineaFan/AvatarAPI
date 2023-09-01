import json
import os

path = "list"

def main(*args, **kwargs):
    # Return a JSON object with the list of filenames

    frames = [x.split(".")[0].lower() for x in os.listdir('assets/frames')]
    sizes = ["512", "2048", "svg"]

    out = {
        "colours": ["blue", "green", "black", "purple", "red", "yellow"],
        "frames": frames,
        "sizes": sizes
    }

    if kwargs.get("output_format", None) == "dict":
        return out
    return json.dumps(out)
