# 📁 Uploads, CMS & SEO — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.media`

---

## 1. Visão Geral

Sistema completo de uploads, CMS block-based e SEO avançado com Storage Provider Pattern. O proprietário administra 100% do conteúdo sem desenvolvedor.

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Storage Provider Pattern** | `StorageProvider` ABC. S3→R2→GCS via config. Zero alteração de código |
| **2** | **Image Processing Pipeline** | Validate → strip EXIF → resize → thumbnail → WebP → hash filename |
| **3** | **Block-Based CMS** | Páginas JSONB compostas de blocos (hero, text, image, CTA, gallery) |
| **4** | **Media Dedup** | SHA-256 content hash. Upload duplicado = retorna existente |
| **5** | **SEO Score Analyzer** | Analisa página e sugere melhorias com score 0-100 |

---

## 2. Storage Provider Pattern

```
StorageProvider (ABC)
├── LocalStorageProvider    → dev (./media/)
├── S3StorageProvider       → AWS S3
├── R2StorageProvider       → Cloudflare R2
├── GCSStorageProvider      → Google Cloud Storage (planejado)
└── AzureBlobStorageProvider → Azure (planejado)
```

### Como Trocar de Provedor

```python
# Configuração (settings.py ou .env)
STORAGE_PROVIDER = "r2"  # "local" | "s3" | "r2"

# Código — NUNCA muda
provider = StorageProviderFactory.create(settings.STORAGE_PROVIDER)
url = await provider.upload(file_data, path, mime_type)
```

---

## 3. Pipeline de Upload

```
1. Validate (extensão whitelist, MIME type, tamanho < 10MB)
2. Compute SHA-256 hash
3. Check duplicate (mesmo hash = mesmo arquivo)
4. Generate unique filename ({hash[:16]}.{ext})
5. Process image (strip EXIF, resize 2000px, thumbnail 400px, WebP)
6. Upload to storage ({tenant_id}/{filename})
7. Create MediaAsset record
```

---

## 4. CMS Block-Based

Páginas são compostas de blocos:

```json
{
  "slug": "home",
  "title": "Home",
  "blocks": [
    {"block_type": "hero", "data": {"title": "Bem-vindo", "subtitle": "...", "cta": "Agende"}, "order": 0},
    {"block_type": "services", "data": {"service_ids": ["s1", "s2"]}, "order": 1},
    {"block_type": "team", "data": {"staff_ids": ["p1", "p2"]}, "order": 2},
    {"block_type": "cta", "data": {"text": "Agende agora", "url": "/booking"}, "order": 3}
  ]
}
```

---

## 5. Segurança dos Uploads

| Mecanismo | Descrição |
|-----------|-----------|
| **Whitelist extensões** | `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.svg`, `.bmp` |
| **Whitelist MIME** | `image/jpeg`, `image/png`, `image/webp`, etc. |
| **Limite tamanho** | 10 MB por arquivo |
| **Hash anti-duplicata** | SHA-256. Mesmo arquivo = retorna existente |
| **Strip EXIF** | Remove metadados (GPS, camera, etc.) |
| **Nome único** | Hash no filename. Sem path traversal |
| **Isolamento tenant** | `/{tenant_id}/` prefix |
