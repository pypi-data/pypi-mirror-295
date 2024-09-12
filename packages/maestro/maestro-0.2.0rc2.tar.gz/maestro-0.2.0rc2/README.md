<div align="center">

  <h1>maestro</h1>

  <p>coming: when it's ready...</p>

</div>

## 👋 hello

**maestro** is a tool designed to streamline and accelerate the fine-tuning process for 
multimodal models. It provides ready-to-use recipes for fine-tuning popular 
vision-language models (VLMs) such as **Florence-2**, **PaliGemma**, and 
**Phi-3.5 Vision** on downstream vision-language tasks.

## 💻 install

Pip install the supervision package in a
[**Python>=3.8**](https://www.python.org/) environment.

```bash
pip install maestro
```

## 🔥 quickstart

### CLI

VLMs can be fine-tuned on downstream tasks directly from the command line with 
`maestro` command:

```bash
maestro florence2 train --dataset='<DATASET_PATH>' --epochs=10 --batch-size=8
```

### SDK

Alternatively, you can fine-tune VLMs using the Python SDK, which accepts the same 
arguments as the CLI example above:

```python
from maestro.trainer.common import MeanAveragePrecisionMetric
from maestro.trainer.models.florence_2 import train, TrainingConfiguration

config = TrainingConfiguration(
    dataset='<DATASET_PATH>',
    epochs=10,
    batch_size=8,
    metrics=[MeanAveragePrecisionMetric()]
)

train(config)
```

## 🦸 contribution

We would love your help in making this repository even better! We are especially 
looking for contributors with experience in fine-tuning vision-language models (VLMs). 
If you notice any bugs or have suggestions for improvement, feel free to open an 
[issue](https://github.com/roboflow/multimodal-maestro/issues) or submit a 
[pull request](https://github.com/roboflow/multimodal-maestro/pulls).
