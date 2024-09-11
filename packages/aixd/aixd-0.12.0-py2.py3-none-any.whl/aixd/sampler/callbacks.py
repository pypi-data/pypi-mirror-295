from typing import Dict, Tuple

import numpy as np


class GeneratorCallback:
    def __call__(self, samples: Dict[str, np.array], objectives: np.array, valid: np.array) -> Tuple[Dict[str, np.array], np.array, np.array]:
        return samples, objectives, valid
