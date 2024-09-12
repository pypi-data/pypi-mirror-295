import os
import mss
import time
from PIL import Image
from notifypy import Notify
import torch
import subprocess
from transformers import AutoTokenizer, AutoModel
from pathlib import Path
import math
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from typing_extensions import Annotated
import platform

app = typer.Typer(
    rich_markup_mode="rich",
)
state = {"verbose": False, "super_verbose": False}

MODEL_PATH = "OpenGVLab/InternVL2-2B"
TORCH_DTYPE = torch.bfloat16
INPUT_IMG_SIZE = 448
MAX_TILES = 12
MAX_NEW_TOKENS = 1
DO_SAMPLE = True
PROMPT = PROMPT = """
<image>

Task: Analyze the given computer screenshot and determine if it shows evidence of focused, productive activity or potentially distracting activity.

Instructions:
1. Examine the screenshot carefully.
2. Look for indicators of focused, productive activities such as:
   - Code editors or integrated development environments (IDEs) in use
   - Document editing software with substantial text visible
   - Spreadsheet applications with data or formulas
   - Research papers or educational materials being read
   - Professional design or modeling software in use
   - Terminal/command prompt windows with active commands

3. Identify potentially distracting activities, including:
   - Social media websites (e.g., Reddit, Twitter, Facebook, Instagram)
   - Video streaming platforms (e.g., YouTube, Twitch, Netflix)
   - News websites or apps not related to work/study
   - Online shopping sites
   - Games or gaming platforms

4. If multiple windows/tabs are visible, prioritize the active or most prominent one.

5. Consider the context: a coding-related YouTube video might be considered focused activity for a programmer.

Response Format:
- Return a single integer:
  - 0 if the screenshot primarily shows evidence of focused, productive activity
  - 1 if the screenshot primarily shows potentially distracting activity or if the nature of the activity cannot be clearly determined

Example responses:
0  (for a screenshot showing active coding in an IDE or focused reading of a research paper)
1  (for a screenshot displaying social media feeds or non-work-related video content)

Important: Provide only the integer response without any additional text or explanation.
"""
NOTIF_INT = 5  # seconds
NOTIF_LEN = 10  # seconds
NOTIF_TITLE = "You there..."
NOTIF_MSG = "Stay focused!"
NOTIF_ICON_PATH = str(Path(__file__).parent / "focus.png")
RETURN_MSG = "[bold green]Good![/bold green]"

NOTIF = Notify(
    default_notification_title=NOTIF_TITLE,
    default_application_name="Modeldemo",
    default_notification_message=NOTIF_MSG,
    default_notification_icon=NOTIF_ICON_PATH,
    enable_logging=state["super_verbose"],
)

DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda"
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    DEVICE = "mps"


# Helper fns
def send_notification():
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(
                ["osascript", "-e", f'display notification "{NOTIF_MSG}" with title "{NOTIF_TITLE}"'], check=True
            )
        elif system == "Linux":
            subprocess.run(["notify-send", NOTIF_TITLE, NOTIF_MSG], check=True)
        elif system == "Windows":
            # Using PowerShell to show a notification
            powershell_command = f"""
            [reflection.assembly]::loadwithpartialname("System.Windows.Forms")
            [reflection.assembly]::loadwithpartialname("System.Drawing")
            $notify = new-object system.windows.forms.notifyicon
            $notify.icon = [System.Drawing.SystemIcons]::Information
            $notify.visible = $true
            $notify.showballoontip({NOTIF_LEN * 1000},"{NOTIF_TITLE}","{NOTIF_MSG}",[system.windows.forms.tooltipicon]::None)
            """
            subprocess.run(["powershell", "-Command", powershell_command], check=True)
        else:
            print(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError:
        print(f"Failed to send notification on {system}")


def clear_terminal() -> None:
    if platform.system() == "Windows":
        _ = os.system("cls")
    else:  # For macOS and Linux
        _ = os.system("clear")


def capture_screenshot() -> Image:
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[0]
        sct_img = sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")


## Fns from: https://huggingface.co/OpenGVLab/InternVL2-1B
def download_model() -> tuple[AutoTokenizer, AutoModel]:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True, use_fast=False)

    torch.set_float32_matmul_precision("high")

    def split_model(model_name):
        device_map = {}
        world_size = torch.cuda.device_count()
        num_layers = {
            "InternVL2-1B": 24,
            "InternVL2-2B": 24,
            "InternVL2-4B": 32,
            "InternVL2-8B": 32,
            "InternVL2-26B": 48,
            "InternVL2-40B": 60,
            "InternVL2-Llama3-76B": 80,
        }[model_name]
        # Since the first GPU will be used for ViT, treat it as half a GPU.
        num_layers_per_gpu = math.ceil(num_layers / (world_size - 0.5))
        num_layers_per_gpu = [num_layers_per_gpu] * world_size
        num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0.5)
        layer_cnt = 0
        for i, num_layer in enumerate(num_layers_per_gpu):
            for _ in range(num_layer):
                device_map[f"language_model.model.layers.{layer_cnt}"] = i
                layer_cnt += 1
        device_map["vision_model"] = 0
        device_map["mlp1"] = 0
        device_map["language_model.model.tok_embeddings"] = 0
        device_map["language_model.model.embed_tokens"] = 0
        device_map["language_model.output"] = 0
        device_map["language_model.model.norm"] = 0
        device_map["language_model.lm_head"] = 0
        device_map[f"language_model.model.layers.{num_layers - 1}"] = 0

        return device_map

    device_map = split_model(MODEL_PATH.split("/")[-1])
    model = AutoModel.from_pretrained(
        MODEL_PATH,
        torch_dtype=TORCH_DTYPE,
        low_cpu_mem_usage=True,
        use_flash_attn=True,
        trust_remote_code=True,
        device_map=device_map,
    ).eval()

    return tokenizer, model


def transform_img(image: Image) -> torch.Tensor:
    IMAGENET_MEAN = (0.485, 0.456, 0.406)
    IMAGENET_STD = (0.229, 0.224, 0.225)

    def build_transform() -> T.Compose:
        MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
        transform = T.Compose(
            [
                T.Lambda(lambda img: img.convert("RGB") if img.mode != "RGB" else img),
                T.Resize((INPUT_IMG_SIZE, INPUT_IMG_SIZE), interpolation=InterpolationMode.BICUBIC),
                T.ToTensor(),
                T.Normalize(mean=MEAN, std=STD),
            ]
        )
        return transform

    def find_closest_aspect_ratio(
        aspect_ratio: float, target_ratios: set[tuple[int, int]], width: int, height: int
    ) -> tuple[int, int]:
        best_ratio_diff = float("inf")
        best_ratio = (1, 1)
        area = width * height
        for ratio in target_ratios:
            target_aspect_ratio = ratio[0] / ratio[1]
            ratio_diff = abs(aspect_ratio - target_aspect_ratio)
            if ratio_diff < best_ratio_diff:
                best_ratio_diff = ratio_diff
                best_ratio = ratio
            elif ratio_diff == best_ratio_diff:
                if area > 0.5 * INPUT_IMG_SIZE * INPUT_IMG_SIZE * ratio[0] * ratio[1]:
                    best_ratio = ratio
        return best_ratio

    def dynamic_preprocess(image: Image, min_num: int = 1, use_thumbnail: bool = False):
        orig_width, orig_height = image.size
        aspect_ratio = orig_width / orig_height

        # calculate the existing image aspect ratio
        target_ratios = {
            (i, j)
            for n in range(min_num, MAX_TILES + 1)
            for i in range(1, n + 1)
            for j in range(1, n + 1)
            if i * j <= MAX_TILES and i * j >= min_num
        }
        target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

        # find the closest aspect ratio to the target
        target_aspect_ratio = find_closest_aspect_ratio(aspect_ratio, target_ratios, orig_width, orig_height)

        # calculate the target width and height
        target_width = INPUT_IMG_SIZE * target_aspect_ratio[0]
        target_height = INPUT_IMG_SIZE * target_aspect_ratio[1]
        blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

        # resize the image
        resized_img = image.resize((target_width, target_height))
        processed_images = []
        for i in range(blocks):
            box = (
                (i % (target_width // INPUT_IMG_SIZE)) * INPUT_IMG_SIZE,
                (i // (target_width // INPUT_IMG_SIZE)) * INPUT_IMG_SIZE,
                ((i % (target_width // INPUT_IMG_SIZE)) + 1) * INPUT_IMG_SIZE,
                ((i // (target_width // INPUT_IMG_SIZE)) + 1) * INPUT_IMG_SIZE,
            )
            # split the image
            split_img = resized_img.crop(box)
            processed_images.append(split_img)
        assert len(processed_images) == blocks
        if use_thumbnail and len(processed_images) != 1:
            thumbnail_img = image.resize((INPUT_IMG_SIZE, INPUT_IMG_SIZE))
            processed_images.append(thumbnail_img)
        return processed_images

    transform = build_transform()
    images = dynamic_preprocess(image, use_thumbnail=True)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values


def predict(img: Image, tokenizer: AutoTokenizer, model: AutoModel) -> str:
    pixel_values = transform_img(img).to(TORCH_DTYPE).cuda()
    generation_config = {"max_new_tokens": MAX_NEW_TOKENS, "do_sample": DO_SAMPLE}
    response = model.chat(tokenizer, pixel_values, PROMPT, generation_config)
    try:
        response = int(response.strip())
    except ValueError:
        response = 1
    return response


# Typer CLI
def run() -> None:
    if state["verbose"]:
        print("Press Ctrl+C to stop at any time.")
        print(f"Using device: {DEVICE}")
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
        ) as progress:
            progress.add_task("Downloading model...", total=None)
            tokenizer, model = download_model()
        print("Model downloaded!")
    else:
        tokenizer, model = download_model()

    notif_active = False
    last_check_time = 0
    while True:
        current_time = time.time()
        if current_time - last_check_time >= NOTIF_INT:  # Check every NOTIF_INT seconds
            img = capture_screenshot()
            pred = predict(img, tokenizer, model)

            if state["super_verbose"]:
                print(f"Prediction: {pred}")

            if pred != 0:
                if not notif_active:
                    if state["verbose"]:
                        print(f"[bold red]{NOTIF_MSG}[/bold red]")
                    send_notification()
                    notif_active = True
                    notif_start_time = current_time
            elif notif_active:
                if state["verbose"]:
                    print(RETURN_MSG)
                notif_active = False

            last_check_time = current_time

        if notif_active and (current_time - notif_start_time >= NOTIF_LEN):  # Deactivate after NOTIF_LEN seconds
            notif_active = False


@app.command(
    help="Stay [bold red]focused.[/bold red]",
    epilog="Made by [bold blue]Andrew Hinh.[/bold blue] :mechanical_arm::person_climbing:",
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
)
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0) -> None:
    try:
        state["verbose"] = verbose > 0
        state["super_verbose"] = verbose > 1
        run()
    except KeyboardInterrupt:
        if state["verbose"]:
            print("\n\nExiting...")
        else:
            clear_terminal()
    except Exception as e:
        if state["verbose"]:
            print(f"Failed with error: {e}")
            print("\n\nExiting...")
        else:
            clear_terminal()
