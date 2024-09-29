import google.generativeai as genai
import os
import dotenv
import typing_extensions as typing
import json
import enum

dotenv.load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI"))

# Experimenting with prompting 

# class ElementType(enum.Enum):
#     TEXT = "text"
#     IMAGE = "image"

# class Element(typing.TypedDict):
#     type: ElementType
#     content: str
#     description: str
#     bounds: list[float]

# Return an array of elements given the base64 image and the bounding boxes
def detect_object(base64, bounds):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
    prompt = f"""
        Detect the object in the area bounded by these bouding boxes:
        {bounds}
        with each elements of the bounding box in the format of [xmin, xmax, ymin, ymax]
        
        Element = {{
            type: str (type of the element text, image, etc)
            content: str (content of the element if the element is text)
        }}

        Return: list[Element]
    """

    # bounds: list[float] (match with the exact bounding box's edges of the element provided scaled 0-1, keep precision to 5 decimal places)

    image = {
        "inline_data": {
            "data": base64,
            "mime_type": "image/png"
        }
    }

    response = model.generate_content(
        [prompt, image]
    )

    print(response.text)
    return json.loads(response.text)