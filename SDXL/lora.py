from gradio_client import Client

client = Client("jasperai/flash-lora")
result = client.predict(
		pre_prompt="storyboard sketch of",
		prompt="realistic scene, detailed, A quiet room with an empty chair, The speaker alone at their table, A phonograph on the table, The narrator (speaking), The person they're talking to (the subject of the diary), A study or office-like space where someone is working quietly.",
		seed=0,
		randomize_seed=True,
		num_inference_steps=15,
		negative_prompt="nsfw, no detail, not realistic",
		guidance_scale=1,
		user_lora_selector="nerijs/pixel-art-xl",
		user_lora_weight=1,
		api_name="/infer"
)
print(result)

# result = client.predict(
# 		prompt="realistic scene, detailed, A quiet room with an empty chair, The speaker alone at their table, A phonograph on the table, The narrator (speaking), The person they're talking to (the subject of the diary), A study or office-like space where someone is working quietly.",
# 		image_input=None,
# 		image_strength=0.0,
# 		cfg_scale=3.5,
# 		steps=28,
# 		lora_scale_1=1.15,
# 		lora_scale_2=1.15,
# 		lora_scale_3=1.15,
# 		randomize_seed=True,
# 		seed=4227398039,
# 		width=512,
# 		height=512,
# 		api_name="/run_lora"
# )
# print(result)