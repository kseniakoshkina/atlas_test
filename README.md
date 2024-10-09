# Atlas Test Task
## msi_finder.py
usage for the microsatellite stability analysis (returns Stable or Unstable):
```bash
python3 msi_finder.py -f analyze_microsatellite_stability str1.tsv test_vector.txt
```

usage for the calculation of microsatellite stability probability (returns the probability that the microsatellite is Unstable):
```bash
python3 msi_finder.py -f find_probability str1.tsv test_vector.txt
```

## artifacts_detection.py
usage for the collection of real SNVs without artifacts (returns Detected Samples and SNVs):
```bash
python3 artifacts_detection.py snv_sample.tsv
```
