"""Leg iconen van Open Planner Studio op main (Lucide) vast als vergelijkingsmateriaal voor het overzichtsblad.

De SVG's in design/iconen/referentie/ops-main/ zijn geen onderdeel van de iconenset. Ze staan er alleen om
een nieuw icoon op ware grootte naast het icoon van main te kunnen zetten. Licentie: ISC, zie
LICENSE-lucide.txt in dezelfde map.

Gebruik (lucide-react uit een OPS-checkout met node_modules):
  python3 scripts/iconen_referentie_lucide.py <pad>/node_modules/lucide-react design/iconen/referentie/ops-main play calendar-clock ...
"""
import pathlib
import re
import sys


def load(icons: pathlib.Path, name: str):
    src = (icons / f'{name}.js').read_text(encoding='utf-8')
    alias = re.search(r"export \{ default \} from './([\w-]+)\.js'", src)
    if alias:
        return load(icons, alias.group(1))
    body = src.split('const __iconNode = ', 1)[1].split('\n];', 1)[0]
    return re.findall(r'"(\w+)",\s*\{([^}]*)\}', body)


def main():
    package, out, names = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:]
    icons = package / 'dist/esm/icons'
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        parts = []
        for tag, attrs in load(icons, name):
            kv = dict(re.findall(r'(\w+): "([^"]*)"', attrs))
            kv.pop('key', None)
            parts.append(f'<{tag} ' + ' '.join(f'{k}="{v}"' for k, v in kv.items()) + '/>')
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
               'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ''.join(parts) + '</svg>')
        (out / f'{name}.svg').write_text(svg, encoding='utf-8')
        print(name, len(parts))


if __name__ == '__main__':
    main()
