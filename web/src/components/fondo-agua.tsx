export function FondoAgua() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 z-[-1] overflow-clip">
    <svg
      viewBox="0 0 1600 1000"
      preserveAspectRatio="none"
      aria-hidden="true"
      focusable="false"
      className="workspace-water block w-full"
    >
      <path
        d="M1600 110C1450 220 1530 410 1260 570C1040 700 1040 890 710 1000H1600Z"
        fill="var(--water-bank)"
      />
      <path
        d="M1600 340C1460 440 1520 550 1320 700C1140 835 1170 930 970 1000H1600Z"
        fill="var(--water-middle)"
      />
      <path
        d="M1600 610C1480 710 1480 865 1270 1000H1600Z"
        fill="var(--water-deep)"
      />
      <path
        d="M1600 155C1480 270 1550 420 1290 590C1080 730 1090 900 790 1000"
        fill="none"
        stroke="var(--water-line)"
        strokeWidth="1"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
    </div>
  );
}
