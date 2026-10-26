/*
 * OpenAEC Blueprint C library: design tokens and the B2 icons.
 *
 * Every string returned is UTF-8, ends with NUL and stays valid for the life
 * of the program; never free it. All functions are safe to call from any
 * thread. Licence: LGPL-3.0-only.
 */
#ifndef OPENAEC_BLUEPRINT_H
#define OPENAEC_BLUEPRINT_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* The version of the library, "YYYY.W.N", such as "2026.44.0". */
const char *oa_version(void);

/* All design tokens of UI 0.4 as one JSON document. */
const char *oa_tokens_json(void);

/* The number of icons. */
size_t oa_icon_count(void);

/* The id of the icon at index, alphabetical, such as "file.open";
 * NULL when index >= oa_icon_count(). */
const char *oa_icon_id(size_t index);

/* The Dutch label of an icon; NULL for an unknown id. */
const char *oa_icon_label(const char *id);

/* The SVG of an icon for a size in pixels: up to 18 px the 16 px master,
 * above that the 24 px master. Main colour currentColor, accent
 * var(--icon-accent, currentColor). NULL for an unknown id. */
const char *oa_icon_svg(const char *id, uint32_t pixels);

#ifdef __cplusplus
}
#endif

#endif /* OPENAEC_BLUEPRINT_H */
