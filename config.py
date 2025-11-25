# Binance API 密钥配置

# API 密钥
API_KEY = '您的币安API密钥'

# API 密钥
API_SECRET = '您的币安API密钥'

# 交易参数配置
# 杠杆参数
LONG_LEVERAGE = 10  # 多单杠杆
SHORT_LEVERAGE = 10  # 空单杠杆

# 交易金额设置
LONG_AMOUNT = 200  # 多单保证金金额(USDT)
SHORT_AMOUNT = 200  # 空单保证金金额(USDT)

# 排除的交易对列表
exclude_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LINKUSDT", "SOLUSDT", "BNBUSDT",
                    "FILUSDT", "DOTUSDT", "MEMEUSDT", "BNXUSDT", "1000SHIBUSDT",
                    "ONDOUSDT", "TRUMPUSDT", "CRVUSDT", "ETHFIUSDT", "TRBUSDT", "SPXUSDT",
                    "MKRUSDT", "BCHUSDT", "TAOUSDT", "ANIMEUSDT", "BUSDT", "LTCUSDT",
                    "DOGEUSDT", "1000PEPEUSDT", "1000000BOBUSDT", "SUIUSDT", "WLDUSDT",
                    "TRXUSDT", "RESOLVUSDT", "FUNUSDT", "MYXUSDT", "TONUSDT", "XLMUSDT",
                     "HYPEUSDT", "FARTCOINUSDT"]  # 在这里添加要排除的交易对
