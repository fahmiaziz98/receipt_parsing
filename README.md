# Receipt Parsing

This project demonstrates how to use the Donut model with CORD dataset to perform receipt parsing. Receipt parsing involves extracting structured information from photographed receipts, such as itemized lists and totals.

## Overview

- The [CORD](https://huggingface.co/datasets/naver-clova-ix/cord-v2) dataset is a collection of receipts and invoices with ground truth annotations.
- We leverage the power of [Hugging Face Transformers](https://huggingface.co/transformers/) to fine-tune a pre-trained [Donut](https://huggingface.co/naver-clova-ix/donut-base) model for receipt parsing.
- The model used in this project is `fahmiaziz/finetune-donut-cord-v2.5`, which is adapted to the CORD-V2 dataset you can see it [here](https://huggingface.co/fahmiaziz/finetune-donut-cord-v2.5).
## Requirements

To run this project, you need:

- Python 3.7+
- PyTorch
- PyTorch-Lightning
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [flask](https://flask.palletsprojects.com/en/2.3.x/installation/#install-flask)

## Model Training and Evaluation

We trained and evaluated our receipt parsing model using the Donut model with CORD-V2 dataset. The goal was to achieve a high accuracy of 90% or above. You can access the detailed training and evaluation results on Weights & Biases (WandB):

- [Model Training and Evaluation Dashboard](https://wandb.ai/fahmiazizfadhil09/Donut-hpo)

![Model Training](evaluation.png)

Here are some highlights of the training and evaluation process:

- **Dataset**: We used the CORD dataset, which includes a diverse collection of receipts and invoices.

- **Model**: Our model is based on the [fahmiaziz/finetune-donut-cord-v2.5](https://huggingface.co/fahmiaziz/finetune-donut-cord-v2.5) architecture that has been fine-tuned from [donut-base](https://huggingface.co/naver-clova-ix/donut-base) and customized specifically for receipt parsing.

- **Training Metrics**: During training, we monitor various metrics, including accuracy, Tree Edit Distance (Tree ED) to ensure model performance.

- **Evaluation**: Our model achieved over 90% accuracy on the test dataset, demonstrating its effectiveness in parsing receipts.

- **Visualization**: The training and evaluation process can be visualized through the WandB dashboard linked above.

Feel free to explore the details of the training and evaluation results in WandB to gain more insight into our model's performance.

## Demonstration
[<img src="https://www.philschmid.de/static/blog/fine-tuning-donut/logo.png">](https://youtu.be/4dclAXt4EQw "Receipt Parsing")

