import { useState } from "react";
import { Card, Button, Badge, themes, applyTheme, type Theme } from "@barbershop/design-system";
import { Check, Palette } from "lucide-react";

export function ThemeConfigPage() {
  const [selectedThemeId, setSelectedThemeId] = useState("urban");

  const handleSelect = (theme: Theme) => {
    setSelectedThemeId(theme.id);
    applyTheme(theme);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Personalizar Tema</h1>
        <p className="text-sm text-text-secondary mt-1">
          Escolha um tema para o site da sua barbearia. As alterações são aplicadas instantaneamente.
        </p>
      </div>

      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {themes.map((theme) => (
          <Card
            key={theme.id}
            variant={selectedThemeId === theme.id ? "selected" : "interactive"}
            className="relative"
            onClick={() => handleSelect(theme)}
          >
            {/* Preview */}
            <div
              className="h-32 rounded-md mb-4 flex items-end p-3"
              style={{ background: theme.preview }}
            >
              <span className="text-white text-sm font-medium drop-shadow-md">
                {theme.name}
              </span>
            </div>

            <h3 className="font-semibold text-text-primary">{theme.name}</h3>
            <p className="text-sm text-text-secondary mt-1">{theme.description}</p>

            {/* Color Swatches */}
            <div className="flex gap-2 mt-3">
              <div className="h-6 w-6 rounded-full border border-border" style={{ backgroundColor: theme.colors.primary }} title="Primary" />
              <div className="h-6 w-6 rounded-full border border-border" style={{ backgroundColor: theme.colors.secondary }} title="Secondary" />
              <div className="h-6 w-6 rounded-full border border-border" style={{ backgroundColor: theme.colors.background }} title="Background" />
            </div>

            {selectedThemeId === theme.id && (
              <Badge variant="success" className="absolute top-3 right-3">
                <Check className="h-3 w-3" /> Ativo
              </Badge>
            )}
          </Card>
        ))}
      </div>

      {/* Custom colors */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Cores Personalizadas</h3>
        <p className="text-sm text-text-secondary mb-4">
          Em breve: ajuste fino de cada cor individualmente.
        </p>
        <div className="grid gap-4 grid-cols-2 sm:grid-cols-4">
          {["primary", "secondary", "background", "surface"].map((color) => (
            <div key={color} className="flex flex-col gap-2">
              <label className="text-sm font-medium text-text-primary capitalize">{color}</label>
              <input type="color" className="w-full h-10 rounded-md border border-border cursor-pointer" />
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
