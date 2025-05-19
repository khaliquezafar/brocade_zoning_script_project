import csv
import os
import re

def read_csv(filepath):
    with open(filepath, mode="r", newline="") as f:
        reader = csv.reader(f)
        return list(reader)

def write_alias_script(data_rows, output_path):
    with open(output_path, mode="w") as f:
        f.write("#### FAB-A Aliases\n")
        for row in data_rows:
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                f.write(f'alicreate "{row[0].strip()}","{row[1].strip()}"\n')
        f.write("\n#### FAB-B Aliases\n")
        for row in data_rows:
            if len(row) >= 4 and row[2].strip() and row[3].strip():
                f.write(f'alicreate "{row[2].strip()}","{row[3].strip()}"\n')

def clean_alias_name(name):
    # Remove _Port1 or _Port2 from zone name construction
    return re.sub(r"_Port[12]$", "", name)

def write_combined_zoning_script(hosts, storage_name, storage_csv_path, output_path, cfgname_a, cfgname_b):
    targets = read_csv(storage_csv_path)[1:]
    fab_a_zones, fab_b_zones = [], []

    with open(output_path, mode="w") as f:
        f.write("##### FAB-A Zones\n")
        for host in hosts[1:]:
            if len(host) < 2:
                continue
            host_a = host[0].strip()
            if not host_a:
                continue
            for tgt in targets:
                if len(tgt) < 2:
                    continue
                tgt_a = tgt[0].strip()
                if tgt_a:
                    # Clean name in zone name only
                    zone = f'Z_{clean_alias_name(host_a)}_{clean_alias_name(tgt_a)}'
                    fab_a_zones.append(zone)
                    f.write(f'zonecreate "{zone}","{host_a};{tgt_a}"\n')

        f.write("\n##### FAB-B Zones\n")
        for host in hosts[1:]:
            if len(host) < 2:
                continue
            host_b = host[1].strip()
            if not host_b:
                continue
            for tgt in targets:
                if len(tgt) < 2:
                    continue
                tgt_b = tgt[1].strip()
                if tgt_b:
                    zone = f'Z_{clean_alias_name(host_b)}_{clean_alias_name(tgt_b)}'
                    fab_b_zones.append(zone)
                    f.write(f'zonecreate "{zone}","{host_b};{tgt_b}"\n')

        f.write("\n##### FAB-A cfgadd \n")
        for z in fab_a_zones:
            f.write(f'cfgadd "{cfgname_a}","{z}"\n')
        if fab_a_zones:
            f.write("cfgsave\n")
            f.write(f'cfgenable "{cfgname_a}"\n')

        f.write("\n##### FAB-B cfgadd \n")
        for z in fab_b_zones:
            f.write(f'cfgadd "{cfgname_b}","{z}"\n')
        if fab_b_zones:
            f.write("cfgsave\n")
            f.write(f'cfgenable "{cfgname_b}"\n')

    print(f"✅ Zoning and cfgadd script saved to {output_path}")

def list_storage_csv_files(storage_data_dir):
    return [f for f in os.listdir(storage_data_dir) if f.startswith("storage_") and f.endswith(".csv")]

def main():
    site = input("Enter site name (HRC/KCA): ").strip().upper()
    if site not in ["HRC", "KCA"]:
        print("❌ Invalid site. Must be HRC or KCA.")
        return
    hosts_data_dir = f"../data/{site}/hosts"
    storage_data_dir = f"../data/{site}/storage"
    results_dir = f"../results/{site}"
    os.makedirs(results_dir, exist_ok=True)

    cfgname_a = "ZSSW2_48000" if site == "HRC" else "ZSSW3_48000"
    cfgname_b = "ZSSW1_48000" if site == "HRC" else "ZSSW4_48000"

    if input("Do you want to create aliases? (yes/no): ").strip().lower() == "yes":
        alias_file = os.path.join(hosts_data_dir, "aliases_wwpn.csv")
        if not os.path.exists(alias_file):
            print(f"❌ File not found: {alias_file}")
        else:
            rows = read_csv(alias_file)
            if len(rows[0]) >= 4:
                write_alias_script(rows[1:], os.path.join(results_dir, "alias_script.txt"))
                print(f"✅ Alias script saved to {results_dir}/alias_script.txt")
            else:
                print("❌ aliases.csv must have at least 4 columns.")
        return

    if input("Do you want to create zones? (yes/no): ").strip().lower() == "yes":
        host_alias_file = os.path.join(hosts_data_dir, "host_aliases.csv")
        if not os.path.exists(host_alias_file):
            print(f"❌ File not found: {host_alias_file}")
            return

        storage_files = list_storage_csv_files(storage_data_dir)
        if not storage_files:
            print(f"❌ No storage CSV files found in {storage_data_dir}")
            return

        print("\nAvailable Storage Systems:")
        for idx, fname in enumerate(storage_files):
            print(f"{idx + 1}. {fname.replace('storage_', '').replace('.csv', '')}")

        selected = input("Enter the numbers of the storage systems to use (comma-separated): ").strip()
        selected_indices = [int(i) - 1 for i in selected.split(",") if i.strip().isdigit()]

        hosts = read_csv(host_alias_file)

        for idx in selected_indices:
            if 0 <= idx < len(storage_files):
                fname = storage_files[idx]
                storage_name = fname.replace("storage_", "").replace(".csv", "")
                storage_path = os.path.join(storage_data_dir, fname)
                output_path = os.path.join(results_dir, f"zoning_{storage_name}.txt")

                write_combined_zoning_script(hosts, storage_name, storage_path, output_path, cfgname_a, cfgname_b)
            else:
                print(f"⚠️ Invalid index: {idx + 1}")

if __name__ == "__main__":
    main()
