# CommercePulse Data Dictionary

## Overview

This document describes the schema, structure, and data quality characteristics of the Olist Brazilian E-commerce dataset used in the CommercePulse project.

**Dataset Source**: [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Time Period**: September 2016 - October 2018
**Geographic Scope**: Brazil
**Total Orders**: 99,441
**Total Customers**: 99,441 (unique customer IDs)
**Total Products**: 32,951
**Total Sellers**: 3,095

---

## Table Schema Documentation

### 1. olist_customers_dataset.csv

**Purpose**: Customer information and location

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| customer_id | string | Unique customer identifier per order | 0 | Foreign key to orders table |
| customer_unique_id | string | Unique customer identifier across all orders | 0 | Used for customer-level analysis |
| customer_zip_code_prefix | integer | Zip code prefix (first 5 digits) | 0 | Used for geolocation joins |
| customer_city | string | Customer city name | 0 | |
| customer_state | string | Customer state (2-letter code) | 0 | SP, RJ, MG, etc. |

**Row Count**: 99,441
**Primary Key**: customer_id
**Relationships**:
- customer_id → olist_orders_dataset.customer_id
- customer_zip_code_prefix → olist_geolocation_dataset.geolocation_zip_code_prefix

**Data Quality**: Excellent - no null values

---

### 2. olist_geolocation_dataset.csv

**Purpose**: Geographic coordinates for zip codes

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| geolocation_zip_code_prefix | integer | Zip code prefix | 0 | Can have multiple rows per zip code |
| geolocation_lat | float | Latitude coordinate | 0 | |
| geolocation_lng | float | Longitude coordinate | 0 | |
| geolocation_city | string | City name | 0 | |
| geolocation_state | string | State (2-letter code) | 0 | |

**Row Count**: 1,000,163
**Primary Key**: None (multiple rows per zip code prefix)
**Note**: This is a large file (58.44 MB) with multiple coordinates per zip code prefix. When joining, aggregate by zip code prefix (e.g., take average lat/lng).

**Data Quality**: Excellent - no null values

---

### 3. olist_order_items_dataset.csv

**Purpose**: Items within each order (one row per item)

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| order_id | string | Order identifier | 0 | Foreign key to orders |
| order_item_id | integer | Item sequence number in order | 0 | 1, 2, 3... for multiple items |
| product_id | string | Product identifier | 0 | Foreign key to products |
| seller_id | string | Seller identifier | 0 | Foreign key to sellers |
| shipping_limit_date | datetime | Shipping deadline | 0 | |
| price | float | Item price (BRL) | 0 | Excludes freight |
| freight_value | float | Freight cost (BRL) | 0 | |

**Row Count**: 112,650
**Primary Key**: (order_id, order_item_id)
**Relationships**:
- order_id → olist_orders_dataset.order_id
- product_id → olist_products_dataset.product_id
- seller_id → olist_sellers_dataset.seller_id

**Data Quality**: Excellent - no null values

**Important Note**: `price` is item price only, not including freight. Total order value = sum(price) + sum(freight_value)

---

### 4. olist_order_payments_dataset.csv

**Purpose**: Payment information for orders

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| order_id | string | Order identifier | 0 | Foreign key to orders |
| payment_sequential | integer | Payment sequence number | 0 | For multiple payment methods |
| payment_type | string | Payment method | 0 | credit_card, boleto, voucher, debit_card |
| payment_installments | integer | Number of installments | 0 | 1 for single payment |
| payment_value | float | Payment amount (BRL) | 0 | |

**Row Count**: 103,886
**Primary Key**: (order_id, payment_sequential)
**Relationships**:
- order_id → olist_orders_dataset.order_id

**Data Quality**: Excellent - no null values

**Payment Types**:
- credit_card: Credit card payment
- boleto: Brazilian bank slip
- voucher: Gift voucher
- debit_card: Debit card

---

### 5. olist_order_reviews_dataset.csv

**Purpose**: Customer reviews for orders

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| review_id | string | Unique review identifier | 0 | |
| order_id | string | Order identifier | 0 | Foreign key to orders |
| review_score | integer | Review score (1-5) | 0 | 5 = best, 1 = worst |
| review_comment_title | string | Review title | 87,656 | High null count expected |
| review_comment_message | string | Review text | 58,247 | High null count expected |
| review_creation_date | datetime | Review submission date | 0 | |
| review_answer_timestamp | datetime | Review response date | 0 | |

**Row Count**: 99,224
**Primary Key**: review_id
**Relationships**:
- order_id → olist_orders_dataset.order_id

**Data Quality**: Good - high null counts in comment fields (expected behavior)

---

### 6. olist_orders_dataset.csv

**Purpose**: Order status and timeline

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| order_id | string | Unique order identifier | 0 | Primary key |
| customer_id | string | Customer identifier | 0 | Foreign key to customers |
| order_status | string | Order status | 0 | See status values below |
| order_purchase_timestamp | datetime | Order purchase time | 0 | Order creation timestamp |
| order_approved_at | datetime | Payment approval time | 160 | Some orders not approved |
| order_delivered_carrier_date | datetime | Handover to logistics | 1,783 | Some orders not delivered |
| order_delivered_customer_date | datetime | Actual delivery date | 2,965 | Some orders not delivered |
| order_estimated_delivery_date | datetime | Estimated delivery date | 0 | Promise date to customer |

**Row Count**: 99,441
**Primary Key**: order_id
**Relationships**:
- customer_id → olist_customers_dataset.customer_id

**Order Status Values**:
- delivered: Order delivered to customer
- shipped: Order shipped but not delivered
- canceled: Order canceled
- unavailable: Product unavailable
- invoiced: Order invoiced
- processing: Order being processed
- created: Order created

**Data Quality**: Good - nulls in date fields are expected based on order status

**Important Notes**:
- Nulls in `order_approved_at`: Orders not yet approved (likely canceled)
- Nulls in `order_delivered_carrier_date`: Orders not shipped
- Nulls in `order_delivered_customer_date`: Orders not delivered
- For delivery analysis, filter by `order_status = 'delivered'`

---

### 7. olist_products_dataset.csv

**Purpose**: Product information and dimensions

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| product_id | string | Unique product identifier | 0 | Primary key |
| product_category_name | string | Product category (Portuguese) | 610 | Join with translation table |
| product_name_lenght | float | Product name length | 610 | Null with category |
| product_description_lenght | float | Description length | 610 | Null with category |
| product_photos_qty | float | Number of photos | 610 | Null with category |
| product_weight_g | float | Product weight (grams) | 2 | |
| product_length_cm | float | Product length (cm) | 2 | |
| product_height_cm | float | Product height (cm) | 2 | |
| product_width_cm | float | Product width (cm) | 2 | |

**Row Count**: 32,951
**Primary Key**: product_id
**Relationships**:
- product_id → olist_order_items_dataset.product_id
- product_category_name → product_category_name_translation.product_category_name

**Data Quality**: Fair - 610 products have missing category and metadata (likely incomplete listings)

---

### 8. olist_sellers_dataset.csv

**Purpose**: Seller information and location

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| seller_id | string | Unique seller identifier | 0 | Primary key |
| seller_zip_code_prefix | integer | Zip code prefix | 0 | |
| seller_city | string | Seller city name | 0 | |
| seller_state | string | Seller state (2-letter code) | 0 | |

**Row Count**: 3,095
**Primary Key**: seller_id
**Relationships**:
- seller_id → olist_order_items_dataset.seller_id
- seller_zip_code_prefix → olist_geolocation_dataset.geolocation_zip_code_prefix

**Data Quality**: Excellent - no null values

---

### 9. product_category_name_translation.csv

**Purpose**: Translation of Portuguese category names to English

| Column | Type | Description | Null Count | Notes |
|--------|------|-------------|------------|-------|
| product_category_name | string | Category name in Portuguese | 0 | Foreign key to products |
| product_category_name_english | string | Category name in English | 0 | |

**Row Count**: 71
**Primary Key**: product_category_name
**Relationships**:
- product_category_name → olist_products_dataset.product_category_name

**Data Quality**: Excellent - no null values

---

## Entity Relationship Diagram

```
customers (customer_id) ────────────┐
                                    │
                                    ▼
                              orders (order_id)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
  order_items (order_id)    order_payments (order_id)   order_reviews (order_id)
        │
        ├───────────────────┬───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
  products (product_id) sellers (seller_id)
        │
        ▼
category_translation (product_category_name)

customers/sellers zip_code ────────────────────┐
                                                │
                                                ▼
                                    geolocation (zip_code_prefix)
```

---

## Key Relationships Summary

| From Table | From Column | To Table | To Column | Relationship Type |
|------------|-------------|----------|-----------|-------------------|
| customers | customer_id | orders | customer_id | One-to-Many |
| orders | order_id | order_items | order_id | One-to-Many |
| orders | order_id | order_payments | order_id | One-to-Many |
| orders | order_id | order_reviews | order_id | One-to-Many |
| order_items | product_id | products | product_id | Many-to-One |
| order_items | seller_id | sellers | seller_id | Many-to-One |
| products | product_category_name | category_translation | product_category_name | Many-to-One |
| customers | customer_zip_code_prefix | geolocation | geolocation_zip_code_prefix | Many-to-Many |
| sellers | seller_zip_code_prefix | geolocation | geolocation_zip_code_prefix | Many-to-Many |

---

## Data Quality Summary

### Overall Data Quality Score: 87/100

| Table | Null % | Duplicate Rows | Quality Score | Issues |
|-------|--------|----------------|---------------|--------|
| customers | 0% | 0 | 100/100 | None |
| geolocation | 0% | 0 | 100/100 | Large file size |
| order_items | 0% | 0 | 100/100 | None |
| order_payments | 0% | 0 | 100/100 | None |
| order_reviews | 54% (comments) | 0 | 75/100 | High nulls in comments (expected) |
| orders | 2.98% (dates) | 0 | 90/100 | Nulls in delivery dates (expected) |
| products | 1.85% | 0 | 85/100 | 610 products missing category |
| sellers | 0% | 0 | 100/100 | None |
| category_translation | 0% | 0 | 100/100 | None |

### Quality Notes

1. **Order Reviews**: High null counts in comment fields are expected - not all customers leave reviews with text
2. **Orders**: Nulls in delivery dates are expected for orders not delivered (canceled, unavailable, etc.)
3. **Products**: 610 products (1.85%) missing category information - these will be excluded from category analysis
4. **Geolocation**: Large file with multiple coordinates per zip code - will need aggregation

---

## Date Fields Summary

| Table | Date Field | Format | Null Count | Usage |
|-------|------------|--------|------------|-------|
| orders | order_purchase_timestamp | YYYY-MM-DD HH:MM:SS | 0 | Order creation |
| orders | order_approved_at | YYYY-MM-DD HH:MM:SS | 160 | Payment approval |
| orders | order_delivered_carrier_date | YYYY-MM-DD HH:MM:SS | 1,783 | Shipping handover |
| orders | order_delivered_customer_date | YYYY-MM-DD HH:MM:SS | 2,965 | Actual delivery |
| orders | order_estimated_delivery_date | YYYY-MM-DD HH:MM:SS | 0 | Promise date |
| order_items | shipping_limit_date | YYYY-MM-DD HH:MM:SS | 0 | Shipping deadline |
| order_reviews | review_creation_date | YYYY-MM-DD HH:MM:SS | 0 | Review submission |
| order_reviews | review_answer_timestamp | YYYY-MM-DD HH:MM:SS | 0 | Review response |

**Timezone**: All timestamps are in UTC (Brazil timezone conversion may be needed for accurate analysis)

---

## Metric Definitions

### Revenue vs Item Price

**Important Distinction**:
- **Item Price**: Sum of `price` column from order_items (excludes freight)
- **Order Value**: Sum of `price` + `freight_value` from order_items
- **Payment Value**: Sum of `payment_value` from order_payments (may include taxes/fees)

For this project:
- Use `price` for category performance (item-price totals)
- Use `payment_value` for revenue analysis
- Calculate `price + freight_value` for total order value

### Delivery Performance Metrics

**On-Time Delivery**: Orders where `order_delivered_customer_date <= order_estimated_delivery_date`

**Delivery Delay**: `order_delivered_customer_date - order_estimated_delivery_date` (in days)

**Scope**: Only include orders with `order_status = 'delivered'` and non-null delivery dates

---

## Business Metrics Mapping

| Metric | Tables Used | Key Columns |
|--------|-------------|-------------|
| Total Orders | orders | order_id, order_status |
| Monthly Trends | orders, order_payments | order_purchase_timestamp, payment_value |
| Category Performance | order_items, products, category_translation | price, product_category_name |
| Category Order/Item Counts | order_items, products, category_translation | order_id, order_item_id |
| Delivery Performance | orders | order_status, delivery dates |
| Order Status Distribution | orders | order_status |
| RFM Analysis | orders, customers, order_payments | dates, customer_unique_id, payment_value |
| Regional Performance | customers, orders | customer_state, order_status |
| Seller Performance | order_items, sellers | seller_id, price |
| Geospatial Analysis | geolocation, customers, sellers | lat, lng, zip_code_prefix |

---

## File Sizes

| File | Size | Notes |
|------|------|-------|
| olist_customers_dataset.csv | ~2 MB | |
| olist_geolocation_dataset.csv | 58.44 MB | ⚠️ Large file |
| olist_order_items_dataset.csv | ~15 MB | |
| olist_order_payments_dataset.csv | ~8 MB | |
| olist_order_reviews_dataset.csv | ~10 MB | |
| olist_orders_dataset.csv | ~7 MB | |
| olist_products_dataset.csv | ~3 MB | |
| olist_sellers_dataset.csv | ~0.5 MB | |
| product_category_name_translation.csv | ~0.01 MB | |
| **Total** | **~104 MB** | |

**Note**: The geolocation file is large. When loading, consider sampling or aggregating by zip code prefix.

---

## Data Usage Recommendations

### For Bronze Layer
- Load all CSVs as-is
- Preserve original schemas
- No transformations

### For Silver Layer
- Join related tables
- Handle null values appropriately
- Convert date strings to datetime types
- Add English category names via translation table

### For Gold Layer
- Filter orders by status for delivery metrics
- Aggregate by appropriate dimensions
- Calculate derived metrics (RFM, delivery delay, etc.)
- Use customer_unique_id for customer-level analysis

---

## Next Steps

1. ✅ Schema documentation complete
2. ⏳ Data profiling report (next)
3. ⏳ Fix Java PATH for PySpark
4. ⏳ Begin Bronze layer implementation

---

**Last Updated**: 2026-10-24
**Version**: 1.0
