# 🔧 Config
YAHOO_1D_DIR = "../data/yahoo_1d"
START_DATE_2000 = "2000-01-01"

# 📁 Estructura: categoria -> {ticker: descripción} -- Util para datos de Yahoo. Potencialmente otras fuentes.
SYMBOL_GROUPS_YAHOO = {
    "cripto": {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "SOL-USD": "Solana",
        "XRP-USD": "Ripple",
        "ADA-USD": "Cardano"
    },
    "commodities": {
        "GC=F": "Oro",
        "SI=F": "Plata",
        "CL=F": "Crudo WTI",
        "BZ=F": "Crudo Brent",
        "NG=F": "Gas Natural",
        "HG=F": "Cobre",
        "ZW=F": "Trigo",
        "ZC=F": "Maíz",
        "ZS=F": "Soja"
    },
    "indexes": {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "Dow Jones",
        "^RUT": "Russell 2000",
        "^N225": "Nikkei",
        "^FTSE": "FTSE",
        "^GDAXI": "DAX Alemania",
        "^STOXX50E": "Euro Stoxx 50",
        "^HSI": "Hang Seng",
        "^BVSP": "Bovespa",
        "DX-Y.NYB": "Índice del Dólar (DXY)",
        "^VIX": "Índice de Volatilidad",
        "^DJT": "Dow Jones Transporte"
    },
    "bonds": {
        "^IRX": "Bonos 2 años",
        "^FVX": "Bonos 5 años",
        "^TNX": "Bonos 10 años",
        "^TYX": "Bonos 30 años"
    },
    "forex": {
        "EURUSD=X": "Euro/Dólar",
        "USDJPY=X": "Dólar/Yen",
        "GBPUSD=X": "Libra/Dólar",
        "AUDUSD=X": "Dólar Australiano/Dólar",
        "USDCAD=X": "Dólar Canadiense/Dólar",
        "USDCHF=X": "Dólar/Franco Suizo",
        "NZDUSD=X": "Dólar Neozelandés/Dólar",
        'EURJPY=X': "Euro/Yen",
        'EURGBP=X': "Euro/Libra",
        'CHFJPY=X': "Franco Suizo/Yen",
        'AUDJPY=X': "Dólar Australiano/Yen",
        'EURAUD=X': "Euro/Dólar Australiano",
        'GBPJPY=X': "Libra/Yen",
        'GBPAUD=X': "Libra/Dólar Australiano",
        'AUDNZD=X': "Dólar Australiano/Dólar Neozelandés"
    },
    "stocks": {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet",
        "META": "Meta Platforms",
        "NVDA": "NVIDIA",
        "AVGO": "Broadcom",
        "ORCL": "Oracle",
        "CRM": "Salesforce",

        # Finanzas
        "JPM": "JP Morgan",
        "BAC": "Bank of America",
        "WFC": "Wells Fargo",
        "GS": "Goldman Sachs",
        "MS": "Morgan Stanley",
        "V": "Visa",
        "MA": "Mastercard",
        "AXP": "American Express",

        # Salud
        "UNH": "UnitedHealth",
        "JNJ": "Johnson & Johnson",
        "PFE": "Pfizer",
        "MRK": "Merck",
        "ABBV": "AbbVie",
        "TMO": "Thermo Fisher",

        # Energía
        "XOM": "ExxonMobil",
        "CVX": "Chevron",
        "COP": "ConocoPhillips",
        "SLB": "Schlumberger",

        # Consumo
        "AMZN": "Amazon",
        "TSLA": "Tesla",
        "WMT": "Walmart",
        "HD": "Home Depot",
        "PG": "Procter & Gamble",
        "KO": "Coca-Cola",
        "MCD": "McDonald's",
        "COST": "Costco",
        "TGT": "Target",

        # Industrial
        "GE": "General Electric",
        "HON": "Honeywell",
        "CAT": "Caterpillar",
        "UPS": "UPS",
        "DE": "Deere & Co",

        # Utilities / REITs
        "NEE": "NextEra Energy",
        "DUK": "Duke Energy",
        "PLD": "Prologis",
        "AMT": "American Tower"
    }
}