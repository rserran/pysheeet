# -*- coding: utf-8 -*-
"""This is a simple cheatsheet webapp."""

import os
import re

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from flask_sslify import SSLify
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from werkzeug.exceptions import NotFound
from werkzeug.utils import safe_join

DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(DIR, "docs", "_build", "html")

# Pysheeet was historically hosted on Read the Docs, which uses
# /en/<slug>/<path> URLs (latest, stable, vX.Y.Z, master). The current flat
# Heroku origin 404s those. Redirect them to the canonical flat URL so Google
# can drop them from the index cleanly instead of 404-churning.
_LEGACY_RTD_PATH = re.compile(r"^en/[^/]+/(.+)$")

# Pre-restructure docs lived at flat paths like /notes/python-typing.html or
# /appendix/python-walrus.html. The 2024-2026 reorg moved them under section
# subdirectories (e.g. /notes/basic/python-typing.html), but Google still
# indexes the legacy URLs. Map them explicitly to the current location.
_LEGACY_FLAT_REDIRECTS = {
    "notes/python-basic.html": "notes/basic/python-basic.html",
    "notes/python-dict.html": "notes/basic/python-dict.html",
    "notes/python-func.html": "notes/basic/python-func.html",
    "notes/python-future.html": "notes/basic/python-future.html",
    "notes/python-generator.html": "notes/basic/python-generator.html",
    "notes/python-heap.html": "notes/basic/python-heap.html",
    "notes/python-list.html": "notes/basic/python-list.html",
    "notes/python-object.html": "notes/basic/python-object.html",
    "notes/python-rexp.html": "notes/basic/python-rexp.html",
    "notes/python-set.html": "notes/basic/python-set.html",
    "notes/python-typing.html": "notes/basic/python-typing.html",
    "notes/python-unicode.html": "notes/basic/python-unicode.html",
    "notes/python-date.html": "notes/os/python-date.html",
    "notes/python-io.html": "notes/os/python-io.html",
    "notes/python-os.html": "notes/os/python-os.html",
    "notes/python-socket.html": "notes/network/python-socket.html",
    "notes/python-ssh.html": "notes/network/python-ssh.html",
    "notes/python-sqlalchemy.html": ("notes/database/python-sqlalchemy.html"),
    "notes/python-asyncio.html": ("notes/asyncio/python-asyncio-guide.html"),
    "notes/python-concurrency.html": "notes/concurrency/index.html",
    "notes/python-c-extensions.html": (
        "notes/extension/python-cext-modern.html"
    ),
    "notes/python-security.html": ("notes/security/python-vulnerability.html"),
    "notes/security/python-security.html": (
        "notes/security/python-vulnerability.html"
    ),
    "appendix/python-walrus.html": "notes/appendix/python-walrus.html",
    "appendix/python-gdb.html": "notes/appendix/python-gdb.html",
    "appendix/python-concurrent.html": "notes/appendix/index.html",
    "appendix/python-asyncio.html": (
        "notes/asyncio/python-asyncio-guide.html"
    ),
    "notes/multitasking/index.html": "notes/concurrency/index.html",
    "notes/multitasking/python-asyncio.html": (
        "notes/asyncio/python-asyncio-guide.html"
    ),
    "notes/multitasking/python-concurrency.html": (
        "notes/concurrency/index.html"
    ),
    "notes/pytorch/pytorch.html": "notes/llm/pytorch.html",
    "notes/pytorch/distributed.html": "notes/llm/pytorch.html",
    "notes/pytorch/index.html": "notes/llm/index.html",
    "notes/pytorch/slurm.html": "notes/hpc/slurm.html",
    # Intermediate restructuring steps (container/ iteration/ string/ →
    # basic/, cryptography/ → security/, io/ → os/ or network/).
    "notes/container/index.html": "notes/basic/index.html",
    "notes/container/python-dict.html": "notes/basic/python-dict.html",
    "notes/container/python-heap.html": "notes/basic/python-heap.html",
    "notes/container/python-list.html": "notes/basic/python-list.html",
    "notes/container/python-set.html": "notes/basic/python-set.html",
    "notes/iteration/index.html": "notes/basic/index.html",
    "notes/iteration/python-generator.html": (
        "notes/basic/python-generator.html"
    ),
    "notes/string/index.html": "notes/basic/index.html",
    "notes/string/python-rexp.html": "notes/basic/python-rexp.html",
    "notes/string/python-unicode.html": "notes/basic/python-unicode.html",
    "notes/cryptography/index.html": "notes/security/index.html",
    "notes/cryptography/python-crypto.html": (
        "notes/security/python-crypto.html"
    ),
    "notes/cryptography/python-tls.html": "notes/security/python-tls.html",
    "notes/io/index.html": "notes/os/index.html",
    "notes/io/python-io.html": "notes/os/python-io.html",
    "notes/io/python-socket.html": "notes/network/python-socket.html",
    # python-socket lived briefly under os/ before moving to network/.
    "notes/os/python-socket.html": "notes/network/python-socket.html",
    # python-ssh lived briefly under security/ before moving to network/.
    "notes/security/python-ssh.html": "notes/network/python-ssh.html",
    # vllm/sglang split was later consolidated into generic llm-bench/serving.
    "notes/llm/distributed.html": "notes/llm/pytorch.html",
    "notes/llm/sglang-bench.html": "notes/llm/llm-bench.html",
    "notes/llm/sglang-serving.html": "notes/llm/llm-serving.html",
    "notes/llm/vllm-bench.html": "notes/llm/llm-bench.html",
    "notes/llm/vllm-serving.html": "notes/llm/llm-serving.html",
    # Nested appendix paths (the unprefixed appendix/* keys above cover the
    # original RTD-flat form; these handle the post-rename location).
    "notes/appendix/python-asyncio.html": (
        "notes/asyncio/python-asyncio-guide.html"
    ),
    "notes/appendix/python-concurrent.html": ("notes/concurrency/index.html"),
    "notes/appendix/python-decorator.html": "index.html",
    # c-extensions was renamed to cext-modern.
    "notes/extension/python-c-extensions.html": (
        "notes/extension/python-cext-modern.html"
    ),
    # Pages deleted without a direct replacement go to the root index so
    # Google drops them via a 301 chain instead of holding the 404s.
    "notes/python-aws.html": "index.html",
    "notes/python-cstyle.html": "index.html",
    "notes/python-code-style.html": "index.html",
    "notes/python-network.html": "notes/network/index.html",
    "notes/python-iterator.html": "notes/basic/python-generator.html",
    "notes/testing/index.html": "index.html",
    "notes/testing/python-tests.html": "index.html",
}


def _resolve_legacy_flat_target(path):
    """Return the nested URL for a known legacy flat path, or None."""
    return _LEGACY_FLAT_REDIRECTS.get(path)


def find_key(token):
    """Find the key from the environment variable."""
    if token == os.environ.get("ACME_TOKEN"):
        return os.environ.get("ACME_KEY")
    for k, v in os.environ.items():
        if v == token and k.startswith("ACME_TOKEN_"):
            n = k.replace("ACME_TOKEN_", "")
            return os.environ.get("ACME_KEY_{}".format(n))


csp = {
    "default-src": "'none'",
    "style-src": ["'self'", "'unsafe-inline'"],
    "script-src": [
        "'self'",
        "*.cloudflare.com",
        "*.cloudflareinsights.com",
        "*.googletagmanager.com",
        "*.google-analytics.com",
        "*.carbonads.com",
        "*.carbonads.net",
        "cdn.carbonads.com",
        "srv.carbonads.net",
        "'unsafe-inline'",
        "'unsafe-eval'",
    ],
    "connect-src": [
        "'self'",
        "*.google-analytics.com",
        "*.analytics.google.com",
        "analytics.google.com",
        "*.googletagmanager.com",
        "*.carbonads.com",
        "*.carbonads.net",
        "*.doubleclick.net",
    ],
    "font-src": "'self'",
    "form-action": "'self'",
    "base-uri": "'self'",
    "img-src": "*",
    "frame-src": ["ghbtns.com", "*.carbonads.com", "*.carbonads.net"],
    "frame-ancestors": "'none'",
    "object-src": "'none'",
}

feature_policy = {"geolocation": "'none'"}

app = Flask(__name__, template_folder=ROOT)
app.config["SECRET_KEY"] = os.urandom(16)
app.config["SESSION_COOKIE_NAME"] = "__Secure-session"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["CSRF_COOKIE_NAME"] = "__Secure-csrf-token"
app.config["CSRF_COOKIE_HTTPONLY"] = True
app.config["CSRF_COOKIE_SECURE"] = True
csrf = SeaSurf(app)
talisman = Talisman(
    app,
    force_https=False,
    content_security_policy=csp,
    feature_policy=feature_policy,
)

if "DYNO" in os.environ:
    sslify = SSLify(app, permanent=True, skips=[".well-known"])


@app.errorhandler(404)
def page_not_found(e):
    """Redirect to 404.html."""
    return render_template("404.html"), 404


@app.before_request
def redirect_canonical_host():
    """301 pythonsheets.com to the canonical www.pythonsheets.com origin."""
    host = (request.host or "").lower()
    if host == "pythonsheets.com" or host.startswith("pythonsheets.com:"):
        url = "{0}://www.{1}{2}".format(request.scheme, host, request.path)
        if request.query_string:
            url += "?" + request.query_string.decode("latin-1")
        return redirect(url, code=301)


@app.before_request
def redirect_legacy_rtd_paths():
    """301 legacy /en/<slug>/... RTD URLs to flat canonical paths."""
    match = _LEGACY_RTD_PATH.match(request.path.lstrip("/"))
    if match:
        return redirect("/" + match.group(1), code=301)


@app.before_request
def redirect_legacy_flat_paths():
    """301 pre-restructure flat URLs to their current nested locations."""
    target = _resolve_legacy_flat_target(request.path.lstrip("/"))
    if target:
        return redirect("/" + target, code=301)


@app.route("/<path:path>")
def static_proxy(path):
    """Find static files safely."""
    try:
        return send_from_directory(ROOT, path)
    except NotFound:
        # Handle file not found or directory errors
        return render_template("404.html"), 404


@app.route("/")
def index_redirection():
    """Redirecting index file."""
    return send_from_directory(ROOT, "index.html")


@csrf.exempt
@app.route("/.well-known/acme-challenge/<token>")
def acme(token):
    """Find the acme-key from environment variable."""
    key = find_key(token)
    if key is None:
        abort(404)
    return key


if __name__ == "__main__":
    # Only run the app in debug mode during development
    app.run(debug=os.environ.get("FLASK_ENV") == "development")
