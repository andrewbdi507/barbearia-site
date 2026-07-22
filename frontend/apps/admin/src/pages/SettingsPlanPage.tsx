import { PlanSelector } from "../components/PlanSelector";

export function SettingsPlanPage() {
  return (
    <div className="animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Plano e Assinatura</h1>
        <p className="text-sm text-text-secondary mt-1">
          Gerencie seu plano, veja o uso atual e faça upgrade quando precisar.
        </p>
      </div>
      <PlanSelector />
    </div>
  );
}

export default SettingsPlanPage;
