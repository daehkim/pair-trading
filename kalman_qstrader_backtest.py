import click

from qstrader import settings
from qstrader.compat import queue
from qstrader.price_parser import PriceParser
from qstrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from qstrader.strategy import Strategies, DisplayStrategy
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.compliance.example import ExampleCompliance
from qstrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.trading_session.backtest import Backtest

from kalman_qstrader_strategy import KalmanPairsTradingStrategy


def run(config, testing, tickers, filename):
    # Set up variables needed for backtest
    events_queue = queue.Queue()
    csv_dir = config.CSV_DATA_DIR
    initial_invst = 1000000.00
    initial_equity = PriceParser.parse(initial_invst)

    # Use Yahoo Daily Price Handler
    price_handler = YahooDailyCsvBarPriceHandler(
        csv_dir, events_queue, tickers,
    )

    # Use the KalmanPairsTrading Strategy
    strategy = KalmanPairsTradingStrategy(tickers, events_queue, initial_invst)
    strategy = Strategies(strategy, DisplayStrategy())

    # Use the Naive Position Sizer (suggested quantities are followed)
    position_sizer = NaivePositionSizer()

    # Use an example Risk Manager
    risk_manager = ExampleRiskManager()

    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler(
        initial_equity, events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the ExampleCompliance component
    compliance = ExampleCompliance(config)

    # Use a simulated IB Execution Handler
    execution_handler = IBSimulatedExecutionHandler(
        events_queue, price_handler, compliance
    )

    # Use the default Statistics
    statistics = TearsheetStatistics(
        config, portfolio_handler, title=""
    )

    # Set up the backtest
    backtest = Backtest(
        price_handler, strategy,
        portfolio_handler, execution_handler,
        position_sizer, risk_manager,
        statistics, initial_equity
    )
    results = backtest.simulate_trading(testing=testing)
    hist = results['cum_returns']
    print('==:++==')
    print(hist.to_csv('6pair.csv', header=['date,total asset']))
    statistics.save('output')
    return results


# @click.command()
# @click.option('--config', default=settings.DEFAULT_CONFIG_FILENAME, help='Config filename')
# @click.option('--testing/--no-testing', default=False, help='Enable testing mode')
# @click.option('--tickers', default='SP500TR', help='Tickers (use comma)')
# @click.option('--filename', default='', help='Pickle (.pkl) statistics filename')
def main():
    config=settings.DEFAULT_CONFIG_FILENAME
    testing=False

    tickers = ['43350', '82651', '44644', '90458',
               '24969', '24985',  '42585', '83621', '60186', '81095',
               '16548', '81577']
    # tickers = [,]
    # tickers =           []
    # pair = pair_list[1]
    # print(pair)
    # tickers = pair.split(",")
    # tickers = ['43350', '82651']
    # tickers = ['44644', '90458']
    # tickers = ['24969', '24985']
    # tickers = ['42585', '83621']
    # tickers = ['60186', '81095']
    # tickers = ['16548', '81577']

    filename = 'vs'.join(tickers)
    config = settings.from_file(config, testing)
    run(config, testing, tickers, filename)


if __name__ == "__main__":
    main()
