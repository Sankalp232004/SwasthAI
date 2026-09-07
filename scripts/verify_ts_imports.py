import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\home\OneDrive\Desktop\Startup\SwasthAI\website\src"
print(f"Scanning imports and exports across: {src_dir}\n")

# Collect all exports from all .ts and .tsx files
exports_by_module = {} # relative module path -> set of exported names

for root, _, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".ts") or f.endswith(".tsx"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, src_dir).replace("\\", "/")
            # remove .tsx or .ts
            mod_alias = "@/" + re.sub(r"\.tsx?$", "", rel_path)
            # also index without /index if index.ts
            mod_alias_no_index = re.sub(r"/index$", "", mod_alias)
            
            with open(full_path, "r", encoding="utf-8") as fp:
                content = fp.read()
            
            # Find all named exports: export function X, export const X, export type X, export interface X, export { X, Y }
            exported_names = set()
            for m in re.finditer(r"export\s+(?:async\s+)?(?:function|const|let|var|type|interface|class|enum)\s+([A-Za-z0-9_]+)", content):
                exported_names.add(m.group(1))
            
            for m in re.finditer(r"export\s*\{([^}]+)\}", content):
                names = [n.strip().split(" as ")[-1].strip() for n in m.group(1).split(",") if n.strip()]
                exported_names.update(names)
            
            if "export default" in content:
                exported_names.add("default")
            
            exports_by_module[mod_alias] = exported_names
            exports_by_module[mod_alias_no_index] = exported_names

print(f"Indexed {len(exports_by_module)} module paths.")

# Now check all imports across all files
issues = []
for root, _, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".ts") or f.endswith(".tsx"):
            full_path = os.path.join(root, f)
            rel_src = os.path.relpath(full_path, src_dir).replace("\\", "/")
            
            with open(full_path, "r", encoding="utf-8") as fp:
                content = fp.read()
            
            # Match imports like: import { A, B } from '@/lib/...'
            for m in re.finditer(r"import\s*\{([^}]+)\}\s*from\s*['\"]([^'\"]+)['\"]", content):
                imported_names = [n.strip().split(" as ")[0].strip() for n in m.group(1).split(",") if n.strip()]
                mod_path = m.group(2)
                
                if mod_path.startswith("@/"):
                    if mod_path not in exports_by_module:
                        issues.append(f"{rel_src}: Import from unknown module '{mod_path}'")
                    else:
                        available = exports_by_module[mod_path]
                        for name in imported_names:
                            if name.startswith("type "):
                                name = name[5:].strip()
                            if name not in available:
                                issues.append(f"{rel_src}: '{name}' is not exported by '{mod_path}'. Available: {sorted(list(available))}")

print(f"\nScan results: {len(issues)} issues found.")
for issue in issues:
    print(f"  ❌ {issue}")

if not issues:
    print("  ✅ All imports match exports across the entire website codebase!")
