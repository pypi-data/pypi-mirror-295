<div align="center">
  <h1>Commitizen Espressif style plugin </h1>
    Commitizen tools plugin with Espressif code style
  <br>
  <br>

[![Release][release-badge]][release-url] [![Pre-commit][pre-commit-badge]][pre-commit-url] [![Conventional Commits][conventional-badge]][conventional-url]

</div>
<hr>

- [Introduction](#introduction)
- [Install](#install)
  - [Build Changelog](#build-changelog)
  - [Bump Release version](#bump-release-version)
  - [Write commit message](#write-commit-message)
  - [Example](#example)
- [Configuration](#configuration)
  - [Minimal setup](#minimal-setup)
  - [Optimal setup](#optimal-setup)
  - [Additional configurable parameters](#additional-configurable-parameters)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This is a plugin for Commitizen that makes it easy to create and maintain a well-organized and good-looking `CHANGELOG.md`.

It also takes care of version bumping and helps you write commit messages that follow Espressif standards.

All of this with minimal config and setup, so your `pyproject.toml` file stays clean and simple.

---

## Install

Of course, you have already created and activated a Python virtual environment... then:

```sh
pip install czespressif
```

.... and add snippet from [Minimal setup](#minimal-setup) - that's it 🤝.

You can also add it to your project `dev` dependencies (suggested) and run the sync command (`pipenv sync`, `pip-sync`, `poetry install`, ...).

Commitizen itself is in the plugin's dependencies, so pip will take care of everything.

> \[!WARNING\]
> Don't try to install it system-wide with `pipx`.
>
> This is a plugin, and that's probably not going to work as you expect.

### Build Changelog

If a changelog already exists in your project, make sure you have staged or committed its latest version.

This command turns your old changelog into a nicely organized template based on the Keep Changelog standard.

```sh
cz changelog
```

### Bump Release version

Is better to first run:

```sh
cz bump --dry-run
```

This only shows the future version and the part of the changelog that will be updated. When all ok, do the same without `--dry-run` flag.

### Write commit message

In case anyone actually prefers this way of creating commit messages, the command:

```sh
cz commit
```

in this plugin is aligned with the Espressif commit linter and DangerJS linters. You can give it a try...

```
? Select the type of change you are committing (Use arrow keys)
 » feat                     ✨ A new feature
   fix                      🐛 A bug fix
   change                   🏗️ A change made to the codebase.
   docs                     📖 Documentation only change
   test                     🚦  Adding missing or correcting existing tests
   ci                       ⚙️ Changes to CI configuration files and scripts
   refactor                 🔧 A changeset neither fixing a bug nor adding a feature
   revert                   🔙 Revert one or more commits
   remove                   🗑️ Removing code or files
```

### Example

If you are unsure about the commit message standard, hit:

```sh
cz example

```

This will bring up a complete example of good commit messages and commit schema in the terminal.

---

## Configuration

Config is accepted in `pyproject.toml` (priority, following example), `.cz.toml`, `.cz.json`, `cz.json`, `.cz.yaml`, `cz.yaml`, and `cz.toml`.

### Minimal setup

> \[!TIP\]
> Try to be minimalistic with custom configs. The best approach is to keep the defaults, so all Espressif projects maintain the same look and feel.
> Also, you will save yourself troubles with non-standard setups.

```ini
[tool.commitizen]
   name            = "czespressif"
   bump_message    = 'change(bump): release $current_version → $new_version [skip-ci]'
```

### Optimal setup

```ini
[tool.commitizen]
  name            = "czespressif"
  bump_message    = 'change(bump): release $current_version → $new_version [skip-ci]'

  # see commitizen docs, following are standard configs
  annotated_tag = true
  changelog_merge_prerelease = true
  tag_format = "v$version"
  update_changelog_on_bump = true

```

### Additional configurable parameters

```ini
[tool.commitizen]
    ...
    changelog_title = "Our changelog"  # custom text of changelog title
    changelog_header = "This is our changelog.\nAll cool things we do are here.\n\nPlease read it."  # custom text of changelog header
    changelog_footer = "This is the end of our changelog.\n\nMore cool things are coming."  # custom text of changelog footer
    changelog_section_line = false  # default (true); false = removes horizontal lines between releases
    changelog_unreleased = false  # default (true); false = removes section Unreleased, keeps only releases

    change_type_order = [  # in which order sections goes in changelog; if you use emojis include them
        '🏗️ Changes',
        '🐛 Bug fixes',
        '🚨 Breaking changes',
        '✨ New features',
        '📖 Documentation',
        '🗑️ Removals',
        '🎨 Code Style',
    ]
    change_type_map = # dependent on mapping in default types, only types with "changelog = True"
    types_in_changelog = ["feat", "fix", "refactor", "style", "ci"] # redefine which types are shown in changelog

    use_emoji = false  # default (true); false = removes emojis from changelog and commit UI (emojis are never added in the commit messages)

    [[tool.commitizen.extra_types]]  # add extra types for 'cz commit' and changelog
        type        = "style"
        heading     = "Code Style"
        emoji       = "🎨"
        description = "Changes that do not affect the meaning of the code (white-space, formatting, etc.)"
        bump        = "PATCH"
        changelog   = true
```

---

## Contributing

We welcome contributions from the community! Please read the [Contributing Guide](CONTRIBUTING.md) to learn how to get involved.

## License

This repository is licensed under the [Apache 2.0 License](LICENSE).

---

<!-- GitHub Badges -->

[conventional-badge]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
[conventional-url]: https://conventionalcommits.org
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[release-badge]: https://img.shields.io/github/v/release/espressif/cz-plugin-espressif
[release-url]: https://github.com/espressif/cz-plugin-espressif/releases
