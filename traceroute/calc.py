import numpy as np

sv1 = [34, 33, 33]
sv2 = [216, 31, 112]
sv3 = [32, 29, 29]

jp1 = [249, 249, 259]
jp2 = [251, 249, 250]
jp3 = [252, 250, 249]

print("Mean | Std:")
print(f"sv1: {np.mean(sv1):.2f} | {np.std(sv1, ddof=1):.2f}")
print(f"sv2: {np.mean(sv2):.2f} | {np.std(sv2, ddof=1):.2f}")
print(f"sv3: {np.mean(sv3):.2f} | {np.std(sv3, ddof=1):.2f}")
print(f"jp1: {np.mean(jp1):.2f} | {np.std(jp1, ddof=1):.2f}")
print(f"jp2: {np.mean(jp2):.2f} | {np.std(jp2, ddof=1):.2f}")
print(f"jp3: {np.mean(jp3):.2f} | {np.std(jp3, ddof=1):.2f}")
