from src import generate

path = "avatar.png"

def main(*args, **kwargs):
    output_format = kwargs.get("output_format", "2048")
    return generate.main(output_format, **kwargs)
