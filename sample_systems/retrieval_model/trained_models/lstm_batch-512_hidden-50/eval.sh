#!/usr/bin/env bash

THEANO_FLAGS='floatX=float32,device=gpu2' python main_with-eval.py \
    --encoder 'lstm' \
    --batch_size 512 \
    --hidden_size 50 \
    --optimizer 'adam' \
    --lr 0.001 \
    --fine_tune_W True \
    --fine_tune_M True \
    --input_dir '../../twitter_dataset' \
    --dataset_fname 'dataset_twitter_bpe.pkl' \
    --W_fname 'W_twitter_bpe.pkl' \
    --test True

