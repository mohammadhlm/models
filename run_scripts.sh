#!/bin/bash

# اجرای فایل choose_model.py
python3 choose_model.py

# بررسی اینکه آیا اجرای choose_model.py موفقیت‌آمیز بوده است
if [ $? -eq 0 ]; then
    echo "اجرای choose_model.py با موفقیت انجام شد."
else
    echo "خطا در اجرای choose_model.py"
    exit 1
fi

# اجرای فایل install-hyperspace.sh
bash install-hyperspace.sh

# بررسی اینکه آیا اجرای install-hyperspace.sh موفقیت‌آمیز بوده است
if [ $? -eq 0 ]; then
    echo "اجرای install-hyperspace.sh با موفقیت انجام شد."
else
    echo "خطا در اجرای install-hyperspace.sh"
    exit 1
fi