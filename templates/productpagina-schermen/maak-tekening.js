// Fictieve tekeningenset voor de schermafbeeldingen van Open PDF Studio: "Woning type A", A3 liggend,
// vector-PDF met plattegronden en een gevel, in revisie A en B (B: keuken 600 mm groter, extra raam).
// Gebruik: node maak-tekening.js <uitmap>
'use strict';
const fs = require('fs');
const zlib = require('zlib');
const path = require('path');
const OUT = process.argv[2] || '.';
const MM = 72 / 25.4; // pt per mm
const W = 420, H = 297; // A3 liggend, mm

function pdfDoc(pages) {
  const objs = [];
  const add = (s) => { objs.push(s); return objs.length; };
  const fontR = add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
  const fontB = add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');
  const pagesId = objs.length + 1 + pages.length * 2; // na de pagina's en hun streams
  const kids = [];
  for (const p of pages) {
    const stream = zlib.deflateSync(Buffer.from(p.content, 'latin1'), { level: 9 });
    const sid = add(`<< /Length ${stream.length} /Filter /FlateDecode >>\nstream\n${stream.toString('latin1')}\nendstream`);
    kids.push(add(`<< /Type /Page /Parent ${pagesId} 0 R /MediaBox [0 0 ${(W * MM).toFixed(2)} ${(H * MM).toFixed(2)}] /Resources << /Font << /F1 ${fontR} 0 R /F2 ${fontB} 0 R >> >> /Contents ${sid} 0 R >>`));
  }
  const pid = add(`<< /Type /Pages /Kids [${kids.map((k) => k + ' 0 R').join(' ')}] /Count ${kids.length} >>`);
  if (pid !== pagesId) throw new Error('pages-id klopt niet');
  const cat = add(`<< /Type /Catalog /Pages ${pid} 0 R >>`);
  const info = add(`<< /Title (${pages.title}) /Author (OpenAEC voorbeeldtekening) /Subject (Fictief voorbeeld) /Creator (OpenAEC) /Producer (maak-tekening.js) >>`);
  let out = '%PDF-1.4\n%\xE2\xE3\xCF\xD3\n';
  const offsets = [];
  objs.forEach((o, i) => { offsets.push(Buffer.byteLength(out, 'latin1')); out += `${i + 1} 0 obj\n${o}\nendobj\n`; });
  const xref = Buffer.byteLength(out, 'latin1');
  out += `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n` + offsets.map((o) => String(o).padStart(10, '0') + ' 00000 n \n').join('');
  out += `trailer\n<< /Size ${objs.length + 1} /Root ${cat} 0 R /Info ${info} 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  return Buffer.from(out, 'latin1');
}

// Tekenhulpen in mm op het papier (oorsprong linksonder).
function canvas() {
  const c = [];
  const p = (v) => (v * MM).toFixed(2);
  const esc = (s) => String(s).replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
  const api = {
    out: c,
    w(lw) { c.push(`${(lw * MM).toFixed(2)} w`); return api; },
    gray(g, fill) { c.push(`${g} ${fill ? 'g' : 'G'}`); return api; },
    rgb(r, g, b, fill) { c.push(`${r} ${g} ${b} ${fill ? 'rg' : 'RG'}`); return api; },
    line(x1, y1, x2, y2) { c.push(`${p(x1)} ${p(y1)} m ${p(x2)} ${p(y2)} l S`); return api; },
    rect(x, y, w, h, mode = 'S') { c.push(`${p(x)} ${p(y)} ${p(w)} ${p(h)} re ${mode}`); return api; },
    poly(pts, mode = 'S') { c.push(pts.map(([x, y], i) => `${p(x)} ${p(y)} ${i ? 'l' : 'm'}`).join(' ') + ` h ${mode}`); return api; },
    dash(on, off) { c.push(on ? `[${p(on)} ${p(off)}] 0 d` : '[] 0 d'); return api; },
    arc(cx, cy, r, a0, a1) { // kwartcirkels via bezier
      const k = 0.5523;
      const pts = [];
      const steps = Math.ceil(Math.abs(a1 - a0) / 90);
      const da = (a1 - a0) / steps;
      let a = a0 * Math.PI / 180;
      c.push(`${p(cx + r * Math.cos(a))} ${p(cy + r * Math.sin(a))} m`);
      for (let i = 0; i < steps; i++) {
        const b = a + da * Math.PI / 180;
        const kk = k * (da / 90);
        const x1 = cx + r * (Math.cos(a) - kk * Math.sin(a)), y1 = cy + r * (Math.sin(a) + kk * Math.cos(a));
        const x2 = cx + r * (Math.cos(b) + kk * Math.sin(b)), y2 = cy + r * (Math.sin(b) - kk * Math.cos(b));
        c.push(`${p(x1)} ${p(y1)} ${p(x2)} ${p(y2)} ${p(cx + r * Math.cos(b))} ${p(cy + r * Math.sin(b))} c`);
        a = b;
      }
      c.push('S');
      return api;
    },
    circle(cx, cy, r, mode = 'S') {
      const k = 0.5523 * r;
      c.push(`${p(cx + r)} ${p(cy)} m ${p(cx + r)} ${p(cy + k)} ${p(cx + k)} ${p(cy + r)} ${p(cx)} ${p(cy + r)} c ${p(cx - k)} ${p(cy + r)} ${p(cx - r)} ${p(cy + k)} ${p(cx - r)} ${p(cy)} c ${p(cx - r)} ${p(cy - k)} ${p(cx - k)} ${p(cy - r)} ${p(cx)} ${p(cy - r)} c ${p(cx + k)} ${p(cy - r)} ${p(cx + r)} ${p(cy - k)} ${p(cx + r)} ${p(cy)} c h ${mode}`);
      return api;
    },
    text(x, y, size, s, { bold = false, align = 'l', rot = 0 } = {}) {
      const wpt = String(s).length * size * (bold ? 0.56 : 0.52); // schatting breedte
      const dx = align === 'c' ? -wpt / 2 : align === 'r' ? -wpt : 0;
      if (rot) {
        const r = rot * Math.PI / 180, cs = Math.cos(r).toFixed(4), sn = Math.sin(r).toFixed(4);
        c.push(`BT /${bold ? 'F2' : 'F1'} ${size} Tf ${cs} ${sn} ${-sn} ${cs} ${p(x)} ${p(y)} Tm ${dx.toFixed(2)} 0 Td (${esc(s)}) Tj ET`);
      } else {
        c.push(`BT /${bold ? 'F2' : 'F1'} ${size} Tf ${(x * MM + dx).toFixed(2)} ${p(y)} Td (${esc(s)}) Tj ET`);
      }
      return api;
    },
  };
  return api;
}

// Tekenkader + titelblok
function frame(c, { titel, nr, schaal, rev, revs }) {
  c.gray(0).w(0.5).rect(10, 10, W - 20, H - 20).w(0.25).rect(12, 12, W - 24, H - 24);
  const bx = W - 12 - 120, by = 12;
  c.w(0.35).rect(bx, by, 120, 46);
  [36, 26, 16].forEach((y) => c.w(0.18).line(bx, by + y, bx + 120, by + y));
  c.line(bx + 60, by, bx + 60, by + 26).line(bx + 90, by, bx + 90, by + 16);
  c.text(bx + 3, by + 41, 6, 'PROJECT', { bold: true }).text(bx + 3, by + 38.2, 9, 'Woning type A  -  Voorbeeldproject', { bold: true });
  c.text(bx + 3, by + 31, 6, 'TEKENING').text(bx + 3, by + 27.8, 9, titel, { bold: true });
  c.text(bx + 3, by + 21.5, 6, 'SCHAAL').text(bx + 3, by + 18, 8, schaal + '  (A3)');
  c.text(bx + 63, by + 21.5, 6, 'DATUM').text(bx + 63, by + 18, 8, rev === 'B' ? '29-10-2026' : '15-10-2026');
  c.text(bx + 3, by + 11.5, 6, 'TEKENINGNUMMER').text(bx + 3, by + 5, 11, nr, { bold: true });
  c.text(bx + 63, by + 11.5, 6, 'STATUS').text(bx + 63, by + 5, 8, 'Voorlopig ontwerp');
  c.text(bx + 93, by + 11.5, 6, 'REVISIE').text(bx + 105, by + 4.5, 13, rev, { bold: true, align: 'c' });
  // revisietabel boven het titelblok
  c.w(0.18).rect(bx, by + 46, 120, 6 + revs.length * 5);
  c.text(bx + 3, by + 48 + revs.length * 5, 6, 'REV   DATUM         OMSCHRIJVING', { bold: true });
  revs.forEach(([r, d, o], i) => c.text(bx + 3, by + 48 + (revs.length - 1 - i) * 5, 6.5, `${r}      ${d}    ${o}`));
  c.text(14, 14, 5.5, 'Fictieve voorbeeldtekening voor Open PDF Studio  -  OpenAEC Foundation');
}

// Plattegrond: coördinaten in meters, schaal 1:50 => 1 m = 20 mm
function plan(c, ox, oy, rev, verdieping) {
  const S = 20;
  const X = (m) => ox + m * S, Y = (m) => oy + m * S;
  const Lx = 9.0, Ly = 10.8, t = 0.3, ti = 0.1;
  // assen
  c.gray(0.45).w(0.13).dash(4, 1.5);
  [0, 4.5, 9.0].forEach((a, i) => { c.line(X(a), Y(-1.6), X(a), Y(Ly + 1.6)); });
  [0, 5.4, 10.8].forEach((a) => { c.line(X(-1.6), Y(a), X(Lx + 1.6), Y(a)); });
  c.dash(0).gray(0.2).w(0.2);
  ['A', 'B', 'C'].forEach((n, i) => { const x = X([0, 4.5, 9.0][i]); c.circle(x, Y(Ly + 2.2), 3.2).text(x, Y(Ly + 2.2) - 1.3, 9, n, { bold: true, align: 'c' }); });
  ['1', '2', '3'].forEach((n, i) => { const y = Y([0, 5.4, 10.8][i]); c.circle(X(-2.2), y, 3.2).text(X(-2.2), y - 1.3, 9, n, { bold: true, align: 'c' }); });
  // buitenmuren (gevuld)
  c.gray(0.25, true).gray(0).w(0.35);
  c.poly([[X(0), Y(0)], [X(Lx), Y(0)], [X(Lx), Y(Ly)], [X(0), Y(Ly)]], 'S');
  c.poly([[X(t), Y(t)], [X(Lx - t), Y(t)], [X(Lx - t), Y(Ly - t)], [X(t), Y(Ly - t)]], 'S');
  // muurvulling als arcering
  c.w(0.1).gray(0.55);
  for (let d = 0; d < (Lx + Ly) * 2; d += 0.12) {
    // korte schuine streepjes in de spouwmuur (alleen langs de randen)
  }
  c.gray(0.6, true);
  c.rect(X(0), Y(0), Lx * S, t * S, 'f').rect(X(0), Y(Ly - t), Lx * S, t * S, 'f').rect(X(0), Y(0), t * S, Ly * S, 'f').rect(X(Lx - t), Y(0), t * S, Ly * S, 'f');
  c.gray(0, true).gray(0);
  // binnenwanden
  const keukenWand = rev === 'B' ? 6.0 : 5.4;
  const wanden = verdieping === 0
    ? [[t, keukenWand, 4.5, keukenWand], [4.5, t, 4.5, 3.6], [4.5, 7.8, 4.5, Ly - t], [4.5, 7.8, Lx - t, 7.8], [6.6, 7.8, 6.6, Ly - t]]
    : [[t, 5.4, Lx - t, 5.4], [4.5, 5.4, 4.5, Ly - t], [6.6, t, 6.6, 5.4], [6.6, 2.7, Lx - t, 2.7]];
  c.gray(0.6, true);
  for (const [x1, y1, x2, y2] of wanden) {
    if (x1 === x2) c.rect(X(x1) - ti * S / 2, Y(Math.min(y1, y2)), ti * S, Math.abs(y2 - y1) * S, 'f');
    else c.rect(X(Math.min(x1, x2)), Y(y1) - ti * S / 2, Math.abs(x2 - x1) * S, ti * S, 'f');
  }
  c.gray(0, true).gray(0).w(0.25);
  for (const [x1, y1, x2, y2] of wanden) {
    if (x1 === x2) { c.line(X(x1) - ti * S / 2, Y(y1), X(x2) - ti * S / 2, Y(y2)).line(X(x1) + ti * S / 2, Y(y1), X(x2) + ti * S / 2, Y(y2)); }
    else { c.line(X(x1), Y(y1) - ti * S / 2, X(x2), Y(y2) - ti * S / 2).line(X(x1), Y(y1) + ti * S / 2, X(x2), Y(y2) + ti * S / 2); }
  }
  // ramen (in de buitenmuur: drie lijnen, wit vlak)
  const ramen = verdieping === 0
    ? [['h', 1.0, 0, 2.4], ['h', 5.6, 0, 2.6], ['v', 0, 7.2, 2.0], ['h', 1.2, Ly, 2.0]].concat(rev === 'B' ? [['v', Lx, 2.0, 1.8]] : [])
    : [['h', 1.0, 0, 2.4], ['h', 5.6, 0, 2.2], ['h', 1.2, Ly, 2.4], ['h', 6.0, Ly, 1.8], ['v', Lx, 3.6, 1.2]];
  for (const [o, a, b, len] of ramen) {
    c.gray(1, true);
    if (o === 'h') { c.rect(X(a), Y(b) - (b ? t * S : 0), len * S, t * S, 'f'); c.gray(0, true).w(0.18).rect(X(a), Y(b) - (b ? t * S : 0), len * S, t * S).line(X(a), Y(b) + (b ? -t * S / 2 : t * S / 2), X(a + len), Y(b) + (b ? -t * S / 2 : t * S / 2)); }
    else { c.rect(X(a) - (a ? t * S : 0), Y(b), t * S, len * S, 'f'); c.gray(0, true).w(0.18).rect(X(a) - (a ? t * S : 0), Y(b), t * S, len * S).line(X(a) + (a ? -t * S / 2 : t * S / 2), Y(b), X(a) + (a ? -t * S / 2 : t * S / 2), Y(b + len)); }
  }
  c.gray(0, true);
  // deuren met draaicirkel
  const deuren = verdieping === 0 ? [[5.4, 7.8, 0.9, 'h'], [6.9, 7.8, 0.8, 'h'], [4.5, 4.4, 0.9, 'v'], [7.4, Ly, 1.0, 'hb']] : [[2.0, 5.4, 0.8, 'h'], [5.0, 5.4, 0.8, 'h'], [7.4, 5.4, 0.8, 'h'], [6.6, 1.0, 0.8, 'v']];
  c.w(0.2);
  for (const [a, b, w, o] of deuren) {
    c.gray(1, true);
    if (o.startsWith('h')) {
      const th = o === 'hb' ? t : ti;
      c.rect(X(a), Y(b) - th * S / 2 - (o === 'hb' ? th * S / 2 : 0), w * S, th * S, 'f').gray(0, true);
      const dir = o === 'hb' ? -1 : -1;
      c.line(X(a), Y(b), X(a), Y(b) + dir * w * S).arc(X(a), Y(b), w * S, 270, 360);
    } else {
      c.rect(X(a) - ti * S / 2, Y(b), ti * S, w * S, 'f').gray(0, true);
      c.line(X(a), Y(b), X(a) + w * S, Y(b)).arc(X(a), Y(b), w * S, 0, 90);
    }
  }
  // trap
  if (verdieping === 0) { c.w(0.15); for (let i = 0; i <= 12; i++) c.line(X(6.6) + 1, Y(7.8) + 2 + i * 3.4, X(Lx - t) - 1, Y(7.8) + 2 + i * 3.4); c.text(X(7.8), Y(9.3), 6, 'trap 13 x 207', { align: 'c' }); }
  else { c.w(0.15); for (let i = 0; i <= 12; i++) c.line(X(4.6) + i * 3.3, Y(5.5), X(4.6) + i * 3.3, Y(7.2)); }
  // ruimtenamen + oppervlakte
  const ruimten = verdieping === 0
    ? [['Woonkamer', 2.4, rev === 'B' ? 3.0 : 2.7, rev === 'B' ? 24.7 : 21.9], ['Keuken', 2.4, rev === 'B' ? 8.6 : 8.3, rev === 'B' ? 18.2 : 21.0], ['Werkkamer', 6.7, 2.0, 15.1], ['Hal', 6.7, 5.7, 8.8], ['Toilet', 5.5, 9.4, 3.1], ['Trap', 7.8, 10.1, 0]]
    : [['Slaapkamer 1', 2.3, 2.7, 24.7], ['Slaapkamer 2', 7.8, 1.3, 8.4], ['Badkamer', 7.8, 4.0, 6.5], ['Slaapkamer 3', 2.3, 8.1, 20.9], ['Overloop', 5.6, 8.5, 9.9]];
  for (const [n, x, y, m2] of ruimten) { c.text(X(x), Y(y), 9, n, { bold: true, align: 'c' }); if (m2) c.text(X(x), Y(y) - 4.2, 7, `${m2.toFixed(1).replace('.', ',')} m²`, { align: 'c' }); }
  // maatvoering (onder en links)
  c.w(0.15).gray(0.1);
  const maatH = (xs, y) => {
    c.line(X(xs[0]), Y(y), X(xs[xs.length - 1]), Y(y));
    xs.forEach((x) => { c.line(X(x), Y(y) - 1.5, X(x), Y(y) + 1.5).line(X(x) - 1, Y(y) - 1, X(x) + 1, Y(y) + 1); });
    for (let i = 1; i < xs.length; i++) c.text((X(xs[i - 1]) + X(xs[i])) / 2, Y(y) + 1.2, 7, String(Math.round((xs[i] - xs[i - 1]) * 1000)), { align: 'c' });
  };
  const maatV = (ys, x) => {
    c.line(X(x), Y(ys[0]), X(x), Y(ys[ys.length - 1]));
    ys.forEach((y) => { c.line(X(x) - 1.5, Y(y), X(x) + 1.5, Y(y)).line(X(x) - 1, Y(y) - 1, X(x) + 1, Y(y) + 1); });
    for (let i = 1; i < ys.length; i++) c.text(X(x) - 1.2, (Y(ys[i - 1]) + Y(ys[i])) / 2, 7, String(Math.round((ys[i] - ys[i - 1]) * 1000)), { align: 'c', rot: 90 });
  };
  maatH([0, 4.5, Lx], -1.0); maatH([0, Lx], -1.8);
  maatV(verdieping === 0 ? [0, keukenWand, 7.8, Ly] : [0, 5.4, Ly], -1.0); maatV([0, Ly], -1.8);
}

function noordpijl(c, x, y) {
  c.w(0.25).circle(x, y, 7).poly([[x, y + 6], [x - 2.5, y - 4], [x, y - 2], [x + 2.5, y - 4]], 'B').text(x, y + 8.5, 9, 'N', { bold: true, align: 'c' });
}
function schaalbalk(c, x, y) {
  c.w(0.2);
  for (let i = 0; i < 5; i++) { if (i % 2 === 0) c.rect(x + i * 20, y, 20, 2, 'f'); c.rect(x + i * 20, y, 20, 2); }
  [0, 1, 2, 3, 4, 5].forEach((m) => c.text(x + m * 20, y + 3.5, 6, `${m} m`, { align: 'c' }));
  c.text(x, y - 4, 6, 'Schaal 1:50');
}

function gevel(c, ox, oy, rev) {
  const S = 20; const X = (m) => ox + m * S, Y = (m) => oy + m * S;
  c.gray(0).w(0.35).rect(X(0), Y(0), 9 * S, 5.4 * S).poly([[X(-0.3), Y(5.4)], [X(4.5), Y(8.6)], [X(9.3), Y(5.4)]], 'S');
  c.w(0.12).gray(0.5); for (let y = 0.1; y < 5.4; y += 0.085 * 2) c.line(X(0), Y(y), X(9), Y(y));
  c.gray(1, true).gray(0).w(0.3);
  const ramen = [[1.0, 0.9, 2.4, 1.5], [5.6, 0.9, 2.6, 1.5], [1.2, 3.4, 2.4, 1.3], [6.0, 3.4, 1.8, 1.3]].concat(rev === 'B' ? [] : []);
  for (const [x, y, w, h] of ramen) { c.rect(X(x), Y(y), w * S, h * S, 'B'); c.w(0.15).line(X(x + w / 2), Y(y), X(x + w / 2), Y(y + h)).w(0.3); }
  c.rect(X(4.0), Y(0), 1.0 * S, 2.3 * S, 'B');
  c.gray(0, true);
  // peilen
  c.w(0.15).gray(0.2);
  [[0, '± 0  peil'], [2.7, '+ 2.700  verdiepingsvloer'], [5.4, '+ 5.400  goot'], [8.6, '+ 8.600  nok']].forEach(([h, t]) => {
    c.line(X(9.4), Y(h), X(11.5), Y(h)).poly([[X(9.6), Y(h)], [X(9.8), Y(h) + 1.6], [X(9.4), Y(h) + 1.6]], 'f').text(X(10.0), Y(h) + 1.2, 7, t);
  });
  c.gray(0.3).w(0.6).line(X(-1.5), Y(0), X(12), Y(0));
}

function maakSet(rev) {
  const revs = rev === 'B' ? [['A', '15-10-2026', 'Eerste uitgave'], ['B', '29-10-2026', 'Keuken 600 mm groter, raam oostgevel']] : [['A', '15-10-2026', 'Eerste uitgave']];
  const pages = [];
  for (const [titel, nr, teken] of [
    ['Plattegrond begane grond', 'WTA-101', (c) => { plan(c, 70, 52, rev, 0); noordpijl(c, 300, 230); schaalbalk(c, 240, 90); }],
    ['Plattegrond eerste verdieping', 'WTA-102', (c) => { plan(c, 70, 52, rev, 1); noordpijl(c, 300, 230); schaalbalk(c, 240, 90); }],
    ['Voorgevel (zuid)', 'WTA-201', (c) => { gevel(c, 70, 70, rev); schaalbalk(c, 240, 52); }],
  ]) {
    const c = canvas();
    teken(c);
    frame(c, { titel, nr, schaal: '1:50', rev, revs });
    pages.push({ content: c.out.join('\n') });
  }
  pages.title = `Woning type A - rev ${rev}`;
  return pdfDoc(pages);
}

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'Woning-type-A_rev-A.pdf'), maakSet('A'));
fs.writeFileSync(path.join(OUT, 'Woning-type-A_rev-B.pdf'), maakSet('B'));
console.log('klaar:', fs.readdirSync(OUT).filter((f) => f.endsWith('.pdf')).join(', '));
