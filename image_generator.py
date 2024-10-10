import torch
from diffusers import FluxPipeline

def generate_image(prompt, number_of_images):
    pipe = FluxPipeline.from_pretrained("./flux1schnell", torch_dtype=torch.bfloat16)
    pipe.enable_sequential_cpu_offload()

    output = pipe(
        prompt,
        guidance_scale=0.0,
        num_images_per_prompt=number_of_images,
        output_type="pil",
        num_inference_steps=4,
        max_sequence_length=256,
        generator=torch.Generator("cpu").manual_seed(0),
    ).images

    return output
    


