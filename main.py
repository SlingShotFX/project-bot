import MetaTrader5 as mt5
from datetime import datetime, timedelta
import logging
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock
from kivy.core.window import Window
from packaging.version import Version, InvalidVersion

try:
    version = Version('1.0.0')
    if version > Version('0.9.0'):
        print("Version is greater than 0.9.0")
except InvalidVersion as e:
    print(f"Invalid version: {e}")


# Add the path to your resources
from kivy.resources import resource_add_path

resource_add_path(r'C:\Users\kkayg\AppData\Roaming\Python\Python312\site-packages\kivymd')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the KV design
kv = '''
ScreenManager:
    LoginScreen:
    TradingScreen:

<LoginScreen>:
    name: 'SFX Login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDLabel:
            text: "SlingShotFX(3093374)"
            halign: "center"
        MDIcon:
            icon: "account"
            halign: "center"
        MDTextField:
            id: server_input
            hint_text: "Server"
            text: 'AccuMarkets-Live'
        MDIcon:
            icon: "key"
            halign: "center"
        MDTextField:
            id: password_input
            hint_text: "Password"
            password: True
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            on_press: app.mt5_login(server_input.text, '3093374', password_input.text)

<TradingScreen>:
    name: 'trading'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDTextField:
            id: symbol_input
            hint_text: "Currency Symbol"
            text: "AUDUSDm"
        MDRaisedButton:
            text: "Start Trading"
            id: start_button
            pos_hint: {"center_x": 0.5}
            on_press: app.start_trading(symbol_input.text)
        MDRaisedButton:
            text: "Stop Trading"
            id: stop_button
            pos_hint: {"center_x": 0.5}
            disabled: True
            on_press: app.stop_trading()
        MDLabel:
            text: "Log:"
            id: log_label
            halign: "center"
        MDLabel:
            text: ""
            id: trade_status_label
            halign: "center"
        MDLabel:
            text: "MetaTrader5"
            id: countdown_label
            halign: "center"
'''

class LoginScreen(MDScreen):
    pass

class TradingScreen(MDScreen):
    pass

class SlingShotFX(MDApp):
    trades_executed = 0
    next_trade_time = None
    trading_event = None

    def build(self):
        self.icon = r'C:\Users\kkayg\Desktop\roboto\sfx.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(kv)

    def mt5_login(self, server, login_id, password):
        if not mt5.initialize(login=int(login_id), password=password, server=server):
            logging.error("initialize() failed, error code = %s", mt5.last_error())
            return False
        logging.info("Connected to %s", server)
        self.root.current = 'trading'
        return True

    def start_trading(self, symbol):
        self.trades_executed = 0
        self.trading_event = Clock.schedule_interval(lambda dt: self.trade(symbol), 5)
        self.root.get_screen('trading').ids.start_button.disabled = True
        self.root.get_screen('trading').ids.stop_button.disabled = False
        logging.info("Trading started.")
        self.update_log("Trading started.")
        self.update_trade_status("Executing...")

    def update_countdown(self, dt):
        if self.next_trade_time:
            remaining_time = self.next_trade_time - datetime.now()
            minutes, seconds = divmod(remaining_time.total_seconds(), 60)
            self.root.get_screen('trading').ids.countdown_label.text = f"Countdown: {int(minutes):02}:{int(seconds):02}"

    def stop_trading(self):
        if self.trading_event:
            self.trading_event.cancel()
            self.trading_event = None
            mt5.shutdown()
            self.root.get_screen('trading').ids.start_button.disabled = False
            self.root.get_screen('trading').ids.stop_button.disabled = True
            logging.info("Trading stopped.")
            self.update_log("Trading stopped.")
            self.update_trade_status("Trading stopped.")
            self.root.get_screen('trading').ids.countdown_label.text = "Countdown: "

    def update_log(self, message):
        self.root.get_screen('trading').ids.log_label.text = f"Log: {message}"

    def update_trade_status(self, message):
        self.root.get_screen('trading').ids.trade_status_label.text = message

    def get_current_rates(self, symbol, timeframe, count=20):
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) < count:
            logging.error("Failed to retrieve candle data for %s", symbol)
            return None
        return rates

    def trade(self, symbol):
        bullish_points, bearish_points = self.check_bullish_bearish_live(symbol)
        current_time = datetime.now()

        if bullish_points and datetime.fromtimestamp(bullish_points[0]['time']).date() == current_time.date():
            self.execute_trade(symbol, "buy")

        if bearish_points and datetime.fromtimestamp(bearish_points[0]['time']).date() == current_time.date():
            self.execute_trade(symbol, "sell")

    def check_bullish_bearish_live(self, symbol):
        rates = self.get_current_rates(symbol, mt5.TIMEFRAME_M5, 50)
        if rates is None:
            return [], []

        prev2, prev1, current = rates[0], rates[1], rates[2]

        bullish_points = []
        bearish_points = []

        # Bullish condition
        if prev1['open'] < prev1['close'] and current['open'] < prev1['close'] and current['close'] > prev2['open']:
            bullish_points.append(current)

        # Bearish condition
        if prev1['open'] > prev1['close'] and current['open'] > prev1['close'] and current['close'] < prev2['open']:
            bearish_points.append(current)

        return bullish_points, bearish_points

    def execute_trade(self, symbol, action, volume=0.5):
        if self.trades_executed >= 20:
            logging.info("Maximum trades executed. Exiting.")
            return

        if action not in ["buy", "sell"]:
            logging.error("Invalid trade action")
            return

        tick = mt5.symbol_info_tick(symbol)
        if not tick or not tick.bid or not tick.ask:
            logging.error("Failed to get tick for symbol %s", symbol)
            return

        price = tick.ask if action == "buy" else tick.bid

        volume_step = mt5.symbol_info(symbol).volume_step
        if volume_step == 0:
            logging.error("Volume step is not defined for %s", symbol)
            return

        rounded_volume = round(volume / volume_step) * volume_step

        if rounded_volume <= 0:
            logging.error("Adjusted volume is zero or negative.")
            return

        logging.info("Executing...")
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": rounded_volume,
            "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error("Failed to send order: %s, %s", result.retcode, result.comment)
            self.update_trade_status(f"Order failed: {result.comment}")
        else:
            self.trades_executed += 1
            logging.info("Order executed: %s %s %s at %s", action, rounded_volume, symbol, price)
            self.update_trade_status(f"Order executed: {action} {rounded_volume} {symbol} at {price}")

if __name__ == "__main__":
    Window.size = (360, 640)
    SlingShotFX().run()
