# modeldemo

Built with:

- uv for project management.
- PyTorch for model training.
- Modal for model infra.
- FastHTML for the frontend.
- Ruff for linting and formatting.

## Set Up

Set up the environment:

```bash
uv sync --all-extras --dev
uv run pre-commit install
```

Optionally, set up Modal:

```bash
modal setup
```

## Repository Structure

```bash
.
├── r&d               # config, frontend, model FT.
├── src
├──── modeldemo
├────── __init__.py # main code.
```

## Development

### CLI

```bash
uv run modeldemo
uvx --from build pyproject-build --installer uv
uvx twine upload dist/*
uv run --with modeldemo --no-project -- modeldemo -vv

manually sort data:
├── src
├──── modeldemo
├────── ft
├──────── data
->
├── src
├──── modeldemo
├────── ft
├──────── data
├────────── train
├──────────── focused
├──────────── distracted
├────────── val
├──────────── focused
├──────────── distracted

uv run main_finetune.py \
--model convnextv2_atto \
--batch_size 32 --update_freq 4 \
--blr 2e-4 \
--epochs 600 \
--warmup_epochs 0 \
--layer_decay_type 'single' \
--layer_decay 0.9 \
--weight_decay 0.3 \
--drop_path 0.1 \
--reprob 0.25 \
--mixup 0. \
--cutmix 0. \
--smoothing 0.2 \
--model_ema True --model_ema_eval True \
--use_amp True \
--data_path data/ \
--output_dir out/ \
--data_set focus
```

```bash
sudo apt install -y notification-daemon
sudo nano /usr/share/dbus-1/services/org.freedesktop.Notifications.service
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/lib/notification-daemon/notification-daemon
```


### Frontend

Run the app:

```bash
uv run src/modeldemo/frontend/main.py
```

### Training

Download the data and model:

```bash
uv run src/modeldemo/training/etl.py
```

or

```bash
modal run src/modeldemo/training/etl.py
```

Run a hyperparameter sweep:

```bash
uv run src/modeldemo/training/sweep.py
```

or

```bash
modal run src/modeldemo/training/sweep.py
```

Train the model:

```bash
torchrun --standalone --nproc_per_node=<n-gpus> src/modeldemo/training/train.py
```

or

```bash
modal run src/modeldemo/training/train_modal.py
```

Run the hellaswag eval on a model checkpoint:

```bash
uv run src/modeldemo/training/hellaswag.py
```

or

```bash
modal run src/modeldemo/training/hellaswag.py
```

Serve a model checkpoint with Modal:

```bash
modal serve src/modeldemo/training/serve_modal.py
```

Check out the following docs for more information:

- [uv](https://docs.astral.sh/uv/getting-started/features/#projects)
- [modal](https://modal.com/docs)
- [ruff](https://docs.astral.sh/ruff/tutorial/)
