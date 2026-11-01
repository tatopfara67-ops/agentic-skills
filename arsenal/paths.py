"""mythos-arsenal path configuration.

All state lives under MYTHOS_ARSENAL_ROOT (env override), defaulting to the
package parent directory. Nothing here is magic: three paths, one resolver.
"""
import os

_PKG_DIR = os.path.dirname(os.path.abspath(__file__))


def root() -> str:
    env = os.environ.get("MYTHOS_ARSENAL_ROOT")
    return os.path.abspath(env) if env else os.path.dirname(_PKG_DIR)


def scope_csv() -> str:
    env = os.environ.get("MYTHOS_ARSENAL_SCOPE")
    return env if env else os.path.join(root(), "scope.csv")


def engagements_dir() -> str:
    env = os.environ.get("MYTHOS_ARSENAL_ENGAGEMENTS")
    return env if env else os.path.join(root(), "engagements")


def skills_dir() -> str:
    env = os.environ.get("MYTHOS_ARSENAL_SKILLS")
    return env if env else os.path.join(root(), "skills")


def wordlists_dir() -> str:
    return os.path.join(_PKG_DIR, "wordlists")


def program_dir(program: str) -> str:
    safe = "".join(c for c in program if c.isalnum() or c in "-_.")
    return os.path.join(engagements_dir(), safe or "default")
