# Auto Hack
* note the setup steps described here are being beta-tested.

## This package does automated vulnerability enumeration and recommends exploits.<br><br>

### How to Run on Non Kali-Linux Operating System (Recommended)
* Clone repo
* cd into repo
* Build image

    ```
    docker build -t autohack .
    ```
* Run as terminal inside container
  ```
  docker run -ti -v ${PWD}:/root/repo autohack
  ```

* Run AutoHack

  ```
  autohack 
  ```
  
---  

### How to Run on Kali-Linux Operating System
* Install AutoHack Python Package

    ```
    pip install autohack
    ```
* Run AutoHack
  ```
  autohack 
  ```