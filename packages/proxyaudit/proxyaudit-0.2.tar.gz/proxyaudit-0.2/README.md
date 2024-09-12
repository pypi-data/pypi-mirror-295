Open Source Library for scraping public proxies available to be used within the project for various purposes.

This Libray fetches open available proxies and sorts them according to the currently working and removes useless working proxies . Running this script timely ensures good quality http proxies 

How to Use :
Before using it please install dependencies if it is not installed automatically:
```python

import asyncio
import aiohttp
import urllib3
import socket

```
Once this dependencies installed go to any free proxy websites. Some examples sites are : 

1.[GeoNode Free proxy List]( https://geonode.com/free-proxy-list "Link Title")

2.[ProxyScrape Free proxy List]( https://proxyscrape.com/free-proxy-list "Link Title")

Go to this websites and copy Load proxies through Url or API

Now 

pip install proxyaudit

```python


import proxyaudit

proxyurl="Url got from website paste here"

run_proxy_check(url)

```

Done a txt file will be generated with all the working proxies