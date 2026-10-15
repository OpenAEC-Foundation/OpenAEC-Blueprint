# Geïmporteerde UI-iconen

Deze map bevat uitsluitend namen die als iconcomponent uit de onderzochte
OpenAEC-UI-broncode zijn geïmporteerd en na de import in code voorkomen.
`imported-ui-icons.json` onderscheidt directe JSX-tags van andere
identifierverwijzingen en bewaart de regelnummers op de vastgelegde commit.
`library-icon-index.json` in de bovenmap legt per SVG het pakket, de versie,
SHA-256 en de verwijzende bronbestanden vast. Een statische codeverwijzing
bewijst niet dat een icoon in iedere applicatietoestand zichtbaar is.

Lucide-SVG's komen rechtstreeks uit `lucide-static`-npm-tarballs met dezelfde
versie als `lucide-react` in de betreffende tool. Solid Icons' `TbOutline*`
componenten zijn uit de SVG-inhoud van `solid-icons@1.2.0/tb/index.js` als
zelfstandige SVG gereconstrueerd. De npm-tarballs zijn met hun gepubliceerde
SHA-512-integriteit gecontroleerd. De originele pakketlicenties staan bij
iedere versie: Lucide ISC, Solid Icons MIT.

Dit is brononderzoek. De bestanden zijn nog geen definitieve OpenAEC-iconset.
