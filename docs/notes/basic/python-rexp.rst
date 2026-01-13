.. meta::
    :description lang=en: Python regular expression cheat sheet covering re module, pattern matching, groups, lookahead, lookbehind, substitution, and common regex patterns
    :keywords: Python, Python Regex, Regular Expression, re module, pattern matching, findall, search, match, sub, lookahead, lookbehind, named groups

==================
Regular Expression
==================

.. contents:: Table of Contents
    :backlinks: none

Regular expressions (regex) are powerful tools for pattern matching and text
manipulation. Python's ``re`` module provides comprehensive support for regex
operations. This cheat sheet covers basic matching, groups, lookaround assertions,
substitution, and common patterns for validating emails, URLs, IP addresses, etc.

Basic Operations
----------------

The ``re`` module provides several functions for pattern matching. Use ``search()``
to find the first match anywhere in the string, ``match()`` to match at the
beginning, and ``fullmatch()`` to match the entire string.

.. code-block:: python

    >>> import re
    >>> # search - find anywhere in string
    >>> re.search(r'\d+', 'abc123def')
    <re.Match object; span=(3, 6), match='123'>

    >>> # match - match at beginning only
    >>> re.match(r'\d+', '123abc')
    <re.Match object; span=(0, 3), match='123'>
    >>> re.match(r'\d+', 'abc123') is None
    True

    >>> # fullmatch - match entire string
    >>> re.fullmatch(r'\d+', '123')
    <re.Match object; span=(0, 3), match='123'>
    >>> re.fullmatch(r'\d+', '123abc') is None
    True

``re.findall()`` - Find All Matches
-----------------------------------

The ``findall()`` function returns all non-overlapping matches as a list of
strings. If the pattern has groups, it returns a list of tuples.

.. code-block:: python

    >>> # find all words
    >>> source = "Hello World Ker HAHA"
    >>> re.findall(r'[\w]+', source)
    ['Hello', 'World', 'Ker', 'HAHA']

    >>> # find all digits
    >>> re.findall(r'\d+', 'a1b22c333')
    ['1', '22', '333']

    >>> # with groups - returns tuples
    >>> re.findall(r'(\w+)=(\d+)', 'a=1 b=2 c=3')
    [('a', '1'), ('b', '2'), ('c', '3')]

``re.split()`` - Split by Pattern
---------------------------------

The ``split()`` function splits a string by pattern occurrences. Use ``maxsplit``
to limit the number of splits.

.. code-block:: python

    >>> re.split(r'\s+', 'a  b   c')
    ['a', 'b', 'c']

    >>> re.split(r'[,;]', 'a,b;c,d')
    ['a', 'b', 'c', 'd']

    >>> re.split(r'(\s+)', 'a b c')  # keep delimiters
    ['a', ' ', 'b', ' ', 'c']

    >>> re.split(r'\s+', 'a b c d', maxsplit=2)
    ['a', 'b', 'c d']

Group Matching
--------------

Parentheses ``(...)`` create capturing groups. Use ``group()`` to access matched
groups. Group 0 is the entire match, group 1 is the first parenthesized group, etc.

.. code-block:: python

    >>> m = re.search(r'(\d{4})-(\d{2})-(\d{2})', '2016-01-01')
    >>> m.groups()
    ('2016', '01', '01')
    >>> m.group()      # entire match
    '2016-01-01'
    >>> m.group(1)     # first group
    '2016'
    >>> m.group(2, 3)  # multiple groups
    ('01', '01')

    # Nested groups - numbered left to right by opening parenthesis
    >>> m = re.search(r'(((\d{4})-\d{2})-\d{2})', '2016-01-01')
    >>> m.groups()
    ('2016-01-01', '2016-01', '2016')

Non-Capturing Group ``(?:...)``
-------------------------------

Use ``(?:...)`` when you need grouping for alternation or quantifiers but don't
need to capture the match. This improves performance and keeps group numbering clean.

.. code-block:: python

    >>> url = 'http://stackoverflow.com/'
    >>> # non-capturing group for protocol
    >>> m = re.search(r'(?:http|ftp)://([^/\r\n]+)(/[^\r\n]*)?', url)
    >>> m.groups()
    ('stackoverflow.com', '/')

    >>> # capturing group - protocol is captured
    >>> m = re.search(r'(http|ftp)://([^/\r\n]+)(/[^\r\n]*)?', url)
    >>> m.groups()
    ('http', 'stackoverflow.com', '/')

Named Groups ``(?P<name>...)``
------------------------------

Named groups make patterns more readable and allow access by name instead of
number. Use ``(?P<name>...)`` to define and ``(?P=name)`` for back reference.

.. code-block:: python

    >>> pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    >>> m = re.search(pattern, '2016-01-01')
    >>> m.group('year')
    '2016'
    >>> m.group('month')
    '01'
    >>> m.groupdict()
    {'year': '2016', 'month': '01', 'day': '01'}

    # named back reference
    >>> re.search(r'^(?P<char>[a-z])(?P=char)', 'aa')
    <re.Match object; span=(0, 2), match='aa'>
    >>> re.search(r'^(?P<char>[a-z])(?P=char)', 'ab') is None
    True

Back Reference ``\1``, ``\2``
-----------------------------

Back references match the same text as a previous capturing group. Use ``\1``
for the first group, ``\2`` for the second, etc.

.. code-block:: python

    >>> # match repeated characters
    >>> re.search(r'([a-z])\1', 'aa') is not None
    True
    >>> re.search(r'([a-z])\1', 'ab') is not None
    False

    >>> # match HTML tags with matching close tag
    >>> pattern = r'<([^>]+)>[\s\S]*?</\1>'
    >>> re.search(pattern, '<bold>test</bold>') is not None
    True
    >>> re.search(pattern, '<bold>test</h1>') is not None
    False

Substitute with ``re.sub()``
----------------------------

The ``sub()`` function replaces pattern matches with a replacement string.
Use ``\1``, ``\2`` in the replacement to reference captured groups.

.. code-block:: python

    >>> # basic substitution
    >>> re.sub(r'[a-z]', ' ', '1a2b3c')
    '1 2 3 '

    >>> # substitute with group reference
    >>> re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\2/\3/\1', '2016-01-01')
    '01/01/2016'

    >>> # using function as replacement
    >>> re.sub(r'\d+', lambda m: str(int(m.group()) * 2), 'a1b2c3')
    'a2b4c6'

    >>> # camelCase to snake_case
    >>> def to_snake(s):
    ...     s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    ...     return re.sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()
    ...
    >>> to_snake('CamelCase')
    'camel_case'
    >>> to_snake('SimpleHTTPServer')
    'simple_http_server'

Lookahead and Lookbehind
------------------------

Lookaround assertions match a position without consuming characters. They are
useful for matching patterns based on context.

+---------------+---------------------+---------------------------+
| Notation      | Name                | Description               |
+===============+=====================+===========================+
| ``(?=...)``   | Positive lookahead  | Followed by ...           |
+---------------+---------------------+---------------------------+
| ``(?!...)``   | Negative lookahead  | Not followed by ...       |
+---------------+---------------------+---------------------------+
| ``(?<=...)``  | Positive lookbehind | Preceded by ...           |
+---------------+---------------------+---------------------------+
| ``(?<!...)``  | Negative lookbehind | Not preceded by ...       |
+---------------+---------------------+---------------------------+

.. code-block:: python

    >>> # positive lookahead - find word before @
    >>> re.findall(r'\w+(?=@)', 'user@example.com')
    ['user']

    >>> # negative lookahead - find digits not followed by px
    >>> re.findall(r'\d+(?!px)', '12px 34em 56')
    ['1', '34', '56']

    >>> # positive lookbehind - find digits after $
    >>> re.findall(r'(?<=\$)\d+', '$100 $200')
    ['100', '200']

    >>> # negative lookbehind - find digits not after $
    >>> re.findall(r'(?<!\$)\d+', '$100 200')
    ['00', '200']

    >>> # insert space before groups of 3 digits from right
    >>> re.sub(r'(?=(\d{3})+$)', ' ', '12345678')
    ' 12 345 678'

Compile Pattern for Reuse
-------------------------

Use ``re.compile()`` to create a reusable pattern object. This improves
performance when the same pattern is used multiple times.

.. code-block:: python

    >>> pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    >>> pattern.search('Date: 2024-01-15')
    <re.Match object; span=(6, 16), match='2024-01-15'>
    >>> pattern.findall('2024-01-15 and 2024-02-20')
    ['2024-01-15', '2024-02-20']

Regex Flags
-----------

Flags modify pattern behavior. Common flags include ``re.IGNORECASE`` (``re.I``),
``re.MULTILINE`` (``re.M``), ``re.DOTALL`` (``re.S``), and ``re.VERBOSE`` (``re.X``).

.. code-block:: python

    >>> # case insensitive
    >>> re.findall(r'[a-z]+', 'Hello World', re.I)
    ['Hello', 'World']

    >>> # multiline - ^ and $ match line boundaries
    >>> re.findall(r'^\w+', 'line1\nline2', re.M)
    ['line1', 'line2']

    >>> # dotall - . matches newline
    >>> re.search(r'a.b', 'a\nb', re.S)
    <re.Match object; span=(0, 3), match='a\nb'>

    >>> # verbose - allow comments and whitespace
    >>> pattern = re.compile(r'''
    ...     \d{4}  # year
    ...     -
    ...     \d{2}  # month
    ...     -
    ...     \d{2}  # day
    ... ''', re.X)
    >>> pattern.match('2024-01-15')
    <re.Match object; span=(0, 10), match='2024-01-15'>

Compare HTML Tags
-----------------

Common patterns for matching different types of HTML tags.

+------------+--------------+--------------+
| Tag Type   | Pattern      | Example      |
+============+==============+==============+
| All tags   | <[^>]+>      | <br />, <a>  |
+------------+--------------+--------------+
| Open tag   | <[^/>][^>]*> | <a>, <table> |
+------------+--------------+--------------+
| Close tag  | </[^>]+>     | </p>, </a>   |
+------------+--------------+--------------+
| Self-close | <[^/>]+/>    | <br />       |
+------------+--------------+--------------+

.. code-block:: python

    >>> # open tag
    >>> re.search(r'<[^/>][^>]*>', '<table>') is not None
    True
    >>> re.search(r'<[^/>][^>]*>', '</table>') is not None
    False

    >>> # close tag
    >>> re.search(r'</[^>]+>', '</table>') is not None
    True

    >>> # self-closing tag
    >>> re.search(r'<[^/>]+/>', '<br />') is not None
    True

Match Email Address
-------------------

A pattern for validating email addresses. Note that fully RFC-compliant email
validation is extremely complex; this covers common cases.

.. code-block:: python

    >>> pattern = re.compile(r'^[\w.+-]+@[\w-]+\.[\w.-]+$')
    >>> pattern.match('hello.world@example.com') is not None
    True
    >>> pattern.match('user+tag@sub.domain.org') is not None
    True
    >>> pattern.match('invalid@') is not None
    False

Match URL
---------

A pattern for matching URLs with optional protocol, domain, and path.

.. code-block:: python

    >>> pattern = re.compile(r'''
    ...     ^(https?://)?           # optional protocol
    ...     ([\da-z.-]+)            # domain
    ...     \.([a-z.]{2,6})         # TLD
    ...     ([/\w.-]*)*/?$          # path
    ... ''', re.X | re.I)
    >>> pattern.match('https://www.example.com/path') is not None
    True
    >>> pattern.match('example.com') is not None
    True

Match IP Address
----------------

A pattern for validating IPv4 addresses (0.0.0.0 to 255.255.255.255).

.. code-block:: python

    >>> pattern = re.compile(r'''
    ...     ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}
    ...     (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
    ... ''', re.X)
    >>> pattern.match('192.168.1.1') is not None
    True
    >>> pattern.match('255.255.255.0') is not None
    True
    >>> pattern.match('256.0.0.0') is not None
    False

Match MAC Address
-----------------

A pattern for validating MAC addresses in colon-separated format.

.. code-block:: python

    >>> pattern = re.compile(r'^([0-9a-f]{2}:){5}[0-9a-f]{2}$', re.I)
    >>> pattern.match('3c:38:51:05:03:1e') is not None
    True
    >>> pattern.match('AA:BB:CC:DD:EE:FF') is not None
    True

Match Phone Number
------------------

Patterns for common phone number formats.

.. code-block:: python

    >>> # US phone number
    >>> pattern = re.compile(r'^(\+1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')
    >>> pattern.match('123-456-7890') is not None
    True
    >>> pattern.match('(123) 456-7890') is not None
    True
    >>> pattern.match('+1 123 456 7890') is not None
    True

Match Password Strength
-----------------------

Pattern to validate password with minimum requirements: at least 8 characters,
one uppercase, one lowercase, one digit, and one special character.

.. code-block:: python

    >>> pattern = re.compile(r'''
    ...     ^(?=.*[a-z])        # at least one lowercase
    ...     (?=.*[A-Z])         # at least one uppercase
    ...     (?=.*\d)            # at least one digit
    ...     (?=.*[@$!%*?&])     # at least one special char
    ...     [A-Za-z\d@$!%*?&]{8,}$  # at least 8 chars
    ... ''', re.X)
    >>> pattern.match('Passw0rd!') is not None
    True
    >>> pattern.match('weakpass') is not None
    False

Simple Lexer
------------

Using regex to build a simple tokenizer for arithmetic expressions. This
demonstrates using named groups and ``scanner()`` for lexical analysis.

.. code-block:: python

    >>> from collections import namedtuple
    >>> tokens = [
    ...     r'(?P<NUMBER>\d+)',
    ...     r'(?P<PLUS>\+)',
    ...     r'(?P<MINUS>-)',
    ...     r'(?P<TIMES>\*)',
    ...     r'(?P<DIVIDE>/)',
    ...     r'(?P<WS>\s+)'
    ... ]
    >>> lex = re.compile('|'.join(tokens))
    >>> Token = namedtuple('Token', ['type', 'value'])
    >>> def tokenize(text):
    ...     scan = lex.scanner(text)
    ...     return (Token(m.lastgroup, m.group())
    ...             for m in iter(scan.match, None) if m.lastgroup != 'WS')
    ...
    >>> list(tokenize('9 + 5 * 2'))
    [Token(type='NUMBER', value='9'), Token(type='PLUS', value='+'), Token(type='NUMBER', value='5'), Token(type='TIMES', value='*'), Token(type='NUMBER', value='2')]

Common Patterns Reference
-------------------------

.. code-block:: python

    # Digits only
    r'^\d+$'

    # Alphanumeric
    r'^[a-zA-Z0-9]+$'

    # Username (3-16 chars, alphanumeric, underscore, hyphen)
    r'^[a-zA-Z0-9_-]{3,16}$'

    # Hex color
    r'^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'

    # Date (YYYY-MM-DD)
    r'^\d{4}-\d{2}-\d{2}$'

    # Time (HH:MM:SS)
    r'^\d{2}:\d{2}:\d{2}$'

    # Slug (URL-friendly string)
    r'^[a-z0-9]+(?:-[a-z0-9]+)*$'

    # Remove HTML tags
    re.sub(r'<[^>]+>', '', html)

    # Extract domain from URL
    re.search(r'https?://([^/]+)', url).group(1)

    # Find all hashtags
    re.findall(r'#\w+', text)

    # Find all @mentions
    re.findall(r'@\w+', text)
