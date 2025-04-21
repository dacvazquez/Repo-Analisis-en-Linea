from huggingface_hub import snapshot_download

# Descarga el modelo PySentimiento
model_path = snapshot_download(
    repo_id="pysentimiento/robertuito-base-uncased",
    cache_dir="./pysentimiento_model",  # Carpeta donde se guardará el modelo
    ignore_patterns=["*.safetensors"],  # excluye archivos no necesarios
)

print(f"Modelo descargado en: {model_path}")