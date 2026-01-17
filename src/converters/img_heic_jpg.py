
from PIL import Image
import pillow_heif
from pathlib import Path
import piexif

# Enable HEIC support
pillow_heif.register_heif_opener()

INPUT_ROOT = Path("D:\\Personeel\\Images\\Indu\\g-drive")
OUTPUT_ROOT = Path("D:\\Personeel\\Images\\Indu\\g-drive")

def convert_heic_best_quality(input_root: Path, output_root: Path):
    for heic_file in input_root.rglob("*.heic"):
        relative_path = heic_file.relative_to(input_root)
        output_file = output_root / relative_path.with_suffix(".jpg")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_file.exists():
            print(f"Skipping (exists): {output_file}")
            continue

        try:
            heif = pillow_heif.open_heif(heic_file)
            img = Image.frombytes(
                heif.mode,
                heif.size,
                heif.data,
                "raw",
                heif.mode,
                heif.stride,
            )

            # Preserve EXIF if available
            exif_bytes = None
            if "exif" in heif.info:
                exif_bytes = heif.info["exif"]

            img.save(
                output_file,
                "JPEG",
                quality=100,        # Max quality
                subsampling=0,      # No chroma subsampling (VERY IMPORTANT)
                optimize=False,     # Avoid recompression tricks
                exif=exif_bytes
            )

            print(f"✔ Converted (max quality): {output_file}")

        except Exception as e:
            print(f"✖ Failed: {heic_file} ({e})")

if __name__ == "__main__":
    convert_heic_best_quality(INPUT_ROOT, OUTPUT_ROOT) 
    print("✅ Conversion complete — quality preserved")

