import re

from telethon.extensions.markdown import DEFAULT_DELIMITERS, DEFAULT_URL_RE
from telethon.helpers import add_surrogate, del_surrogate, strip_text
from telethon.tl.types import (MessageEntityCode, MessageEntityPre,
                               MessageEntityTextUrl)


def parse_lang(text: str, i: int, end: int) -> tuple[str, str, int]:
    """
    Extracts the language of a code block from a message.
    :param text: the message to extract the language from.
    :param i: the start of the code block.
    :param end: the end of the code block.
    :return: a tuple consisting of (language, text, end).
    """
    # Default language values
    lang = ''

    # Find first newline after delimiter
    start_code = text.find('\n', i)

    # If no newline is found, assume that no language is specified
    if not start_code == -1:
        unvalidated_lang = text[i:start_code].strip()

        # Validate language against regex; return default if not matching
        if re.compile(r'[a-zA-Z0-9_-]{1,32}'
                      ).fullmatch(unvalidated_lang) is not None:
            lang = unvalidated_lang

            # Remove lang and extra newline from the text; update 'end'
            code_block = text[start_code:end].strip()
            text = text[:i] + code_block + text[end:]
            end = i + len(code_block)

    return lang, text, end


def patched_parse(message, delimiters=None, url_re=None):
    """
    Parses the given markdown message and returns its stripped representation
    plus a list of the MessageEntity's that were found.

    :param message: the message with markdown-like syntax to be parsed.
    :param delimiters: the delimiters to be used, {delimiter: type}.
    :param url_re: the URL bytes regex to be used. Must have two groups.
    :return: a tuple consisting of (clean message, [message entities]).
    """
    if not message:
        return message, []

    if url_re is None:
        url_re = DEFAULT_URL_RE
    elif isinstance(url_re, str):
        url_re = re.compile(url_re)

    if not delimiters:
        if delimiters is not None:
            return message, []
        delimiters = DEFAULT_DELIMITERS

    # Build a regex to efficiently test all delimiters at once.
    # Note that the largest delimiter should go first, we don't
    # want ``` to be interpreted as a single back-tick in a code block.
    delim_re = re.compile('|'.join('({})'.format(re.escape(k))
                                   for k in
                                   sorted(delimiters, key=len, reverse=True)))

    # Cannot use a for loop because we need to skip some indices
    i = 0
    result = []

    # Work on byte level with the utf-16le encoding to get the offsets right.
    # The offset will just be half the index we're at.
    message = add_surrogate(message)
    while i < len(message):
        m = delim_re.match(message, pos=i)

        # Did we find some delimiter here at `i`?
        if m:
            delim = next(filter(None, m.groups()))

            # +1 to avoid matching right after (e.g. "****")
            end = message.find(delim, i + len(delim) + 1)

            # Did we find the earliest closing tag?
            if end != -1:

                # Remove the delimiter from the string
                message = ''.join((
                    message[:i],
                    message[i + len(delim):end],
                    message[end + len(delim):]
                ))

                # Check other affected entities
                for ent in result:
                    # If the end is after our start, it is affected
                    if ent.offset + ent.length > i:
                        # If the old start is also before ours, it is fully enclosed
                        if ent.offset <= i:
                            ent.length -= len(delim) * 2
                        else:
                            ent.length -= len(delim)

                # Append the found entity
                ent = delimiters[delim]
                if ent == MessageEntityPre:
                    lang, message, end = parse_lang(message, i, end)
                    result.append(ent(i, end - i - len(delim), lang))
                else:
                    result.append(ent(i, end - i - len(delim)))

                # No nested entities inside code blocks
                if ent in (MessageEntityCode, MessageEntityPre):
                    i = end - len(delim)

                continue

        elif url_re:
            m = url_re.match(message, pos=i)
            if m:
                # Replace the whole match with only the inline URL text.
                message = ''.join((
                    message[:m.start()],
                    m.group(1),
                    message[m.end():]
                ))

                delim_size = m.end() - m.start() - len(m.group())
                for ent in result:
                    # If the end is after our start, it is affected
                    if ent.offset + ent.length > m.start():
                        ent.length -= delim_size

                result.append(MessageEntityTextUrl(
                    offset=m.start(), length=len(m.group(1)),
                    url=del_surrogate(m.group(2))
                ))
                i += len(m.group(1))
                continue

        i += 1

    message = strip_text(message, result)
    return del_surrogate(message), result
