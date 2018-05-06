#!/bin/bash
export PYTHONPATH="$(pwd)"                                                       
export CUDA_VISIBLE_DEVICES="1"   

python3.6 src/translate.py \
  --trdec \
  --model_dir="outputs_orm_trdec_exp5_v16_s1" \
  --data_path="data/orm_data/" \
  --source_vocab="vocab.orm" \
  --target_word_vocab="vocab.random_bina_word.eng" \
  --target_tree_vocab="vocab.random_bina_rule.eng" \
  --source_test="set0-test.tok.piece.orm" \
  --target_test="set0-test.tok.piece.eng" \
  --target_tree_test="set0-test.tok.eng.random_bina" \
  --beam_size=15 \
  --max_len=500 \
  --n_train_sents=10000 \
  --merge_bpe \
  --poly_norm_m=0.5 \
  --out_file="beam15_m0.5" \
  --max_tree_len=3000 \
  --no_lhs \
  --pos=1 \
  --cuda \
  "$@"

python3.6 src/translate.py \
  --trdec \
  --model_dir="outputs_orm_trdec_exp5_v16_s2" \
  --data_path="data/orm_data/" \
  --source_vocab="vocab.orm" \
  --target_word_vocab="vocab.random_bina_word.eng" \
  --target_tree_vocab="vocab.random_bina_rule.eng" \
  --source_test="set0-test.tok.piece.orm" \
  --target_test="set0-test.tok.piece.eng" \
  --target_tree_test="set0-test.tok.eng.random_bina" \
  --beam_size=15 \
  --max_len=500 \
  --n_train_sents=10000 \
  --merge_bpe \
  --poly_norm_m=0.5 \
  --out_file="beam15_m0.5" \
  --max_tree_len=3000 \
  --no_lhs \
  --pos=1 \
  --cuda \
  "$@"


python3.6 src/translate.py \
  --trdec \
  --model_dir="outputs_orm_trdec_exp5_v16_s3" \
  --data_path="data/orm_data/" \
  --source_vocab="vocab.orm" \
  --target_word_vocab="vocab.random_bina_word.eng" \
  --target_tree_vocab="vocab.random_bina_rule.eng" \
  --source_test="set0-test.tok.piece.orm" \
  --target_test="set0-test.tok.piece.eng" \
  --target_tree_test="set0-test.tok.eng.random_bina" \
  --beam_size=15 \
  --max_len=500 \
  --n_train_sents=10000 \
  --merge_bpe \
  --poly_norm_m=0.5 \
  --out_file="beam15_m0.5" \
  --max_tree_len=3000 \
  --no_lhs \
  --pos=1 \
  --cuda \
  "$@"


python3.6 src/translate.py \
  --trdec \
  --model_dir="outputs_orm_trdec_exp5_v16_s4" \
  --data_path="data/orm_data/" \
  --source_vocab="vocab.orm" \
  --target_word_vocab="vocab.random_bina_word.eng" \
  --target_tree_vocab="vocab.random_bina_rule.eng" \
  --source_test="set0-test.tok.piece.orm" \
  --target_test="set0-test.tok.piece.eng" \
  --target_tree_test="set0-test.tok.eng.random_bina" \
  --beam_size=15 \
  --max_len=500 \
  --n_train_sents=10000 \
  --merge_bpe \
  --poly_norm_m=0.5 \
  --out_file="beam15_m0.5" \
  --max_tree_len=3000 \
  --no_lhs \
  --pos=1 \
  --cuda \
  "$@"


python3.6 src/translate.py \
  --trdec \
  --model_dir="outputs_orm_trdec_exp5_v16_s5" \
  --data_path="data/orm_data/" \
  --source_vocab="vocab.orm" \
  --target_word_vocab="vocab.random_bina_word.eng" \
  --target_tree_vocab="vocab.random_bina_rule.eng" \
  --source_test="set0-test.tok.piece.orm" \
  --target_test="set0-test.tok.piece.eng" \
  --target_tree_test="set0-test.tok.eng.random_bina" \
  --beam_size=15 \
  --max_len=500 \
  --n_train_sents=10000 \
  --merge_bpe \
  --poly_norm_m=0.5 \
  --out_file="beam15_m0.5" \
  --max_tree_len=3000 \
  --no_lhs \
  --pos=1 \
  --cuda \
  "$@"


#python3.6 src/translate.py \
#  --trdec \
#  --model_dir="outputs_orm_trdec_exp5_v14_s1" \
#  --data_path="data/orm_data/" \
#  --source_vocab="vocab.orm" \
#  --target_word_vocab="vocab.random_bina_word.eng" \
#  --target_tree_vocab="vocab.random_bina_rule.eng" \
#  --source_test="set0-test.tok.piece.orm" \
#  --target_test="set0-test.tok.piece.eng" \
#  --target_tree_test="set0-test.tok.eng.random_bina" \
#  --beam_size=15 \
#  --max_len=500 \
#  --n_train_sents=10000 \
#  --merge_bpe \
#  --poly_norm_m=1 \
#  --out_file="beam15_m1" \
#  --max_tree_len=3000 \
#  --no_lhs \
#  --pos=1 \
#  --cuda \
#  "$@"
#
#python3.6 src/translate.py \
#  --trdec \
#  --model_dir="outputs_orm_trdec_exp5_v14_s2" \
#  --data_path="data/orm_data/" \
#  --source_vocab="vocab.orm" \
#  --target_word_vocab="vocab.random_bina_word.eng" \
#  --target_tree_vocab="vocab.random_bina_rule.eng" \
#  --source_test="set0-test.tok.piece.orm" \
#  --target_test="set0-test.tok.piece.eng" \
#  --target_tree_test="set0-test.tok.eng.random_bina" \
#  --beam_size=15 \
#  --max_len=500 \
#  --n_train_sents=10000 \
#  --merge_bpe \
#  --poly_norm_m=1 \
#  --out_file="beam15_m1" \
#  --max_tree_len=3000 \
#  --no_lhs \
#  --pos=1 \
#  --cuda \
#  "$@"
#
#python3.6 src/translate.py \
#  --trdec \
#  --model_dir="outputs_orm_trdec_exp5_v14_s3" \
#  --data_path="data/orm_data/" \
#  --source_vocab="vocab.orm" \
#  --target_word_vocab="vocab.random_bina_word.eng" \
#  --target_tree_vocab="vocab.random_bina_rule.eng" \
#  --source_test="set0-test.tok.piece.orm" \
#  --target_test="set0-test.tok.piece.eng" \
#  --target_tree_test="set0-test.tok.eng.random_bina" \
#  --beam_size=15 \
#  --max_len=500 \
#  --n_train_sents=10000 \
#  --merge_bpe \
#  --poly_norm_m=1 \
#  --out_file="beam15_m1" \
#  --max_tree_len=3000 \
#  --no_lhs \
#  --pos=1 \
#  --cuda \
#  "$@"
#
#python3.6 src/translate.py \
#  --trdec \
#  --model_dir="outputs_orm_trdec_exp5_v14_s4" \
#  --data_path="data/orm_data/" \
#  --source_vocab="vocab.orm" \
#  --target_word_vocab="vocab.random_bina_word.eng" \
#  --target_tree_vocab="vocab.random_bina_rule.eng" \
#  --source_test="set0-test.tok.piece.orm" \
#  --target_test="set0-test.tok.piece.eng" \
#  --target_tree_test="set0-test.tok.eng.random_bina" \
#  --beam_size=15 \
#  --max_len=500 \
#  --n_train_sents=10000 \
#  --merge_bpe \
#  --poly_norm_m=1 \
#  --out_file="beam15_m1" \
#  --max_tree_len=3000 \
#  --no_lhs \
#  --pos=1 \
#  --cuda \
#  "$@"
#
#python3.6 src/translate.py \
#  --trdec \
#  --model_dir="outputs_orm_trdec_exp5_v14_s5" \
#  --data_path="data/orm_data/" \
#  --source_vocab="vocab.orm" \
#  --target_word_vocab="vocab.random_bina_word.eng" \
#  --target_tree_vocab="vocab.random_bina_rule.eng" \
#  --source_test="set0-test.tok.piece.orm" \
#  --target_test="set0-test.tok.piece.eng" \
#  --target_tree_test="set0-test.tok.eng.random_bina" \
#  --beam_size=15 \
#  --max_len=500 \
#  --n_train_sents=10000 \
#  --merge_bpe \
#  --poly_norm_m=1 \
#  --out_file="beam15_m1" \
#  --max_tree_len=3000 \
#  --no_lhs \
#  --pos=1 \
#  --cuda \
#  "$@"
#