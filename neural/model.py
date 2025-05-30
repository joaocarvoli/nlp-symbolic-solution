from huggingface_hub import hf_hub_download
import torch
from pytorch_lightning import LightningModule
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from torchmetrics.classification import Precision

bert_model = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(bert_model, do_lower_case=False)

class SentimentLitModel(LightningModule):
    def __init__(self, model_name, lr=2e-5, num_labels=2, total_steps=1000):
        super().__init__()
        self.save_hyperparameters()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )
        self.val_precision = Precision(task='binary')
        self.loss_fn = torch.nn.CrossEntropyLoss()
    
    def forward(self, **batch):
        return self.model(**batch)
    
    def training_step(self, batch, batch_idx):
        outputs = self.model(**batch)
        loss = outputs.loss
        self.log("train_loss", loss)
        return loss
    
    def validation_step(self, batch, batch_idx):
        outputs = self.model(**batch)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=-1)
        self.val_precision(preds, batch["labels"])
        self.log("val_precision", self.val_precision, prog_bar=True)
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.hparams.lr)
        scheduler = get_linear_schedule_with_warmup(
            optimizer, 
            num_warmup_steps=int(0.1 * self.hparams.total_steps),
            num_training_steps=self.hparams.total_steps
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'interval': 'step',
                'frequency': 1
            }
        }

ckpt_path = hf_hub_download(
    repo_id='jvcarvoli/bertimbau-for-sentiment',
    filename='epoch=4-step=19930.ckpt'
)

ckpt = torch.load(ckpt_path, map_location='cpu')
model = SentimentLitModel.load_from_checkpoint(
    ckpt_path,
    model_name=bert_model,
)
