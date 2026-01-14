.. meta::
    :description lang=en: Python file I/O tutorial covering reading, writing, binary files, pathlib, context managers, file modes, temporary files, and efficient file handling patterns
    :keywords: Python, Python3, file, I/O, read, write, binary, text, pathlib, Path, context manager, open, with statement, encoding, shutil, tempfile, glob

=============
Files and I/O
=============

:Source: `src/basic/fileio_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/fileio_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

Python provides comprehensive support for file operations and filesystem
manipulation through several built-in modules. The ``open()`` function is the
foundation for reading and writing files, supporting text and binary modes with
configurable encoding. The ``pathlib`` module (Python 3.4+) offers a modern,
object-oriented interface for path manipulation that works consistently across
operating systems. For high-level operations like copying directory trees or
moving files across filesystems, the ``shutil`` module provides convenient
functions. The ``tempfile`` module handles creation of temporary files and
directories with automatic cleanup, essential for secure handling of
intermediate data. Together, these modules cover virtually all file I/O needs
from simple text processing to complex filesystem operations.

Reading Files
-------------

The ``open()`` function returns a file object that supports multiple read
methods. Always use the ``with`` statement (context manager) to ensure files
are properly closed even if an exception occurs. The ``read()`` method loads
the entire file into memory, while iterating over the file object processes
one line at a time, which is more memory-efficient for large files. Always
specify ``encoding="utf-8"`` explicitly to avoid platform-dependent behavior.

.. code-block:: python

    # Read entire file as string
    with open("example.txt", encoding="utf-8") as f:
        content = f.read()

    # Read all lines as list
    with open("example.txt", encoding="utf-8") as f:
        lines = f.readlines()

    # Iterate line by line (memory efficient)
    with open("example.txt", encoding="utf-8") as f:
        for line in f:
            print(line.rstrip())

    # Read specific number of characters
    with open("example.txt", encoding="utf-8") as f:
        first_100 = f.read(100)

    # Read single line
    with open("example.txt", encoding="utf-8") as f:
        first_line = f.readline()

Writing Files
-------------

Python offers several modes for writing files. Mode ``"w"`` creates a new file
or truncates an existing one, ``"a"`` appends to the end without truncating,
and ``"x"`` creates exclusively (raising ``FileExistsError`` if the file
already exists). The ``write()`` method writes a single string, while
``writelines()`` writes an iterable of strings. Note that neither method adds
newlines automatically—you must include ``\n`` in your strings. You can also
redirect ``print()`` output to a file using the ``file`` parameter.

.. code-block:: python

    # Write string to file (overwrites)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Hello, World!\n")

    # Write multiple lines
    lines = ["line 1\n", "line 2\n", "line 3\n"]
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Append to file
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("Appended line\n")

    # Create new file (fails if exists)
    with open("new_file.txt", "x", encoding="utf-8") as f:
        f.write("New content")

    # Print to file
    with open("output.txt", "w", encoding="utf-8") as f:
        print("Hello", "World", sep=", ", file=f)

Binary Files
------------

Binary mode (``"rb"``, ``"wb"``) reads and writes raw bytes without any
encoding or newline translation. This is essential for non-text files like
images, PDFs, executables, or any file where byte-level accuracy matters.
Binary data is represented as ``bytes`` objects in Python. When processing
large binary files, read in chunks to avoid loading the entire file into
memory at once.

.. code-block:: python

    # Read binary file
    with open("image.png", "rb") as f:
        data = f.read()
    print(type(data))  # <class 'bytes'>

    # Write binary file
    with open("copy.png", "wb") as f:
        f.write(data)

    # Read binary in chunks
    chunk_size = 8192
    with open("large_file.bin", "rb") as f:
        while chunk := f.read(chunk_size):
            process(chunk)

File Modes
----------

The ``open()`` function accepts a mode string that controls how the file is
opened. The mode combines access type (read, write, append) with content type
(text or binary). Text mode performs encoding/decoding and newline translation,
while binary mode works with raw bytes. The ``+`` modifier enables both reading
and writing on the same file handle.

Common file modes:

- ``"r"`` - Read text (default)
- ``"w"`` - Write text (truncates)
- ``"a"`` - Append text
- ``"x"`` - Exclusive create (fails if exists)
- ``"rb"`` - Read binary
- ``"wb"`` - Write binary
- ``"r+"`` - Read and write
- ``"w+"`` - Write and read (truncates)

Reading File in Chunks
----------------------

When processing files larger than available memory, reading in chunks prevents
memory exhaustion. A generator function that yields chunks is memory-efficient
and works well with streaming processing. The walrus operator (``:=``) provides
a clean way to read until the file is exhausted. The ``iter()`` function with
a sentinel value offers an alternative pattern for chunk-based reading.

.. code-block:: python

    def read_chunks(filepath, chunk_size=8192):
        """Read file in chunks."""
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    # Process large file
    for chunk in read_chunks("large_file.bin"):
        process(chunk)

    # Using iter with sentinel
    with open("file.txt", encoding="utf-8") as f:
        for chunk in iter(lambda: f.read(1024), ""):
            print(chunk, end="")

pathlib Basics
--------------

The ``pathlib`` module, introduced in Python 3.4, provides an object-oriented
approach to filesystem paths. Unlike string-based path manipulation, ``Path``
objects handle platform differences automatically (forward slashes on Unix,
backslashes on Windows). The ``/`` operator joins path components intuitively,
and methods like ``resolve()`` convert relative paths to absolute. ``Path``
objects are the recommended way to work with filesystem paths in modern Python.

.. code-block:: python

    from pathlib import Path

    # Create path objects
    p = Path("folder/file.txt")
    p = Path.home() / "Documents" / "file.txt"

    # Current and home directories
    cwd = Path.cwd()
    home = Path.home()

    # Absolute path
    abs_path = Path("file.txt").resolve()

Path Properties
---------------

``Path`` objects expose various properties to extract components of a path.
The ``name`` property returns the final component, ``stem`` returns the name
without the suffix, and ``suffix`` returns the file extension including the
dot. The ``parent`` property returns the directory containing the path, and
``parts`` returns a tuple of all path components. Methods like ``with_suffix()``
and ``with_name()`` create new paths with modified components without affecting
the original.

.. code-block:: python

    from pathlib import Path

    p = Path("/home/user/documents/report.pdf")

    print(p.name)      # report.pdf
    print(p.stem)      # report
    print(p.suffix)    # .pdf
    print(p.parent)    # /home/user/documents
    print(p.parts)     # ('/', 'home', 'user', 'documents', 'report.pdf')
    print(p.anchor)    # /

    # Multiple suffixes
    p2 = Path("archive.tar.gz")
    print(p2.suffixes)  # ['.tar', '.gz']

    # Change suffix
    p3 = p.with_suffix(".txt")
    print(p3)  # /home/user/documents/report.txt

    # Change name
    p4 = p.with_name("summary.pdf")
    print(p4)  # /home/user/documents/summary.pdf

Path Operations
---------------

``Path`` objects provide methods to check file existence and type, retrieve
file metadata, and perform read/write operations. The ``exists()``, ``is_file()``,
and ``is_dir()`` methods test path status without raising exceptions. The
``stat()`` method returns detailed file information including size and
modification time. For simple file operations, ``read_text()``, ``write_text()``,
``read_bytes()``, and ``write_bytes()`` provide convenient one-liner alternatives
to the ``open()`` context manager pattern.

.. code-block:: python

    from pathlib import Path

    p = Path("example.txt")

    # Check existence and type
    p.exists()      # True/False
    p.is_file()     # True if regular file
    p.is_dir()      # True if directory
    p.is_symlink()  # True if symbolic link

    # File stats
    stat = p.stat()
    print(stat.st_size)   # File size in bytes
    print(stat.st_mtime)  # Modification time

    # Read and write with pathlib
    content = p.read_text(encoding="utf-8")
    p.write_text("New content", encoding="utf-8")

    # Binary read/write
    data = p.read_bytes()
    p.write_bytes(b"binary data")

Listing Directories
-------------------

Python offers several ways to list directory contents, each with different
trade-offs. The ``pathlib`` method ``iterdir()`` returns an iterator of ``Path``
objects, allowing you to check file types and access properties directly. The
``os.scandir()`` function is highly efficient because it retrieves file type
information during directory iteration without additional system calls. The
simpler ``os.listdir()`` returns just filenames as strings, requiring additional
calls to get file information.

.. code-block:: python

    from pathlib import Path
    import os

    # pathlib - iterate directory
    p = Path(".")
    for item in p.iterdir():
        print(item.name, "dir" if item.is_dir() else "file")

    # pathlib - glob patterns
    for py_file in Path(".").glob("*.py"):
        print(py_file)

    # Recursive glob
    for py_file in Path(".").rglob("*.py"):
        print(py_file)

    # os.scandir (efficient, returns DirEntry)
    with os.scandir(".") as entries:
        for entry in entries:
            print(entry.name, entry.is_file())

    # os.listdir (simple list)
    files = os.listdir(".")

Glob Patterns
-------------

Glob patterns provide a shell-like syntax for matching multiple files. The
``*`` wildcard matches any characters except path separators, ``?`` matches
a single character, and ``**`` matches any number of directories recursively.
The ``pathlib`` methods ``glob()`` and ``rglob()`` (recursive glob) return
iterators of matching ``Path`` objects. Note that ``pathlib`` glob doesn't
support brace expansion like ``{py,txt}``—use multiple glob calls or the
``glob`` module for complex patterns.

.. code-block:: python

    from pathlib import Path

    # All Python files in current directory
    list(Path(".").glob("*.py"))

    # All Python files recursively
    list(Path(".").rglob("*.py"))

    # Multiple extensions
    list(Path(".").glob("*.{py,txt}"))  # Won't work
    # Use instead:
    py_files = list(Path(".").glob("*.py"))
    txt_files = list(Path(".").glob("*.txt"))

    # Single character wildcard
    list(Path(".").glob("file?.txt"))  # file1.txt, file2.txt

    # Using glob module
    import glob
    glob.glob("**/*.py", recursive=True)

Creating Directories
--------------------

Creating directories is straightforward with both ``pathlib`` and ``os``. The
``mkdir()`` method creates a single directory, raising ``FileExistsError`` if
it already exists. The ``parents=True`` parameter creates all intermediate
directories (like ``mkdir -p`` in Unix), and ``exist_ok=True`` suppresses the
error if the directory already exists. These options together make directory
creation idempotent and safe for concurrent execution.

.. code-block:: python

    from pathlib import Path
    import os

    # pathlib - create directory
    Path("new_dir").mkdir()

    # Create with parents (like mkdir -p)
    Path("path/to/nested/dir").mkdir(parents=True, exist_ok=True)

    # os.makedirs
    os.makedirs("path/to/dir", exist_ok=True)

shutil - High-Level File Operations
------------------------------------

The ``shutil`` module provides high-level operations for copying, moving,
and removing files and directory trees.

**Copying Files:**

.. code-block:: python

    import shutil

    # Copy file (content only)
    shutil.copy("source.txt", "dest.txt")

    # Copy file preserving metadata (timestamps, permissions)
    shutil.copy2("source.txt", "dest.txt")

    # Copy to directory (keeps original filename)
    shutil.copy("file.txt", "backup/")  # -> backup/file.txt

    # Copy file object to file object
    with open("src.txt", "rb") as src, open("dst.txt", "wb") as dst:
        shutil.copyfileobj(src, dst)

    # Copy only file content (no metadata)
    shutil.copyfile("source.txt", "dest.txt")

**Copying Directory Trees:**

.. code-block:: python

    import shutil

    # Copy entire directory tree
    shutil.copytree("source_dir", "dest_dir")

    # Copy with ignore patterns
    shutil.copytree(
        "source",
        "dest",
        ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git")
    )

    # Copy into existing directory (Python 3.8+)
    shutil.copytree("source", "existing_dest", dirs_exist_ok=True)

    # Custom ignore function
    def ignore_large_files(directory, files):
        """Ignore files larger than 1MB."""
        ignored = []
        for f in files:
            path = os.path.join(directory, f)
            if os.path.isfile(path) and os.path.getsize(path) > 1_000_000:
                ignored.append(f)
        return ignored

    shutil.copytree("source", "dest", ignore=ignore_large_files)

    # Copy with symlinks preserved
    shutil.copytree("source", "dest", symlinks=True)

**Moving Files and Directories:**

.. code-block:: python

    import shutil
    from pathlib import Path

    # Move file (works across filesystems)
    shutil.move("old_name.txt", "new_name.txt")

    # Move file to directory
    shutil.move("file.txt", "archive/")  # -> archive/file.txt

    # Move entire directory
    shutil.move("old_dir", "new_dir")

    # pathlib rename (same filesystem only)
    Path("old.txt").rename("new.txt")

    # pathlib replace (overwrites destination)
    Path("source.txt").replace("dest.txt")

**Removing Files and Directories:**

.. code-block:: python

    import shutil
    from pathlib import Path

    # Delete entire directory tree
    shutil.rmtree("dir_with_contents")

    # Delete with error handler
    def on_error(func, path, exc_info):
        print(f"Error deleting {path}: {exc_info[1]}")

    shutil.rmtree("dir", onerror=on_error)

    # Delete ignoring errors
    shutil.rmtree("dir", ignore_errors=True)

    # Delete file
    Path("file.txt").unlink()
    Path("file.txt").unlink(missing_ok=True)  # No error if missing

    # Delete empty directory
    Path("empty_dir").rmdir()

**Disk Usage:**

.. code-block:: python

    import shutil

    # Get disk usage statistics
    usage = shutil.disk_usage("/")
    print(f"Total: {usage.total // (1024**3)} GB")
    print(f"Used: {usage.used // (1024**3)} GB")
    print(f"Free: {usage.free // (1024**3)} GB")

**Finding Executables:**

.. code-block:: python

    import shutil

    # Find executable in PATH
    python_path = shutil.which("python")
    print(python_path)  # /usr/bin/python

    # Returns None if not found
    result = shutil.which("nonexistent")
    print(result)  # None

**Archiving:**

.. code-block:: python

    import shutil

    # Create archive (zip, tar, gztar, bztar, xztar)
    shutil.make_archive("backup", "zip", "source_dir")  # -> backup.zip
    shutil.make_archive("backup", "gztar", "source_dir")  # -> backup.tar.gz

    # Extract archive
    shutil.unpack_archive("backup.zip", "extract_dir")
    shutil.unpack_archive("backup.tar.gz", "extract_dir")

    # List supported formats
    print(shutil.get_archive_formats())
    print(shutil.get_unpack_formats())

Temporary Files
---------------

The ``tempfile`` module creates temporary files and directories with unique
names in a secure manner. ``NamedTemporaryFile`` creates a file that is
automatically deleted when closed (unless ``delete=False``). The ``suffix``
parameter adds a file extension, useful when other programs need to identify
the file type. ``TemporaryDirectory`` creates a directory that is recursively
deleted when the context manager exits, perfect for test fixtures or
intermediate processing. These functions use the system's temp directory by
default, which you can query with ``gettempdir()``.

.. code-block:: python

    import tempfile
    from pathlib import Path

    # Temporary file (auto-deleted when closed)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=True) as f:
        f.write("temporary content")
        print(f.name)  # /tmp/tmpXXXXXX.txt

    # Temporary file that persists
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        temp_path = f.name
        f.write("persistent temp")
    # Clean up manually later
    Path(temp_path).unlink()

    # Temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file = Path(tmpdir) / "file.txt"
        temp_file.write_text("content")
        # Directory deleted when exiting context

    # Get temp directory path
    print(tempfile.gettempdir())  # /tmp

Symbolic Links
--------------

Symbolic links (symlinks) are special files that point to another file or
directory. They're useful for creating shortcuts, managing multiple versions,
or organizing files without duplication. The ``symlink_to()`` method creates
a symlink pointing to the specified target. The ``is_symlink()`` method checks
if a path is a symlink, and ``readlink()`` returns the target path. The
``resolve()`` method follows all symlinks to return the canonical absolute path.

.. code-block:: python

    from pathlib import Path
    import os

    # Create symlink with pathlib
    Path("link_name").symlink_to("target_file")

    # Create symlink with os
    os.symlink("target", "link")

    # Read symlink target
    target = Path("link_name").readlink()
    target = os.readlink("link")

    # Check if symlink
    Path("link_name").is_symlink()

    # Resolve symlink to real path
    real_path = Path("link_name").resolve()

File Permissions
----------------

Unix-like systems use permission bits to control file access. The ``stat()``
method returns file metadata including the permission mode. The ``chmod()``
method modifies permissions using octal notation (e.g., ``0o644`` for
owner read/write, group/other read-only) or by combining ``stat`` module
constants. The ``os.access()`` function checks if the current process has
specific permissions on a file, useful for pre-flight checks before attempting
operations.

.. code-block:: python

    from pathlib import Path
    import os
    import stat

    p = Path("script.sh")

    # Get permissions
    mode = p.stat().st_mode
    print(oct(mode))  # 0o100644

    # Make executable
    p.chmod(p.stat().st_mode | stat.S_IXUSR)

    # Set specific permissions (owner rw, group r, other r)
    p.chmod(0o644)

    # Check if readable/writable
    os.access("file.txt", os.R_OK)  # Readable
    os.access("file.txt", os.W_OK)  # Writable
    os.access("file.txt", os.X_OK)  # Executable

Working with CSV Files
----------------------

CSV (Comma-Separated Values) is a common format for tabular data exchange.
Python's ``csv`` module handles the complexities of CSV parsing, including
quoted fields, different delimiters, and proper escaping. The ``writer``
object writes rows as lists, while ``DictWriter`` writes dictionaries using
column headers as keys. Similarly, ``reader`` yields rows as lists, and
``DictReader`` yields dictionaries. Always open CSV files with ``newline=""``
to let the csv module handle line endings correctly across platforms.

.. code-block:: python

    import csv

    # Write CSV
    with open("data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age", "city"])
        writer.writerow(["Alice", 30, "NYC"])
        writer.writerows([["Bob", 25, "LA"], ["Carol", 35, "Chicago"]])

    # Read CSV
    with open("data.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            print(row)

    # DictReader/DictWriter
    with open("data.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row["name"], row["age"])

Working with JSON Files
-----------------------

JSON (JavaScript Object Notation) is the standard format for data interchange
in web APIs and configuration files. Python's ``json`` module serializes Python
objects (dicts, lists, strings, numbers, booleans, None) to JSON strings and
deserializes JSON back to Python objects. The ``dump()`` and ``load()`` functions
work directly with file objects, while ``dumps()`` and ``loads()`` work with
strings. The ``indent`` parameter produces human-readable formatted output.

.. code-block:: python

    import json
    from pathlib import Path

    data = {"name": "Alice", "scores": [95, 87, 92]}

    # Write JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Read JSON
    with open("data.json", encoding="utf-8") as f:
        loaded = json.load(f)

    # pathlib shorthand
    Path("data.json").write_text(json.dumps(data, indent=2))
    loaded = json.loads(Path("data.json").read_text())

Compressed Files
----------------

Python supports several compression formats through dedicated modules. The
``gzip`` module handles gzip compression, commonly used for log files and web
content. Use ``"rt"`` and ``"wt"`` modes for text, ``"rb"`` and ``"wb"`` for
binary. The ``zipfile`` module creates and extracts ZIP archives, supporting
multiple files in a single archive. The ``writestr()`` method adds content
directly from strings without creating temporary files. Both modules integrate
seamlessly with Python's file handling patterns.

.. code-block:: python

    import gzip
    import zipfile
    from pathlib import Path

    # Write gzip file
    with gzip.open("file.txt.gz", "wt", encoding="utf-8") as f:
        f.write("compressed content")

    # Read gzip file
    with gzip.open("file.txt.gz", "rt", encoding="utf-8") as f:
        content = f.read()

    # Create zip archive
    with zipfile.ZipFile("archive.zip", "w") as zf:
        zf.write("file1.txt")
        zf.write("file2.txt")
        zf.writestr("new.txt", "content from string")

    # Extract zip archive
    with zipfile.ZipFile("archive.zip", "r") as zf:
        zf.extractall("output_dir")
        # Extract single file
        zf.extract("file1.txt", "output_dir")

    # List zip contents
    with zipfile.ZipFile("archive.zip", "r") as zf:
        print(zf.namelist())

File Locking
------------

File locking prevents data corruption when multiple processes access the same
file. On Unix systems, ``fcntl.flock()`` provides advisory locking—processes
must cooperatively check locks. ``LOCK_EX`` requests an exclusive lock for
writing, while ``LOCK_SH`` allows shared read access. The ``LOCK_NB`` flag
makes the call non-blocking, raising ``BlockingIOError`` if the lock isn't
immediately available. Always release locks in a ``finally`` block to prevent
deadlocks. Note that Windows uses different locking mechanisms (``msvcrt``).

.. code-block:: python

    import fcntl
    import time

    # Exclusive lock (Unix)
    with open("data.txt", "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write("exclusive write")
            time.sleep(1)  # Simulate work
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    # Non-blocking lock attempt
    with open("data.txt", "w") as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            f.write("got lock")
        except BlockingIOError:
            print("File is locked by another process")

Watching File Changes (inotify)
-------------------------------

The Linux inotify API provides efficient filesystem event monitoring without
polling. Applications can watch directories for file creation, deletion,
modification, and other events. This is useful for auto-reloading configuration
files, triggering builds on source changes, or synchronizing directories.
The example below demonstrates direct inotify access via ``ctypes``; for
production use, consider the ``watchdog`` library which provides a
cross-platform abstraction.

.. code-block:: python

    import ctypes
    import os
    import struct
    import selectors
    from ctypes.util import find_library
    from pathlib import Path

    # inotify constants
    IN_CREATE = 0x00000100
    IN_DELETE = 0x00000200
    IN_MODIFY = 0x00000002

    libc = ctypes.CDLL(find_library("c"))

    class Inotify:
        def __init__(self, path, mask=IN_CREATE | IN_DELETE | IN_MODIFY):
            self.path = path
            self.mask = mask
            self.fd = None
            self.wd = None

        def __enter__(self):
            self.fd = libc.inotify_init()
            path_bytes = str(self.path).encode("utf-8")
            self.wd = libc.inotify_add_watch(self.fd, path_bytes, self.mask)
            return self

        def __exit__(self, *args):
            libc.inotify_rm_watch(self.fd, self.wd)
            os.close(self.fd)

        def read_events(self):
            data = os.read(self.fd, 4096)
            offset = 0
            while offset < len(data):
                wd, mask, cookie, length = struct.unpack_from("iIII", data, offset)
                offset += 16
                name = data[offset:offset + length].rstrip(b"\0").decode("utf-8")
                offset += length
                yield mask, name

    # Usage
    with Inotify(Path("/tmp")) as inotify:
        for mask, filename in inotify.read_events():
            print(f"Event {mask}: {filename}")
