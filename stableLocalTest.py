from diffusers import StableDiffusionPipeline
import torch
from tkinter import *
from PIL import ImageTk, Image


prompt = input("Enter a description of terrain from an aerial view: ")
print("Entered prompt: ", prompt)


#recommended setup for GPUs with low memory (such as myself)
model_id = "runwayml/stable-diffusion-v1-5"
pipe = pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    revision="fp16", 
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

image = pipe(prompt).images[0]  
image.save("StableDiffusionOutput.png")


win = Tk()
win.title("Stable Diffusion Picture Output")

win.geometry("600x600")

frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open("StableDiffusionOutput.png"))

label = Label(frame, image = img)
label.pack()

win.mainloop()

