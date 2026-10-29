// Voorbeeld van een stappenbestand, uit Open PDF Studio (de beelden op open-aec.com/open-pdf-studio/).
// Draaien:
//   URL=https://open-pdf-studio.open-aec.com/ DSF=0.75 BEELD=meten node schermen.mjs voorbeeld-stappen.mjs
// Elk beeld start in een schone browser; zo beïnvloeden de beelden elkaar niet.
// De tekening in bestanden/ is fictief; zet nooit echte projecten of persoonsgegevens in beeld.

// Tekening in meters (as A/1 = 0,0) naar een schermpunt. Plattegrond op A3: 70/52 mm, 20 mm per meter (1:50).
async function plek(app) {
  const [l, t, w, h] = await app.eval(`(() => { const r = document.getElementById('pdf-canvas').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })()`);
  const mm = (x, y) => [l + x / 420 * w, t + (297 - y) / 297 * h];
  return { mm, m: (x, y) => mm(70 + x * 20, 52 + y * 20) };
}

async function openen(app, naam) {
  await app.files(naam);
  await app.key('o', { ctrl: true });
  await app.waitFor(`document.title.includes(${JSON.stringify(naam)})`, 8000);
  await app.sleep(1500);
  await app.hide('#assistant-launcher,#analytics-settings');
}

const beelden = {
  // 03 Meten: schaalgebied 1:50 over het blad, dan een oppervlakte meten (klik per hoek, dubbelklik om te sluiten).
  async meten(app) {
    await openen(app, 'Woning-type-A_rev-A.pdf');
    await app.click('Start');
    await app.click('Pagina passend');
    await app.sleep(1000);
    const p = await plek(app);
    await app.click('Tekenen');
    await app.click('#btn-create-scale-region-full-page');
    // … schaal kiezen in het venster, dan:
    await app.click('Apply');
    await app.click('Annotatie');
    await app.click('#tool-measure-area');
    const hoeken = [[0.3, 0.3], [4.45, 0.3], [4.45, 5.35], [0.3, 5.35]];
    for (const [x, y] of hoeken.slice(0, -1)) await app.mouse(...p.m(x, y));
    await app.mouse(...p.m(...hoeken.at(-1)), { clickCount: 2 });
    await app.key('Escape');
    await app.move(1590, 990); // muis uit beeld
    await app.sleep(500);
  },
};

export default async (app) => {
  const beeld = process.env.BEELD;
  await beelden[beeld](app);
  await app.shot(`open-pdf-studio-feat-${beeld}.png`);
};
