import os
import time

def take_screenshot(driver, folder, step_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_path = os.path.join("screenshots", folder)
    os.makedirs(folder_path, exist_ok=True)
    path = os.path.join(folder_path, f"{timestamp}_{step_name}.png")
    driver.save_screenshot(path)
    print(f"[CAPTURA] Guardada: {path}")
