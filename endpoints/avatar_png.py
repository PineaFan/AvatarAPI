from src import generate

path = "avatar.png"

def main(*args, **kwargs):
    output_format = kwargs.get("output_format", "2048")
    if "output_format" in kwargs:
        del kwargs["output_format"]
    return generate.main(output_format, **kwargs)
