#!/usr/bin/env python3
"""Check the fonts inside report PDFs against the OpenAEC font package (issue #26).

Usage:
  python scripts/check_report_pdf.py rapport.pdf [meer.pdf ...]
  python scripts/check_report_pdf.py --self-test

For every font in the PDF it reports whether the font is embedded, whether the
embedded data really is the font the PDF names (Open Calc Studio wrote "Inter"
but embedded Segoe UI), and whether it comes from the font package. Reads
uncompressed and Flate-compressed objects and object streams; no PDF library
needed.
"""

import re
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_font_package import FONTS, name_table  # noqa: E402

OBJECT = re.compile(rb"(\d+)\s+(\d+)\s+obj\b(.*?)\bendobj", re.S)
STREAM = re.compile(rb"^(.*?)\bstream\r?\n(.*?)\r?\n?endstream", re.S)


def package_names():
    """PostScript names of every file in the font package."""
    return {name_table(p.read_bytes()).get(6) for p in FONTS.glob("*.ttf")}


def decode(dictionary, data):
    if b"/FlateDecode" in dictionary:
        try:
            return zlib.decompress(data)
        except zlib.error:
            return None
    return data if b"/Filter" not in dictionary else None


def objects(pdf):
    """Returns {number: (dictionary bytes, decoded stream or None)}."""
    found = {}
    for match in OBJECT.finditer(pdf):
        number, body = int(match.group(1)), match.group(3)
        stream = STREAM.match(body)
        if stream:
            found[number] = (stream.group(1), decode(stream.group(1), stream.group(2)))
        else:
            found[number] = (body, None)
    # Objects packed in object streams (PDF 1.5).
    for dictionary, data in list(found.values()):
        if b"/ObjStm" not in dictionary or data is None:
            continue
        first = int(re.search(rb"/First\s+(\d+)", dictionary).group(1))
        count = int(re.search(rb"/N\s+(\d+)", dictionary).group(1))
        header = list(map(int, data[:first].split()))[: 2 * count]
        offsets = [(header[i], header[i + 1]) for i in range(0, len(header), 2)]
        for i, (number, offset) in enumerate(offsets):
            end = offsets[i + 1][1] if i + 1 < len(offsets) else len(data) - first
            found.setdefault(number, (data[first + offset: first + end], None))
    return found


def name(dictionary, key):
    match = re.search(rb"/" + key + rb"\s*/([^\s/\[\]<>()]+)", dictionary)
    return match.group(1).decode("latin-1") if match else None


def ref(dictionary, key):
    match = re.search(rb"/" + key + rb"\s+(\d+)\s+\d+\s+R", dictionary)
    return int(match.group(1)) if match else None


def check(pdf, allowed):
    """Returns (lines, ok) for one PDF's bytes."""
    found = objects(pdf)
    lines, ok = [], True
    described = set()
    for dictionary, _ in found.values():
        if not re.search(rb"/Type\s*/FontDescriptor", dictionary):
            continue
        font_name = name(dictionary, b"FontName") or "?"
        described.add(font_name)
        bare = font_name.split("+", 1)[-1]
        program = next((ref(dictionary, key) for key in (b"FontFile2", b"FontFile3", b"FontFile") if ref(dictionary, key)), None)
        if program is None:
            lines.append(f"  {bare}: niet ingesloten")
            ok = False
            continue
        data = found.get(program, (b"", None))[1]
        names = name_table(data) if data and data[:4] in (b"\x00\x01\x00\x00", b"true", b"OTTO") else {}
        inside = names.get(6)
        if inside is None:
            lines.append(f"  {bare}: ingesloten, naam in de fontdata niet te lezen")
        elif inside != bare:
            lines.append(f"  {bare}: FOUT, de PDF noemt {bare} maar sluit {inside} ({names.get(1, '?')}) in")
            ok = False
            continue
        if bare not in allowed:
            lines.append(f"  {bare}: ingesloten, maar niet uit het fontpakket")
            ok = False
        elif inside is not None:
            lines.append(f"  {bare}: in orde")
    for dictionary, _ in found.values():
        if not re.search(rb"/Type\s*/Font\b", dictionary):
            continue
        descriptor = ref(dictionary, b"FontDescriptor")
        if descriptor is not None:
            # TrueType data (FontFile2) under /Type1 is invalid and readers may refuse
            # it; Open Geotechniek Studio's pdf-writer backend writes this.
            if re.search(rb"/Subtype\s*/Type1\b", dictionary) and b"/FontFile2" in found.get(descriptor, (b"", None))[0]:
                lines.append(f"  {name(dictionary, b'BaseFont') or '?'}: FOUT, TrueType-data als /Type1-font beschreven")
                ok = False
            continue
        if b"/DescendantFonts" in dictionary:
            continue
        base = name(dictionary, b"BaseFont") or "?"
        if base not in described and b"/Type3" not in dictionary:
            lines.append(f"  {base}: niet ingesloten (standaardfont van de PDF-lezer)")
            ok = False
    return lines, ok


def fixture():
    """A small PDF with a correct, a mislabelled, a non-embedded and a mistyped font."""
    def ttf(file):
        data = (FONTS / file).read_bytes()
        packed = zlib.compress(data)
        return b"<< /Length %d /Filter /FlateDecode /Length1 %d >>\nstream\n" % (len(packed), len(data)) + packed + b"\nendstream"

    parts = [
        b"<< /Type /Font /Subtype /TrueType /BaseFont /AAAAAA+Inter-Regular /FontDescriptor 2 0 R >>",
        b"<< /Type /FontDescriptor /FontName /AAAAAA+Inter-Regular /FontFile2 3 0 R >>",
        ttf("Inter-Regular.ttf"),
        b"<< /Type /Font /Subtype /TrueType /BaseFont /BBBBBB+Inter-SemiBold /FontDescriptor 5 0 R >>",
        b"<< /Type /FontDescriptor /FontName /BBBBBB+Inter-SemiBold /FontFile2 6 0 R >>",
        ttf("NotoSans-Regular.ttf"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /JetBrainsMono-Regular /FontDescriptor 9 0 R >>",
        b"<< /Type /FontDescriptor /FontName /JetBrainsMono-Regular /FontFile2 10 0 R >>",
        ttf("JetBrainsMono-Regular.ttf"),
    ]
    return b"%PDF-1.7\n" + b"".join(b"%d 0 obj\n" % (i + 1) + body + b"\nendobj\n" for i, body in enumerate(parts)) + b"%%EOF\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    allowed = package_names()
    if sys.argv[1:] == ["--self-test"]:
        lines, ok = check(fixture(), allowed)
        expected = [
            "  Inter-Regular: in orde",
            "  Inter-SemiBold: FOUT, de PDF noemt Inter-SemiBold maar sluit NotoSans-Regular (Noto Sans) in",
            "  JetBrainsMono-Regular: in orde",
            "  Helvetica: niet ingesloten (standaardfont van de PDF-lezer)",
            "  JetBrainsMono-Regular: FOUT, TrueType-data als /Type1-font beschreven",
        ]
        assert lines == expected and not ok, lines
        print("PDF-fontcontrole: zelftest geslaagd (juist, verkeerd benoemd, niet ingesloten en verkeerd getypeerd font herkend)")
        return 0
    if not sys.argv[1:]:
        print(__doc__)
        return 2
    failed = 0
    for path in sys.argv[1:]:
        lines, ok = check(Path(path).read_bytes(), allowed)
        print(f"{path}: {'in orde' if ok else 'niet in orde'}")
        print("\n".join(lines) if lines else "  geen fonts gevonden")
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
