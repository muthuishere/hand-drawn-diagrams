# Share this store with the team — the remote is YOUR script (delete me if unused)

`ctx-optimize remote push` / `remote pull` run the commands you declare in
config.json next to this file — the binary ships no transport of its own:

    "remote": {
      "push": "node .ctxoptimize/push.js",
      "pull": "node .ctxoptimize/pull.js"
    }

Any shell line works — `node x.js`, `python3 y.py`, `sh z.sh`, or inline
(`rsync -a ... && git -C ... push`). Commit the scripts and the config;
teammates clone and a bare `ctx-optimize remote pull` just works.

Your command receives the store context in env:

    CTX_STORE_DIR     local store tree (push: source · pull: destination, pre-created)
    CTX_STORE_KEY     the store's key under ~/ctxoptimize/  (here: hand-drawn-diagrams)
    CTX_SCOPE_PREFIX  module store-key segment when run inside a module, else empty
    CTX_DIRECTION     "push" or "pull" — one script can serve both

Exit non-zero to fail the verb. Secrets: env-var NAMES only — never
hardcode or print values, in scripts or config.

## Git lane (only needs git — recommended)

`push.js.sample` + `pull.js.sample` in this directory are a complete,
zero-dependency implementation: a git repo (e.g. a private
`your-org/ctx-stores` on GitHub) hosts every store; push copies the tree in
and commits, pull clones/pulls and copies it out. Arm them:

    gh repo create your-org/ctx-stores --private     # once per team
    mv .ctxoptimize/push.js.sample .ctxoptimize/push.js
    mv .ctxoptimize/pull.js.sample .ctxoptimize/pull.js
    # set STORE_REPO_URL in both, add the "remote" block above to config.json, commit

Store artifacts are sorted ndjson — git diffs and merges them cleanly.

## S3 lane (AWS, R2, MinIO, Hetzner — needs the aws CLI)

One script serves both directions via CTX_DIRECTION — save as
`.ctxoptimize/s3sync.js` and declare it for both push and pull:

    #!/usr/bin/env node
    const { execFileSync } = require("node:child_process");
    const S3_URL = "s3://your-bucket/ctx";  // store key is appended
    const dir = process.env.CTX_STORE_DIR, key = process.env.CTX_STORE_KEY;
    const remote = S3_URL + "/" + key;
    const [from, to] = process.env.CTX_DIRECTION === "push" ? [dir, remote] : [remote, dir];
    execFileSync("aws", ["s3", "sync", from, to, "--delete"], { stdio: "inherit" });

Credentials come from the standard `AWS_*` env vars / profiles; non-AWS
endpoints (R2, MinIO): set `AWS_ENDPOINT_URL` in your environment.

## Anything else (GCS, artifactory, rsync-over-ssh, corporate stores)

Write the script that copies `CTX_STORE_DIR` to/from your host and declare
it. The binary never cares what the transport is — it only runs your
command and hands it the env above.
