# 🚀 Azure Cosmos DB Billing Optimization

Welcome to the **Cost Optimization Project** for billing records in Azure's serverless architecture!\
This repo combines **Terraform** for infrastructure and **Python** for serverless logic, while keeping your APIs unchanged and your bills optimized. 💰✨

---

## 🧩 Project Overview

This solution helps you:

- 🗃️ Store **active records** (< 3 months) in Azure **Cosmos DB**
- 🧊 Archive **older records** in **Azure Blob Storage** to reduce costs
- ⚙️ Use **Azure Functions** to migrate, access, and manage billing data seamlessly
- 🛡️ Wrap all requests behind **Azure API Management** to maintain consistent APIs

---

## 🏗️ Architecture

```text
[Client Apps]
      |
      v
[Azure API Management]
      |_____________________
      |                     |
      v                     v
[Azure Cosmos DB]   [Azure Functions]
      |                     |
      v                     v
[Active Records]    [Azure Blob Storage]
      |                     |
      v                     v
[Metadata Index]    [Archived Records]
```



---

## ⚙️ Technologies Used

| 🌐 Component     | 💼 Service                     | 🧠 Purpose                              |
| ---------------- | ------------------------------ | --------------------------------------- |
| Infrastructure   | Terraform                      | IaC to provision all Azure resources    |
| Serverless Logic | Python (Azure Functions)       | Logic for archival and fallback reads   |
| Storage (Active) | Azure Cosmos DB (SQL API)      | Fast access for current billing records |
| Storage (Cold)   | Azure Blob Storage (Cool Tier) | Cost-effective archival of old data     |
| API Gateway      | Azure API Management           | Unified endpoint, no contract changes   |

---

## 🛠️ Quick Start

```bash
# 1. Clone the repository 📥
https://github.com/rithwicklink/azure-cosmos-billing-optimization.git
# 2. Deploy Infrastructure 🚀
cd terraform
terraform init
terraform apply

# 3. Deploy Python Functions 🐍
cd ../functions
func azure functionapp publish billing-archival
func azure functionapp publish billing-retrieval
```

> 💡 Tip: Use `env.tfvars` or `terraform.tfvars` to customize resource names and regions.

---

## 💸 Cost Optimization Strategy

- 🧹 Archives records older than 90 days to Blob Storage (Cool Tier)
- 🧮 Reduces Cosmos DB RUs by indexing only what’s needed
- 🧑‍💻 Read requests to old records automatically **fallback** to Blob via proxy logic
- 📊 Supports optional **Synapse Analytics** for archived data (bonus)

---

## 📂 Repository Structure

```bash
.
├── terraform/              # Terraform IaC modules
├── functions/              # Python Azure Functions
│   ├── archival/           # Function to move old records to Blob
│   └── retrieval/          # Function to read archived records if not found in Cosmos
├── docs/                   # Architecture diagrams & references
└── README.md               # This file 📘
```

---

## 🔒 Security & Access

- 🧾 Uses Managed Identity for Function-to-Blob/Cosmos access
- 🔐 Securely assigns RBAC roles via Terraform
- 🚫 No hard-coded secrets — everything uses Azure Key Vault or environment variables

---

## 🔗 Related Resources

- 🤖 **Grok Conversation on this Topic (Grok AI chat coversation link):** [View Discussion](https://grok.com/share/c2hhcmQtMw%3D%3D_a55e9872-ba50-4314-8c7b-d5f29392461b)

---

## 🌍 Contributing

We welcome contributions! Feel free to:

- Submit PRs for feature improvements 🧑‍💻
- Report issues or suggest enhancements 🐞
- Share your use case in a new issue 💬

---

##

