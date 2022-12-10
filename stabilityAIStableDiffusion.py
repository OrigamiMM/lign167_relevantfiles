import numpy as np
from PIL import Image
import PIL.ImageOps
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import imgToOBJ as ito

MAP_SIZE = (256,256)  # Should be same as image size: 256 x 256
MAP = np.zeros(MAP_SIZE)

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
AIKEY = 'INSERTYOURKEYHERE'
os.environ['STABILITY_KEY'] = AIKEY

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
    engine="stable-diffusion-768-v2-0", # Set the engine to use for generation.
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)

promptString = input("Enter terrain specific prompt here: ")
answers = stability_api.generate(prompt=promptString,
                                 seed=992446758, steps=30,cfg_scale=8.0,width=256, height=256, samples=1, sampler=generation.SAMPLER_K_DPMPP_2M )
filename = ""
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            filename = str(artifact.seed)+ ".png"
            img.save(filename)

filename_root = filename[: len(filename) -4]

#image processing
im = Image.open(filename)
im = im.convert('L')
im.save(filename_root + '_bnw.png')

im = Image.open(filename_root + '_bnw.png')
jpg_im = im.convert('RGB')
pix = jpg_im.load()

for y in range(256):
  for x in range(256):
    MAP[y,x] = pix[x,y][0]

MAP_norm = (MAP-np.min(MAP))/(np.max(MAP)-np.min(MAP))

ito.generateOBJ(MAP_SIZE, MAP_norm, filename_root + ".obj")
