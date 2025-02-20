from transformers import AutoModelForCausalLM, AutoTokenizer


class QWEN:

    def __init__(self, debug=False):
        # for debug
        self.debug = debug

        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, torch_dtype="auto", device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def __call__(self, input):
        # create the prompts with the text
        prompts = [
            f"show me short english prompts that describe the objects, the people and the place in this text: \"{input}\", no formatting, no symbols, no conversation, no numbers",
            f"answer in original language prompt, summary the following text in a short way: {input}",
        ]
        responses = []
        for prompt in prompts:
            messages = [
                {
                    "role": "system",
                    "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
                },
                {"role": "user", "content": prompt},
            ]
            # make the prompt in a way to the model understand
            text = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(
                self.model.device
            )

            # generate the qwen text
            generated_ids = self.model.generate(**model_inputs, max_new_tokens=512)
            generated_ids = [
                output_ids[len(input_ids) :]
                for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            # get the response of the LLM
            response = self.tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0]

            if self.debug:
                print(response)

            # add the answer
            responses.append(response)

        # process answer
        responses[0] = responses[0].replace("\n", "")
        responses[0] = responses[0].replace("-", "")

        return {"image_description": responses[0], "summary": responses[1]}
