// ============================================================
// Theme Registry — todos os temas do sistema
// ============================================================
import type { Theme } from "./types";
import { luxury } from "./luxury";
import { modern } from "./modern";
import { classic } from "./classic";
import { urban } from "./urban";
import { minimal } from "./minimal";

export const themes: Record<string, Theme> = {
  luxury,
  modern,
  classic,
  urban,
  minimal,
};

export const themeList: Theme[] = Object.values(themes);

export function getTheme(id: string): Theme {
  return themes[id] || luxury;
}

export { type Theme } from "./types";
