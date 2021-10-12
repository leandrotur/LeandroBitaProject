"""
"""
from typing import Dict, Any


def validate_market_data(body: Dict[str, Any]) -> tuple:
    """Validates the content and the types of the market_data endpoint 
    request body.
    """
    security_id = body['security_id']
    date = body['date']
    close = body['close']
    mic = body.get('mic', None)
    open = body.get('open', "NULL")
    high = body.get('high', "NULL")
    low = body.get('low', "NULL")
    volume = body.get('volume', 0.0)
    split_adj_factor = body.get('split_adj_factor', 1.0)
    div_adj_factor = body.get('div_adj_factor', 1.0)

    # Validating types.
    assert isinstance(security_id, int)
    assert isinstance(date, str)
    assert isinstance(close, (int, float))
    assert isinstance(volume, (int, float))
    assert isinstance(split_adj_factor, (int, float))
    assert isinstance(div_adj_factor, (int, float))
    if open != "NULL":
        assert isinstance(open, (int, float))
    if high != "NULL":
        assert isinstance(high, (int, float))
    if low != "NULL":
        assert isinstance(low, (int, float))

    return security_id, date, close, mic, open, high, low, volume, split_adj_factor, div_adj_factor


