# TODO

## PlatformValidator

- [x] config.json (root dir) should be of type as given in architecture
```json
{
  "PlatformParser": [
    "Atcoder" : {
      "required": {
        "language_extension": "cpp",
        "...": "..."
      },
      "optional": {
        "file_path": "temp/",
        "...": "..."
      },
    },
    "Codeforces": {
      "required": {
        "language_extension": "cpp",
        "...": "..."
      },
      "optional": {
        "file_path": "temp/",
        "...": "..."
      },
    }
  ]
}
```
- [x] Implement `configParser.py` to parse json and return the config [also if config does not exists return some default values]
    - [x] Will check if config is available and all the required fields are present
- [x] Implement `PlatformValidator.py`
    - [x] Check the Pascal Case for classname and relation with file name (Atcoder.py -> AtcoderParser)
    - [x] Check all elements are initalized in constructor
    - [x] Check all the functions are implemented

- [x] replace exit() with sys.exit()
    