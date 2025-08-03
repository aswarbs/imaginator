import os
from PIL import Image

def save_to_all_same_names(new_image: Image.Image,
                           original_path: str,
                           root_dir: str,
                           extensions=None,
                           case_insensitive: bool = False,
                           make_backup: bool = True,
                           backup_suffix: str = ".bak"):
    """
    Overwrite every file under root_dir whose basename matches original_path's basename.
    Args:
        new_image: PIL Image to save.
        original_path: path of the source image (used for basename matching and format).
        root_dir: directory to traverse (recursively).
        extensions: iterable of allowed extensions (if None, infer from original and common ones).
        case_insensitive: if True, match filenames case-insensitively.
        make_backup: if True, rename existing target to target+backup_suffix before writing.
        backup_suffix: suffix to append for backups.
    Returns:
        List of paths written to.
    """
    if extensions is None:
        # Default to common image extensions plus original's
        extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    else:
        extensions = set(e.lower() for e in extensions)

    basename = os.path.basename(original_path)
    match_name = basename.lower() if case_insensitive else basename

    written = []
    # Determine format to save in (use original file's format if possible)
    _, orig_ext = os.path.splitext(original_path)
    save_format = None
    if orig_ext:
        save_format = Image.EXTENSION.get(orig_ext.lower())
    # Fallback: let PIL infer from filename when saving

    for root, _, files in os.walk(root_dir):
        for f in files:
            f_ext = os.path.splitext(f)[1].lower()
            if f_ext not in extensions:
                continue
            candidate = f.lower() if case_insensitive else f
            if candidate != match_name:
                continue
            target_path = os.path.join(root, f)
            try:
                if make_backup:
                    backup_path = target_path + backup_suffix
                    if not os.path.exists(backup_path):
                        os.replace(target_path, backup_path)
                    else:
                        # if backup already exists, overwrite target without additional backup
                        os.remove(target_path)
                # Save new image to target_path
                # Use same format as original if we resolved it, else let PIL decide by extension
                if save_format:
                    new_image.save(target_path, format=save_format)
                else:
                    new_image.save(target_path)
                written.append(target_path)
            except Exception as e:
                # You might want to log or collect failures separately
                print(f"Failed to write {target_path}: {e}")
    print("saved")
    return written
