import pandas as pd
import numpy as np
from ..EM_for_BMM import data_preprocessor


def test_data_preprocessor():

    for i in range(1, 6):
        n = 10**i
        labels = pd.DataFrame(np.random.choice(a=range(10), size=n))
        x = pd.DataFrame(np.uint8(np.random.rand(n, i)*255))

        df = pd.concat([labels, x], axis=1)

        assert (data_preprocessor(df)[1].to_numpy() == labels.to_numpy().flatten()).all()
        assert (data_preprocessor(df)[0].max() <= 1).all()
