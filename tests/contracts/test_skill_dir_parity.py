"""The two tracked skill directories must not drift apart.

`.agents/skills/` is a read-only mirror of upstream calesthio/OpenMontage.
`.claude/skills/` is the directory Claude Code loads natively. 62 skills exist
in both, and on 2026-09-04 two of them had silently diverged:

- `elevenlabs`: the `.claude/` copy was 4 months stale (March vs August) and
  lacked the whole "OpenMontage provider routing" section — so the agent was
  reading an instruction that did not know about `fal_elevenlabs_tts` and still
  implied asking the user for a `.env` credential.
- `ai-video-gen`: the `.claude/` copy was missing the Kling Official path.

A stale skill is worse than a missing one: the agent follows it instead of
questioning it. Nothing surfaced either drift, so this test does.

When a difference is intentional, sync the copies and put the local edit in the
upstream-facing copy, or add the skill to INTENTIONALLY_DIVERGENT below with a
comment saying why. Do not silence a whole directory without a reason.
"""

from __future__ import annotations

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_MIRROR = REPO_ROOT / ".agents" / "skills"
NATIVE_DIR = REPO_ROOT / ".claude" / "skills"

# skill name -> why the two copies are allowed to differ
INTENTIONALLY_DIVERGENT: dict[str, str] = {}


def _shared_skill_names() -> list[str]:
    if not UPSTREAM_MIRROR.is_dir() or not NATIVE_DIR.is_dir():
        return []
    mirrored = {p.name for p in UPSTREAM_MIRROR.iterdir() if p.is_dir()}
    native = {p.name for p in NATIVE_DIR.iterdir() if p.is_dir()}
    return sorted(mirrored & native)


def _differing_files(left: Path, right: Path) -> list[str]:
    """Every path under both trees whose contents differ, or which is missing."""
    comparison = filecmp.dircmp(str(left), str(right))
    found: list[str] = []

    def walk(node: filecmp.dircmp, prefix: str) -> None:
        for name in node.diff_files:
            found.append(f"{prefix}{name} (contents differ)")
        for name in node.left_only:
            found.append(f"{prefix}{name} (only in .agents/skills)")
        for name in node.right_only:
            found.append(f"{prefix}{name} (only in .claude/skills)")
        for name in node.funny_files:
            found.append(f"{prefix}{name} (unreadable)")
        for name, sub in node.subdirs.items():
            walk(sub, f"{prefix}{name}/")

    walk(comparison, "")
    return sorted(found)


def test_shared_skills_are_identical_in_both_tracked_directories() -> None:
    shared = _shared_skill_names()
    assert shared, (
        "found no skill present in both .agents/skills and .claude/skills — "
        "either a directory moved or this test is pointed at the wrong paths"
    )

    drifted: dict[str, list[str]] = {}
    for name in shared:
        if name in INTENTIONALLY_DIVERGENT:
            continue
        differences = _differing_files(UPSTREAM_MIRROR / name, NATIVE_DIR / name)
        if differences:
            drifted[name] = differences

    if drifted:
        report = "\n".join(
            f"  {name}:\n" + "\n".join(f"    - {d}" for d in diffs)
            for name, diffs in sorted(drifted.items())
        )
        raise AssertionError(
            f"{len(drifted)} skill(s) differ between the two tracked skill "
            f"directories:\n{report}\n\n"
            "The agent loads .claude/skills/, so a stale copy there is an "
            "instruction it will follow. Sync the copies (usually "
            "`cp -r .agents/skills/<name> .claude/skills/<name>`, since "
            ".agents/skills mirrors upstream), or record the exception in "
            "INTENTIONALLY_DIVERGENT in this file with a reason."
        )


def test_intentional_divergences_are_still_shared_skills() -> None:
    """An allowlist entry for a skill that no longer exists is dead weight."""
    shared = set(_shared_skill_names())
    stale = sorted(set(INTENTIONALLY_DIVERGENT) - shared)
    assert not stale, (
        f"INTENTIONALLY_DIVERGENT lists skill(s) that are no longer in both "
        f"directories: {stale}. Remove the entries."
    )
