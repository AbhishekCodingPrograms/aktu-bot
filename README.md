# 🚀 AKTU Auto Blog Generator (Full Automation System)

> 🔥 Turn AKTU notices into **SEO-optimized blog posts automatically** and publish directly to WordPress — 24/7 without manual work.

---

## 📌 Overview

AKTU Auto Blog Generator is a **Python-based automation system** that:

* Scrapes latest notices from AKTU website
* Converts them into **1000+ word SEO blog posts**
* Publishes directly to your WordPress site
* Runs automatically using cron jobs or GitHub Actions

👉 Perfect for:

* Students running blog sites (like notesgallery.com)
* EdTech content creators
* Internship / exam update websites

---

## 🧠 System Workflow

```
AKTU Website
   ↓
Web Scraper (Python)
   ↓
AI Content Generator (SEO Blog)
   ↓
Content Optimization
   ↓
WordPress REST API
   ↓
Live Blog Post 🚀
```

---

## ✨ Features

* ✅ Automatic AKTU notice scraping
* ✅ AI-generated SEO blog posts (Hindi + English mix)
* ✅ WordPress auto publishing
* ✅ Duplicate post prevention
* ✅ Fully automated (cron / scheduler support)
* ✅ Lightweight & beginner-friendly

---

## 📂 Project Structure

```
aktu-auto-blog/
│
├── scraper.py          # Scrapes AKTU notices
├── generator.py        # Generates SEO blog using AI
├── publisher.py        # Publishes post to WordPress
├── main.py             # Main automation script
├── config.py           # API keys & configuration
├── database.json       # Stores published notices
├── requirements.txt    # Dependencies
└── .github/
    └── workflows/
        └── auto-blog.yml  # GitHub Actions automation
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/aktu-auto-blog.git
cd aktu-auto-blog
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Edit `config.py`:

```python
OPENAI_API_KEY = "your_openai_api_key"

WP_URL = "https://yourwebsite.com/wp-json/wp/v2/posts"
WP_USERNAME = "your_username"
WP_PASSWORD = "your_application_password"

AKTU_URL = "https://aktu.ac.in/circulars.html"
```

---

## ▶️ Run Locally

```bash
python main.py
```

👉 If configured correctly, a blog post will appear on your WordPress site.

---

## 🌐 Deployment Options

---

### 🥇 Option 1: VPS Deployment (Recommended)

Run 24/7 using a VPS (Hostinger / AWS / DigitalOcean)

#### Steps:

```bash
ssh root@your_server_ip
apt update && apt install python3-pip git -y
git clone https://github.com/your-username/aktu-auto-blog.git
cd aktu-auto-blog
pip3 install -r requirements.txt
python3 main.py
```

---

### ⏰ Setup Cron Job

```bash
crontab -e
```

```bash
0 * * * * /usr/bin/python3 /root/aktu-auto-blog/main.py
```

👉 Runs every hour automatically

---

### 🥈 Option 2: GitHub Actions (Free)

Create file:

```
.github/workflows/auto-blog.yml
```

```yaml
name: AKTU Auto Blog

on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - run: pip install -r requirements.txt

      - run: python main.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          WP_USERNAME: ${{ secrets.WP_USERNAME }}
          WP_PASSWORD: ${{ secrets.WP_PASSWORD }}
```

---

### 🔐 Add Secrets

Go to:
**Repo → Settings → Secrets**

Add:

* OPENAI_API_KEY
* WP_USERNAME
* WP_PASSWORD

---

## 🧩 SEO Strategy

This system generates content with:

* 🔥 Focus keyword = notice title
* 🔥 Proper H1, H2, H3 headings
* 🔥 FAQs section
* 🔥 Human-like tone (Hindi-English mix)
* 🔥 Google Discover optimized format

---

## ⚠️ Important Guidelines

* ❌ Do not publish too many posts/day (limit: 5–10)
* ❌ Avoid raw AI content (add manual touch)
* ✔ Use internal linking
* ✔ Add featured images for better CTR

---

## 🚀 Future Enhancements

* 🖼️ Auto featured image generator
* 📢 Telegram notification bot
* 🏷️ Auto tags & categories
* 📊 RankMath SEO integration
* 🌐 Multi-site publishing

---

## 🧪 Example Output

👉 Input:

```
AKTU Exam Form Last Date Extended 2026
```

👉 Output:

* 1000+ word blog
* Structured headings
* FAQs
* SEO optimized content

---

## 💡 Use Cases

* AKTU updates blog
* Internship alert website
* College news portal
* AI automated blogging system

---

## 🤝 Contributing

Pull requests are welcome!

You can improve:

* Scraper accuracy
* SEO quality
* Automation features

---

## 📜 License

Open-source project — free to use and modify.

---

## 👨💻 Author

**Prateek Maurya**
B.Tech Student | Developer | Blogger

---

## ⭐ Support

If you found this project useful:

👉 Star ⭐ this repo
👉 Share with friends
👉 Build your own AI blog system

---

## 🔥 Final Note

This project is not just a script —
it’s a **complete automated content system** that can generate traffic, grow your website, and even help you earn online.

🚀 Build once. Run forever.
