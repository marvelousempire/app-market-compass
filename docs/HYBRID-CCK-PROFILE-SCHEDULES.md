# Hybrid CCK profile schedules for universal measurement

**State:** draft Market Compass domain projections (2026-11-03). Not canonically registered, not CCK-certified, not scheduled jobs, and not commissioned on FiveMac.

## Authority and separation

- **CCK That** (`marvelousempire/cck-that`) governs the 77-field Crown / Character / Key profile and its minimum required floor. A field label is not a Queen Yeah Right witness or a SHA attestation.
- **Schema That Studio** (`marvelousempire/schema-that-studio`) publishes indexed schemas by ID and SHA-256; never silently copy its canonical JSON Schema or claim registration. The draft `contracts/hcck-profile-schedule.v1.schema.json` here needs upstream review and catalog registration before canonical use.
- **ELSE** authors and governs versioned measurement methods and perspectives. A user-supplied method in Market Compass is not automatically an ELSE-approved method.
- **READYPLAY** owns player evidence/consent and official game/training records. Market Compass consumes an *authorized* export only after a future integration.
- **Market Compass** owns the general study/visualization and the local draft schedule templates. They are not a financial market or an enforcement of foreign source ownership.

Each profile schedule describes a domain's required metadata, when a measurement should be recorded, whether an evidence reference is required, and what subject type may be simulated. It is **not** a daemon or an authority to retrieve records. Observation times are explicit UTC timestamps in the example request.

## Draft catalog

| Profile ID | Subject | Schedule | Evidence ref |
| --- | --- | --- | --- |
| `readyplay-player-v1` | Consented player performance | Accepted game or session | Required |
| `equity-v1` | Stock / quoted company | Source session or day | Required |
| `option-v1` | Option contract | Quote snapshot | Required |
| `device-v1` | Phone, computer, camera | Inspection or reading | Optional |
| `batch-v1` | Eggs or a physical batch | Batch inspection | Optional |
| `participant-v1` | Market Compass participant/section | Authorized method or evidence update | Required |
| `general-v1` | Other measurable subject | Source observation | Optional |

Participant template instances are **Omo's Intel** (King of Clubs), **Prince's Principles** (King of Diamonds), **Prince's Intel** (no King card), **Marvin's Metrics** (King of Spades), and **Wuda's Watch** (King of Hearts). Names and cards grant no scoring, source access, or trade permissions. The King of Hearts is assigned, not reserved.

## Browser workflow in the Market Compass development branch

1. In **Choose the Measurement Profile**, select one of the seven schedule templates.
2. For the participant profile, choose the named section and inspect its King-card label.
3. Review the domain's required source fields, cadence, and evidence requirements.
4. Select **Load synthetic profile into Simulation Lab**. The example is strictly synthetic, including any player, options or equity metadata; it is not a verified source read.
5. Select **Simulate**. The browser sends the full profiled payload to `POST /api/hcck/simulate`, which checks subject type, required fields and evidence references, then calculates using the existing `POST /api/simulate` kernel only after shape checks pass.
6. A held request shows the exact missing/unknown fields and generates **no chart**. A valid draft shape shows a hypothetical 0–100 method-relative points chart and can be downloaded with **Export JSON**.

An ordinary unprofiled laptop example still uses `POST /api/simulate`; loading a profile does not break it.

## Contract endpoints

- `GET /api/hcck/profiles`: seven local profile templates, five participant instances, required CCK minimum fields, schema-owner references and `schedules_running: false`.
- `POST /api/hcck/simulate`: `profile_id`, `source_fields`, a nonempty draft `cck_profile_ref`, and a `simulation` object.
- `POST /api/simulate`: generic subject, author-defined metrics/weights, timestamped observations.
- `GET /api/participants`: independent names and King-card metadata.

A matching draft is returned as `state: draft-shape-matched` with `cck_witness_verified: false` and `source_verified: false`. The system cannot claim a real CCK-issued certificate, verified consent, Gitea source authority, ELSE methodology signature, or READYPLAY player verification from these inputs alone. Invalid types and unauthorized subjects are rejected; missing source fields or required reference markers return a **held** response.

## Tests and commissioning boundary

Tests cover the seven templates and five named participants, source-field holds, subject-kind mismatch, READYPLAY evidence-reference holds, equity/option read-only constraints, ordinary unprofiled simulation, browser asset loading, and that the draft JSON Schema matches the profile fields and schedules.

The draft JSON Schema has not been registered in Schema That Studio. The upstream CCK owner has not performed its witness and readback, Gitea authority remains to be reconciled, and no live Mac runtime readback exists. The next owner-authorized bricks are upstream schema registration, issued CCK profile records, an ELSE method publisher, READYPLAY consented evidence adapter, and signed commissioning receipts.
