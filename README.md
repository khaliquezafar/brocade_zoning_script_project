# 🧰 SAN Zoning Script Generator 

This Python script automates the creation of `alicreate`, `zonecreate`, and `cfgadd` commands for Brocade SAN zoning configuration. It supports multi-site zoning (e.g., site1, site2), dynamic alias and zone file selection, and generate zoning script for multiple storages in the environment. This script is created for SAN fabric and storage environment however, can be adjusted for any environment as the input is dynamically configured.
---

## 📁 Directory Structure

```
SAN_zoning_script_generator/
├── data/
│   ├── site1/
│   │   ├── cfg/
│   │   │   └── cfg.csv               
│   │   ├── hosts/
│   │   │   ├── aliases_wwpn.csv
│   │   │   └── host_aliases_pl1.csv
│   │   └── storage/
│   │       └── storage_unity1.csv
│   ├── site2/
│   │   ├── cfg/
│   │   │   └── cfg.csv          
│   │   ├── hosts/
│   │   │   ├── aliases_wwpn.csv
│   │   │   └── host_aliases_host_clus01.csv
│   │   └── storage/
│   │       └── storage01.csv
├── results/
│   └── site1/
│       ├── alias_script.txt
│       └── zoning_<storage>.txt
│   └── sit2/
│       ├── alias_script.txt
│       └── zoning_<storage>.txt
---

## 📄 cfg.csv Format

Each `cfg.csv` file must contain a single row with two columns:

| FAB-A CFG Name | FAB-B CFG Name |
|----------------|----------------|
| zone_cfg01     | zone_cfg02     |  

---

## 🔢 Example CSV Inputs

### `aliases_wwpn.csv`
```csv
host_fab_a_alias,host_fab_a_wwpn,host_fab_b_alias,host_fab_b_wwpn
HST01_A,10:00:00:00:00:00:00:01,HST01_B,20:00:00:00:00:00:00:01
HST02_A,10:00:00:00:00:00:00:02,HST02_B,20:00:00:00:00:00:00:02
```

### `host_aliases_host_clus01.csv`
```csv
HST01_A,HST01_B
HST02_A,HST02_B
```

### `storage01.csv`
```csv
target_fab_a_wwpn,target_fab_b_wwpn
50:00:00:00:00:00:00:01,60:00:00:00:00:00:00:01
50:00:00:00:00:00:00:02,60:00:00:00:00:00:00:02
```

---

## 🚀 How to Run the Script

### On Windows Command Prompt / PowerShell/ Linux CLI and sample run

```bash
cd path\to\SAN_zoning_script_generator\scripts
python zoning_script.py
Enter site name (site1/site1): site2
Do you want to create aliases? (yes/no): no
Do you want to create zones? (yes/no): yes

Available Host Alias Files:
1. host_clus01
Select the host alias file number: 1

Available Storage Systems:
1. storage01
2. storage02
Enter the numbers of the storage systems to use (comma-separated): 1
✅ Zoning and cfgadd script saved to ../results/site2\zoning_storage01.txt

```

### 🧑‍💻 Interactive Prompts

1. Enter site name → `site1` or `site2`
2. Create aliases? → `yes` or `no`
3. Create zones? → `yes` or `no`
4. Select `host_aliases_*.csv` file
5. Select one or more `storage*.csv` files

---

## ✅ Output Files

Saved in:

```
results/site1/
├── alias_script.txt            # alicreate commands
└── zoning_storage01.txt           # zonecreate + cfgadd + cfgenable

results/site2/
├── alias_script.txt            # alicreate commands
└── zoning_storage01.txt           # zonecreate + cfgadd + cfgenable
```

---

## 📌 Notes

- Supports multiple host and storage profiles.
- Reads fabric names dynamically from `cfg.csv`.

---

## 👨‍💻 Author

Khalique Zafar

Created for automated dual-fabric SAN zoning configuration in datacenters.
