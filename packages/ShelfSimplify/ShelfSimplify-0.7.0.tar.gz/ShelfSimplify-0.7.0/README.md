------------Shelf_Simplify------------

Author : B.Arun Kumar(ArunProgrammer)

This package could be used to perform low or medium level file management operations
, and file automation because this package has 13 functions simplified in it, and they are -

_-------------------------------------_

1)Creating Files


```python
from ShelfSimplify import createfile
    
createfile("FilenameWithExtension", "Content")
```

2)Appending Files

```python
from ShelfSimplify import appendfile

appendfile("FilenameWithExtension", "Content")
```

3)Reading Files

```python
from ShelfSimplify import readfile

readfile("FilenameWithExtension")
```

4)Getting User's system's info

```python
from ShelfSimplify import getsysdetails

getsysdetails()
```
or,

```python
from ShelfSimplify import getsys_node, getsys_version, getsys_release, getsys_machine
from ShelfSimplify import getsys_processor, getsys_system

getsys_node()
getsys_processor()
getsys_system()
getsys_machine()
getsys_version()
getsys_release()
```

5)Renaming Files

```python
from ShelfSimplify import renamefile

renamefile("Filename with extension", "Newname with Extension")
```

6)Replacing Files

```python
from ShelfSimplify import replacefile

replacefile("Current location", "New location")
```

7)Removing Files

```python
from ShelfSimplify import removefile

removefile("Filename with extension")
```

-________________________________________________________________________-

Overall, this package helps to manage files simply using python.
Updates will be coming soon.

-ArunProgrammer(Author) 