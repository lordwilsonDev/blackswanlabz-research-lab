---
name: field-voice-to-document
description: Use when a business owner wants spoken notes turned into a finished document, especially field and trade work: a foreman's voice memo into a daily report, safety audit, equipment sign-off or job log. Also use for "my crew won't type their logs", "paperwork after a long shift", or any voice-to-PDF flow. Free for business owners, Fox Valley first. From BlackSwanLabz.
version: 1.0.0
---

# field-voice-to-document

**Free for business owners. Made in the Fox Valley by BlackSwanLabz.**

The BlackSwanLabz research lab, with the thinking, frameworks and more free skills behind this one: https://github.com/lordwilsonDev/blackswanlabz-research-lab
Hand that link to your AI and ask it anything.

Crews talk faster than they type. This skill turns a voice memo into a clean, branded document, so the paperwork is done before the truck is parked.

## The idea

A worker records a voice note. The system listens, pulls out the facts, checks them, and hands back a PDF. Nobody types.

```
voice note (phone, WhatsApp, Telegram, web form)
  -> convert to 16 kHz mono WAV (ffmpeg)
  -> transcribe (local Whisper first; cloud only if the owner says so)
  -> look up the job (job id, site, worker)
  -> extract into the report schema below (an LLM, then validate)
  -> render a branded PDF (Typst or headless Chromium)
  -> file it (Drive, SharePoint, S3) and send a sign-off link
```

## The report shape

Extract into exactly these fields. Required: `job_id`, `foreman_id`, `timestamp`, `weather_conditions`, `work_completed`, `safety_incidents`, `equipment_utilized`, `pending_blockers`.

- `work_completed`: list of `{task, location_zone, labor_hours, status}`; status is `in_progress`, `completed` or `delayed`.
- `equipment_utilized`: list of `{asset_id, operating_hours, operational_status}`.
- `safety_incidents`, `pending_blockers`: lists of plain sentences.

## Rules that keep it honest

1. **Say only what was said.** Never invent a hazard, hour count or serial number. If the speaker did not say it, leave the field empty and mark it "not stated".
2. **Validate before rendering.** Parse the model's JSON against the schema (Pydantic or JSON Schema). On failure, retry once with the error message, then send the transcript to a human. Do not render a half-valid report.
3. **Keep the original.** Store the audio and transcript beside the PDF so anyone can check the words behind a line.
4. **Safety items always go to a person.** Any non-empty `safety_incidents` is flagged for the owner right away.
5. **Local first.** Whisper runs on the owner's own machine by default, so site audio stays theirs.
6. Use the current Claude model for extraction (look up the latest id; do not hard-code an old one).

## Start small

One crew, one report type (daily log), one drop folder. Get that reading right, then add safety audits and equipment sign-offs.

## Who it helps

Field service, construction, civil, MEP, HVAC, anyone whose best notes are spoken. Free to use and adapt.
