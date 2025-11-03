#!/usr/bin/env python3
import os, yaml, sys, json

def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def validate_cis_baseline(cis_data):
    min_score = cis_data.get("min_compliance_score", 0)
    if min_score < 85:
        print(f"[FAIL] Minimum compliance score too low: {min_score}")
        return False
    print(f"[OK] CIS Baseline Version: {cis_data['version']}, Min Score: {min_score}")
    return True

def validate_cve_thresholds(cve_data):
    if cve_data["allow_critical"] != 0:
        print("[FAIL] Critical CVEs allowed — must be 0.")
        return False
    print("[OK] CVE Thresholds — No criticals allowed, policy version:", cve_data["cve_policy_version"])
    return True

def validate_base_images(base_data):
    required_os = ["ubuntu", "rhel", "amazonlinux"]
    for os_name in required_os:
        if os_name not in base_data:
            print(f"[FAIL] Missing base image policy for {os_name}")
            return False
    print("[OK] Approved base image policies present for Ubuntu, RHEL, and Amazon Linux.")
    return True

if __name__ == "__main__":
    base_dir = "policies"
    cis_data = load_yaml(os.path.join(base_dir, "cis-baseline.yml"))
    cve_data = load_yaml(os.path.join(base_dir, "cve-thresholds.yml"))
    base_data = load_yaml(os.path.join(base_dir, "approved-base-images.yml"))

    all_valid = (
        validate_cis_baseline(cis_data)
        and validate_cve_thresholds(cve_data)
        and validate_base_images(base_data)
    )

    if not all_valid:
        print("\n❌ Policy validation failed — build blocked.")
        sys.exit(1)
    else:
        print("\n✅ All governance policies validated successfully.")
