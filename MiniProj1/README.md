https://github.com/Patel-N/COMP472_ShortKings/tree/Q2_Neil/MiniProj1

# Todo before runnning
In the root folder of the miniProj.ipynb file run this in command line
```sh
mkdir precision
mkdir classification_reports
mkdir confusion_matrix_figures
```


# Package to install

```sh
python -m pip install -U matplotlib
pip3 install -U scikit-learn scipy matplotlib
pip install pretty_confusion_matrix
pip install fpdf
pip install -U nltk
python -m nltk.downloader all
pip install gensim
```

# How to run
There is only one file to run which is `miniProj.ipynb`. If there data being extracted is not `goemotions.json.gz`, then we will need to modify the path in the cell with comment `#1.2`. Once that is done, run all and everything should work, if all the dependencies are installed correctly.
