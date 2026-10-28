# community-plugins

Community maintained [proto](https://moonrepo.dev/proto) plugins for third-party tools, written
in the [non-WASM TOML format](https://moonrepo.dev/docs/proto/non-wasm-plugin).

Every plugin lives in [`tools/`](./tools) as a single `<tool>.toml` file, and each one is
install-tested against Linux, macOS, and Windows in CI.

## Usage

Add a plugin to your `.prototools`:

```shell
proto plugin add biome "https://raw.githubusercontent.com/moonrepo/community-plugins/master/tools/biome.toml"
```

Or by hand:

```toml
[plugins.tools]
biome = "https://raw.githubusercontent.com/moonrepo/community-plugins/master/tools/biome.toml"
```

Then install as usual:

```shell
proto install biome
```

## Available tools

| Tool                                             | Description                                                                       |
| :----------------------------------------------- | :-------------------------------------------------------------------------------- |
| [act](./tools/act.toml)                           | Run your GitHub Actions locally.                                                   |
| [actionlint](./tools/actionlint.toml)             | Static checker for GitHub Actions workflow files.                                  |
| [atmos](./tools/atmos.toml)                       | Orchestration for Terraform, Helmfile, and other DevOps workflows.                 |
| [bazel](./tools/bazel.toml)                       | A fast, scalable, multi-language and extensible build system.                      |
| [biome](./tools/biome.toml)                       | A performant toolchain for web projects.                                           |
| [caddy](./tools/caddy.toml)                       | Fast and extensible multi-platform HTTP/1-2-3 web server with automatic HTTPS.     |
| [cmake](./tools/cmake.toml)                       | A cross-platform, open-source build system generator.                              |
| [cosign](./tools/cosign.toml)                     | Code signing and transparency for containers and binaries.                         |
| [dagger](./tools/dagger.toml)                     | Programmable CI/CD engine that runs your pipelines in containers.                  |
| [dprint](./tools/dprint.toml)                     | A pluggable and configurable code formatting platform written in Rust.             |
| [flyctl](./tools/flyctl.toml)                     | A command-line interface for fly.io.                                               |
| [gitleaks](./tools/gitleaks.toml)                 | A fast, light-weight, portable secret scanner for Git repositories.                |
| [grain](./tools/grain.toml)                       | A strongly-typed functional language that compiles to WebAssembly.                 |
| [gum](./tools/gum.toml)                           | A tool for glamorous shell scripts.                                                |
| [hurl](./tools/hurl.toml)                         | Runs HTTP requests defined in a simple plain text format.                          |
| [hyperfine](./tools/hyperfine.toml)               | A command-line benchmarking tool.                                                  |
| [infisical](./tools/infisical.toml)               | The CLI for the open source secret management platform Infisical.                  |
| [jira](./tools/jira.toml)                         | An interactive command line tool for Atlassian Jira.                               |
| [just](./tools/just.toml)                         | A handy way to save and run project-specific commands.                             |
| [mage](./tools/mage.toml)                         | A make/rake-like build tool using Go.                                              |
| [mkcert](./tools/mkcert.toml)                     | Zero-config locally trusted development certificates.                              |
| [ninja](./tools/ninja.toml)                       | A small build system with a focus on speed.                                        |
| [octopus](./tools/octopus.toml)                   | Command line interface for Octopus Deploy.                                         |
| [oxlint](./tools/oxlint.toml)                     | A JavaScript linter that needs no configuration by default.                        |
| [pixi](./tools/pixi.toml)                         | A fast package management tool for the conda ecosystem.                            |
| [pulumi](./tools/pulumi.toml)                     | Infrastructure as code in any programming language.                                |
| [rattler-build](./tools/rattler-build.toml)       | A fast Conda package builder.                                                      |
| [ruff](./tools/ruff.toml)                         | An extremely fast Python linter and code formatter.                                |
| [shellcheck](./tools/shellcheck.toml)             | A static analysis tool for shell scripts.                                          |
| [shfmt](./tools/shfmt.toml)                       | A shell formatter for POSIX Shell, Bash and mksh.                                  |
| [task](./tools/task.toml)                         | A task runner / build tool that aims to be simpler than GNU Make.                  |
| [traefik](./tools/traefik.toml)                   | A modern HTTP reverse proxy and load balancer for microservices.                   |
| [trufflehog](./tools/trufflehog.toml)             | Find and verify credentials.                                                       |
| [watchexec](./tools/watchexec.toml)               | Executes commands in response to file modifications.                               |
| [wizer](./tools/wizer.toml)                       | The WebAssembly pre-initializer.                                                   |

## Contributing a plugin

Add a `tools/<id>.toml` file. The file name is the tool's ID, and unless you override it, it is
also the name proto expects the installed executable to have.

The available fields are documented under
[non-WASM plugins](https://moonrepo.dev/docs/proto/non-wasm-plugin), with the schema itself
defined in
[`internal-schema/src/schema.rs`](https://github.com/moonrepo/plugins/blob/master/tools/internal-schema/src/schema.rs).
Unknown keys are silently ignored rather than rejected, so a typo fails quietly at install time —
worth a second look before opening a pull request.

### The `[plugin]` section

Unique to this repository, and ignored by proto. It supplies the metadata used to list the tool
in the [proto registry](https://github.com/moonrepo/proto/tree/master/registry):

```toml
[plugin]
description = "A performant toolchain for web projects."
homepage-url = "https://biomejs.dev/"
repository-url = "https://github.com/biomejs/biome"
```

`repository-url` points at the tool's own source repository. Omit `homepage-url` when it would
be identical to `repository-url`.

### Conventions

- **Declare `archs` on every platform.** Without it an unsupported architecture fails with a
  download 404 instead of a clear "unsupported architecture" error. List only what upstream
  actually publishes.
- **Check the archive layout.** If the binary sits inside a directory, set `archive-prefix`; if
  it sits in a subdirectory such as `bin/`, set `exe-path`. These commonly differ between the
  Unix tarball and the Windows zip for the same release.
- **Add a `[platform.freebsd]` section when upstream ships BSD builds.** proto falls back to the
  `linux` entry for BSD hosts, which otherwise hands them a Linux binary.
- **Block self-updating tools** with `[metadata] self-upgrade-commands`, so the tool cannot
  replace the binary proto is managing.
- **Only add `checksum-url` if upstream publishes checksums for the whole version range you
  support.** A missing checksum file is a hard install error, not a warning.
- **Anchor `version-pattern`.** Patterns are matched unanchored, so in a monorepo an
  unanchored pattern will happily match another product's tags.
- Prefer `exe-path` over the deprecated `bin-path`, and `[install.exes.*]` over the deprecated
  `[install.primary]` / `[install.secondary]`.

Upstream projects rename release assets and retag more often than you would expect. Verify
against a real release rather than assuming the existing file is still correct.

## Testing

[`test-changed-plugins.yml`](./.github/workflows/test-changed-plugins.yml) runs on pull requests
and tests only the plugins the pull request touched.
[`test-plugins.yml`](./.github/workflows/test-plugins.yml) tests everything on push to `master`,
or on demand. Both build their job matrix with the same script and hand it to the shared
[`install-plugins.yml`](./.github/workflows/install-plugins.yml), which installs one plugin per
job and then runs `proto bin` to confirm the executable was actually located — `proto install`
alone only warns when it cannot find the binary it just unpacked.

Platform coverage comes from each plugin's own `archs` lists, so a tool is never scheduled on a
runner it does not claim to support. To preview the plan:

```shell
# Everything
./scripts/plan-install-matrix.py

# Just what you changed
./scripts/plan-install-matrix.py biome ruff
```

To try a plugin locally before opening a pull request:

```shell
proto plugin add biome "file://./tools/biome.toml"
proto install biome
proto bin biome
```
