.. meta::
    :description lang=en: Python operating system interface tutorial covering file operations, process management, environment variables, path manipulation, system information, and cross-platform OS interactions
    :keywords: Python, os module, operating system, file system, process, environment variables, path, directory, subprocess, platform, system info, CPU, memory

================
Operating System
================

:Source: `src/basic/os_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/os_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Python's ``os`` module provides a portable way to interact with the operating system,
abstracting platform-specific details behind a consistent API. Whether you're managing
files and directories, spawning processes, reading environment variables, or querying
system information, the ``os`` module handles the differences between Windows, Linux,
and macOS. For path manipulation, the ``os.path`` submodule (or the modern ``pathlib``)
provides cross-platform path handling. This cheat sheet covers common OS operations
with practical examples.

Get System Information
----------------------

Retrieve basic information about the operating system, platform, and current process.
These functions are useful for writing cross-platform code that adapts to the runtime
environment.

.. code-block:: python

    import os
    import platform

    # Operating system name
    os.name                    # 'posix' (Linux/macOS) or 'nt' (Windows)

    # Platform details
    platform.system()          # 'Linux', 'Darwin', 'Windows'
    platform.release()         # '5.15.0-generic', '22.1.0', '10'
    platform.machine()         # 'x86_64', 'arm64', 'AMD64'
    platform.processor()       # 'x86_64', 'arm', ''
    platform.python_version()  # '3.12.0'

    # Current process
    os.getpid()               # Process ID
    os.getppid()              # Parent process ID
    os.getcwd()               # Current working directory
    os.getlogin()             # Current username

Get Number of CPUs
------------------

Determine the number of CPU cores available for parallel processing. This is essential
for configuring thread pools, multiprocessing workers, or understanding system capacity.
Note that ``cpu_count()`` returns logical cores (including hyperthreading), not physical
cores.

.. code-block:: python

    import os

    # Number of logical CPUs
    cpu_count = os.cpu_count()
    print(f"CPUs: {cpu_count}")  # CPUs: 8

    # For physical cores (Linux only)
    # cat /proc/cpuinfo | grep "cpu cores" | uniq

Set CPU Affinity
----------------

CPU affinity binds a process to specific CPU cores, useful for performance optimization,
reducing cache misses, or isolating workloads. This feature is Linux-specific and not
available on macOS or Windows through the ``os`` module.

.. code-block:: python

    import os

    # Linux only - set process to run on specific CPUs
    pid = os.getpid()
    affinity = {0, 1}  # Run on CPU 0 and 1 only
    os.sched_setaffinity(pid, affinity)

    # Get current affinity
    current = os.sched_getaffinity(pid)
    print(f"Running on CPUs: {current}")  # Running on CPUs: {0, 1}

Environment Variables
---------------------

Environment variables store configuration that persists across process invocations.
Use ``os.environ`` as a dictionary to read, set, or delete variables. Changes only
affect the current process and its children, not the parent shell.

.. code-block:: python

    import os

    # Read environment variable
    home = os.environ.get('HOME')           # Returns None if not set
    path = os.environ['PATH']               # Raises KeyError if not set
    debug = os.getenv('DEBUG', 'false')     # With default value

    # Set environment variable
    os.environ['MY_VAR'] = 'my_value'

    # Delete environment variable
    del os.environ['MY_VAR']
    os.unsetenv('MY_VAR')  # Alternative

    # List all environment variables
    for key, value in os.environ.items():
        print(f"{key}={value}")

Path Operations
---------------

Path manipulation is one of the most common OS tasks. The ``os.path`` module provides
cross-platform functions that handle path separators (``/`` vs ``\``) automatically.
For modern Python (3.4+), consider using ``pathlib`` for an object-oriented approach.

.. code-block:: python

    import os

    # Join paths (handles separators automatically)
    path = os.path.join('/home', 'user', 'file.txt')
    # Linux: '/home/user/file.txt'
    # Windows: '\\home\\user\\file.txt'

    # Split path components
    dirname = os.path.dirname('/home/user/file.txt')   # '/home/user'
    basename = os.path.basename('/home/user/file.txt') # 'file.txt'
    name, ext = os.path.splitext('file.txt')           # ('file', '.txt')

    # Absolute and relative paths
    abs_path = os.path.abspath('.')           # Full path
    rel_path = os.path.relpath('/home/user')  # Relative to cwd
    real_path = os.path.realpath('link')      # Resolve symlinks

    # Path checks
    os.path.exists('/path/to/file')    # True if exists
    os.path.isfile('/path/to/file')    # True if regular file
    os.path.isdir('/path/to/dir')      # True if directory
    os.path.islink('/path/to/link')    # True if symbolic link

    # Path info
    os.path.getsize('/path/to/file')   # Size in bytes
    os.path.getmtime('/path/to/file')  # Modification time (timestamp)

Directory Operations
--------------------

Create, remove, and navigate directories. These operations are fundamental for file
management, build systems, and data processing pipelines.

.. code-block:: python

    import os

    # Create directory
    os.mkdir('new_dir')                    # Single directory
    os.makedirs('path/to/new_dir')         # Create parent dirs too
    os.makedirs('path/to/dir', exist_ok=True)  # Don't error if exists

    # Remove directory
    os.rmdir('empty_dir')                  # Must be empty
    # For non-empty: use shutil.rmtree()

    # Change directory
    os.chdir('/path/to/dir')
    print(os.getcwd())                     # Print current directory

    # List directory contents
    entries = os.listdir('.')              # List of names
    for entry in entries:
        print(entry)

    # Walk directory tree
    for root, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            print(path)

File Operations
---------------

Low-level file operations using file descriptors. For most use cases, Python's built-in
``open()`` function is preferred, but ``os`` functions are useful for special cases like
non-blocking I/O or when you need precise control over file descriptors.

.. code-block:: python

    import os

    # Rename/move file
    os.rename('old_name.txt', 'new_name.txt')
    os.replace('src.txt', 'dst.txt')  # Atomic, overwrites dst

    # Remove file
    os.remove('file.txt')
    os.unlink('file.txt')  # Same as remove

    # File permissions (Unix)
    os.chmod('file.txt', 0o644)  # rw-r--r--
    os.chown('file.txt', uid, gid)  # Change owner

    # Create symbolic link
    os.symlink('target', 'link_name')

    # Low-level file operations
    fd = os.open('file.txt', os.O_RDONLY)
    data = os.read(fd, 1024)  # Read up to 1024 bytes
    os.close(fd)

Execute Commands
----------------

Run external commands and programs. For simple cases, ``os.system()`` works, but
``subprocess`` module is recommended for more control over input/output and error
handling.

.. code-block:: python

    import os
    import subprocess

    # Simple command (returns exit code)
    exit_code = os.system('ls -la')

    # Better: use subprocess
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    print(result.stdout)
    print(result.returncode)

    # Run and capture output
    output = subprocess.check_output(['date'], text=True)
    print(output.strip())

    # Run with input
    result = subprocess.run(
        ['grep', 'pattern'],
        input='line1\npattern here\nline3',
        capture_output=True,
        text=True
    )

Process Management
------------------

Create and manage child processes. The ``os.fork()`` function is Unix-specific; for
cross-platform process creation, use the ``multiprocessing`` module instead.

.. code-block:: python

    import os

    # Fork process (Unix only)
    pid = os.fork()
    if pid == 0:
        # Child process
        print(f"Child PID: {os.getpid()}")
        os._exit(0)
    else:
        # Parent process
        print(f"Parent PID: {os.getpid()}, Child PID: {pid}")
        os.waitpid(pid, 0)  # Wait for child

    # Execute new program (replaces current process)
    # os.execv('/bin/ls', ['ls', '-la'])

    # Send signal to process
    os.kill(pid, signal.SIGTERM)

Temporary Files
---------------

Create temporary files and directories that are automatically cleaned up. The
``tempfile`` module provides secure, cross-platform temporary file handling.

.. code-block:: python

    import tempfile
    import os

    # Temporary file (auto-deleted when closed)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write('temporary data')
        temp_path = f.name
    print(f"Temp file: {temp_path}")
    os.unlink(temp_path)  # Manual cleanup if delete=False

    # Temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file = os.path.join(tmpdir, 'file.txt')
        with open(temp_file, 'w') as f:
            f.write('data')
        # Directory and contents deleted after with block

    # Get temp directory path
    print(tempfile.gettempdir())  # /tmp or C:\Users\...\Temp

Using pathlib (Modern Alternative)
----------------------------------

The ``pathlib`` module (Python 3.4+) provides an object-oriented interface to paths,
making code more readable and less error-prone than string-based ``os.path`` operations.

.. code-block:: python

    from pathlib import Path

    # Create path objects
    p = Path('/home/user/file.txt')
    p = Path.home() / 'documents' / 'file.txt'  # Use / operator

    # Path components
    p.name          # 'file.txt'
    p.stem          # 'file'
    p.suffix        # '.txt'
    p.parent        # Path('/home/user')
    p.parts         # ('/', 'home', 'user', 'file.txt')

    # Path checks
    p.exists()
    p.is_file()
    p.is_dir()

    # Read/write files
    content = p.read_text()
    p.write_text('new content')
    data = p.read_bytes()

    # Directory operations
    Path('new_dir').mkdir(parents=True, exist_ok=True)
    for child in Path('.').iterdir():
        print(child)

    # Glob patterns
    for py_file in Path('.').glob('**/*.py'):
        print(py_file)


System Monitoring with psutil
-----------------------------

The ``psutil`` (process and system utilities) library provides cross-platform access
to system monitoring data that isn't available through the standard ``os`` module.
It covers CPU, memory, disk, network, and process information. Install with
``pip install psutil``.

.. code-block:: python

    import psutil

    # CPU information
    psutil.cpu_count()                    # Logical CPUs
    psutil.cpu_count(logical=False)       # Physical cores
    psutil.cpu_percent(interval=1)        # CPU usage %
    psutil.cpu_percent(percpu=True)       # Per-CPU usage
    psutil.cpu_freq()                     # CPU frequency

    # Memory information
    mem = psutil.virtual_memory()
    mem.total                             # Total RAM in bytes
    mem.available                         # Available RAM
    mem.percent                           # Usage percentage
    mem.used                              # Used RAM

    # Swap memory
    swap = psutil.swap_memory()
    swap.total, swap.used, swap.percent

    # Disk information
    psutil.disk_partitions()              # List partitions
    usage = psutil.disk_usage('/')
    usage.total, usage.used, usage.percent

    # Network information
    psutil.net_io_counters()              # Bytes sent/received
    psutil.net_connections()              # Active connections
    psutil.net_if_addrs()                 # Interface addresses

    # Process information
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        print(proc.info)

    # Current process
    p = psutil.Process()
    p.pid
    p.name()
    p.cpu_percent()
    p.memory_info()
    p.num_threads()

    # System boot time
    import datetime
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
