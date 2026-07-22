import { ThemeSelector } from "../components/ThemeSelector";

export function ThemeConfigPage() {
  return (
    <div className="animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Personalizar Tema</h1>
        <p className="text-sm text-text-secondary mt-1">
          Escolha um tema para o site da sua barbearia. As alterações são aplicadas instantaneamente.
        </p>
      </div>
      <ThemeSelector />
    </div>
  );
}
