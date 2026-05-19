# Database Security Vulnerability Lab

## Overview
This project is a Dockerized CTF-style database security lab containing three database vulnerabilities:

1. Privilege Escalation – SECURITY DEFINER Abuse (PostgreSQL)
2. Privilege Escalation – CVE-2019-9193 COPY TO PROGRAM (PostgreSQL)
3. Injection – Blind SQL Injection (Flask + PostgreSQL)

---

## Prerequisites
Install:
- Docker Desktop
- Git

Verify installation:

```powershell
docker --version
docker compose version
git --version