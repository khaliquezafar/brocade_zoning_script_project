# 🧰 CIT Storage & Backup (ENGCLOUD) SAN Zoning Script Generator 

This Python script automates the creation of `alicreate`, `zonecreate`, and `cfgadd` commands for Brocade SAN zoning configuration. It supports multi-site zoning (e.g., HRC, KCA), dynamic alias and zone file selection, and generate zoning script for multiple storages in the environment. This script is created for ENGCLOUD SAN fabric and storage environment however, can be adjusted for any environment as the input is dynamically configured.
---

## 📁 Directory Structure

```
engcloud_zoning_script_generator/
├── data/
│   ├── HRC/
│   │   ├── cfg/
│   │   │   └── cfg.csv               
│   │   ├── hosts/
│   │   │   ├── aliases_wwpn.csv
│   │   │   └── host_aliases_pl1.csv
│   │   └── storage/
│   │       └── storage_unity1.csv
│   ├── KCA/
│   │   ├── cfg/
│   │   │   └── cfg.csv          
│   │   ├── hosts/
│   │   │   ├── aliases_wwpn.csv
│   │   │   └── host_aliases_pl1.csv
│   │   └── storage/
│   │       └── storage_unity1.csv
├── results/
│   └── HRC/
│       ├── alias_script.txt
│       └── zoning_<storage>.txt
│   └── KCA/
│       ├── alias_script.txt
│       └── zoning_<storage>.txt
├── results/
|       ├── zoning_script.py
```

---

## 📄 cfg.csv Format

Each `cfg.csv` file must contain a single row with two columns:

| FAB-A CFG Name | FAB-B CFG Name |
|----------------|----------------|
| ZSSW2_48000     | ZSSW1_48000     |   ← for `HRC`

---

## 🔢 Example CSV Inputs

### `aliases_wwpn.csv`
```csv
host_fab_a_alias,host_fab_a_wwpn,host_fab_b_alias,host_fab_b_wwpn
HST01_A,10:00:00:00:00:00:00:01,HST01_B,20:00:00:00:00:00:00:01
HST02_A,10:00:00:00:00:00:00:02,HST02_B,20:00:00:00:00:00:00:02
```

### `host_aliases_hrc.csv`
```csv
HST01_A,HST01_B
HST02_A,HST02_B
```

### `storage_unity1.csv`
```csv
target_fab_a_wwpn,target_fab_b_wwpn
50:00:00:00:00:00:00:01,60:00:00:00:00:00:00:01
50:00:00:00:00:00:00:02,60:00:00:00:00:00:00:02
```

---

## 🚀 How to Run the Script

### On Windows Command Prompt / PowerShell/ Linux CLI and sample run

```bash
cd path\to\engcloud_zoning_script_generator\scripts
python zoning_script.py
Enter site name (HRC/KCA): KCA
Do you want to create aliases? (yes/no): no
Do you want to create zones? (yes/no): yes

Available Host Alias Files:
1. PL2
Select the host alias file number: 1

Available Storage Systems:
1. KCA_UNITY_Hybrid-01
2. KCA_UNITY_Hybrid-02
Enter the numbers of the storage systems to use (comma-separated): 1
✅ Zoning and cfgadd script saved to ../results/KCA\zoning_KCA_UNITY_Hybrid-01.txt

```

### 🧑‍💻 Interactive Prompts

1. Enter site name → `HRC` or `KCA`
2. Create aliases? → `yes` or `no`
3. Create zones? → `yes` or `no`
4. Select `host_aliases_*.csv` file
5. Select one or more `storage_*.csv` files

---

## ✅ Output Files

Saved in:

```
results/HRC/
├── alias_script.txt            # alicreate commands
└── zoning_unity1.txt           # zonecreate + cfgadd + cfgenable

results/KCA/
├── alias_script.txt            # alicreate commands
└── zoning_unity1.txt           # zonecreate + cfgadd + cfgenable
```

---

## 📌 Notes

- Supports multiple host and storage profiles.
- Reads fabric names dynamically from `cfg.csv`.

---

## 👨‍💻 Author

Khalique Zafar

Created for automated dual-fabric SAN zoning configuration in datacenters.
