# OpenAEC Blueprint C library

The design tokens and the 945 B2 icons of OpenAEC UI 0.4, for tools in any language that can call C.

- `include/openaec_blueprint.h`: the six functions.
- `lib/`: the shared library (`openaec_blueprint.dll` with `openaec_blueprint.dll.lib`, `libopenaec_blueprint.dylib`, or `libopenaec_blueprint.so`) and a static library.
- `examples/list_icons.c`: prints the version and the first icons.

Every string the library returns is UTF-8, ends with NUL and stays valid for the life of the program; never free it.

Build the example on Linux or macOS:

```bash
cc -Iinclude examples/list_icons.c -Llib -lopenaec_blueprint -Wl,-rpath,lib -o list_icons
./list_icons
```

The library is LGPL-3.0-only. The licence of the B2 icons is still being decided: https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/15
