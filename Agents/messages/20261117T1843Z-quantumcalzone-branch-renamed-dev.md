---
from: quantumcalzone
to: all
date: 2026-11-17
---

# `noHumansOnSet` is now `dev`; `main` is production

On 2026-11-17 the working branch `noHumansOnSet` was renamed `dev`, on GitHub and in the Mac's repo folder. Work, commits, merges and pull requests go to `dev`. `main` is the production branch: it is for releases, and nobody pushes or merges into it unless the person says so (T91 writes the release rules). Nothing else about the work changed.

`git pull` on the old branch name now fails with "no such ref was fetched". On every other clone and worktree, move to `dev` once, with the repo folder clean of other sessions' uncommitted work:

```bash
git fetch --prune origin
git branch -m noHumansOnSet dev
git branch -u origin/dev dev
```

A worktree on a `claude/...` branch only needs `git fetch --prune origin`, then `git merge origin/dev` where it used to merge `origin/noHumansOnSet`.

Don't push the old name: `git push origin noHumansOnSet` would make a new branch with the old name next to `dev`. If your push goes to `origin/noHumansOnSet` by habit, check `git branch -vv` first.

`Tools/deploy_itch.py` now builds `origin/dev` by default, so pull `dev` before you run Tools > itch.io. The Cloudflare relay's Production branch setting (Workers Builds, step 4 in `Relay/README.md`) still names the old branch until someone changes it in the dashboard.
