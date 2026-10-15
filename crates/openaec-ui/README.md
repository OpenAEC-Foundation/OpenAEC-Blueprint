# openaec-ui

Native Rust shell, theme tokens, typography, semantic icons and controls shared by OpenAEC desktop tools. Implement `Application` and call `run`, or use `frame::FrameSlots` from an existing Iced event loop.

`frame::status_bar` owns the shared 22 px status band, one-pixel top rule, theme colors and horizontal padding. An existing application supplies its own status cells and actions as an Iced `Element`; the same component is used by the Style Repo shell and Pointcloud Studio.

`frame::document_bar` owns the 30 px document band from the pinned Tauri Style Book: the one-pixel top and bottom rules, theme background and 4 px horizontal inset. Applications keep their own tab identity and navigation behavior.

`widgets::document_tab_style` and `widgets::document_close_style` give those app-owned tabs the shared 24 px appearance and a legible close action. Pointcloud retains its middle-click, shortening, scrolling and keyboard behavior while using the same visual tab styles as the Style Repo.

`widgets::ribbon_group` owns the 94 px ribbon-group geometry from the pinned Tauri template: 4 px top inset, 8 px sides, a ruled 9 px caption and a right separator. Applications pass their actual tools and measured group width. Pointcloud keeps its adaptive collapse and domain actions; the Style Repo uses the same group around its catalogue commands.

`model::RibbonControl` adds typed ribbon inputs to `Command`: a slider, a two-thumb range, a compact stack of sliders, segmented choices, select lists, numeric text input, a color choice and a style gallery. Applications own the selected values and receive changes through their message type; `widgets::ribbon_control` draws the controls with the shared tokens. The range widget keeps both handles on one rail and supports mouse and touch dragging. Select lists accept application-owned labels, messages and width; slider stacks accept source-specific labels and icons within the same ribbon geometry. The color choice shows the current application color even when it came from a style preset outside the listed palette. `RibbonSwatch` carries a labelled color preview and application message, so the gallery contains no PDF-specific meaning. The gallery shows an application-selected number of tiles and provides an aligned popup for the full set.

`widgets::color_grid` renders an app-owned palette in vertical columns with keyboard-focusable color buttons and tooltips. `widgets::popover` and `widgets::popover_aligned` anchor arbitrary app content over the shell, moves it above the anchor when there is insufficient room below, and closes on an outside click. `RibbonCustomColor` lets an application supply a validated custom-color editor inside the same popup. The Style Repo uses them together in the PDF ribbon; a software-rendered pixel test checks all 42 source colors in their 7 × 6 arrangement, and an event test checks palette actions and outside-click dismissal.

`widgets::property_grid_row_with`, `property_grid_control_with`, and `property_section_with` provide the shared properties dock. Rows are 28 px high with aligned label and value columns and a bottom rule; section headers are 24 px high. Callers supply their own localized text, input controls and theme resolver. The Style Repo uses the static-theme wrappers for its right dock, while Pointcloud uses the resolver variants so theme changes update the live panel.

This package contains the shared Rust implementation, six bundled fonts with their [separate license notices](NOTICE.md), 26 canonical control icons, and four reviewed CAD/Pointcloud domain meanings with separate 16 px artwork. `icons::DomainIcon` keeps those commands distinct from the general `icons::Icon` set. Source icons collected for design research, unapproved FEM/BIM drafts and Style Repo screenshots live in the sibling `openaec-style-repo` application and are not included in this crate package.

The sibling Style Repo application documents the source inventory and the Pointcloud integration.
