# 99 acres Web Scrapper Python

---

## Features:

- This python script allows to scrap any society data from 99 acres.
- Currently, It fetches data for only one page.

- But we can simply loop with adding page-numbers to extract all pages data.[ **Soon will add that**]

- Currently, this website extract only list properties type of page:

![Scrap Page](./assets/image.png)

---

### Demo

Demo CSV file has been added with this repository named as 99 acres.csv.

![Demo video](/assets/Demo.mp4)

![Online Player Link](https://streamable.com/f8rg3t) **Expires at 26 Sep 24**

---

### Type of content

When we search anything on 99 acres searchBar we will get two kinds of webpage.

Both have separate classes,id so I am going to scrap them one-by-one(Breaking complex into small-measurable tasks)

- Society specific webpage
  (Not supported yet)
  ![Society_deatils](/assets/image%20copy.png)

- List of all properties related to society(Supported)

![list_properties](/assets/image.png)

---

### Technologies and libraries Used:

- Python3
- Selenium
- Beautifulsoup4
- Pandas

---

#### Copyright and Ownership:

- 🚨 **All csv content belongs to 99acres.com and it is only for educational and learning purposes** 🚨.

- ⚠️It should not be used for commercial purposes.⚠️

---

### Note:

This website is completely dynamic and server-side rendered so you may get staleElementException.(Element has been modified/changed after we have selected it in our code) Just try again it will work.

---
