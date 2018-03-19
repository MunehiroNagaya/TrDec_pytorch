import torch
import torch.nn.init as init
from torch.autograd import Variable
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.nn.functional as F

import numpy as np
from utils import *

class MlpAttn(nn.Module):
  def __init__(self, hparams):
    super(MlpAttn, self).__init__()
    self.hparams = hparams
    self.w_trg = nn.Linear(self.hparams.d_model, self.hparams.d_model)
    self.w_att = nn.Linear(self.hparams.d_model, 1)
    if self.hparams.cuda:
      self.w_trg = self.w_trg.cuda()
      self.w_att = self.w_att.cuda()
  
  def forward(self, q, k, v, attn_mask=None):
    batch_size, d_q = q.size()
    batch_size, len_k, d_k = k.size()
    batch_size, len_v, d_v = v.size()
    # v is bi-directional encoding of source
    assert d_k == d_q 
    assert 2*d_k == d_v
    assert len_k == len_v
    # (batch_size, len_k, d_k)
    att_src_hidden = k + self.w_trg(q).unsqueeze(1)
    att_src_weights = self.w_att(att_src_hidden).squeeze(2)
    if not attn_mask is None:
      att_src_weights.data.masked_fill_(attn_mask, -self.hparams.inf)
    att_src_weights = F.softmax(att_src_weights)
    ctx = torch.bmm(att_src_weights.unsqueeze(1), v).squeeze(1)
    return ctx

class DotProdAttn(nn.Module):
  def __init__(self, hparams):
    super(DotProdAttn, self).__init__()
    self.dropout = nn.Dropout(hparams.dropout)
    #self.src_enc_linear = nn.Linear(hparams.d_model * 2, hparams.d_model)
    self.softmax = nn.Softmax(dim=-1)
    self.hparams = hparams

  def forward(self, q, k, v, attn_mask = None):
    """ 
    dot prodct attention: (q * k.T) * v
    Args:
      q: [batch_size, d_q] (target state)
      k: [batch_size, len_k, d_k] (source enc key vectors)
      v: [batch_size, len_v, d_v] (source encoding vectors)
      attn_mask: [batch_size, len_k] (source mask)
    Return:
      attn: [batch_size, d_v]
    """
    batch_size, d_q = q.size()
    batch_size, len_k, d_k = k.size()
    batch_size, len_v, d_v = v.size()
    # v is bi-directional encoding of source
    assert d_k == d_q 
    assert 2*d_k == d_v
    assert len_k == len_v
    # [batch_size, len_k, d_model]
    #k_vec = self.src_enc_linear(k)
    # [batch_size, len_k]
    attn_weight = torch.bmm(k, q.unsqueeze(2)).squeeze(2)
    if not attn_mask is None:
      attn_weight.data.masked_fill_(attn_mask, -self.hparams.inf)
    attn_weight = self.softmax(attn_weight)
    # [batch_size, d_v]
    ctx = torch.bmm(attn_weight.unsqueeze(1), v).squeeze(1)
    return ctx

class Encoder(nn.Module):
  def __init__(self, hparams, *args, **kwargs):
    super(Encoder, self).__init__()

    self.hparams = hparams
    #print("d_word_vec", self.hparams.d_word_vec)
    self.word_emb = nn.Embedding(self.hparams.source_vocab_size,
                                 self.hparams.d_word_vec,
                                 padding_idx=hparams.pad_id)

    self.layer = nn.LSTM(self.hparams.d_word_vec, 
                         self.hparams.d_model, 
                         bidirectional=True, 
                         dropout=hparams.dropout)

    # bridge from encoder state to decoder init state
    self.bridge = nn.Linear(hparams.d_model * 2, hparams.d_model, bias=False)
    
    self.dropout = nn.Dropout(self.hparams.dropout)
    if self.hparams.cuda:
      self.word_emb = self.word_emb.cuda()
      self.layer = self.layer.cuda()
      self.dropout = self.dropout.cuda()
      self.bridge = self.bridge.cuda()

  def forward(self, x_train, x_len):
    """Performs a forward pass.

    Args:
      x_train: Torch Tensor of size [batch_size, max_len]
      x_mask: Torch Tensor of size [batch_size, max_len]. 1 means to ignore a
        position.
      x_len: [batch_size,]

    Returns:
      enc_output: Tensor of size [batch_size, max_len, d_model].
    """
    batch_size, max_len = x_train.size()
    #print("x_train", x_train)
    #print("x_len", x_len)
    x_train = x_train.transpose(0, 1)
    # [batch_size, max_len, d_word_vec]
    word_emb = self.word_emb(x_train)
    #word_emb = self.dropout(word_emb)
    packed_word_emb = pack_padded_sequence(word_emb, x_len)
    enc_output, (ht, ct) = self.layer(packed_word_emb)
    #enc_output, (ht, ct) = self.layer(word_emb)
    enc_output, _ = pad_packed_sequence(enc_output,  padding_value=self.hparams.pad_id)
    enc_output = enc_output.permute(1, 0, 2)
    #print(enc_output)
    #print(ht.size())

    dec_init_cell = self.bridge(torch.cat([ct[0], ct[1]], 1))
    dec_init_state = F.tanh(dec_init_cell)
    #dec_init_state = self.bridge(torch.cat([ht[0], ht[1]], 1))
    dec_init = (dec_init_state, dec_init_cell)
    #print(dec_init_state)
    #print(dec_init_cell)
    #exit(0)
    return enc_output, dec_init

class Decoder(nn.Module):
  def __init__(self, hparams):
    super(Decoder, self).__init__()
    self.hparams = hparams
    
    # transform encoder state vectors into attention key vector
    self.enc_to_k = nn.Linear(hparams.d_model * 2, hparams.d_model, bias=False)
    #self.attention = DotProdAttn(hparams)
    self.attention = MlpAttn(hparams)
    # transform [ctx, h_t] to readout state vectors before softmax
    self.ctx_to_readout = nn.Linear(hparams.d_model * 2 + hparams.d_model, hparams.d_model, bias=False)
    self.readout = nn.Linear(hparams.d_model, hparams.target_vocab_size, bias=False)
    self.word_emb = nn.Embedding(self.hparams.target_vocab_size,
                                 self.hparams.d_word_vec,
                                 padding_idx=hparams.pad_id)
    # input: [y_t-1, input_feed]
    self.layer = nn.LSTMCell(hparams.d_word_vec + hparams.d_model, 
                             hparams.d_model)
    self.dropout = nn.Dropout(hparams.dropout)
    if self.hparams.cuda:
      self.enc_to_k = self.enc_to_k.cuda()
      self.ctx_to_readout = self.ctx_to_readout.cuda()
      self.readout = self.readout.cuda()
      self.word_emb = self.word_emb.cuda()
      self.layer = self.layer.cuda()
      self.dropout = self.dropout.cuda()

  def forward(self, x_enc, dec_init, x_mask, y_train, y_mask):
    # get decoder init state and cell, use x_ct
    """
    x_enc: [batch_size, max_x_len, d_model * 2]

    """
    batch_size_x = x_enc.size()[0]
    batch_size, y_max_len = y_train.size()
    assert batch_size_x == batch_size

    hidden = dec_init 
    #x_enc_k = self.enc_to_k(x_enc.contiguous().view(-1, self.hparams.d_model * 2)).contiguous().view(batch_size, -1, self.hparams.d_model)
    x_enc_k = self.enc_to_k(x_enc)
    #input_feed = Variable(torch.zeros(batch_size, self.hparams.d_model), requires_grad=False)
    input_feed = Variable(dec_init[1][1].data.new(batch_size, self.hparams.d_model).zero_(), requires_grad=False)
    if self.hparams.cuda:
      input_feed = input_feed.cuda()
    # [batch_size, y_len, d_word_vec]
    trg_emb = self.word_emb(y_train)
    logits = []
    for t in range(y_max_len):
      y_emb_tm1 = trg_emb[:, t, :]
      y_input = torch.cat([y_emb_tm1, input_feed], dim=1)
      
      h_t, c_t = self.layer(y_input, hidden)
      ctx = self.attention(h_t, x_enc_k, x_enc, attn_mask=x_mask)
      pre_readout = F.tanh(self.ctx_to_readout(torch.cat([h_t, ctx], dim=1)))
      pre_readout = self.dropout(pre_readout)

      score_t = self.readout(pre_readout)
      logits.append(score_t)

      input_feed = pre_readout
      hidden = (h_t, c_t)
    # [len_y, batch_size, trg_vocab_size]
    logits = torch.stack(logits).transpose(0, 1).contiguous()
    return logits

class Seq2Seq(nn.Module):
  
  def __init__(self, hparams):
    super(Seq2Seq, self).__init__()
    self.encoder = Encoder(hparams)
    self.decoder = Decoder(hparams)

  def forward(self, x_train, x_mask, x_len, y_train, y_mask, y_len):
    # [batch_size, x_len, d_model * 2]
    #print("x_train", x_train)
    #print("x_mask", x_mask)
    #print("x_len", x_len)
    x_enc, dec_init = self.encoder(x_train, x_len)
    # [batch_size, y_len-1, trg_vocab_size]
    logits = self.decoder(x_enc, dec_init, x_mask, y_train, y_mask)
    return logits

  #def translate(self, x_train, x_mask, x_len):
  #  x_enc, x_ht, x_ct = self.encoder(x_train, x_len)

