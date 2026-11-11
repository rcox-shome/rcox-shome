# Reese Cox

I build native Mac apps and tools that keep work close at hand.

My projects range from a keyboard shortcut for generating a password to a spatial canvas for organizing notes and files. I'm interested in thoughtful desktop interactions, local storage, and the details that make a small tool useful every day.

### Selected work

| Project | What it does | Explore |
| :--- | :--- | :--- |
| **ChordShot** | Capture a region with a mouse chord or trackpad gesture. Press Space during selection to switch from a screenshot to a silent recording. | [Free Mac beta](https://github.com/rcox-shome/chordshot-releases) |
| **Nodetaker** | Organize notes, media, and connections on a spatial canvas, with a local Markdown vault. | [Overview & downloads](https://github.com/rcox-shome/nodetaker-releases) |
| **Password Anywhere** | Generate a password from a global shortcut, with native macOS integration and clipboard cleanup that preserves anything copied afterward. | [Source](https://github.com/rcox-shome/password-anywhere) |

[![A sample planning map in Nodetaker, with connected notes arranged on a spatial canvas](https://nodetakerapp.com/screens/hero-app.jpg)](https://github.com/rcox-shome/nodetaker-releases)

<sub>Nodetaker sample canvas, shown in the v0.2.0 beta interface.</sub>

### A few details worth exploring

- **Small, inspectable code.** Password Anywhere uses Swift, SwiftUI, and AppKit without third-party packages. Start with its [random-number generation](https://github.com/rcox-shome/password-anywhere/blob/main/PasswordAnywhere/PasswordGenerator/SecureRandom.swift) or [clipboard cleanup](https://github.com/rcox-shome/password-anywhere/blob/main/PasswordAnywhere/Clipboard/ClipboardManager.swift).
- **Interaction is part of the product.** ChordShot turns selection, capture, and recording into one gesture-driven workflow.
- **Files you can keep working with.** Nodetaker brings a visual workspace to notes stored as Markdown.

### Compare notes

I'd like to connect with people building Mac utilities, local-first applications, and thoughtful tools for everyday work.

Try [ChordShot](https://github.com/rcox-shome/chordshot-releases), share [beta feedback](https://github.com/rcox-shome/chordshot-releases/issues/new?template=beta-feedback.yml), or explore [Password Anywhere's contribution guide](https://github.com/rcox-shome/password-anywhere/blob/main/CONTRIBUTING.md).

<sub>Password Anywhere is open source. ChordShot and Nodetaker have public downloads; their application source remains private.</sub>
