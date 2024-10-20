import winreg
from typing import Optional


def format_product_key(decoded_chars: list[str]) -> str:
    """
    Formats a decoded product key by inserting dashes into the key at the appropriate
    intervals.

    Args:
        decoded_chars (list[str]): A list of characters representing the decoded product key.

    Returns:
        str: The formatted product key as a string (e.g., XXXXX-XXXXX-XXXXX-XXXXX-XXXXX).
    """
    formatted_key = decoded_chars[:]

    for i in range(5, len(formatted_key), 6):
        formatted_key.insert(i, '-')

    return ''.join(formatted_key)


def get_windows_product_key() -> Optional[str]:
    """
    Retrieves the Windows product key from the Windows registry.

    Returns:
        Optional[str]: The decoded Windows product key as a string, or None if an error occurs.
    """
    registry_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    product_id_key = "DigitalProductId"

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        digital_product_id, _ = winreg.QueryValueEx(registry_key, product_id_key)
        winreg.CloseKey(registry_key)

        decoded_key = decode_product_key(digital_product_id)
        return format_product_key(decoded_key)
    except FileNotFoundError:
        print(f"Registry path '{registry_path}' or key '{product_id_key}' not found.")
    except OSError as e:
        print(f"OS error while accessing the registry: {e}")
    except Exception as e:
        print(f"Unexpected error while retrieving the product key: {e}")

    return None


def decode_product_key(digital_product_id: bytes) -> list[str]:
    """
    Decodes the digital product ID from the Windows registry into a list of characters
    representing the product key.

    Args:
        digital_product_id (bytes): The binary data containing the Windows product key.

    Returns:
        list[str]: A list of characters representing the decoded product key.
    """
    key_offset = 52
    chars = "BCDFGHJKMPQRTVWXY2346789"
    decoded_chars = []
    product_id = list(digital_product_id[key_offset:key_offset + 15])

    for _ in range(24, -1, -1):
        current = 0
        for j in range(14, -1, -1):
            current = current * 256 ^ product_id[j]
            product_id[j] = current // 24
            current %= 24
        decoded_chars.insert(0, chars[current])

    return decoded_chars


if __name__ == "__main__":
    product_key = get_windows_product_key()
    if product_key:
        print(f"Windows Product Key: {product_key}")
    else:
        print("Failed to retrieve the Windows product key.")
