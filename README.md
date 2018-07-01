# manga-dl

## to-do

- [x] read url, beautifulsoup4

- [x] download to folder

- [x] format better filename

- [x] transform images to pdf (img2pdf)

- [ ] component pdf_build create pdf from imgs already downloaded

- [ ] download specific chapters (with chapter no matching)

- [ ] rename imgs filename(after manual delete ad page)

## Instruction

### manga_dl.py

Still testing some functions

```python
python manga_dl.py -m some-manga-park-url
```

### pdf_builder.py

Convert imgs to pdf, structure it can handle `some-manga\chapters`, it can convert all imgs under chapters to pdf in that folder.

```python
python pdf_builder.py some-local-folder
```