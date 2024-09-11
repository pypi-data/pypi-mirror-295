from pathlib import Path

import lightning as L
from tokenizers import Tokenizer

from .blocks import FragmentEmbedding, StructureHead

tkn = Tokenizer.from_file(str(Path(__file__).parent.parent / "ckpt" / "tokenizer.json"))


class CSTseq(L.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.ms2_encoder = FragmentEmbedding(
            config.get("d_input", 38), config.get(
                "d_model"), config.get("dropout", 0.1)
        )
        self.struct_decoder = StructureHead(
            config.get("d_model"),
            tkn.get_vocab_size(),
            config.get("n_heads"),
            config.get("encoder_layers"),
            config.get("decoder_layers"),
            dropout=config.get("dropout", 0.1),
        )
        self.lr = config.get("lr")
        self.warmup_steps = config.get("warmup_steps")
        self.weight_decay = config.get("weight_decay")
        self.save_hyperparameters()

    def forward(self, src, tgt, src_padding_mask=None, tgt_padding_mask=None, tgt_mask=None):
        src = self.ms2_encoder(src)
        struct = self.struct_decoder(
            src, tgt, tgt_mask, src_padding_mask, tgt_padding_mask)
        return struct

    def encode(self, src, src_padding_mask=None):
        src = self.ms2_encoder(src)
        return self.struct_decoder.encode(src, src_padding_mask)

    def decode(self, tgt, mem, tgt_mask, mem_padding_mask=None, tgt_padding_mask=None):
        return self.struct_decoder.decode(tgt, mem, tgt_mask, mem_padding_mask, tgt_padding_mask)
