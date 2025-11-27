# Payment & Monetization Integration Plan (TapPay)

## 1. Overview
This document outlines the plan to integrate **TapPay (Tappy)** for payment processing and implement a usage-based monetization model for Carte AI.

**Goal**:
- New users receive **10 free searches**.
- Beyond 10, users must **Subscribe** (Monthly) or **Purchase Credits** (Single/Bundle).
- Enable a mechanism to grant access to friends (Coupon/Referral).

---

## 2. Monetization Model

### A. User Tiers
1.  **Free User**:
    - Default upon registration.
    - **Balance**: 10 Credits (1 Credit = 1 Recommendation Request).
    - **Limit**: Hard stop when credits = 0.
2.  **Subscriber (Pro)**:
    - **Monthly Plan**: NT$ 90/month.
    - **Yearly Plan**: NT$ 720/year (Save ~33%).
    - **Benefit**: Unlimited searches.
3.  **Pay-As-You-Go (Single)**:
    - One-time purchase.
    - **Price**: NT$ 30 for 1 search (or a small bundle, e.g., 3 searches). *Clarification needed: Is "Single 30" for 1 search or a day pass? Assuming 1 search or small pack for now.*

### B. "Friend Trial" Strategy
- **Coupon System**: Implement a simple code redemption endpoint.
    - Admin generates codes (e.g., `VIP-FRIEND`).
    - User redeems code -> Adds credits or grants X days of Pro status.

---

## 3. Technical Architecture

### A. Database Schema (Firestore: `users` collection)
Update the user document structure to track usage and subscription.

```json
{
  "uid": "user_123",
  "email": "user@example.com",
  "credits": 10,                // Remaining search credits
  "total_searches": 5,          // Lifetime usage stats
  "subscription": {
    "status": "active",         // "active", "inactive", "canceled"
    "plan_id": "monthly_pro",
    "current_period_end": "2025-12-31T23:59:59Z",
    "tappy_rec_trade_id": "rec_..." // For recurring payments
  },
  "is_friend_referral": false   // Flag for special tracking
}
```

### B. Backend API (`payment-service`)

#### 1. Usage Check Middleware
- **Before** every `POST /api/recommendation`:
    - Check `db.users.get(uid).credits > 0` OR `subscription.status == 'active'`.
    - If valid: Proceed, then decrement credit (if not subscribed).
    - If invalid: Return `403 Payment Required`.

#### 2. Payment Endpoints
- `POST /api/payment/pay-by-prime`:
    - Receives `prime` token from frontend.
    - Calls TapPay `pay-by-prime` API.
    - On success: Update user credits or subscription status.
- `POST /api/payment/redeem`:
    - Input: `code` (string).
    - Logic: Validate code -> Grant credits.

### C. Frontend Integration (TapPay)

#### 1. TapPay SDK Setup
- Load TapPay SDK in `layout.tsx` or a dedicated `PaymentProvider`.
- Configure with `APP_ID` and `APP_KEY`.

#### 2. UI Components
- **Pricing Modal**: Shows when user hits limit.
    - Options: "Subscribe (NT$199/mo)" vs "Buy 5 Credits (NT$50)".
- **TPDirect Form**: Secure iframe for credit card input.
    - `TPDirect.card.getPrime((result) => { ... })`

---

## 4. Implementation Steps (Phased)

### Phase 1: Foundation (The "Skeleton")
- [ ] Update Firestore `save_user_activity` to also track/deduct credits.
- [ ] Create `PaymentService` class (mocked initially).
- [ ] Add `check_user_quota` dependency to `dining_agent.py`.

### Phase 2: TapPay Integration
- [ ] Register for TapPay Sandbox.
- [ ] Implement `pay_by_prime` in backend.
- [ ] Build Frontend Payment Modal with `TPDirect`.

### Phase 3: Subscription & Coupons
- [ ] Implement recurring payment logic (TapPay `card_token`).
- [ ] Build Coupon redemption UI.

---

## 5. Quick Start for AI (Context for LLM)
*When implementing, follow these rules:*
1.  **Fail Safe**: If payment service is down, default to allowing access (or fail gracefully with a nice message), don't crash.
2.  **Secure**: Never log credit card numbers. Only log `rec_trade_id` or transaction results.
3.  **Atomic**: Credit deduction and API generation should ideally happen closely. If generation fails, refund the credit.

