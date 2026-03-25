# Restaurant Business Tutorial: Building Data Contracts and Products with Ontos

A comprehensive, step-by-step guide to building data governance for a restaurant business using the Ontos platform.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Part 1: Setting Up the Organization](#3-part-1-setting-up-the-organization)
   - [3.0 Creating Tags](#30-creating-tags-required-step)
   - [3.1 Creating Domain Structure](#31-creating-domain-structure)
   - [3.2 Setting Up Teams](#32-setting-up-teams)
   - [3.3 Creating Projects](#33-creating-projects)
   - [3.4 Verifying Your Setup](#34-verifying-your-setup)
4. [Part 2: Creating Datasets](#4-part-2-creating-datasets)
5. [Part 3: Building Data Contracts](#5-part-3-building-data-contracts)
6. [Part 4: Packaging Data Products](#6-part-4-packaging-data-products)
7. [Part 5: Compliance and Governance](#7-part-5-compliance-and-governance)
8. [Part 6: Best Practices Summary](#8-part-6-best-practices-summary)
9. [Appendix: Sample Data Reference](#appendix-sample-data-reference)

---

## 1. Introduction

This tutorial guides you through building a complete data governance solution for a fictional restaurant business called **Bella Cucina**. You'll learn how to use Ontos to:

- Organize data assets using domains, tags, and projects
- Create and manage datasets for restaurant operations
- Define data contracts with quality rules and service level objectives
- Package datasets into data products for different consumers
- Implement compliance policies and monitoring

### What You'll Build

By the end of this tutorial, you'll have created:

| Component | Example |
|-----------|---------|
| **Domains** | Restaurant Operations (root), Kitchen, Front of House, Analytics, Supply Chain |
| **Tags** | 12 domain tags for categorization |
| **Teams** | Analytics Team, Kitchen Team, Data Governance Team |
| **Projects** | Customer Insights, Menu Optimization, Inventory Forecasting |
| **Datasets** | Customers, Menu Items, Orders, Reservations, Inventory, Staff, Suppliers, Reviews |
| **Data Contracts** | Customer data contract, Order data contract, etc. |
| **Data Products** | Customer 360, Daily Sales Analytics, Inventory Forecast |

### The Restaurant Domain

Bella Cucina is a mid-sized Italian restaurant chain with the following data needs:

- **Customer Management**: Track customer preferences, loyalty, and feedback
- **Menu & Orders**: Manage menu items, pricing, and order history
- **Reservations**: Handle booking and seating management
- **Inventory**: Track ingredients, supplies, and supplier relationships
- **Staff**: Manage employee schedules and performance
- **Analytics**: Generate business intelligence and reporting

---

## 2. Prerequisites

Before starting this tutorial, ensure you have:

- [ ] **Ontos installed and running** locally or on Databricks
- [ ] **Access to the Ontos UI** at `http://localhost:3000` (or your Databricks workspace)
- [ ] **Basic understanding** of data governance concepts
- [ ] **Python 3.9+** installed (for sample data generation scripts)

### Required Roles

You'll need appropriate permissions to complete this tutorial:

| Role | Required For |
|------|--------------|
| **Admin** | Creating domains, tags, teams, and projects |
| **Data Producer** | Creating datasets and data products |
| **Data Steward** | Creating data contracts and compliance policies |

---

## 3. Part 1: Setting Up the Organization

### 3.0 Creating Tags (Required Step)

Before creating domains, you need to set up a tag taxonomy that will be used throughout your data governance setup. Tags help categorize and discover assets across your organization.

#### Why Tags Matter

Tags provide:

- **Categorization**: Group related assets, contracts, and products
- **Discovery**: Search and filter assets by business context
- **Governance**: Apply policies based on tag attributes (e.g., PII handling)
- **Semantic Meaning**: Connect data to business concepts through ontology

#### Understanding Tag Namespaces

Tag namespaces help organize tags into logical groups. We'll use:

- `domain:*` - Tags that classify data by business area
- `sensitivity:*` - Tags that indicate data sensitivity levels
- `type:*` - Tags that classify data asset types
- `quality:*` - Tags that indicate data quality states

#### Creating Domain Tags

Navigate to **Settings** → **Tags** and create the following tags:

**Root Domain Tags (2 tags):**

| Tag Name | Description | Namespace |
|----------|-------------|-----------|
| `restaurant` | Restaurant industry classification | `domain` |
| `hospitality` | Hospitality sector classification | `domain` |

**Sub-Domain Tags (10 tags):**

| Tag Name | Description | Namespace | Parent Domain |
|----------|-------------|-----------|---------------|
| `kitchen` | Kitchen operations | `domain` | Kitchen |
| `food-prep` | Food preparation activities | `domain` | Kitchen |
| `service` | Customer service operations | `domain` | Front of House |
| `guest-experience` | Guest experience management | `domain` | Front of House |
| `analytics` | Business intelligence and analytics | `domain` | Analytics |
| `reporting` | Business reporting activities | `domain` | Analytics |
| `bi` | Business intelligence | `domain` | Analytics |
| `inventory` | Inventory management | `domain` | Supply Chain |
| `suppliers` | Supplier relationships | `domain` | Supply Chain |
| `procurement` | Procurement activities | `domain` | Supply Chain |

#### Best Practices for Tag Creation

When creating tags:

1. **Use consistent naming**:
   - Lowercase with hyphens for multi-word tags (e.g., `food-prep`, not `Food Prep`)
   - Avoid spaces or special characters

2. **Group related tags in namespaces**:
   - All domain tags use `domain` namespace
   - This helps with filtering and governance policies

3. **Add clear descriptions**:
   - Describe what the tag represents
   - Include context for when it should be used
   - Reference the parent domain for sub-domain tags

4. **Plan for future tags**:
   - As your organization grows, you'll need additional tags
   - Consider sensitivity classifications: `sensitivity:public`, `sensitivity:internal`, `sensitivity:confidential`
   - Consider quality indicators: `quality:certified`, `quality:experimental`

#### Creating Tags in the UI

1. Navigate to **Settings** → **Tags**
2. Click **Create Tag**
3. Fill in the form:

For root domain tags:
- Tag Name: `restaurant`
- Description: `Restaurant industry classification`
- Namespace: `domain`
- Leave Parent Domain empty

For sub-domain tags (example - `kitchen`):
- Tag Name: `kitchen`
- Description: `Kitchen operations`
- Namespace: `domain`
- Parent Domain: `Kitchen` (select from dropdown after Kitchen domain is created)

4. Click **Create**
5. Repeat for all 12 tags (2 root + 10 sub-domain)

#### Tag Creation Order Recommendation

Create tags in this order to ensure parent domains exist:

**Step 1: Create root domain tags**
1. `restaurant`
2. `hospitality`

**Step 2: Create Kitchen domain tags**
3. `kitchen`
4. `food-prep`

**Step 3: Create Front of House domain tags**
5. `service`
6. `guest-experience`

**Step 4: Create Analytics domain tags**
7. `analytics`
8. `reporting`
9. `bi`

**Step 5: Create Supply Chain domain tags**
10. `inventory`
11. `suppliers`
12. `procurement`

This order ensures that when you create sub-domain tags, their parent domain is already available in the Parent Domain dropdown.

#### Verification

After creating all tags:

- [ ] All 12 domain tags created (2 root + 10 sub-domain)
- [ ] Tags appear in dropdown menus when creating domains
- [ ] Tag search returns results when typing
- [ ] Each tag has proper namespace, description, and parent domain relationship

---

### 3.1 Creating Domain Structure

Domains organize your data by business area. For our restaurant, we'll create:

```
Restaurant Operations (root)
├── Kitchen
├── Front of House
├── Analytics
└── Supply Chain
```

#### Steps

1. Navigate to **Domains** in the sidebar
2. Click **Create Domain**
3. Create the root domain:

| Field | Value |
|-------|-------|
| Name | `restaurant-operations` |
| Description | `Core restaurant operations data including orders, menu, customers, and inventory` |
| Parent Domain | None (this is root) |
| Tags | `restaurant`, `hospitality` |

4. Create sub-domains under "Restaurant Operations":

**Kitchen Domain:**

| Field | Value |
|-------|-------|
| Name | `kitchen` |
| Description | `Kitchen operations including menu preparation, recipes, and food quality` |
| Parent | Restaurant Operations |
| Tags | `kitchen`, `food-prep` |

**Front of House Domain:**

| Field | Value |
|-------|-------|
| Name | `front-of-house` |
| Description | `Guest-facing operations including service, reservations, and customer experience` |
| Parent | Restaurant Operations |
| Tags | `service`, `guest-experience` |

**Analytics Domain:**

| Field | Value |
|-------|-------|
| Name | `analytics` |
| Description | `Business intelligence, reporting, and data analytics` |
| Parent | Restaurant Operations |
| Tags | `analytics`, `reporting`, `bi` |

**Supply Chain Domain:**

| Field | Value |
|-------|-------|
| Name | `supply-chain` |
| Description | `Inventory management, suppliers, and procurement` |
| Parent | Restaurant Operations |
| Tags | `inventory`, `suppliers`, `procurement` |

#### API Example

```bash
curl -X POST http://localhost:8000/api/domains \
  -H "Content-Type: application/json" \
  -d '{
    "name": "restaurant-operations",
    "description": "Core restaurant operations data",
    "tags": ["restaurant", "hospitality"]
  }'
```

---

### 3.2 Setting Up Teams

Teams are groups of users who collaborate on data products.

#### Create Analytics Team

1. Navigate to **Teams** → **Create Team**
2. Fill in the form:

| Field | Value |
|-------|-------|
| Name | `analytics-team` |
| Title | `Analytics Team` |
| Description | `Business intelligence and data analytics for restaurant operations` |
| Domain | Analytics |
| Slack Channel | `#analytics-team` |
| Lead | `analytics.lead@bellacucina.com` |

3. Add team members:

| Member | Type | Role Override |
|--------|------|---------------|
| `data.engineer@bellacucina.com` | User | Data Producer |
| `analyst@bellacucina.com` | User | Data Consumer |
| `bi.developer@bellacucina.com` | User | Data Producer |

#### Create Kitchen Team

| Field | Value |
|-------|-------|
| Name | `kitchen-team` |
| Title | `Kitchen Team` |
| Description | `Chefs, cooks, and kitchen staff` |
| Domain | Kitchen |
| Lead | `head.chef@bellacucina.com` |

#### Create Data Governance Team

| Field | Value |
|-------|-------|
| Name | `data-governance` |
| Title | `Data Governance Team` |
| Description | `Data stewards responsible for data quality and compliance` |
| Domain | Restaurant Operations |
| Lead | `data.steward@bellacucina.com` |

**Members:**

| Member | Role Override |
|--------|---------------|
| `data.steward@bellacucina.com` | Data Steward |
| `compliance@bellacucina.com` | Data Steward |

---

### 3.3 Creating Projects

Projects organize team work on specific initiatives.

#### Create Customer Insights Project

1. Navigate to **Projects** → **Create Project**
2. Fill in the form:

| Field | Value |
|-------|-------|
| Name | `customer-insights` |
| Title | `Customer Insights Platform` |
| Description | `Build comprehensive customer analytics including 360-degree view, segmentation, and lifetime value analysis` |
| Type | Team |
| Owner Team | analytics-team |

3. Add collaborating teams:
   - kitchen-team (provides menu preference data)
   - data-governance (reviews contracts for PII handling)

#### Create Additional Projects

| Project | Owner | Description |
|---------|-------|-------------|
| `menu-optimization` | kitchen-team | Analyze menu performance and optimize pricing |
| `inventory-forecasting` | analytics-team | Predict inventory needs based on demand patterns |
| `compliance-reporting` | data-governance | Automated compliance monitoring and reporting |

---

### 3.4 Verifying Your Setup

Navigate to each section to verify:

- [ ] **Tags**: All 12 domain tags created (restaurant, hospitality, kitchen, food-prep, service, guest-experience, analytics, reporting, bi, inventory, suppliers, procurement)
- [ ] **Domains**: 5 domains created (1 root + 4 sub-domains) with correct tags assigned
- [ ] **Teams**: 3 teams created with correct members
- [ ] **Projects**: 4 projects created with proper team assignments

---

## 4. Part 2: Creating Datasets

> **Note**: This section is under development. Check back for the complete guide to creating restaurant datasets.

In this section, you'll create the following datasets for Bella Cucina:

| Dataset | Description | Domain |
|---------|-------------|--------|
| `customers` | Customer profiles and preferences | Front of House |
| `menu_items` | Menu items with pricing and ingredients | Kitchen |
| `orders` | Order history and details | Front of House |
| `reservations` | Reservation bookings | Front of House |
| `inventory` | Ingredient and supply inventory | Supply Chain |
| `staff` | Employee information | Kitchen |
| `suppliers` | Supplier details and contacts | Supply Chain |
| `reviews` | Customer reviews and ratings | Front of House |

### Sample Data Generation

Python scripts using the Faker library will be provided to generate realistic sample data:

```
docs/tutorials/restaurant-business/scripts/
├── generate_customers.py
├── generate_menu_items.py
├── generate_orders.py
├── generate_reservations.py
├── generate_inventory.py
├── generate_staff.py
├── generate_suppliers.py
└── generate_reviews.py
```

---

## 5. Part 3: Building Data Contracts

> **Note**: This section is under development. Check back for the complete guide to creating data contracts.

In this section, you'll define data contracts that specify:

- **Schema definitions**: Column types, constraints, and descriptions
- **Quality rules**: Data validation and quality checks
- **Service Level Objectives (SLOs)**: Freshness, availability, and accuracy targets
- **Ownership**: Data producers, consumers, and stewards
- **Access control**: Who can read/write the data

### Example Contract Structure

```yaml
contract_id: customer-data-contract
version: 1.0.0
status: active
dataset: customers
owner: analytics-team
schema:
  - name: customer_id
    type: uuid
    nullable: false
    description: Unique customer identifier
  - name: email
    type: string
    nullable: false
    pii: true
quality_rules:
  - name: email_format
    rule: email_regex_validation
    severity: error
slo:
  freshness: 24h
  availability: 99.9%
```

---

## 6. Part 4: Packaging Data Products

> **Note**: This section is under development. Check back for the complete guide to creating data products.

In this section, you'll create data products that package datasets for different consumers:

| Product Type | Example | Target Consumer |
|--------------|---------|-----------------|
| **Source-aligned** | Raw Orders | Data Engineers |
| **Aggregate** | Daily Sales Summary | Business Analysts |
| **Consumer-aligned** | Customer 360 | Marketing Team |

### Product Lifecycle

1. **Design**: Define the product specification
2. **Build**: Create the transformation pipelines
3. **Publish**: Register in the data catalog
4. **Subscribe**: Consumers request access
5. **Monitor**: Track usage and quality

---

## 7. Part 5: Compliance and Governance

> **Note**: This section is under development. Check back for the complete guide to compliance setup.

In this section, you'll implement compliance policies for:

- **PII Protection**: Handling customer personal data
- **Data Retention**: How long to keep different data types
- **Access Logging**: Who accessed what data and when
- **Quality Monitoring**: Continuous validation of data contracts

### Compliance Policies

```yaml
policy_id: pii-handling
name: PII Data Handling Policy
applies_to:
  tags: [sensitivity:confidential]
rules:
  - type: encryption_at_rest
    enabled: true
  - type: access_logging
    enabled: true
    retention: 90d
  - type: masking
    fields: [email, phone, address]
```

---

## 8. Part 6: Best Practices Summary

### Naming Conventions

| Asset Type | Convention | Example |
|------------|------------|---------|
| Domains | lowercase with hyphens | `restaurant-operations` |
| Tags | lowercase with hyphens | `food-prep` |
| Teams | lowercase with hyphens, suffix `-team` | `analytics-team` |
| Projects | lowercase with hyphens | `customer-insights` |
| Datasets | lowercase with underscores | `menu_items` |
| Data Products | lowercase with hyphens | `customer-360` |

### Tagging Strategy

- Use namespaces to group related tags
- Apply tags consistently across all assets
- Plan for future tags and classifications
- Document tag meanings in descriptions

### Team Organization

- Create domain-specific teams
- Assign clear ownership for each data product
- Include data governance representation
- Use role overrides for fine-grained access control

---

## Appendix: Sample Data Reference

### Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  customers  │────<│   orders    │>────│  menu_items │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                    │
      │                   v                    │
      │             ┌─────────────┐            │
      │             │ reservations│            │
      │             └─────────────┘            │
      │                                        │
      v                                        v
┌─────────────┐                         ┌─────────────┐
│   reviews   │                         │  inventory  │
└─────────────┘                         └─────────────┘
                                              │
                                              v
                                        ┌─────────────┐
                                        │  suppliers  │
                                        └─────────────┘
```

### Dataset Schemas

> **Note**: Detailed schemas will be provided in the Part 2 update.

---

## Contributing

Found an issue or want to improve this tutorial? Please submit a pull request or open an issue on the [Ontos GitHub repository](https://github.com/larsgeorge/ontos).

---

## License

This tutorial is part of the Ontos project and is licensed under the Apache License 2.0.
