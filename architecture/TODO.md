# TODO

## PlatformValidator

- [ ] config.yaml (root dir) should be of type as given in architecture
```yaml
PlatformParser:
  Atcoder:
    no_of_problems: 5
    ...
  Codeforces:
    no_of_problems: 5
    ...
GlobalConfig:
  ...
```
- [ ] Implement `configParser.py` to parse yaml and return the config [also if config does not exists return some default values]
    - [ ] Will check if config is available and all the required fields are present
- [ ] Implement `PlatformValidator.py`
    - [ ] Check the Pascal Case for classname and relation with file name (Atcoder.py -> AtcoderParser)
    - [ ] Check all elements are initalized in constructor
    - [ ] Check all the functions are implemented

    
    