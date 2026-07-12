"""
Pull critical datasets for QuantumPilot AI
- phanerozoic/qiskit-calibration-drift (8.04M rows) -> sample for dev
- weiyouLiao S-ZNE repo
- nvidia/QCalEval
"""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATASET_ROOT = ROOT / "datasets"

print("=== 1. Pulling calibration-drift (sample 100k rows) ===")
try:
    from datasets import load_dataset
    # Stream and take first 100k to avoid OOM
    ds = load_dataset("phanerozoic/qiskit-calibration-drift", split="train", streaming=True)
    # Take 100k
    sample = []
    for i, row in enumerate(ds):
        sample.append(row)
        if i % 10000 == 0:
            print(f"  {i} rows fetched...")
        if i >= 99999:
            break
    import pandas as pd
    df = pd.DataFrame(sample)
    print(f"Sample shape: {df.shape}")
    print(df.head())
    df.to_parquet(DATASET_ROOT / "calibration_drift" / "drift_sample_100k.parquet")
    df.to_csv(DATASET_ROOT / "calibration_drift" / "drift_sample_100k.csv", index=False)
    print("Saved drift_sample_100k")
    
    # Also get statistics for NeuralUCB context
    print("\nBackend distribution:")
    print(df['backend'].value_counts().head())
    print("\nProperty_family distribution:")
    print(df['property_family'].value_counts().head(10))
    
except Exception as e:
    print(f"Error pulling drift: {e}")
    import traceback; traceback.print_exc()

print("\n=== 2. Pulling S-ZNE repo via git ===")
try:
    import subprocess
    szne_path = DATASET_ROOT / "szne" / "repo"
    if not szne_path.exists():
        subprocess.run(["git", "clone", "https://github.com/weiyouLiao/Sample-efficient-quantum-error-mitigation-via-classical-learning-surrogates.git", str(szne_path)], check=True)
        print(f"Cloned to {szne_path}")
    else:
        print(f"Already exists at {szne_path}")
        # pull
        subprocess.run(["git", "-C", str(szne_path), "pull"], check=True)
    # Copy our live calibration into szne for comparison
    import shutil, glob
    for f in glob.glob("/home/user/ibm_*_qubits_full.csv"):
        shutil.copy(f, DATASET_ROOT / "calibration_drift" / Path(f).name)
        print(f"Copied {f}")
except Exception as e:
    print(f"Error cloning S-ZNE: {e}")

print("\n=== 3. Pulling QCalEval (243 rows) ===")
try:
    from datasets import load_dataset
    ds = load_dataset("nvidia/QCalEval", split="test")
    print(f"QCalEval size: {len(ds)}")
    df = ds.to_pandas()
    df.to_parquet(DATASET_ROOT / "qcaleval" / "qcaleval.parquet")
    print("Saved QCalEval")
    print(df[['id','experiment_type']].head())
except Exception as e:
    print(f"Error QCalEval: {e}")

print("\n=== Done ===")
