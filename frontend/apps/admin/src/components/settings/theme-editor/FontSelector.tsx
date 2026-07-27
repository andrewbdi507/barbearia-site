// ============================================================
// FontSelector — Dropdown de seleção de fonte
// ============================================================

import { type ChangeEvent } from "react";

interface FontSelectorProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
}

const FONTS = [
  { value: "Inter", label: "Inter (Moderna)" },
  { value: "Bebas Neue", label: "Bebas Neue (Impactante)" },
  { value: "Playfair Display", label: "Playfair Display (Elegante)" },
  { value: "Merriweather", label: "Merriweather (Clássica)" },
  { value: "Lora", label: "Lora (Tradicional)" },
  { value: "Cormorant Garamond", label: "Cormorant Garamond (Sofisticada)" },
  { value: "DM Sans", label: "DM Sans (Limpa)" },
  { value: "Montserrat", label: "Montserrat (Geométrica)" },
  { value: "Lato", label: "Lato (Versátil)" },
  { value: "Source Sans 3", label: "Source Sans 3 (Leitura)" },
];

export function FontSelector({ label, value, onChange }: FontSelectorProps) {
  return (
    <div>
      <label className="text-xs font-medium text-text-secondary block mb-1.5">{label}</label>
      <select
        value={value}
        onChange={(e: ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
        className="w-full bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50 appearance-none cursor-pointer"
      >
        {FONTS.map((f) => (
          <option key={f.value} value={f.value}>
            {f.label}
          </option>
        ))}
      </select>
      <p className="mt-1 text-xs text-text-disabled" style={{ fontFamily: value }}>
        Preview: {value}
      </p>
    </div>
  );
}
