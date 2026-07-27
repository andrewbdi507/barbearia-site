// ============================================================
// Theme Registry — todos os temas do sistema
// ============================================================
import type { Theme } from "./types";
import { luxury } from "./luxury";
import { modern } from "./modern";
import { classic } from "./classic";
import { urban } from "./urban";
import { minimal } from "./minimal";
import { custom } from "./custom";

export const themes: Record<string, Theme> = {
  luxury,
  modern,
  classic,
  urban,
  minimal,
  custom,
};

export const themeList: Theme[] = Object.values(themes);

export function getTheme(id: string): Theme {
  return themes[id] || custom;
}

export { type Theme } from "./types";
