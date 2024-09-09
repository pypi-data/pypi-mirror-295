#!/usr/bin/env python3
from sklearn.preprocessing import LabelEncoder
import joblib, pickle
import numpy as np
from pkg_resources import resource_filename
#import importlib.resources as resources
import fire, warnings
from dataclasses import dataclass
import pandas as pd

@dataclass
class Regbot:
  opening: float
  high: float
  asks: float
  bids: float
  vc: float
  ema_26: float
  ema_12: float
  macd: float
  macdsignal: float
  macd_histogram: float
  low: float
  grad_histogram: float
  mean_grad_hist: int
  close: float
  pct_change: float
  volume: float
  grad_vol_sma: float
  ratio4: float
  rsi_05: float
  rsi_15: float
  sma_25: float
  short_close_grad: float
  long_close_grad: float
  close_grad_neg: float
  grad_sma_25: float
  long_kdj: int
  long_grad_kdj: float
  long_jcrosk: int
  short_kdj: int
  short_grad_kdj: float


  imit_model_path: str = resource_filename(__name__, 'imit_model.pkl')
  label_encoder_path: str = resource_filename(__name__, 'imit_label_encoder.pkl')

  def loadmodel(self):
      try:
          # Use the `files` API to locate and open the binary file
          model_path = resource_filename(__name__, 'imit_model.pkl')
          with open(f"{model_path}", "rb") as model:
              clf = joblib.load(model)
              return clf
      except Exception as e:
          print(f"Error loading model: {e}")
          return None

  def loadencoder(self):
      try:
          # Use the `files` API to locate and open the binary file
          encoder_path = resource_filename(__name__, 'imit_label_encoder.pkl')
          with open(f"{encoder_path}", "rb") as encoder:
              le = joblib.load(encoder)
              return le
      except Exception as e:
          print(f"Error loading label encoder: {e}")
          return None


  def prepareInput(self):
    stuff = [self.opening, self.high, self.asks, self.bids, self.vc, self.ema_26,
                            self.ema_12, self.macd, self.macdsignal, self.macd_histogram, self.low,
                            self.grad_histogram, self.mean_grad_hist, self.close, self.pct_change,
                            self.volume, self.grad_vol_sma, self.ratio4, self.rsi_05, self.rsi_15,
                            self.sma_25, self.short_close_grad, self.long_close_grad, self.close_grad_neg,
                            self.grad_sma_25, self.long_kdj, self.long_grad_kdj, self.long_jcrosk,
                            self.short_kdj, self.short_grad_kdj
                            ]
    try:
      test_data = np.array([stuff]
                            )
      return test_data
    except Exception as e:
      print(e)


  def buySignalGenerator(self):
    try:
      model = self.loadmodel()
      data = self.prepareInput().reshape(1,-1)
      preds = model.predict(data)
      label_encoder = self.loadencoder()
      return label_encoder.inverse_transform(preds.astype(int))
    except Exception as e:
      print(e)


def imit_signal(*args):
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            return Regbot(*args).buySignalGenerator()[0]
    except Exception as e:
        print(e)


if __name__ == '__main__':
  fire.Fire(imit_signal)

