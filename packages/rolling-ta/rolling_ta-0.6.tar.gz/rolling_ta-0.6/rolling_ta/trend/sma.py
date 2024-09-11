from typing import Deque
from collections import deque

import numpy as np
import pandas as pd

from rolling_ta.indicator import Indicator
from rolling_ta.logging import logger


class SMA(Indicator):
    """
    A class to represent the Simple Moving Average (SMA) indicator.

    The SMA calculates the average of a selected range of prices by the number of periods in that range.
    It smooths out price data to help identify trends over time. This class computes the SMA using historical
    price data over a specified period.

    Material
    --------
        https://www.investopedia.com/terms/s/sma.asp
        https://pypi.org/project/ta/

    Attributes
    ----------
    _sma : pd.Series
        A pandas Series storing the calculated SMA values for each period.
    _sma_latest : float
        The latest SMA value.
    _window : deque
        A deque holding the most recent closing prices within the specified window.
    _window_sum : float
        The sum of values within the window for fast SMA calculation.

    Methods
    -------
    **__init__(data: pd.DataFrame, period: int = 12, memory: bool = True, init: bool = True)** -> None

        Initializes the SMA indicator with the given data, period, and options.

    **init()** -> None

        Calculates the initial SMA values based on the provided data.

    **update(data: pd.Series)** -> None

        Updates the SMA based on new incoming data.

    **sma()** -> pd.Series

        Returns the stored SMA values if memory is enabled.

    **sma_latest()** -> float

        Returns the latest SMA value.
    """

    _sma: pd.Series
    _sma_latest = np.nan

    _window: Deque[np.float64]
    _window_sum = np.nan

    def __init__(
        self,
        data: pd.DataFrame,
        period: int = 12,
        memory: bool = True,
        init: bool = True,
    ) -> None:
        """
        Initializes the SMA indicator with the given data, period, and options.

        Args:
            data (pd.DataFrame): The initial dataframe to use. Must contain a "close" column.
            period (int): Default=12 | Window length.
            memory (bool): Default=True | Memory flag, if false removes all information not required for updates.
            init (bool, optional): Default=True | Calculate the immediate indicator values upon instantiation.
        """
        super().__init__(data, period, memory, init)
        logger.debug(
            f"SMA init: [data_len={len(data)}, period={period}, memory={memory}, init={init}]"
        )

        if init:
            self.init()

    def init(self):
        """
        Calculates the initial SMA values based on the provided data.

        This method computes the initial SMA values using the specified window length. It also initializes
        internal attributes required for rolling updates and stores the computed SMA values if memory is enabled.
        """
        close = self._data["close"]

        self._window = deque(close[-self._period :], maxlen=self._period)
        self._window_sum = np.sum(self._window)

        sma = close.rolling(window=self._period, min_periods=self._period).mean()
        self._sma_latest = sma.iloc[-1]

        # Use memory for sma.
        if self._memory:
            self._count = close.shape[0]
            self._sma = sma

        # Remove dataframe to avoid memory consumption.
        self._data = None

    def update(self, data: pd.Series):
        """
        Updates the SMA based on new incoming data.

        Args:
            data (pd.Series): A pandas Series containing the new data. Must include a "close" value.
        """
        close = data["close"]

        first_close = self._window[0]
        self._window.append(close)

        self._window_sum = (self._window_sum - first_close) + close
        self._sma_latest = self._window_sum / self._period

        if self._memory:
            self._sma[self._count] = self._sma_latest
            self._count += 1

    def sma(self):
        """
        Returns the stored SMA values if memory is enabled.

        Returns:
            pd.Series: A pandas Series containing the SMA values.

        Raises:
            MemoryError: If function called and memory = False
        """
        if not self._memory:
            raise MemoryError("SMA._memory = False")
        return self._sma

    def sma_latest(self):
        """
        Returns the latest SMA value.

        Returns:
            float: The most recent SMA value.
        """
        return self._sma_latest
