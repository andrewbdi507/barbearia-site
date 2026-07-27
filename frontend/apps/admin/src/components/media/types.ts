// ============================================================
// Media Module — Shared Types
// ============================================================

/** Resposta do endpoint POST /api/v1/media/upload */
export interface MediaUploadResponse {
  id: string;
  url: string;
  filename: string;
  size_bytes: number;
  content_hash: string;
  width: number | null;
  height: number | null;
}

/** Erro de validação local (antes do upload) */
export interface MediaValidationError {
  code: "empty" | "type" | "size" | "preview";
  message: string;
}

/** Estados do ciclo de vida do upload */
export type MediaUploadStatus =
  | "idle"
  | "dragging"
  | "preview"
  | "uploading"
  | "success"
  | "error";

/** Props públicas do MediaUploader */
export interface MediaUploaderProps {
  /** Tipo de mídia enviado ao backend (logo, banner, gallery, etc.) */
  mediaType?: string;
  /** MIME types aceitos (ex: "image/*" ou ".jpg,.png") */
  accept?: string;
  /** Tamanho máximo em bytes (default: 10 MB) */
  maxSize?: number;
  /** Desabilita o componente */
  disabled?: boolean;
  /** Texto do label principal */
  label?: string;
  /** Texto descritivo abaixo do label */
  description?: string;
  /** URL de preview inicial (imagem já salva) */
  initialPreview?: string;
  /** Chamado após upload bem-sucedido */
  onUploaded?: (response: MediaUploadResponse) => void;
  /** Chamado quando o usuário remove a imagem */
  onRemoved?: () => void;
  /** Chamado em caso de erro (validação ou upload) */
  onError?: (error: MediaValidationError | Error) => void;
  /** Classes CSS extras */
  className?: string;
}

/** Payload enviado ao backend via FormData */
export interface UploadPayload {
  file: File;
  mediaType: string;
}

/** Opções da função uploadWithProgress */
export interface UploadWithProgressOptions {
  file: File;
  mediaType: string;
  onProgress?: (pct: number) => void;
  signal?: AbortSignal;
}
