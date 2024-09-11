import math
import torch
from torch import nn


class PositionalEncoding(nn.Module):
    """
    Learnable positional encoding
    """

    def __init__(self, d_model: int, dropout: float, maxlen: int = 1024):
        super().__init__()
        self.pos_embedding = nn.Embedding(maxlen, d_model)
        self.dropout = nn.Dropout(dropout)
        # Precompute position indices
        self.register_buffer('positions', torch.arange(maxlen).unsqueeze(1))

    def forward(self, embedding):
        """
        embedding: (seq_len, batch_size, d_model)
        """
        # Use precomputed positions and truncate to the current seq_len
        seq_len = embedding.size(0)
        pos = self.positions[:seq_len]
        return self.dropout(embedding + self.pos_embedding(pos))


class TokenEmbedding(nn.Module):
    """
    Embedding for the SMILES tokens
    """

    def __init__(self, vocab_size: int, d_model: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.emb_size = d_model

    def forward(self, tokens):
        return self.embedding(tokens) * math.sqrt(self.emb_size)


class FragmentEmbedding(nn.Module):
    """
    Embedding for the fragment peaks.

    peaks: (seq_len, batch_size, d_input)
    d_input: [feature0, feature1, ..., featureN, scale, ion_mode]
    - feature: count of the corresponding atom type
    - scale: intensity
    - ion_mode: ionization mode
    """

    def __init__(self, d_input: int, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.fc = nn.Linear(d_input - 2, d_model)
        self.ion_embedding = nn.Embedding(2, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, peaks):
        x = peaks[..., :-2] * torch.sqrt(peaks[..., -2, None])
        x = self.fc(x)
        x += self.ion_embedding(peaks[..., -1].long())
        return self.dropout(x)


class StructureHead(nn.Module):
    def __init__(self, d_model: int, vocab_size: int, n_head: int, n_encoder_layers: int, n_decoder_layers: int,
                 dropout: float = 0.1, activation: str = "gelu"):
        super().__init__()
        self.seq2seq = nn.Transformer(d_model=d_model, dim_feedforward=4 * d_model, nhead=n_head,
                                      num_encoder_layers=n_encoder_layers,
                                      num_decoder_layers=n_decoder_layers,
                                      dropout=dropout, activation=activation, norm_first=True)
        self.tokenEmbedding = TokenEmbedding(vocab_size, d_model)
        self.positionalEncoding = PositionalEncoding(d_model, dropout=dropout)
        self.generator = nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt, tgt_mask, src_key_padding_mask, tgt_key_padding_mask):
        tgt = self.positionalEncoding(self.tokenEmbedding(tgt))
        output = self.seq2seq(src, tgt, tgt_mask=tgt_mask,
                              src_key_padding_mask=src_key_padding_mask,
                              memory_key_padding_mask=src_key_padding_mask,
                              tgt_key_padding_mask=tgt_key_padding_mask)
        return self.generator(output)

    def encode(self, src, src_key_padding_mask):
        return self.seq2seq.encoder(src, src_key_padding_mask=src_key_padding_mask)

    def decode(self, tgt, memory, tgt_mask, memory_key_padding_mask, tgt_key_padding_mask):
        tgt = self.positionalEncoding(self.tokenEmbedding(tgt))
        output = self.seq2seq.decoder(tgt, memory, tgt_mask=tgt_mask,
                                      memory_key_padding_mask=memory_key_padding_mask,
                                      tgt_key_padding_mask=tgt_key_padding_mask)
        return self.generator(output)
