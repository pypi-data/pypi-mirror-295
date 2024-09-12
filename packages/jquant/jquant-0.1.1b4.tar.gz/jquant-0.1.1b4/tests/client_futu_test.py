import json
import logging

import jquant


class TestExchange:
    _platform = "futu.hk"
    _inst = "HK.00700"
    _insts = [_inst]
    _strategy = "GridStrategy"
    _investor = "PROD001"

    pc = jquant.PlatformClient(
        _strategy,
        "localhost:8081",
        # "192.168.1.200:18081",
        # "172.16.2.41:8081",
        metadata=[
            ("initial-metadata-1", "The value should be str"),
            ("authorization", "gRPC Python is great"),
        ],
    )

    def test_get_ticker(self):
        reply = self.pc.get_ticker(platform=self._platform, instrument=self._inst)
        print(f"recv from server, result={reply}")

    def test_get_tickers(self):
        reply = self.pc.get_tickers(platforms=[self._platform], instruments=self._insts)
        print(f"recv from server, result={reply}")

    def test_get_kline(self):
        reply = self.pc.get_kline(
            platform=self._platform, instrument=self._inst, period="1m"
        )
        print(f"recv from server, result={reply}")

    def test_get_position(self):
        reply = self.pc.get_position(
            platform=self._platform,
        )
        print(f"recv from server, result={reply}")

    def test_get_instrument(self):
        reply = self.pc.get_instruments(
            platform=self._platform,
            kinds=[jquant.InstrumentKind.FUTURE],
            instruments=self._insts,
        )
        print(f"recv from server, result={reply}")

    def test_get_config(self):
        reply = self.pc.get_config(
            platform=self._platform,
            strategy=self._strategy,
        )
        print(f"recv from server, reply={reply}")

        # 获取策略配置
        strategy = json.loads(reply.get("strategy", "{}"))
        print(f"strategy={strategy}")

        # 获取该策略的合约配置
        instruments = json.loads(reply.get("instruments", "{}"))
        print(f"instruments={instruments}")

    def test_get_order(self):
        reply = self.pc.get_order(
            platform=self._platform,
            instrument=self._inst,
            client_order_id="84041793665",
        )
        print(f"recv from server, result={reply}")

    def test_get_orders(self):
        orders = self.pc.get_orders(
            platform=self._platform,
            instruments=self._insts,
            investor=self._investor,
            strategy=self._strategy,
        )
        # print(f"recv from server, result={orders}")
        for order in orders:
            print(f"order={order}")

    def test_cancel(self):
        reply = self.pc.cancel(
            platform=self._platform,
            instrument=self._inst,
            client_order_ids=["89745522817"],
        )
        print(f"recv from server, result={reply}")

    def test_buy(self):
        reply = self.pc.buy(
            platform=self._platform,
            instrument=self._inst,
            price="102.5",
            amount="1",
            investor=self._investor,
            strategy=self._strategy,
            source="01",
            tag="01",
            # VolumeCondition="3",
        )
        print(f"recv from server, result={reply}")

    def test_close_buy(self):
        reply = self.pc.close_buy(
            platform=self._platform,
            instrument=self._inst,
            price="102",
            amount="1",
            investor=self._investor,
            strategy=self._strategy,
        )
        print(f"recv from server, result={reply}")

    def test_sell(self):
        reply = self.pc.sell(
            platform=self._platform,
            instrument=self._inst,
            price="559",
            amount="1",
            investor=self._investor,
            strategy=self._strategy,
            source="01",
            tag="01",
            # VolumeCondition="3",
        )
        print(f"recv from server, result={reply}")

    def test_close_sell(self):
        reply = self.pc.close_sell(
            platform=self._platform,
            instrument=self._inst,
            price="3832",
            amount="1",
            investor=self._investor,
            strategy=self._strategy,
            CombOffsetFlag="3",
        )
        print(f"recv from server, result={reply}")

    def test_subscribe_order(self):
        self.pc.subscribe_order(
            platform=self._platform,
            instruments=[self._inst],
            investor=self._investor,
            strategy=self._strategy,
            handler=self.on_order,
        )

    def on_order(self, orders):
        for order in orders:
            print(f"order={order}")

    def test_subscribe_ticker(self):
        self.pc.subscribe_tick(
            platforms=[self._platform],
            instruments=self._insts,
            handler=self.on_tick,
        )

    def on_tick(self, ticker):
        # print(f"recv from server, ticker={ticker}")
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    t = TestExchange()

    # t.test_get_ticker()
    # t.test_get_order()
    # t.test_get_orders()
    # t.test_buy()
    # t.test_closebuy()
    # t.test_cancel()
    # t.test_get_instrument()
    t.test_subscribe_ticker()
    # t.test_subscribe_order()
    # t.test_get_position()
