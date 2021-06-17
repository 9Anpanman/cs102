def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    low_first = ord("a")
    low_last = ord("z")
    high_first = ord("A")
    high_last = ord("Z")
    eng_alp = 26
    for i, letter in enumerate(plaintext):
        shift = ord((keyword[i % len(keyword)]).lower()) - low_first
        if letter.isalpha() and shift != 0:
            chr_i = ord(letter)
            if low_first <= chr_i <= low_last:
                chr_i = chr_i + shift
                if chr_i > low_last:
                    chr_i = chr_i - eng_alp
                ciphertext += chr(chr_i)
            elif high_first <= chr_i <= high_last:
                chr_i = chr_i + shift
                if chr_i > high_last:
                    chr_i = chr_i - eng_alp
                ciphertext += chr(chr_i)
        else:
            ciphertext += letter
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    low_first = ord("a")
    low_last = ord("z")
    high_first = ord("A")
    high_last = ord("Z")
    eng_alp = 26
    for i, letter in enumerate(ciphertext):
        shift = ord((keyword[i % len(keyword)]).lower()) - low_first
        if letter.isalpha() and shift != 0:
            chr_i = ord(letter)
            if low_first <= chr_i <= low_last:
                chr_i = chr_i - shift
                if chr_i < low_first:
                    chr_i = chr_i + eng_alp
                plaintext += chr(chr_i)
            elif high_first <= chr_i <= high_last:
                chr_i = chr_i - shift
                if chr_i < high_first:
                    chr_i = chr_i + eng_alp
                plaintext += chr(chr_i)
        else:
            plaintext += letter
    return plaintext
