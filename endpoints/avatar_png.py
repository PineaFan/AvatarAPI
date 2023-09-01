from src import generate

path = "avatar.png"

def main(*args, **kwargs):
    if "output_format" in kwargs:
        del kwargs["output_format"]
    return generate.main(output_format="png", **kwargs)
