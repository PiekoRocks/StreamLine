# StreamLine
A centralized application for managing and tracking fire hydrants.

## Live Link
https://web.engr.oregonstate.edu/~johnsn26/CS340-Group-91-Step-3/index.html

## Overview
Our **StreamLine** application is designed to manage data for over **5,000 fire hydrants** across urban, suburban, and rural areas. Fire hydrants require **regular maintenance**, including inspections and repairs performed by field workers. 

To ensure operational efficiency and **make it easier to keep hydrants working for emergencies**, hydrant status must be tracked, allowing field workers to **prioritize tasks effectively**.

### **The Problem**
Most hydrant information is stored in **multiple systems** (spreadsheets, handwritten logs, legacy software), making it challenging to access **reliable and comprehensive** hydrant data.

### **The Solution**
StreamLine serves as a **centralized hub** for hydrant data, consolidating:
- **Unique IDs** – Each hydrant is assigned a distinct identifier for accurate record-keeping.
- **Locations** – Real-time GPS coordinates ensure easy hydrant identification and mapping.
- **Hydrant Types** – Categorization of hydrants based on specifications and capacity.
- **Maintenance Logs** – Detailed records of past and upcoming maintenance activities.
- **Inspection History** – Tracks inspection status, ensuring compliance with safety standards.

## **Diagrams**
### **Schema Diagram**
<img width="643" alt="Screenshot 2025-02-18 at 5 18 21 PM" src="https://github.com/user-attachments/assets/39508c03-2155-48d2-b9c3-69db66a0b8f2" />

### **Entity Relationship Diagram**
<img width="648" alt="Screenshot 2025-02-18 at 5 18 38 PM" src="https://github.com/user-attachments/assets/54cb871c-f0f2-4d5a-8487-96b698af417e" />

## Tech Stack

### **Front-End**
- [x] **HTML5**
- [x] **CSS3**
- [x] **JavaScript**

### **Back-End**
- [ ] **Flask** (Lightweight Python Web Framework)
- [x] **SQL** (Database)
- [ ] **Vanilla JavaScript** (for client-side logic & API calls)

## **Installation Guide**
### **Clone the Repository**
```bash
git clone https://github.com/PiekoRocks/StreamLine
```

### **Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Windows (PowerShell)**
```bash
python -m venv venv
venv\Scripts\activate
```

### **Install Dependencies**
```bash
pip install flask mysql-connector-python
```

### **Run the Flask Server**
```bash
python app.py
```

## **Project Tree**
```plaintext
STREAMLINE/
│── sql/
│   ├── StreamLine-ddl.sql
│   ├── StreamLine-dml.sql
│
│── static/
│   ├── index.js
│   ├── logo.png
│   ├── style.css
│
│── templates/
│   ├── base.html
│   ├── hydrants_inspections.html
│   ├── hydrants.html
│   ├── index.html
│   ├── inspections.html
│   ├── maintenance.html
│   ├── regions.html
│   ├── workers_inspections.html
│   ├── workers.html
│
├── app.py
├── README.md
```


