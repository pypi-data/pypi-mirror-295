from requests import get


def yosafe_get_yosafe_subpackage_2():
    text = "yosafe_subpackage_2"
    url = "https://cowsay.morecode.org/say"
    params = {
        "message": text,
        "format": "text",
    }
    response = get(url, params=params)
    if response.status_code == 200:
        return response.text 
    else:
        return f"Error: {response.status_code} - Could not retrieve ASCII art."


def yosafe_sub(a, b):
    return a - b



