<!--
README template for an OpenAEC tool, after the README of Open Planner Studio.
The requirements are in README-standaard.md next to this file.

1. Copy this file to the root of the tool's repository as README.md.
2. Replace everything between <angle brackets>. Delete a section that does not
   apply rather than leaving it empty. Keep the order.
3. Make README.nl.md with the same structure in Dutch.
4. Put the images in docs/images/readme/ (PNG, at most 150 kB each), made by a
   script in the repository so they can be made again.
Delete this comment.
-->

**English** · [Nederlands](README.nl.md)

<div align="center">

# Open &lt;Name&gt; Studio

**&lt;One sentence: what it is and what sets it apart.&gt;**

[![Release](https://img.shields.io/github/v/release/OpenAEC-Foundation/<repo>?label=release&color=D97706)](https://github.com/OpenAEC-Foundation/<repo>/releases/latest)
[![CI](https://github.com/OpenAEC-Foundation/<repo>/actions/workflows/<ci>.yml/badge.svg)](https://github.com/OpenAEC-Foundation/<repo>/actions/workflows/<ci>.yml)
[![License](https://img.shields.io/github/license/OpenAEC-Foundation/<repo>)](#license)

### [Try in your browser](<web url>) &nbsp;·&nbsp; [Download](https://github.com/OpenAEC-Foundation/<repo>/releases/latest)

![<What the image shows>](docs/images/readme/<demo.gif or hero.png>)

</div>

Open &lt;Name&gt; Studio is &lt;what it is, for whom&gt;. &lt;What it does, in one or two sentences.&gt;

It runs &lt;in your browser with nothing to install, or&gt; as a desktop app on Windows, macOS and Linux.

## Try it

**[Open the browser version](<web url>)**. &lt;What the user sees first and can do right away.&gt;

## Download

Every release is on the [releases page](https://github.com/OpenAEC-Foundation/<repo>/releases/latest). The easiest way is the [OpenAEC Installer](https://github.com/OpenAEC-Foundation/openaec-installer): it installs, updates and starts every OpenAEC tool.

| Platform | Installer |
|----------|-----------|
| **Windows** | `.exe` installer (x64) |
| **macOS** | `.dmg` (universal: Apple silicon and Intel) |
| **Linux** | `.deb`, `.rpm`, `.AppImage` |

&lt;How updates work.&gt; Every file is signed: Windows with Authenticode, macOS with a Developer ID and notarized by Apple, Linux with the OpenAEC OpenPGP key and a build attestation.

## Why use it?

- **Free and open.** &lt;License&gt;. No licence fees, no account, no lock-in.
- **Open formats.** &lt;IFC or IFCX use&gt;.
- **&lt;Strength&gt;.** &lt;One sentence.&gt;
- **&lt;Strength&gt;.** &lt;One sentence.&gt;

## Screenshots

| | |
|---|---|
| ![<alt>](docs/images/readme/<one>.png) **<Caption>** | ![<alt>](docs/images/readme/<two>.png) **<Caption>** |
| ![<alt>](docs/images/readme/<three>.png) **<Caption>** | ![<alt>](docs/images/readme/<four>.png) **<Caption>** |
| ![<alt>](docs/images/readme/<five>.png) **<Caption>** | ![<alt>](docs/images/readme/<six>.png) **<Caption>** |

<!-- Add rows as long as each image shows something new. -->

## &lt;Main feature&gt;

- **&lt;Capability&gt;.** &lt;What it does, with a link to the documentation.&gt;

<!-- Screenshots that explain this feature, not repeated from the gallery. Delete if none. -->

| | |
|---|---|
| ![<alt>](docs/images/readme/<feature-one>.png) **<Caption>** | ![<alt>](docs/images/readme/<feature-two>.png) **<Caption>** |

## Interoperability

| Format | Open | Save / export |
|--------|------|---------------|
| **IFC** | &lt;Yes / No&gt; | &lt;Yes / No&gt; |

&lt;What does not survive each format.&gt;

## MCP

&lt;What the MCP server can do, what the user controls, and where it runs. Or delete this section.&gt;

## Testing and reliability

- **&lt;Count&gt; &lt;kind of tests&gt;** in `<path>`. &lt;What they prove.&gt;

Count sources: &lt;the files the numbers above come from&gt;.

## Current limitations

- **&lt;What does not work yet.&gt;** &lt;Explanation.&gt;

Found something? [Open an issue](https://github.com/OpenAEC-Foundation/<repo>/issues).

## Under the hood

&lt;The technique in one paragraph.&gt; The shared look and icons come from [OpenAEC Blueprint](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint).

## Contributing

- **Try it on a real project** and report bugs or missing features as an [issue](https://github.com/OpenAEC-Foundation/<repo>/issues/new). Describe what you did, what you expected and what happened.
- **Write code.** Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md), and open a pull request.

## Quick start (developers)

```bash
git clone https://github.com/OpenAEC-Foundation/<repo>.git
cd <repo>
<install command>
<run command>
```

Requires &lt;Node, Rust or Python versions&gt;.

Versions follow the OpenAEC scheme `YYYY.W.N`: year, ISO week without a leading zero, and a number within the week that starts at 0, such as `2026.44.0`.

Open &lt;Name&gt; Studio is part of the [OpenAEC Foundation](https://github.com/OpenAEC-Foundation) family of apps.

## License

&lt;License&gt;. See [LICENSE](LICENSE).

## Trademarks

&lt;Only when the README names products of others: Open &lt;Name&gt; Studio is an independent project and is not affiliated with, endorsed by or sponsored by them. Or delete this section.&gt;
