# Testing with Salesforce's Blip2 model

from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from io import BytesIO
import base64
import torch

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)

processor.patch_size = 10
processor.vision_feature_select_strategy = "full"

with open("binary-chart.svg.txt", "r") as f:
    base64bin = f.read()

im = Image.open(BytesIO(base64.b64decode(base64bin)))

# conversation = [
#     {
#         "role": "user",
#         "content": [
#             { "type": "text", "text": 
#                 """Find the bounding box of the elements and output the coordinates of xmin, xmax, ymin, ymax in this schema:
#                     Element = {{
#                         type: str (type of the element text, image, etc)
#                         content: str (content of the element if the element is text)
#                         bounds: list[float] (match with the exact bounding box's edges of the element provided scaled 0-1, keep precision to 5 decimal places)
#                     }}
#                 """
#             },
#             { "type": "image"}
#         ]
#     }
# ]

# prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

inputs = processor(images=im, text="Find the bounding boxes of texts in the image", return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=50)

print(processor.batch_decode(outputs, skip_special_tokens=True)[0])