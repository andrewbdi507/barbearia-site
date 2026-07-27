// ============================================================
// RadiusSlider — Controle de border-radius com preview
// ============================================================

import { type ChangeEvent } from "react";

interface RadiusSliderProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
}

const PRESETS = [
  { label: "0px", value: "0px", desc: "Reto" },
  { label: "4px", value: "4px", desc: "Suave" },
  { label: "8px", value: "8px", desc: "Padrão" },
  { label: "14px", value: "14px", desc: "Arredondado" },
  { label: "20px", value: "20px", desc: "Moderno" },
  { label: "28px", value: "28px", desc: "Pílula" },
];

export function RadiusSlider({ label, value, onChange }: RadiusSliderProps) {
  return (
    <div>
      <label className="text-xs font-medium text-text-secondary block mb-2">{label}</label>
      <div className="flex gap-1.5 flex-wrap">
        {PRESETS.map((p) => (
          <button
            key={p.value}
            onClick={() => onChange(p.value)}
            className={`px-3 py-1.5 text-xs rounded-md border transition-all ${
              value === p.value
                ? "border-primary bg-primary/10 text-primary font-medium"
                : "border-border text-text-secondary hover:border-border/80"
            }`}
            title={p.desc}
          >
            {p.label}
          </button>
        ))}
      </div>
      {/* Preview box */}
      <div className="mt-3 flex gap-3">
        <div
          className="h-10 w-10 bg-primary/20 border border-primary/30 flex items-center justify-center text-[10px] text-text-secondary"
          style={{ borderRadius: value }}
        >
          {value}
        </div>
        <div
          className="h-10 flex-1 bg-surface border border-border flex items-center justify-center text-[10px] text-text-disabled"
          style={{ borderRadius: value }}
        >
          Preview
        </div>
      </div>
      <input
        type="text"
        value={value}
        onChange={(e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value)}
        className="mt-2 w-full bg-surface rounded-md border border-border px-2.5 py-1 text-xs text-text-secondary font-mono focus:outline-none focus:border-primary/50"
        placeholder="8px"
      />
    </div>
  );
}
