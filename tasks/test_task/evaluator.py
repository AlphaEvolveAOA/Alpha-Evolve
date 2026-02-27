import subprocess
import sys

def evaluate(program_path):
    try:
        result = subprocess.run(
            [sys.executable, program_path],
            capture_output= True,
            text= True,
            timeout= 5
        )
    
        output = result.stdout.strip()
        
        if "AI" in output:
            return {"fitness": 10}
        else:
            return {"fitness": 1}
    
    except Exception:
        return {"fitness": 0}

    
    
    