import re
import sys

def update_buildozer_requirements(requirements_file, spec_file):
    try:
        with open(requirements_file, 'r') as f:
            extra_requirements = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {requirements_file}")
        sys.exit(1)

    extra_req_string = ",".join(extra_requirements)
    base_req = "python,kivy,webview-android,pywebview,pysdl2"

    try:
        with open(spec_file, 'r') as f:
            spec_lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {spec_file}")
        sys.exit(1)

    updated = False
    new_spec_lines = []

    for line in spec_lines:
        if line.strip().startswith('requirements ='):
            new_line = f"requirements = {base_req}"
            if extra_req_string:
                new_line += f",{extra_req_string}"
            new_line += "\n"
            new_spec_lines.append(new_line)
            updated = True
        else:
            new_spec_lines.append(line)

    if not updated:
        print("⚠️ 'requirements =' line not found, appending at the end.")
        line = f"requirements = {base_req}"
        if extra_req_string:
            line += f",{extra_req_string}"
        new_spec_lines.append(line + "\n")

    with open(spec_file, 'w') as f:
        f.writelines(new_spec_lines)

    print(f"✅ Updated '{spec_file}' with extra requirements from '{requirements_file}'")

if __name__ == "__main__":
    update_buildozer_requirements("build-recipes.txt", "buildozer.spec")
