<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <img src="images/logo.png" alt="Logo" width="80" height="80">

  <h3 align="center">Event-Driven Book Store Microservices Architecture</h3>

  <p align="center">
    Distributed Book Store System built using FastAPI, Python, RabbitMQ, OAuth2/JWT, RBAC & Angular
    <br />
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#">View Demo</a>
    &middot;
    <a href="#">Report Bug</a>
    &middot;
    <a href="#">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#book-store-overview">Book Store Overview</a></li>
        <li><a href="#architecture-diagram">Architecture Diagram</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This project is a **complete Event-Driven Book Store Application**, designed for the **SDE Major Project** course.  
The architecture is built using **microservices**, communicating asynchronously using **RabbitMQ**.

### ✨ Key Capabilities

- Browse, search, and view books  
- Add books to cart  
- Checkout & place orders  
- Personalized recommendations using BERT  
- Authentication with OAuth2 + JWT  
- Role-Based Access Control (Admin / User)  
- Event-driven order flow using RabbitMQ  

---

## 📚 Book Store Overview

The Book Store contains the following core microservices:

### **1. User Service**
Handles:
- Registration
- Login (OAuth2)
- JWT access token generation
- Roles (Admin, User)

### **2. Book Catalog Service**
Provides:
- All books list
- Book details
- Search by title/author
- Admin can add/update/remove books

Uses your dataset (10k books).

### **3. Cart Service**
Manages:
- Add to cart
- Remove from cart
- Update quantities
- Per-user cart storage

### **4. Order Service (Event-Driven)**
When a user places an order:
- FastAPI publishes `order.created` event to RabbitMQ  
- Worker microservice receives event  
- Order is processed asynchronously  

This removes load from the main API.

### **5. Recommendation Service (BERT)**
Your BERT / SentenceTransformer model returns:
- Books similar to a selected book  
- Personalized suggestions  

RabbitMQ can optionally trigger recommendations asynchronously.

### **6. Notification Service **
Listens to:
- 'auth success'

Sends user notification (email / toast message).

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Architecture Diagram

