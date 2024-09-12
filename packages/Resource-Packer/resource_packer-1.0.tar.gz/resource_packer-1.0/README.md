# AssetPacker
A commandline tool to automatically package assets into your source code.

---

## Commandline

### Installation
Install the python package via pip: `pip install Resource-Packer`

### Arguments
| Argument | Description |
| --- | --- |
| -output | Path to source files to generate. This include the filename. |
| -include | List of directories containing assets to include in the package. |

### Example
Packaging all assets from `/Source/Assets` into `../GameAssets.hpp` and `../GameAssets.cpp`<br>
`assetpack -output ../GameAssets -include /Source/Assets`

## CMake

### Installation
Include this repository in your source. Include `AssetPacker.cmake` in your cmake structure.

### Example
Packaging all assets from `/Assets` and use them in our `MyGame` target<br>
```
include(AssetPacker/AssetPacker.cmake)
add_executable(MyGame main.cpp)

pack_assets(MyGame "/Assets" "/Source")
```
