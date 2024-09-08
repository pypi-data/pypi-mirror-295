""" Methods used to convert units to other units """


def convert_kg_to_lb(weight_kg: float) -> float:
    """ Converts weight in kilograms to pounds

    Args:
        weight_kg (float): The weight in kg.

    Returns:
        float: The weight in lb

    Raises:
        ValueError: When a negative weight is provided as input.
    """
    if weight_kg < 0:
        raise ValueError("weight_kg must be positive!")
    return weight_kg * 2.20462
