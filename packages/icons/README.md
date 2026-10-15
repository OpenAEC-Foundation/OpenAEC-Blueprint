# @openaec/icons

OpenAEC-iconen. Bron: [`design/icons/`](../../design/icons/) — voeg daar iconen toe,
niet hier. `src/generated/` wordt gemaakt door `npm run generate`.

```tsx
import { Icon, editUndo } from "@openaec/icons";

<Icon svg={editUndo} size={20} title="Ongedaan maken" />
```

Iconen zijn `currentColor`: ze nemen de tekstkleur van hun omgeving over.
Dynamisch op id opzoeken (bijv. vanuit een ribbon-definitie) kan via
`import { iconsById } from "@openaec/icons/by-id"`; dat laadt wel alle iconen.
