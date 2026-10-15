# openaec-ui

Native Rust shell, theme tokens, typography, semantic icons and controls shared by OpenAEC desktop tools. Implement `Application` and call `run`, or use `frame::FrameSlots` from an existing Iced event loop.

`frame::status_bar` owns the shared 22 px status band, one-pixel top rule, theme colors and horizontal padding. An existing application supplies its own status cells and actions as an Iced `Element`; the same component is used by the Style Repo shell and Pointcloud Studio.

This package contains only the shared Rust implementation, six bundled fonts with their [separate license notices](NOTICE.md), and 22 canonical icons. Source icons collected for design research, unapproved FEM/BIM drafts and Style Repo screenshots live in the sibling `openaec-style-repo` application and are not included in this crate package.

The sibling Style Repo application documents the source inventory and the Pointcloud integration.
