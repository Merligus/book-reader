from gradio_client import Client
import shutil


class SDXL:
    def __init__(self, debug=False):
        self.debug = debug
        self.client = Client("diffusers/unofficial-SDXL-Turbo-i2i-t2i")

    def __call__(self, input):
        result = self.client.predict(
            init_image=None,
            prompt=f"realistic scene, detailed faces, detailed, no words, no watermark, {input}",  # A quiet room with an empty chair, The speaker alone at their table, A phonograph on the table, The narrator (speaking), The person they're talking to (the subject of the diary), A study or office-like space where someone is working quietly.",
            strength=0.7,
            steps=5,
            seed=7,
            api_name="/predict",
        )

        if self.debug:
            print(result)

        shutil.move(result, "./result.png")

        return "result.png"
