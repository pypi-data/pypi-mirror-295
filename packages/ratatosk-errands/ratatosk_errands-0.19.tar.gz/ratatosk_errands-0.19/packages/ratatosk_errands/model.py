from pydantic import BaseModel


class DiffusionInstructions(BaseModel):
    prompt: str
    image_identifier: str
    negative_prompt: str | None = None
    num_inference_steps: int | None = None
    guidance_scale: float | None = None


class ImageToImageInstructions(DiffusionInstructions):
    base_image_identifier: str
    strength: float | None = None


class TextToImageInstructions(DiffusionInstructions):
    width: int | None = None
    height: int | None = None


class ChatInstructions(BaseModel):
    prompt: str
    max_new_tokens: int | None = None
    temperature: float | None = None
    repetition_penalty: float | None = None


class Errand(BaseModel):
    instructions: TextToImageInstructions | ImageToImageInstructions | ChatInstructions
    origin: str
    destination: str
    errand_identifier: str
    timestamp: float


class DiffusionReply(BaseModel):
    image_identifier: str


class ChatReply(BaseModel):
    message: str


class Echo(BaseModel):
    errand: Errand
    reply: DiffusionReply | ChatReply
