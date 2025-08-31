# CRM Celery + Redis Setup

This guide explains how to set up **Celery** with **Redis** and **Celery Beat** for scheduled tasks in the CRM project.  
It covers installation, configuration, running services, and verifying logs.

---

## 1. Install Dependencies

### 1.1 System Requirements
- Python 3.8+
- Redis (must be installed and running locally)
- A working Django project named **crm**

### 1.2 Install Python Packages
Add to `requirements.txt`:
