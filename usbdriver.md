## Step 1
```
uname -a
```

```
Linux raspberrypi 5.10.17-v7+ #1421 SMP Thu May 27 13:59:01 BST 2021 armv7l GNU/Linux
```

## Step 2
```
wget http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-kernal-build.tar.gz
```

```kernal```: 5.10.17-v7

```build```: 1421

---
Example
```
wget http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.10.17-v7-1421.tar.gz
```

## Step 3
```
tar xzf 8188eu-kernal-build.tar.gz
```
---
Example
```
tar xzf 8188eu-5.10.17-v7-1421.tar.gz
```

## Step 4
```
./install.sh
```

### Reboot and connect to WiFi