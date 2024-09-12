import torch
from sentence_transformers import SentenceTransformer
from transformers import BertModel, BertTokenizer


class Encoder:
    def __init__(self, encoder=None, tokenizer=None, device: str = "cpu") -> None:
        self.encoder = encoder
        self.tokenizer = tokenizer
        self.device = device
        if encoder:
            self.encoder = self.encoder.to(self.device)

    @classmethod
    def from_sentence_transformer(cls, model_name: str, device: str = "cpu"):
        encoder = SentenceTransformer(model_name)
        return cls(encoder, device=device)

    @classmethod
    def from_hugging_face(cls, model_name: str, device: str = "cpu"):
        tokenizer = BertTokenizer.from_pretrained(model_name)
        encoder = BertModel.from_pretrained(model_name)
        return cls(encoder, tokenizer, device)

    def encode(self, sentences, return_tensors="pt"):
        if self.tokenizer:  # use Hugging Face BERT
            tokens = self.tokenizer(
                sentences, padding=True, truncation=True, return_tensors=return_tensors
            )
            tokens = {key: value.to(self.device) for key, value in tokens.items()}

            with torch.no_grad():
                outputs = self.encoder(**tokens)
            embeddings = outputs.last_hidden_state[
                :, 0, :
            ]  # Use the [CLS] token embeddings
            return embeddings

        else:
            return self.encoder.encode(sentences, convert_to_tensor=True).to(
                self.device
            )
