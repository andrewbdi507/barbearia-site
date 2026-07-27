// ============================================================
// MediaUploader — Componente reutilizável de upload
// Drag & drop, preview, progresso, validação.
// ============================================================

import {
  useState, useRef, useEffect, useCallback,
  type DragEvent, type ChangeEvent,
} from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, X, Check, AlertTriangle, RefreshCw } from "lucide-react";
import { uploadWithProgress, validateFile, formatBytes } from "./utils";
import type { MediaUploaderProps, MediaUploadStatus, MediaValidationError, MediaUploadResponse } from "./types";

// ---- Constantes ----
const DEFAULT_MAX_SIZE = 10 * 1024 * 1024; // 10 MB

export function MediaUploader({
  mediaType = "gallery",
  accept = "image/*",
  maxSize = DEFAULT_MAX_SIZE,
  disabled = false,
  label = "Upload de Imagem",
  description = "Arraste uma imagem ou clique para selecionar.",
  initialPreview,
  onUploaded,
  onRemoved,
  onError,
  className = "",
}: MediaUploaderProps) {
  // ---- State ----
  const [status, setStatus] = useState<MediaUploadStatus>(initialPreview ? "preview" : "idle");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(initialPreview || null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<MediaValidationError | Error | null>(null);
  const [uploadResponse, setUploadResponse] = useState<MediaUploadResponse | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // ---- Cleanup: revoke object URL on unmount ----
  useEffect(() => {
    return () => {
      if (previewUrl && !initialPreview) {
        URL.revokeObjectURL(previewUrl);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ---- Gerar preview local ----
  const generatePreview = useCallback((f: File) => {
    // Revoga preview anterior (local, não inicial)
    if (previewUrl && previewUrl !== initialPreview) {
      URL.revokeObjectURL(previewUrl);
    }
    try {
      const url = URL.createObjectURL(f);
      setPreviewUrl(url);
      return url;
    } catch {
      setStatus("error");
      const err: MediaValidationError = { code: "preview", message: "Erro ao gerar preview da imagem." };
      setError(err);
      onError?.(err);
      return null;
    }
  }, [previewUrl, initialPreview, onError]);

  // ---- Iniciar upload ----
  const startUpload = useCallback(async (f: File) => {
    setStatus("uploading");
    setProgress(0);
    setError(null);

    const ctrl = new AbortController();
    abortRef.current = ctrl;

    try {
      const response = await uploadWithProgress({
        file: f,
        mediaType,
        onProgress: setProgress,
        signal: ctrl.signal,
      });
      setUploadResponse(response);
      setStatus("success");
      onUploaded?.(response);
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === "AbortError") {
        // Cancelado: volta ao estado preview (arquivo ainda selecionado)
        setStatus("preview");
        return;
      }
      setStatus("error");
      const e = err instanceof Error ? err : new Error("Falha no upload.");
      setError(e);
      onError?.(e);
    } finally {
      abortRef.current = null;
    }
  }, [mediaType, onUploaded, onError]);

  // ---- Processar arquivo selecionado ----
  const handleFile = useCallback((f: File | null) => {
    setError(null);
    setUploadResponse(null);

    // Validação
    const validationError = validateFile(f, accept, maxSize);
    if (validationError) {
      setStatus("error");
      setError(validationError);
      onError?.(validationError);
      return;
    }

    if (!f) return;

    setFile(f);
    const url = generatePreview(f);
    if (url) {
      setStatus("preview");
      startUpload(f);
    }
  }, [accept, maxSize, generatePreview, startUpload, onError]);

  // ---- Handlers de interação ----
  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    if (disabled) return;
    setStatus("idle");
    const dropped = e.dataTransfer.files[0];
    handleFile(dropped || null);
  }, [disabled, handleFile]);

  const handleDragOver = useCallback((e: DragEvent) => {
    e.preventDefault();
    if (!disabled && status !== "uploading") setStatus("dragging");
  }, [disabled, status]);

  const handleDragLeave = useCallback(() => {
    if (!disabled && status !== "uploading") setStatus("idle");
  }, [disabled, status]);

  const handleInputChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    handleFile(selected || null);
    // Reset input para permitir selecionar o mesmo arquivo novamente
    e.target.value = "";
  }, [handleFile]);

  const handleRemove = useCallback(() => {
    abortRef.current?.abort();
    if (previewUrl && previewUrl !== initialPreview) {
      URL.revokeObjectURL(previewUrl);
    }
    setFile(null);
    setPreviewUrl(initialPreview || null);
    setProgress(0);
    setError(null);
    setUploadResponse(null);
    setStatus(initialPreview ? "preview" : "idle");
    onRemoved?.();
  }, [previewUrl, initialPreview, onRemoved]);

  const handleRetry = useCallback(() => {
    if (file) startUpload(file);
  }, [file, startUpload]);

  const handleCancelUpload = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  const openFileDialog = useCallback(() => {
    if (!disabled && status !== "uploading") inputRef.current?.click();
  }, [disabled, status]);

  // ---- Render helpers ----
  const renderDropZone = () => (
    <motion.button
      type="button"
      onClick={openFileDialog}
      onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") openFileDialog(); }}
      className={`w-full border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center gap-3 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 ${
        status === "dragging"
          ? "border-primary bg-primary/5"
          : "border-border hover:border-border/80 hover:bg-surface-hover/50"
      } ${disabled ? "opacity-40 cursor-not-allowed" : ""}`}
      aria-label={label}
      role="button"
      tabIndex={0}
    >
      <div className="p-3 rounded-full bg-surface-hover">
        <Upload className="h-6 w-6 text-text-secondary" />
      </div>
      <div>
        <p className="text-sm font-medium text-text-primary">{label}</p>
        <p className="text-xs text-text-secondary mt-1">{description}</p>
      </div>
      <p className="text-xs text-text-disabled">
        {accept.replace(/\*/g, "").replace(/\//g, " ").trim().toUpperCase() || "Todos"} • Máx {formatBytes(maxSize)}
      </p>
    </motion.button>
  );

  const renderPreview = () => (
    <div className="relative rounded-xl border border-border overflow-hidden">
      {previewUrl && (
        <img
          src={previewUrl}
          alt={file?.name || "Preview"}
          className="w-full h-48 object-cover"
          onError={() => {
            setStatus("error");
            setError({ code: "preview", message: "Erro ao carregar preview." });
          }}
        />
      )}
      {/* Overlay com ações */}
      <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/70 to-transparent p-3 flex items-center justify-between">
        <span className="text-white text-xs truncate max-w-[60%]" title={file?.name}>
          {file?.name || "Imagem"} — {file ? formatBytes(file.size) : ""}
        </span>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={openFileDialog}
            disabled={status === "uploading"}
            className="p-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-white text-xs transition-colors"
            aria-label="Alterar imagem"
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            onClick={handleRemove}
            className="p-1.5 rounded-lg bg-white/20 hover:bg-red-500/60 text-white text-xs transition-colors"
            aria-label="Remover imagem"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  );

  const renderProgress = () => (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-border p-5 flex flex-col items-center gap-3"
    >
      <RefreshCw className="h-5 w-5 text-primary animate-spin" />
      <div className="w-full bg-surface-hover rounded-full h-2 overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.2 }}
        />
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs text-text-secondary">{progress}%</span>
        <button
          type="button"
          onClick={handleCancelUpload}
          className="text-xs text-text-disabled hover:text-error transition-colors"
        >
          Cancelar
        </button>
      </div>
    </motion.div>
  );

  const renderSuccess = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="rounded-xl border border-success/30 bg-success/5 p-5 flex flex-col items-center gap-3"
    >
      <div className="p-2 rounded-full bg-success/10">
        <Check className="h-5 w-5 text-success" />
      </div>
      <p className="text-sm font-medium text-text-primary">Upload concluído!</p>
      {uploadResponse && (
        <code className="text-xs text-text-disabled bg-surface rounded px-2 py-1 max-w-full truncate">
          {uploadResponse.url}
        </code>
      )}
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={openFileDialog}
          className="text-xs text-primary hover:underline"
        >
          Substituir
        </button>
        <button
          type="button"
          onClick={handleRemove}
          className="text-xs text-text-secondary hover:text-error transition-colors"
        >
          Remover
        </button>
      </div>
    </motion.div>
  );

  const renderError = () => (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-error/30 bg-error/5 p-5 flex flex-col items-center gap-3"
    >
      <div className="p-2 rounded-full bg-error/10">
        <AlertTriangle className="h-5 w-5 text-error" />
      </div>
      <p className="text-sm font-medium text-text-primary text-center">
        {error?.message || "Erro no upload."}
      </p>
      <div className="flex items-center gap-2">
        {file && (
          <button
            type="button"
            onClick={handleRetry}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium hover:bg-primary-hover transition-colors"
          >
            <RefreshCw className="h-3 w-3" /> Tentar novamente
          </button>
        )}
        <button
          type="button"
          onClick={openFileDialog}
          className="text-xs text-text-secondary hover:text-text-primary transition-colors"
        >
          Escolher outro arquivo
        </button>
        <button
          type="button"
          onClick={handleRemove}
          className="text-xs text-text-secondary hover:text-error transition-colors"
        >
          Remover
        </button>
      </div>
    </motion.div>
  );

  // ---- Render principal ----
  return (
    <div
      className={`media-uploader ${className}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <AnimatePresence mode="wait">
        {(status === "idle" || status === "dragging") && (
          <motion.div
            key="dropzone"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {renderDropZone()}
          </motion.div>
        )}

        {status === "preview" && (
          <motion.div
            key="preview"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {renderPreview()}
          </motion.div>
        )}

        {status === "uploading" && (
          <div key="progress">{renderProgress()}</div>
        )}

        {status === "success" && (
          <div key="success">{renderSuccess()}</div>
        )}

        {status === "error" && (
          <div key="error">{renderError()}</div>
        )}
      </AnimatePresence>

      {/* Input oculto */}
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={handleInputChange}
        disabled={disabled}
        aria-hidden="true"
      />
    </div>
  );
}
