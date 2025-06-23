#!/bin/bash

# Absolute paths
PCAP_DIR="/home/pooltab/Desktop/NetworkDatasetCreation/CEFlows"
CIC_DIR="/home/pooltab/Desktop/CIC_Testing/cicflowmeter/src"
VENV_ACTIVATE="/home/pooltab/Desktop/CIC_Testing/CICTestVenv/bin/activate"

# Activate virtual environment
source "$VENV_ACTIVATE"

# Change to CICFlowMeter src directory
cd "$CIC_DIR" || exit 1

# Process each .pcap file
for pcap_file in "$PCAP_DIR"/*.pcap; do
    # Get the base filename (no path, no extension)
    base_name=$(basename "$pcap_file" .pcap)

    # Define the output CSV path
    csv_file="$PCAP_DIR/${base_name}.csv"

    echo "Processing: $pcap_file → $csv_file"

    # Run the cicflowmeter command
    python3 -m cicflowmeter.sniffer -f "$pcap_file" -c "$csv_file"
done

echo "✅ All PCAPs processed."
