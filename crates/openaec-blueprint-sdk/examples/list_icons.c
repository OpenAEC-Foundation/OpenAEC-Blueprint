/* Lists the version, the number of icons and the first five icons.
 * Ends with code 1 when something is missing. */
#include <stdio.h>
#include <string.h>
#include "openaec_blueprint.h"

int main(void) {
    const char *version = oa_version();
    size_t count = oa_icon_count();
    printf("OpenAEC Blueprint %s, %zu icons\n", version, count);
    if (count == 0 || strlen(oa_tokens_json()) == 0) return 1;
    for (size_t i = 0; i < count && i < 5; i++) {
        const char *id = oa_icon_id(i);
        const char *svg = oa_icon_svg(id, 24);
        if (svg == NULL || strncmp(svg, "<svg", 4) != 0) return 1;
        printf("  %s  %s  (%zu bytes)\n", id, oa_icon_label(id), strlen(svg));
    }
    return oa_icon_svg("does.not-exist", 16) == NULL ? 0 : 1;
}
