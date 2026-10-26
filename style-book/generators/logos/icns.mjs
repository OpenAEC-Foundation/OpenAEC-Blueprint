// ICNS met PNG-afbeeldingen. Type per pixelgrootte.
const TYPES = { 16: "icp4", 32: "icp5", 64: "icp6", 128: "ic07", 256: "ic08", 512: "ic09", 1024: "ic10" };

export function packIcns(pngs) {
  const chunks = pngs.map(({ size, data }) => {
    const type = TYPES[size];
    if (!type) throw new Error(`Geen ICNS-type voor ${size}px`);
    const head = Buffer.alloc(8);
    head.write(type, 0, "ascii");
    head.writeUInt32BE(8 + data.length, 4);
    return Buffer.concat([head, data]);
  });
  const body = Buffer.concat(chunks);
  const head = Buffer.alloc(8);
  head.write("icns", 0, "ascii");
  head.writeUInt32BE(8 + body.length, 4);
  return Buffer.concat([head, body]);
}
