#!/usr/bin/env python3
"""statediff.py — which ancestor states changed fate between two versions of LENS.md.
Run:  python3 statediff.py OLD_LENS.md NEW_LENS.md ancestry_manifest.json
Each LENS.md needs its LENS_META.md beside it. Prints every state whose fate moved, then the count.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_recall import classify
a, _, _ = classify(sys.argv[1], sys.argv[3]); b, _, _ = classify(sys.argv[2], sys.argv[3])
moves = [(k, a[k], b[k]) for k in a if a[k] != b[k]]
for k, x, y in moves: print(k, x, "->", y)
print(f"moves={len(moves)}")
