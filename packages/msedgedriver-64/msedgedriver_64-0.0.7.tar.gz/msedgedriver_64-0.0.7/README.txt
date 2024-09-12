This module downloads the SELENIUM ms edge driver that matches the version of ms edge the user has. 

just use install() command and the msedge driver will be there in that directory


```
pip install msedgedriver_64
```
now that the library is installed, lets use it.

```
import msedgedriver_64
from selenium import webdriver  

msedgedriver_64.install() #you will notice a file named msedgedriver.exe is downloaded in your directory

Driver = webdriver.Edge('msedgedriver.exe')#msedgedriver was installed by above command

```

This only works for microsoft edge and will work for any microsoft edge browser version. As it first checks your browser version and installs driver version accourdingly.