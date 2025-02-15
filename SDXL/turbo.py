from gradio_client import Client
import shutil

client = Client("diffusers/unofficial-SDXL-Turbo-i2i-t2i", verbose=True)
result = client.predict(
		init_image=None,
		prompt="realistic scene, detailed, A quiet room with an empty chair, The speaker alone at their table, A phonograph on the table, The narrator (speaking), The person they're talking to (the subject of the diary), A study or office-like space where someone is working quietly.",
		strength=0.7,
		steps=2,
		seed=7,
		api_name="/predict"
)
shutil.move(result, "./image.png")
print(result)