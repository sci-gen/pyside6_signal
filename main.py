import sys
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# 1. シグナルを定義するクラス (QObjectを継承する必要があります)
class SignalEmitter(QObject):
    # 引数なしのカスタムシグナルを定義
    custom_signal = Signal()

    def __init__(self):
        super().__init__()

    # (ステップ2) ボタンクリックによってこのメソッドが呼び出される
    def emit_the_signal(self):
        print("シグナルを発行します...") # (ステップ2-1) このメッセージが出力される
        # (ステップ2-2) ここでカスタムシグナルを発行
        #              -> このシグナルに接続されているスロット (on_signal_received) が呼び出される
        self.custom_signal.emit()

# 2. スロット（シグナルを受け取るメソッド）を持つクラス
class SignalReceiver(QWidget):
    def __init__(self):
        super().__init__()
        self.emitter = SignalEmitter() # シグナルを発行するオブジェクト
        self.init_ui()

        # 3. シグナルとスロットの接続 (準備段階)
        #    `emitter` オブジェクトの `custom_signal` が発行されたら、
        #    `self` (SignalReceiverオブジェクト) の `on_signal_received` メソッドを呼び出す、という設定。
        #    この接続は emit() される前に確立されている必要がある。
        self.emitter.custom_signal.connect(self.on_signal_received)

    def init_ui(self):
        self.setWindowTitle("PySide6 Minimal Signal Example")
        layout = QVBoxLayout(self)
        button = QPushButton("シグナルを発行", self)

        # (ステップ1) ボタンがクリックされると、接続されたメソッド (emit_the_signal) を呼び出す
        #            これが一連の処理の起点。
        #            QPushButton の 'clicked' シグナルが発行され、
        #            それに接続された 'self.emitter.emit_the_signal' が実行される。
        button.clicked.connect(self.emitter.emit_the_signal)

        layout.addWidget(button)
        self.setLayout(layout)

    # 4. スロットとなるメソッド
    #    (ステップ3) `custom_signal` が emit() された結果、このメソッドが呼び出される
    @Slot()
    def on_signal_received(self):
        # (ステップ3-1) このメッセージが出力される
        print("カスタムシグナルを受け取りました！")

# アプリケーションの実行
if __name__ == '__main__':
    app = QApplication(sys.argv)
    receiver_widget = SignalReceiver()
    receiver_widget.show()
    sys.exit(app.exec())