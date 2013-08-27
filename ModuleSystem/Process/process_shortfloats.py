def sf(input):
    """
    --swyter. build msys with short floats
    """
    input=str(input).rstrip('0')
    if (input[-1]=="."):
     input+="0"
    return input