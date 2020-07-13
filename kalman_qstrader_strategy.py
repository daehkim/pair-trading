# kalman_qstrader_strategy.py

from math import floor

import numpy as np

from qstrader.price_parser import PriceParser
from qstrader.event import (SignalEvent, EventType)
from qstrader.strategy.base import AbstractStrategy


class KalmanPairsTradingStrategy(AbstractStrategy):
    """
    Requires:
    tickers - The list of ticker symbols
    events_queue - A handle to the system events queue
    short_window - Lookback period for short moving average
    long_window - Lookback period for long moving average
    """
    def __init__(
        self, tickers, events_queue, initial_investment
    ):
        self.tickers = tickers
        self.num_pairs = len(tickers) // 2
        self.events_queue = events_queue
        self.time = None
        self.days = 0
        self.investment_per_pair = initial_investment / 1.0 / self.num_pairs
        # print(self.investment_per_pair)
        self.trader_data = [{
            'latest_prices': np.array([-1.0, -1.0]),
            'invested':None,
            'delta':1e-4,
            'wt':1e-4/(1-1e-4)*np.eye(2),
            'vt':1e-3,
            'theta':np.zeros(2),
            'P':np.zeros((2, 2)),
            'R':None,
            'qty':None,
            'cur_hedge_qty':None
        } for _ in range(self.num_pairs)]

    def _set_correct_time_and_price(self, event):
        """
        Sets the correct price and event time for prices
        that arrive out of order in the events queue.
        """
        # Set the first instance of time
        if self.time is None:
            self.time = event.time

        # Set the correct latest prices depending upon
        # order of arrival of market bar event
        price = event.adj_close_price/PriceParser.PRICE_MULTIPLIER
        idx = self.tickers.index(event.ticker)
        pair_idx = idx // 2

        if event.time == self.time:
            self.trader_data[pair_idx]['latest_prices'][idx % 2] = price
        else:
            self.time = event.time
            self.days += 1
            self.trader_data[pair_idx]['latest_prices'] = np.array([-1.0, -1.0])
            self.trader_data[pair_idx]['latest_prices'][idx % 2] = price

    def calculate_signals(self, event):
        """
        Calculate the Kalman Filter strategy.
        """
        if event.type == EventType.BAR:
            self._set_correct_time_and_price(event)

            pair_idx = -1

            # Only trade if we have both observations
            for data in self.trader_data:
                pair_idx += 1
                if not all(data['latest_prices'] > -1.0):
                    continue
                F = np.asarray([data['latest_prices'][0], 1.0]).reshape((1, 2))
                y = data['latest_prices'][1]
                if data['R'] is not None:
                    data['R'] = data['C'] + data['wt']
                else:
                    data['R'] = np.zeros((2, 2))
                yhat = F.dot(data['theta'])
                et = y - yhat
                Qt = F.dot(data['R']).dot(F.T) + data['vt']
                sqrt_Qt = np.sqrt(Qt)
                At = data['R'].dot(F.T) / Qt
                data['theta'] = data['theta'] + At.flatten() * et
                data['C'] = data['R'] - At * F.dot(data['R'])

                if self.days > 1:
                    # If we're not in the market...
                    if data['invested'] is None:
                        if et < -sqrt_Qt:
                            # Long Entry
                            # print("LONG: %s" % event.time)
                            data['qty'] = floor(self.investment_per_pair / data['latest_prices'][1])
                            data['cur_hedge_qty'] = floor(self.investment_per_pair / data['latest_prices'][0])
                            # data['cur_hedge_qty'] = int(
                            #     floor(data['qty'] * data['theta'][0]))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2+1], "BOT",
                                            data['qty']))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2], "SLD",
                                            data['cur_hedge_qty']))
                            data['invested'] = "long"
                        elif et > sqrt_Qt:
                            # Short Entry
                            # print("SHORT: %s" % event.time)
                            data['qty'] = floor(self.investment_per_pair / data['latest_prices'][1])
                            data['cur_hedge_qty'] = floor(self.investment_per_pair / data['latest_prices'][0])
                            # data['cur_hedge_qty'] = int(floor(data['qty'] * data['theta'][0]))
                            # self.cur_hedge_qty = int(
                            #     floor(self.qty * self.theta[0]))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2+1], "SLD",
                                            data['qty']))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2], "BOT",
                                            data['cur_hedge_qty']))
                            data['invested'] = "short"
                    # If we are in the market...
                    if data['invested'] is not None:
                        if data['invested'] == 'long' and et > -sqrt_Qt:
                            # print("CLOSING LONG: %s" % event.time)
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2+1], "SLD",
                                            data['qty']))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2], "BOT",
                                            data['cur_hedge_qty']))
                            data['invested'] = None
                        elif data['invested'] == "short" and et < sqrt_Qt:
                            # print("CLOSING SHORT: %s" % event.time)
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2+1], "BOT",
                                            data['qty']))
                            self.events_queue.put(
                                SignalEvent(self.tickers[pair_idx*2], "SLD",
                                            data['cur_hedge_qty']))
                            data['invested'] = None
