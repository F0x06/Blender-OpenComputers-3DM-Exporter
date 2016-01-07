
## Blender-OpenComputers-3DM-Exporter<br/>Blender Minecraft OpenComputers 3DM (print3d) Exporter

[Official OpenComputers forum post](https://oc.cil.li/index.php?/topic/817-blender-3dm-print3d-exporter/)

### Copyright

Copyright (c) 2016 Kevin Velickovic<br />

Please read the [COPYRIGHT.md](COPYRIGHT.md) file for more information.

### Screenshots

![](http://image.noelshack.com/fichiers/2016/01/1452209866-20160107232850787.jpeg)
![](http://image.noelshack.com/fichiers/2016/01/1452209873-20160107233113573.jpeg)

### Requirements

This plugin requires Blender 2.76

### Installation

Install plugin:
* Open Blender
* Go in File > User Preferences > Addons tab
* Click on "Install from file" button.
* Browse and click the downloaded 3dm_exporter.py file and push the "Install from file..." button.

Activate plugin:
* Open Blender
* Go in File > User Preferences > Addons tab
* In the "Exporter" category, you must find "OpenComputers 3DM Exporter"
* Check it, and push "Save User Settings" button.

### Features

* Bounding boxes to view the build area ( 16 x 16 x 16 )
* Layers support, only export the active layer so you can easily create multi-part models
* Material name export in 3DM file

### Usage

* Create a model only with cubes, cubes sizes must be integers and the total area covered by cubes can be 16 x 16 x 16 units max, you can use the "Bounding box" option of the plugin to view the build area, goto Scene properties -> OpenComputers 3DM Exporter -> Bounding box, and push the "Add" button, and build only inside the bounding box

* Export you 3DM file, goto Scene properties -> OpenComputers 3DM Exporter and push the "Export" button, chose a destination file name, and push the "Export" button

* Import your 3DM file inside your computer in Minecraft, and use the "print3d" function to print your model, enjoy :]

* You can also use my web-based viewer to test you model at: http://f0x.me/OpenComputers-3D-Designer

### License

This program is licensed under the terms of the
[GNU Affero General Public License v3](http://www.gnu.org/licenses/agpl.html)
(GNU AGPL)

Please read the [COPYRIGHT.md](COPYRIGHT.md) file for more information.
