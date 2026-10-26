// One icon from the OpenAEC B2 set (design 0.4), from public/icons/standard.svg.
// 16 px uses the 16 px drawing, anything larger the 24 px drawing.

const SPRITE = `${import.meta.env.BASE_URL}icons/standard.svg`;

export default function B2Icon({ id, size = 16 }: { id: string; size?: number }) {
  const drawing = size <= 16 ? 16 : 24;
  return (
    <svg className="oa-icon" width={size} height={size} aria-hidden="true">
      <use href={`${SPRITE}#i${drawing}-${id}`} />
    </svg>
  );
}
