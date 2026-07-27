// ============================================================
// ColorPicker — Input de cor com preview
// ============================================================

import { type ChangeEvent } from "react";

interface ColorPickerProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
}

export function ColorPicker({ label, value, onChange }: ColorPickerProps) {
  return (
    <div className="flex items-center gap-3">
      <div
        className="h-9 w-9 rounded-lg border border-border flex-shrink-0"
        style={{ backgroundColor: value }}
      />
      <div className="flex-1 min-w-0">
        <label className="text-xs font-medium text-text-secondary block mb-1">{label}</label>
        <input
          type="text"
          value={value}
          onChange={(e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value)}
          className="w-full bg-surface rounded-md border border-border px-2.5 py-1.5 text-sm text-text-primary font-mono focus:outline-none focus:border-primary/50"
          placeholder="#000000"
          maxLength={7}
        />
      </div>
      <input
        type="color"
        value={value}
        onChange={(e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value)}
        className="h-9 w-9 rounded-md border border-border cursor-pointer p-0.5 bg-transparent"
        title={label}
      />
    </div>
  );
}
