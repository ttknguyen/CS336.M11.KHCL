<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h3 align="center"><b>CS336.M11.KHCL - Multimedia Information Retrieval</b></h3>
<h1 align="center"><font color="blue"><b>IMAGE SEARCH ENGINE</b></font></h1>

## Table Content
* [Information Subject](#Information-Subject)
* [Team](#Team)
* [Usage (for colab only)](#Usage-(for-colab-only))

## Information Subject
* **Subject:** Multimedia Information Retrieval
* **Class:** CS336.M11.KHCL
* **Lecturer:** Ngo Duc Thanh
## Team
| STT | Name | MSSV | Email | Github |
| :---: | --- | --- | --- | --- |
| 1 | Thai Tran Khanh Nguyen | 19520188 | *19520188@gm.uit.edu.vn* | [ttknguyen](https://github.com/ttknguyen) | 
| 2 | Doan Nguyen Nhat Quang | 19520235 |  *19520235@gm.uit.edu.vn* | [JD981](https://github.com/JD981) | 
| 3 | Nguyen Pham Vinh Nguyen | 19520186 | *19520186@gm.uit.edu.vn* | [nivla0607](https://github.com/nivla0607) | 
| 4 | Nguyen Khanh Nhu | 19520209 | *19520209@gm.uit.edu.vn* | [nkn-nhu](https://github.com/nkn-nhu) |

## Usage (for colab only)
Link video demo: https://youtu.be/HQFgYrPgjX4\
Check if GPU is available on Google Colab or not for running our API
```sh
!nvidia-smi -L
```
<details>
  <summary><b>Git clone</b></summary><br/>

Clone API source code from our github repository.

  ```
!git clone https://github.com/ttknguyen/CS336.M11.KHCL.git
%cd ./CS336.M11.KHCL/
  ```

</details>

<details>
  <summary><b>Installation</b></summary><br/>
We have a script to do the entire installation in one shot.
This step may takes a few minutes for:

*   Dowloading data, include: corpus, features & models
*   Installing some neccessary libraries for running demo
*   Loading ngrok authentication token
  ```
!bash setup.sh
  ```
</details>

<details>
  <summary><b>Feature Extraction</b></summary><br/>
If you want to extract new dataset, run these cells below to extract feature 

```
python3 feature_extractor.py --method <method id> --root <root path> --data_path <corpus path> --feartures_path <feature path>
```

Must follow the example of data path setup in cells below before running

```
python3 feature_extractor.py\
  --method 0\
  --root /content/CS336.M11.KHCL/\
  --data_path /content/CS336.M11.KHCL/data/test/oxford5k/jpg/\
  --features_path /content/CS336.M11.KHCL/data/\
```

which arguments is defined here:

*   --method: the method you want to extract feature 
*   --root: root folder path of your project
*   --data_path: path of your corpus folder
*   --feartures_path: path of feature file you want to store after extraction

If not, you may pass this step because we have download it when running **setup.sh** in the previous step
</details>

<details>
  <summary><b>Start back-end Server</b></summary><br/>
=> Start the API by running cell below and wait a few seconds for loading features into RAM.

=> After starting *Server* successfully, you copy the URL link of back-end *Server* with the following form "***http:// * .ngrok.io***", then patse it into *Client* website when accessing this URL: http://searchengine-ir.surge.sh

<h3><b>FOR CUSTOMIZATION</b></h3>

```
python3 app.py -ng <0 or 1> -r <root path> -pd <data path> -pc <corpus path>
```


*   -ng: Expose local web server to the internet with ngrok (0: off, 1: on)
*   -r: Path to your root folder of project
*   -pd: Path to your dataset folder
*   -pc: Path to your images database (corpus), use for return image


<br>
<h5>=> If nothing change, the arguments above will be set as the cell below </h5>

```
python3 app.py -ng 1\
              -r /content/CS336.M11.KHCL/\
              -pd /content/CS336.M11.KHCL/data/\
              -pc /content/CS336.M11.KHCL/data/test/oxford5k/jpg/
```
</details>