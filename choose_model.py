import requests

MODELS_URL = "https://raw.githubusercontent.com/mohammadhlm/models/main/models.txt"

def fetch_models_table(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching the file:", e)
        return None

def parse_table(table_text):
    models = []
    lines = table_text.splitlines()
    for line in lines:
        line = line.strip()
        # Process only the lines that start with the vertical bar
        if not line.startswith("│"):
            continue
        # Remove the leading and trailing vertical bars and split by "│"
        parts = line.strip("│").split("│")
        cols = [col.strip() for col in parts]
        # Expecting columns in the order: repo, file, params, size
        if len(cols) >= 4:
            model = {
                "repo": cols[0],
                "filename": cols[1],
                "params": cols[2],
                "size": cols[3]
            }
            models.append(model)
    return models

def generate_model_id(filename):
    # Extract model_base from the filename (before the first dot)
    if '.' in filename:
        base = filename.split('.')[0]
    else:
        base = filename
    return base.title() + "-GGUF"

def parse_size(size_str):
    # Convert size string (e.g., "1217752864") from bytes to GB
    try:
        size_bytes = float(size_str)
        size_gb = size_bytes / (1024 ** 3)
        return size_gb
    except:
        return None

def parse_params(params_str):
    # Convert parameter string like "8B" or "1.5B" to a float representing billions.
    try:
        if not params_str:
            return None
        if params_str.upper().endswith("B"):
            num_str = params_str[:-1]
            return float(num_str)
        return float(params_str)
    except:
        return None

def cpu_param_limit(cpu_cores):
    # Define the maximum allowed parameters (in billions) based on number of CPU cores.
    try:
        cores = float(cpu_cores)
    except:
        cores = 0
    if cores < 4:
        return 2.0
    elif cores < 8:
        return 8.0
    else:
        return float('inf')

def select_best_model(models, max_ram_gb, cpu_cores):
    best_model = None
    best_params = -1
    limit_params = cpu_param_limit(cpu_cores)
    for model in models:
        size_gb = parse_size(model.get("size", "0"))
        # Skip if size cannot be parsed or exceeds the available RAM.
        if size_gb is None or size_gb > max_ram_gb:
            continue
        # Check the parameter count
        param_val = parse_params(model.get("params", ""))
        if param_val is None:
            continue
        if param_val > limit_params:
            continue
        # Select the model with the highest parameter count among eligible models
        if param_val > best_params:
            best_params = param_val
            best_model = model
    return best_model

def main():
    table_text = fetch_models_table(MODELS_URL)
    if not table_text:
        return

    models = parse_table(table_text)
    if not models:
        print("No models found.")
        return

    try:
        max_ram = float(input("Enter available RAM (in GB): "))
    except ValueError:
        print("RAM must be a number.")
        return

    try:
        cpu_cores = float(input("Enter number of CPU cores: "))
    except ValueError:
        print("CPU cores must be a number.")
        return

    best = select_best_model(models, max_ram, cpu_cores)
    if best is None:
        print("No model found with the given specifications.")
        return

    repo = best["repo"]
    filename = best["filename"]
    model_id = generate_model_id(filename)
    final_str = f"hf:{repo}/{model_id}:{filename}"
    print("\nFinal model identifier:")
    print(final_str)

    # Save the chosen model identifier to a file so that the Bash script can use it.
    try:
        with open("chosen_model.txt", "w") as f:
            f.write(final_str)
        print("\nModel identifier saved to chosen_model.txt")
    except Exception as e:
        print("Error saving the model identifier:", e)

if __name__ == "__main__":
    main()