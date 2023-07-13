import logging
from typing import Callable
import time
import random
import math
from wrapsql import on_complete, on_error

logger = logging.getLogger(__name__)

# takes on_complete function and on_error function that take a float and string
# respectively and returns None
def start_calculation(id : int, calculation_type: str, x_value: float, y_translation: int,
                      on_complete: Callable[[int, float], None],
                      on_error: Callable[[int, str], None]):
    """
    Simulates a long-running calculation.
    Returns None.
    Calls `on_complete` with the floating-point result of the calculation when it finishes.
    Calls `en_error` with a `CalculationException` if it encounters an exception while performing
      the long-running calculation.
    """

    # sleep between 5 and 30 seconds to simulate a long-running calculation
    sleep = random.randint(5, 30)
    logger.debug(f"Sleeping {sleep} seconds ...")
    time.sleep(sleep)

    error = _simulate_error()
    if error:
        logger.debug(f"calculation error = {error}")
        on_error(id, error)
    else:
        result = _calculate(calculation_type, x_value, y_translation)
        logger.debug(f"calculation result = {result}")
        on_complete(id, result)


def _calculate(calculation_type, x_value, y_translation):

    f = {
        "red": math.log,
        "green": math.sin,
        "blue": math.cos
    }[calculation_type]

    return f(x_value) + y_translation


def _simulate_error():

    # errors and how often out of 100 calculations each will occur
    weighted_errors = {
        None: 70,
        "Failed to flux capacitor": 8,
        "Faulty ignition": 4,
        "Dropped ball": 6,
        "Lost connection to satellite": 12
    }

    return random.choices(population=list(weighted_errors.keys()),
                          weights=list(weighted_errors.values()))[0]

