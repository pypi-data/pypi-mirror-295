# MetalMental Logger

MetalMental Loggerは、ログレベルを指定するだけで、標準出力およびファイルにログを出力するシンプルなロガーライブラリです<br>
https://pypi.org/project/metalmental-logger/

## 特徴

- 簡単な設定
- 複数のログレベル（DEBUG、INFO、WARNING、ERROR、CRITICAL）
- ログのファイル出力とコンソール出力のサポート

## インストール

```bash
pip install metalmental-logger
```

## 使い方
```bash
vi sample.py
```
```python
import logging
from metalmental_logger.logger import metalmental_logger

# ロガーのインスタンスを作成
logger = metalmental_logger(log_level=logging.DEBUG)

def sample_function():
    # ログメッセージを出力
    logger.debug("これはデバッグメッセージです")
    logger.info("これは情報メッセージです")
    logger.warning("これは警告メッセージです")
    logger.error("これはエラーメッセージです")
    logger.critical("これは重大なエラーメッセージです")

sample_function()
```
```bash
python sample.py
```
```bash
[prompt]$ python sample.py
[2024-09-11 19:48:53.889 JST] [DEBUG] [9行目] [関数名: sample_function] これはデバッグメッセージです
[2024-09-11 19:48:53.889 JST] [INFO] [10行目] [関数名: sample_function] これは情報メッセージです
[2024-09-11 19:48:53.889 JST] [WARNING] [11行目] [関数名: sample_function] これは警告メッセージです
[2024-09-11 19:48:53.889 JST] [ERROR] [12行目] [関数名: sample_function] これはエラーメッセージです
[2024-09-11 19:48:53.889 JST] [CRITICAL] [13行目] [関数名: sample_function] これは重大なエラーメッセージです
[prompt]$
[prompt]$
[prompt]$ cat logs/2024-09-11.log
[2024-09-11 19:48:53.889 JST] [DEBUG] [9行目] [関数名: sample_function] これはデバッグメッセージです
[2024-09-11 19:48:53.889 JST] [INFO] [10行目] [関数名: sample_function] これは情報メッセージです
[2024-09-11 19:48:53.889 JST] [WARNING] [11行目] [関数名: sample_function] これは警告メッセージです
[2024-09-11 19:48:53.889 JST] [ERROR] [12行目] [関数名: sample_function] これはエラーメッセージです
[2024-09-11 19:48:53.889 JST] [CRITICAL] [13行目] [関数名: sample_function] これは重大なエラーメッセージです
[prompt]$
```

## ライセンス
MITライセンスで提供されています<br>
詳細はLICENSEファイルを参照してください

## 著者
MetalMental - flupino@metalmental.net