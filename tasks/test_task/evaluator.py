import importlib.util

def evaluate(program_path):
    try:
        # Load the candidate program as a module
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call the greet() function directly
        output = module.greet()

        # Convert to string just in case
        output = str(output)

        if "AI" in output:
            return {"fitness": 10}
        else:
            return {"fitness": 1}

    except Exception as e:
        print("Evaluation error:", e)
        return {"fitness": 0}