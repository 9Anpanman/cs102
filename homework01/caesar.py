import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    low_first = ord("a")
    low_last = ord("z")
    high_first = ord("A")
    high_last = ord("Z")
    eng_alp = 26
    for i in plaintext:
        if i.isalpha():
            if low_first <= ord(i) <= low_last:
                a = chr((((ord(i) - low_first) + shift) % eng_alp) + low_first)
                ciphertext += a
            elif high_first <= ord(i) <= high_last:
                a = chr((((ord(i) - high_first) + shift) % eng_alp) + high_first)
                ciphertext += a
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    low_first = ord("a")
    low_last = ord("z")
    high_first = ord("A")
    high_last = ord("Z")
    eng_alp = 26
    for i in ciphertext:
        if i.isalpha():
            if low_first <= ord(i) <= low_last:
                a = chr((((ord(i) - low_first) - shift) % eng_alp) + low_first)
                plaintext += a
            elif high_first <= ord(i) <= high_last:
                a = chr((((ord(i) - high_first) - shift) % eng_alp) + high_first)
                plaintext += a
        else:
            plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    lst = []
    for key in dictionary:
        for shift in range(26):
            plaintext = decrypt_caesar(ciphertext, shift)
            if key == plaintext:
                lst.append(shift)
    for i in range(26):
        if best_shift < lst.count(i):
            best_shift = i
    return best_shift
