# Exact original Dynamic World TIFF transfer parts

These six archives transfer the two missing annual TIFF exports without another Earth Engine run. They are byte fragments, not six independently readable images.

Extract all six ZIPs into ONE directory. Each ZIP contains one distinct .bin part plus identical REASSEMBLY.json, reassemble.py and this README. Keep one identical copy of each shared helper. Run python reassemble.py in that directory. It verifies every part and both complete TIFF SHA256 hashes.

Then perform the actual annual-raster checks and historical imagery review described in UrbanHeat-DynamicWorld-Export-Review-2026-10-07.md. Keep the original analysis and historical thresholds unchanged. The primary common coverage remains 30.94%, below the provisional 50% gate. Do not infer general urban change or classify missing/border pixels as water or absence of vegetation. Do not claim scientific validation merely from successful reconstruction.

No repository publication, analysis rerun or hackathon submission was performed in creating these transfer files.
