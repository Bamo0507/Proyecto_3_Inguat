import { cn } from "@/lib/utils";

export function FirmaAgua({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 120 120" fill="none" aria-hidden="true" focusable="false" className={cn("pointer-events-none", className)}>
      <path d="M120 12C74 8 17 29 17 66c0 32 47 48 103 37" />
      <path d="M120 29C85 24 36 38 36 66c0 23 34 34 84 23" />
      <path d="M120 46c-28-5-64 1-64 20 0 15 26 20 64 10" />
    </svg>
  );
}
