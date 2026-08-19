from PIL import Image
import numpy as np

path = r"C:\Users\syeda012\.cursor\projects\c-Users-syeda012-projects-rym-work-ifp-frequency-cap-tests\assets\c__Users_syeda012_AppData_Roaming_Cursor_User_workspaceStorage_d7982efdbaf5229bbe2543ad2c759976_images_image-2b04b977-c9b2-4a76-b6cf-ec8ba129e3cd.png"
arr = np.array(Image.open(path).convert("RGB"))
h, w = arr.shape[:2]


def is_red(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    return r > 70 and g < 55 and b < 55


print("--- strong vertical transitions avg y 50-560 ---")
for x in range(1, w - 1):
    diffs = []
    for y in range(50, 560, 5):
        if is_red(arr[y, x]) or is_red(arr[y, x + 1]):
            continue
        diffs.append(abs(int(arr[y, x].mean()) - int(arr[y, x + 1].mean())))
    if not diffs:
        continue
    avg = sum(diffs) / len(diffs)
    if avg > 10:
        print(f"x={x}/{x+1} avg_diff={avg:.1f}")

print("\n--- panel split: brightest row mean in center x=280-680 ---")
best = None
for y in range(300, 420):
    row = arr[y, 280:680]
    mask = np.array([not is_red(p) for p in row])
    if mask.sum() < 200:
        continue
    m = row[mask].mean()
    if best is None or m > best[0]:
        best = (m, y)
print(f"brightest tab row y={best[1]} mean={best[0]:.1f}")

for y in range(338, 350):
    m = arr[y, 280:680].mean()
    print(f"y={y} mean={m:.1f}")
