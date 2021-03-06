## 0.5.2 (2021-07-30)

### Fix

* Added overwrite=True to the blob client upload for baselines (#60) [Natalia Maximo]


## 0.5.1 (2021-07-30)

### Changes

* Added more error checking for blob storage (#58) [Natalia Maximo]


## 0.5 (2021-07-30)

### New

* Implemented exclusion XPath feature  and added cookbook (#56) [Natalia Maximo]


## 0.4 (2021-07-27)

### New

* Added visual parity documentation (#53) [Natalia Maximo]

* Added blob storage plugin (#44) [Natalia Maximo]

* Added LocalStorage plugin for VisualParity (#42) [Natalia Maximo]

* Added run_id to reports and to the ctx object (#40) [Natalia Maximo]

* Added logic for visualparity validation (#39) [Natalia Maximo]

  note: since there is not yet a storage plugin, this validation will always be false

* Added --version cli arg (#33) [Natalia Maximo]

* Added VisualParity validation state, report, and reorganized validations (#37) [Natalia Maximo]

### Changes

* Set up the main running function to use handler functions (#45) [Natalia Maximo]

* Create the snapshot parent directory if it does not exist (#43) [Natalia Maximo]

* Added pre-commit fixes on all files that needed them (#31) [Natalia Maximo]

### Fix

* Removed extra comma in example "Validation.json" in README.md (#50) [rajeevdodda]

* Reverted to LocalStorage for VP integration test (#51) [Natalia Maximo]


## 0.3.1 (2021-07-09)

### Changes

* Document parser only after plugins run (#26) [Natalia Maximo]

### Fix

* Fixed doc pipeline and changelog generation (#25) [Natalia Maximo]


## 0.3 (2021-07-07)

### New

* Added logging (#18) [Natalia Maximo]

* Added pre-commit dev tool (#20) [Natalia Maximo]

### Changes

* Added doc generation pipeline (#17) [Natalia Maximo]

* Reorganized hookspecs (#19) [Natalia Maximo]

### Fix

* Typo in release pipeline file (#23) [Natalia Maximo]


## 0.2 (2021-06-29)

### New

* Added release pipeline workflow file (#15) [Natalia Maximo]

* Added pytest-quilla documentation (#11) [Natalia Maximo]

* Added test pipeline workflow file (#9) [Natalia Maximo]

* Added code analysis workflow file. [Natalia Maximo]

* Initial migration from ADO. [Natalia Maximo]

### Other

* Updated SUPPORT.md and setup file (#13) [Natalia Maximo]

* Update README.md. [Natalia Maximo]


## 0.1 (2021-06-28)

### Other

* SUPPORT.md committed. [Microsoft Open Source]

* SECURITY.md committed. [Microsoft Open Source]

* README.md committed. [Microsoft Open Source]

* LICENSE committed. [Microsoft Open Source]

* CODE_OF_CONDUCT.md committed. [Microsoft Open Source]

* Initial commit. [microsoft-github-operations[bot]]


