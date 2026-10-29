---
name: self-driving-intake
description: Use when a business owner loses leads between the inquiry form and the booked appointment: unpaid invoices, unsigned waivers, "they filled out the form and vanished". Builds an intake funnel that moves a new lead through payment, paperwork and scheduling on its own. For solo practices, clinics, consultants, coaches, small legal offices. Free for business owners, Fox Valley first. From BlackSwanLabz.
version: 1.0.0
---

# self-driving-intake

**Free for business owners. Made in the Fox Valley by BlackSwanLabz.**

The BlackSwanLabz research lab, with the thinking, frameworks and more free skills behind this one: https://github.com/lordwilsonDev/blackswanlabz-research-lab
Hand that link to your AI and ask it anything.

Most people who ask for an appointment mean it. They drop off because the next step was unclear or came late. This skill gives every lead a clear next step, at the right time, until they are booked.

## The flow

```
form submitted
  -> dedupe (same person, same hour = one lead)
  -> create the contact, score priority
  -> send the payment link (Stripe Checkout)
       paid    -> send intake form + waiver -> signed -> send scheduling link -> booked
       unpaid  -> friendly nudge at 12h and 24h
```

## States

| State | Starts when | The system does | If nothing happens |
|---|---|---|---|
| `LEAD_SUBMITTED` | form arrives | create contact, score priority | flag a bad email for a person |
| `PAYMENT_PENDING` | checkout link made | text + email the link | nudge at 12h and 24h |
| `DOCS_PENDING` | payment confirmed | send questionnaire and waiver | text at 18h |
| `SCHEDULE_READY` | signature verified | send a private scheduling link | alert staff after 48h |
| `CONFIRMED` | booking registered | set up the call, put prep notes in the CRM | send a brief 2h before |

## Rules

1. **Move on facts, not guesses.** A state changes only on a real event: a Stripe `checkout.session.completed` webhook, a verified signature, a calendar booking.
2. **Safe to repeat.** Every webhook handler is idempotent: the same event twice changes nothing the second time. Lock on the lead id.
3. **Kind nudges, capped.** Two reminders per step, never more. Every message offers a human reply path and an opt-out.
4. **Respect consent and privacy.** Collect only what the practice needs. For health or legal intake, store sensitive answers in a system the owner already trusts and has the right agreements with (for example HIPAA terms); do not copy them into logs or prompts.
5. **Staff see everything.** A simple dashboard lists each lead, its state and its next timer.
6. **Test with Stripe test mode** and a fake lead before any real person touches it.

## Start small

One form, one payment link, one reminder. Add waivers and scheduling once the first loop runs clean.

## Who it helps

Solo practitioners, clinics, consultants, coaches, small law offices. Free to use and adapt.
