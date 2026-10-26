<!--
README template for an OpenAEC tool. Copy this file to the root of the tool's
repository as README.md, replace everything between <angle brackets>, and
delete sections that do not apply. Keep the order: people read the top first.
Write it in English, like the rest of a tool repository.
-->

<p align="center">
  <img src="docs/icon.png" alt="" width="96">
</p>

<h1 align="center">Open &lt;Name&gt; Studio</h1>

<p align="center">
  &lt;One sentence: what the tool does, for whom.&gt;
</p>

<p align="center">
  <a href="https://github.com/OpenAEC-Foundation/&lt;repo&gt;/releases/latest"><img src="https://img.shields.io/github/v/release/OpenAEC-Foundation/&lt;repo&gt;?style=flat-square&color=D97706" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-LGPL--3.0-D97706?style=flat-square" alt="License"></a>
</p>

![Open <Name> Studio](docs/screenshot.png)

## Install

The easiest way is the [OpenAEC Installer](https://github.com/OpenAEC-Foundation/openaec-installer): it installs, updates and starts every OpenAEC tool.

Or download the file for your system from the [latest release](https://github.com/OpenAEC-Foundation/<repo>/releases/latest):

| System | File |
| --- | --- |
| Windows 10 and 11 | `<repo>_<version>_x64-setup.exe` |
| macOS 11 and later | `<repo>_<version>_macos-universal.dmg` |
| Ubuntu, Linux Mint | `<repo>_<version>_amd64.deb` |
| Fedora | `<repo>_<version>_x86_64.rpm` |
| Any Linux | `<repo>_<version>_amd64.AppImage` |
| Snap Store | `sudo snap install <repo>` |

Every release is signed: Windows with an Authenticode signature, macOS with a Developer ID and notarized by Apple, Linux with the OpenAEC OpenPGP key and a build attestation. `SHA256SUMS` checks all files at once.

## What it does

- <The three to six things a user does with it, one line each.>

## Versions

Versions follow the OpenAEC scheme `YYYY.W.N`: year, ISO week without a leading zero, and a number within the week that starts at 0. The release of the first build in week 44 of 2026 is `2026.44.0`, its tag `v2026.44.0`.

## For developers

```bash
git clone https://github.com/OpenAEC-Foundation/<repo>.git
cd <repo>
<install command>
<run command>
<test command>
```

- Shared look and icons: [OpenAEC Blueprint](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint).
- AI and automation: <the MCP server and API, or "not yet">.
- Open file format: <IFC/IFCX use, or "not applicable">.
- Agreements for people and AI assistants working in this repository: [`AGENTS.md`](AGENTS.md).

## Contributing

Report a problem or an idea as an [issue](https://github.com/OpenAEC-Foundation/<repo>/issues). Describe what you did, what you expected and what happened.

## License

<License>, see [`LICENSE`](LICENSE). Part of the [OpenAEC Foundation](https://github.com/OpenAEC-Foundation): free and open-source tools for the built environment.
