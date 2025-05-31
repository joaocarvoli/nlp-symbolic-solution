from huggingface_hub import hf_hub_download
import torch
from pytorch_lightning import LightningModule
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from torchmetrics.classification import BinaryPrecision

bert_model = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(bert_model, do_lower_case=False)

class SentimentLitModel(LightningModule):
    def __init__(self, model_name, lr=1e-5, total_steps=1000, weight_decay=0.01, dropout=0.3):
        super().__init__()
        self.save_hyperparameters()

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=1
        )
        
        self.model.config.hidden_dropout_prob = dropout
        
        self.val_precision = BinaryPrecision()
        self.loss_fn = torch.nn.BCEWithLogitsLoss()

    def forward(self, batch):
        # Only pass model inputs, not labels
        inputs = {k: v for k, v in batch.items() if k != "labels"}
        return self.model(**inputs)
    
    def training_step(self, batch, batch_idx):
        batch = {k: v.to(self.device) for k, v in batch.items()}
        outputs = self(batch)
        logits = outputs.logits.squeeze(-1)
        loss = self.loss_fn(logits, batch["labels"].float())
        self.log("train_loss", loss, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        batch = {k: v.to(self.device) for k, v in batch.items()}
        outputs = self(batch)
        logits = outputs.logits.squeeze(-1)
        preds = torch.sigmoid(logits) > 0.5
        self.val_precision(preds.int(), batch["labels"].int())
        self.log("val_precision", self.val_precision, prog_bar=True)
    
    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        batch = {k: v.to(self.device) for k, v in batch.items()}
        outputs = self(batch)
        logits = outputs.logits.squeeze(-1)
        probs = torch.sigmoid(logits)
        preds = (probs > 0.5).int()
        return {'probs': probs, 'preds': preds}

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(), 
            lr=self.hparams.lr, 
            weight_decay=self.hparams.weight_decay
        )
        scheduler = get_linear_schedule_with_warmup(
            optimizer, 
            num_warmup_steps=int(0.2 * self.hparams.total_steps),
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
    filename='version-27-epoch=2-step=11958.ckpt'
)

ckpt = torch.load(ckpt_path, map_location='cpu')
model = SentimentLitModel.load_from_checkpoint(
    ckpt_path,
    model_name=bert_model
)
