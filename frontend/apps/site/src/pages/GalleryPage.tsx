import { Card } from "@barbershop/design-system";
import { Image } from "lucide-react";

export function GalleryPage() {
  return (
    <div className="animate-fade-in">
      <section className="mx-auto max-w-6xl px-4 py-16">
        <div className="text-center mb-12">
          <Image className="mx-auto mb-4 h-12 w-12 text-primary" />
          <h1 className="text-3xl md:text-4xl font-bold mb-4">Galeria</h1>
          <p className="text-lg text-muted-foreground max-w-lg mx-auto">
            Confira alguns dos nossos trabalhos e inspire-se para o seu próximo visual.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i} variant="interactive" className="overflow-hidden p-0">
              <div className="aspect-square bg-muted flex items-center justify-center">
                <Image className="h-12 w-12 text-muted-foreground" />
              </div>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
