import os
import itertools

class ImageLoader:
    def __init__(self, directory, extensions=None, recursive=True):
        if extensions is None:
            extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
        self.directory = directory
        self.extensions = tuple(e.lower() for e in extensions)
        self.recursive = recursive
        self._build_cycle()

    def _gather_paths(self):
        paths = []
        seen_names = set()
        if self.recursive:
            for root, _, files in os.walk(self.directory):
                for f in sorted(files):
                    if f.lower().endswith(self.extensions):
                        name = f  # keep case-sensitivity; use f.lower() if you want case-insensitive dedupe
                        if name in seen_names:
                            continue
                        full = os.path.join(root, f)
                        paths.append(full)
                        seen_names.add(name)
        else:
            for f in sorted(os.listdir(self.directory)):
                if f.lower().endswith(self.extensions):
                    name = f
                    if name in seen_names:
                        continue
                    full = os.path.join(self.directory, f)
                    if os.path.isfile(full):
                        paths.append(full)
                        seen_names.add(name)
        return paths


    def _build_cycle(self):
        self.paths = self._gather_paths()
        if not self.paths:
            raise ValueError(f"No images found in {self.directory} with extensions {self.extensions}")
        self._cycle = itertools.cycle(self.paths)
        self.current = None

    def next_image_path(self):
        # if underlying filesystem might have changed, you can rebuild before cycling:
        # self._build_cycle()
        self.current = next(self._cycle)
        return self.current

    def refresh(self):
        """Re-scan the directory tree and rebuild the cycle (preserving position not guaranteed)."""
        self._build_cycle()

    def get_all_paths(self):
        return list(self.paths)
