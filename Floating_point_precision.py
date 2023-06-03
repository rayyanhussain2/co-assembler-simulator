def float_binary(val):
    binary = ""
    frac = val % 1
    while (frac != 0):
        frac *= 2
        if frac > 1:
            binary += "1"
            frac = frac % 1

        elif frac == 1:
            binary += "1"
            break
        else:
            binary += "0"
    i = str(bin(int(val)))[2:]
    l = len(i) + len(binary)
    if (frac!= 0):
        binary  = i + "." + binary + (6 - l)*"0"
    else:
        binary  = i + "." + (6 - l)*"0"

    return binary


def floating_point_precision_val(binary_no):
    exponent = int(("0b" +binary_no[0:3]),2)
    bias = 3
    mantissa = binary_no[3:]
    fraction = 0
    for i in range(len(mantissa)):
        fraction += (2**(-(i+1))) * int(mantissa[i])
    power = exponent - bias
    value = 1 + fraction
    ans = value * (2 ** power)
    if power == -3:
        ans = 0

    return ans


def floating_point_precision_bin(val):
    k = val.split(".")
    shift = len(k[0])-1
    mantissa = k[0][1:] + k[1]
    exponent = shift + 3
    exponentb = str(bin(exponent))[2:]
    exponentb = (3 - len(exponentb))*"0" + exponentb
    return exponentb + mantissa

