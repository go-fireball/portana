
def get_base_symbol(symbol: str) -> str:
    return symbol.split("_")[0] if "_" in symbol else symbol
