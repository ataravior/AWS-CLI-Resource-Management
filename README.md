# 🚀 AWS CLI Automation with Pulumi & Boto3

A fully automated AWS CLI tool built with **Pulumi Automation API** and **Boto3**, allowing seamless **creation, management, and deletion** of AWS resources like **EC2, S3, and Route 53** – all from an intuitive command-line interface.

---

##  Demo

![Image](https://github.com/user-attachments/assets/68a71360-6d92-488d-9893-a033d6b93776)


##  **Why This Project?**
 ** Pulumi + Boto3 Hybrid** – The best of **Infrastructure as Code** & AWS SDK  
 ** Interactive CLI** – A **fast and simple** AWS management experience  
 ** Filtered AWS Resources** – Only manage what **you created**  
 ** Modular & Scalable** – Easily extend for new AWS services  

---

##  **Tech Stack**
- ** Pulumi Automation API** – Automate AWS infrastructure provisioning  
- ** AWS Boto3** – Direct AWS SDK integration for advanced control  
- ** Python 3.x** – Core language for scripting and automation  
- ** CLI-Driven Interface** – Fully interactive & user-friendly  
- ** IAM Role-Based Authentication** – Secure AWS access  

---

##  **Installation & Setup**
```sh
git clone https://github.com/ataravior/aws-cli-automation.git
cd aws-cli-automation

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install Dependencies
pip install -r requirements.txt

# Configure AWS Credentials
aws configure
```

---

##  **How It Works**
 **Interactive CLI** – The menu guides users through AWS management  
 **Pulumi Runs in the Background** – No need to confirm manually  
 **Everything is Tagged** – Only manage AWS resources created via this CLI  
 **Supports EC2, S3, and Route 53** – More services coming soon!  

### **Run the CLI**
```sh
python main.py
```

#### **Example Menu**
```
Select an action:
1. Manage EC2 Instances
2. Manage S3 Buckets
3. Manage Route53 DNS
4. Exit
```

---

##  **Automated AWS Services**
###  **EC2 Management**
 Create, List, Start, Stop & Terminate instances  
 Uses only **CLI-created** instances for safety  

###  **S3 Bucket Management**
 Create & Manage AWS S3 Buckets  
 Upload files **without UI hassle**  

###  **Route 53 DNS Automation**
 Manage **DNS Zones** & **Records**  
 Automate domain configurations **within seconds**  

---

##  **Pulumi Automation**
Pulumi runs **without interruptions**:
```sh
export PULUMI_CONFIG_PASSPHRASE=""  # Skip manual confirmation
```
If needed, manually deploy:
```sh
pulumi up --yes
```

---


##  **Contribute**
🚀 PRs are welcome! Fork, commit, and create a **Pull Request**.    
🔥 **If this project helps you, give it a ⭐ on GitHub!**  

