import re
from enum import Enum
from typing import List, Optional

class TokenType(Enum):
    CHARACTER = "character"
    ANSI_CODE = "ansi_code"
    EMOJI = "emoji"
    COMBINING_CHAR = "combining_char"
    ZERO_WIDTH_SPACE = "zero_width_space"

class Token:
    def __init__(self, value: str, token_type: TokenType, display_length: int, ansi_reset_code: Optional[str] = None, active_ansi_codes: Optional[List[str]] = None):
        self.value = value  # Raw value of the token (e.g., a character, emoji, or ANSI code)
        self.token_type = token_type  # Type of the token (character, ANSI code, etc.)
        self.display_length = display_length  # Displayed length of the token (0 for ANSI, combining chars, etc.)
        self.ansi_reset_code = ansi_reset_code  # Optional ANSI reset code
        self.active_ansi_codes = active_ansi_codes if active_ansi_codes is not None else []  # List of active ANSI codes

    def __repr__(self):
        return f"Token(value={repr(self.value)}, type={self.token_type}, length={self.display_length}, active_ansi_codes={self.active_ansi_codes})"


def tokenize_string(string: str) -> List[Token]:
    """
    Break a string into tokens based on ANSI codes, emojis, combining characters, etc.
    Track multiple active ANSI codes.
    """
    tokens = []
    ansi_code_pattern = re.compile(r'\x1b\[[0-9;]*m')
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F]')
    active_ansi_codes = []  # To track the list of active ANSI codes

    index = 0
    while index < len(string):
        # Match ANSI code
        ansi_match = ansi_code_pattern.match(string, index)
        if ansi_match:
            ansi_code = ansi_match.group()

            # If it's a reset code, clear active ANSI codes
            if ansi_code == '\033[0m':
                active_ansi_codes.clear()
            else:
                # Add the current ANSI code to the list of active codes
                active_ansi_codes.append(ansi_code)

            # Add the ANSI code token with current active codes
            tokens.append(Token(ansi_code, TokenType.ANSI_CODE, 0, ansi_reset_code='\033[0m', active_ansi_codes=list(active_ansi_codes)))
            index += len(ansi_match.group())
            continue

        char = string[index]

        # Handle zero-width spaces
        if char == '\u200B':
            tokens.append(Token(char, TokenType.ZERO_WIDTH_SPACE, 0, active_ansi_codes=list(active_ansi_codes)))

        # Handle combining characters
        elif re.match(r'[\u0300-\u036F]', char):
            tokens.append(Token(char, TokenType.COMBINING_CHAR, 0, active_ansi_codes=list(active_ansi_codes)))

        # Handle emojis
        elif emoji_pattern.match(char):
            tokens.append(Token(char, TokenType.EMOJI, 1, active_ansi_codes=list(active_ansi_codes)))

        # Handle regular characters
        else:
            tokens.append(Token(char, TokenType.CHARACTER, 1, active_ansi_codes=list(active_ansi_codes)))

        index += 1

    return tokens

