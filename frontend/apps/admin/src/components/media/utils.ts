// ============================================================
// Media Module — Utility functions
// uploadWithProgress() — isolada do React
// ============================================================

import type { MediaUploadResponse, UploadWithProgressOptions } from "./types";

const API = `${import.meta.env.VITE_API_URL || ""}/api/v1`;

/** Faz upload com barra de progresso usando XMLHttpRequest.
 *
 * Isolada do React para ser reutilizável em qualquer contexto.
 */
export function uploadWithProgress({
  file,
  mediaType,
  onProgress,
  signal,
}: UploadWithProgressOptions): Promise<MediaUploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("media_type", mediaType);

    xhr.open("POST", `${API}/media/upload`);

    const token = sessionStorage.getItem("access_token");
    if (token) {
      xhr.setRequestHeader("Authorization", `Bearer ${token}`);
    }

    // Progresso
    xhr.upload.addEventListener("progress", (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    });

    // Abort
    if (signal) {
      signal.addEventListener("abort", () => xhr.abort());
    }

    // Resposta
    xhr.addEventListener("load", () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          resolve(JSON.parse(xhr.responseText) as MediaUploadResponse);
        } catch {
          reject(new Error("Resposta inválida do servidor."));
        }
      } else if (xhr.status === 401) {
        sessionStorage.removeItem("access_token");
        window.location.href = "/login";
        reject(new Error("Sessão expirada."));
      } else {
        try {
          const err = JSON.parse(xhr.responseText) as { message?: string; detail?: string };
          reject(new Error(err.message || err.detail || `Erro ${xhr.status}`));
        } catch {
          reject(new Error(`Erro ${xhr.status}: ${xhr.statusText}`));
        }
      }
    });

    xhr.addEventListener("error", () => reject(new Error("Falha na conexão. Verifique sua internet.")));
    xhr.addEventListener("abort", () => reject(new DOMException("Upload cancelado.", "AbortError")));

    xhr.send(formData);
  });
}

/** Formata bytes para exibição humana */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** i).toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

/** Valida arquivo antes do upload. Retorna erro ou null. */
export function validateFile(
  file: File | null,
  accept: string,
  maxSize: number,
): { code: "empty" | "type" | "size"; message: string } | null {
  if (!file || file.size === 0) {
    return { code: "empty", message: "Nenhum arquivo selecionado." };
  }

  // Valida MIME type contra a lista de accept
  if (accept && accept !== "*" && accept !== "*/*") {
    const allowed = accept.split(",").map((s) => s.trim());
    const match = allowed.some((a) => {
      if (a.startsWith(".")) return file.name.toLowerCase().endsWith(a.toLowerCase());
      if (a.endsWith("/*")) return file.type.startsWith(a.replace("/*", "/"));
      return file.type === a;
    });
    if (!match) {
      return { code: "type", message: `Formato não permitido. Use: ${accept}` };
    }
  }

  if (file.size > maxSize) {
    return { code: "size", message: `Arquivo muito grande. Máximo: ${formatBytes(maxSize)}.` };
  }

  return null;
}
