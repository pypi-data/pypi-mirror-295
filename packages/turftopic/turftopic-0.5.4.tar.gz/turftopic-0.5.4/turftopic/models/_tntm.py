import math
import random
from typing import Optional, Union

import numpy as np
import pyro
import pyro.distributions as dist
import torch
import torch.nn as nn
import torch.nn.functional as F
from pyro.infer import SVI, TraceMeanField_ELBO
from rich.console import Console
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from turftopic.base import ContextualModel, Encoder
from turftopic.vectorizer import default_vectorizer


class EncoderNetwork(nn.Module):
    def __init__(self, contextualized_size, num_topics, hidden, dropout):
        super().__init__()
        self.drop = nn.Dropout(dropout)  # to avoid component collapse
        self.fc1 = nn.Linear(contextualized_size, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.fcmu = nn.Linear(hidden, num_topics)
        self.fclv = nn.Linear(hidden, num_topics)
        self.bnmu = nn.BatchNorm1d(num_topics, affine=False)
        self.bnlv = nn.BatchNorm1d(num_topics, affine=False)

    def forward(self, inputs):
        h = F.softplus(self.fc1(inputs))
        h = F.softplus(self.fc2(h))
        h = self.drop(h)
        logtheta_loc = self.bnmu(self.fcmu(h))
        logtheta_logvar = self.bnlv(self.fclv(h))
        logtheta_scale = (0.5 * logtheta_logvar).exp()  # Enforces positivity
        return logtheta_loc, logtheta_scale


class DecoderNetwork(nn.Module):
    def __init__(self, vocab_size, num_topics, dropout, word_embeddings, mu_init, ):
        super().__init__()
        self.topic_embeddings = nn.Parameter(mu_init)
        self.topic_sigma = nn.Parameter()
        self.bn = nn.BatchNorm1d(vocab_size, affine=False)
        self.drop = nn.Dropout(dropout)

    def forward(self, inputs):
        inputs = self.drop(inputs)
        return F.softmax(self.bn(self.beta(inputs)), dim=1)


class Model(nn.Module):
    def __init__(
        self, vocab_size, contextualized_size, num_topics, hidden, dropout
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.num_topics = num_topics
        self.encoder = EncoderNetwork(
            contextualized_size, num_topics, hidden, dropout
        )

    def model(self, bow, contextualized):
        topic_covariances = pyro.plate("topic_covariances", dist.Wishart(torch.eye(self.num_topics), 1))
        topic_means = pyro.plate("topic_means", dist.Normal(0, (1/self.num_topics) * topic_covariances))
        with pyro.plate("documents", bow.shape[0]):
            logtheta_loc = bow.new_zeros((bow.shape[0], self.num_topics))
            logtheta_scale = bow.new_ones((bow.shape[0], self.num_topics))
            logtheta = pyro.sample(
                "logtheta",
                dist.Normal(logtheta_loc, logtheta_scale).to_event(1),
            )
            theta = F.softmax(logtheta, -1)
            total_count = int(bow.sum(-1).max())
            beta = dist.Normal()
            pyro.sample(
                "obs", dist.Multinomial(total_count, count_param), obs=bow
            )

    def guide(self, bow, contextualized):
        pyro.module("encoder", self.encoder)
        with pyro.plate("documents", contextualized.shape[0]):
            logtheta_loc, logtheta_scale = self.encoder(contextualized)
            logtheta = pyro.sample(
                "logtheta",
                dist.Normal(logtheta_loc, logtheta_scale).to_event(1),
            )

    def beta(self):
        return self.decoder.beta.weight.cpu().detach().T

