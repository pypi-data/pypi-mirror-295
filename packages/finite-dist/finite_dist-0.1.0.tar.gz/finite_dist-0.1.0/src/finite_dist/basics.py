from typing_extensions import TypeVar, Mapping
from collections import Counter
import numpy as np

T = TypeVar('T')
PDist = Counter[T] | Mapping[T, float]

def softmax(p: PDist[T]) -> Counter[T]:
  ks, vs = zip(*p.items())
  vs = np.exp(vs)
  vs /= np.sum(vs)
  return Counter(dict(zip(ks, vs)))

def normalize(p: PDist[T]) -> Counter[T]:
  ks, vs = zip(*p.items())
  vs = np.array(vs)
  vs /= np.sum(vs)
  return Counter(dict(zip(ks, vs)))

def posterior(prior: PDist[T], likelihood: PDist[T]) -> Counter[T]:
  return normalize({ k: prior[k] * likelihood[k] for k in prior })