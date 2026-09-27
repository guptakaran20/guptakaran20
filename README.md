<div align="center">

# Hi 👋, I'm Karan Gupta

### Full Stack Developer • Backend Engineer • Software Engineer

Building distributed backend systems, AI-powered applications, and real-time web platforms.

<p>
<a href="https://guptakaran0720.vercel.app">
<img src="https://img.shields.io/badge/Portfolio-Visit-success?style=for-the-badge"/>
</a>
<a href="https://github.com/guptakaran20">
<img src="https://img.shields.io/github/followers/guptakaran20?style=for-the-badge&logo=github"/>
</a>
<a href="https://linkedin.com/in/guptakaran0720">
<img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin"/>
</a>
<a href="https://leetcode.com/u/guptakaran0720/">
<img src="https://img.shields.io/badge/LeetCode-1870%20Knight-FFA116?style=for-the-badge&logo=leetcode&logoColor=white"/>
</a>
<a href="https://guptakaran0720.vercel.app/resume.pdf">
<img src="https://img.shields.io/badge/Resume-Download-orange?style=for-the-badge&logo=readthedocs"/>
</a>
<a href="mailto:guptakaran0720@gmail.com">
<img src="https://img.shields.io/badge/Gmail-Contact-red?style=for-the-badge&logo=gmail"/>
</a>
</p>

<img src="https://komarev.com/ghpvc/?username=guptakaran20&label=Profile%20Views&color=0e75b6&style=flat"/>

</div>

---

# 💫 About Me

```text
$ whoami

Karan Gupta

Full Stack Developer @ XCEED NIT Jalandhar

B.Tech Instrumentation & Control Engineering
NIT Jalandhar (2025 – 2029) · CGPA 8.49

Currently Building @ XCEED
├── ILEED – Intelligent Learning Engagement and Entity Detection
└── XCEED Learning App – Android & iOS (Capacitor)

Recently Shipped
├── EventFlow     → distributed workflow orchestration engine
├── ImportlyAI    → AI-powered CSV import pipeline
├── CodeArena     → real-time coding battle platform
└── Aarogya Club  → real-time orientation quiz (9 merged PRs)

Interested In
├── Distributed Systems
├── AI Applications
├── Data Science
└── Cloud-native Infrastructure
```

---

# 🏆 Highlights

- 💼 Full Stack Developer @ **XCEED NIT Jalandhar** — attendance platform for **1,000+ students** across **30+ cameras**
- 📈 **1,400+ contributions** on GitHub in the last year
- 🔀 **160 pull requests raised, 149 merged** — **135** at XCEED, **10** to community & open-source repos
- 📱 Built the **XCEED Learning App** (Android, with iOS on the way) — delta OTA updates, push notifications and an automated web → app sync pipeline
- 🌱 **GSSoC'26** contributor — merged PR tagged `level:advanced`
- 🟠 **600+** LeetCode problems solved · **1870 rating** · ⭐ **Knight** · top **5.7%** globally
- ⚡ Hands-on with **Redis Streams**, **WebSockets**, **gRPC** and **real-time distributed systems**
- 🐳 Dockerizing services with CI pipelines (lint, type-check, tests) on **GitHub Actions**
- ☁️ Deploying on **AWS EC2 + Nginx**, **Render** and **Vercel**

---

# 💼 Experience

### 🏅 Full Stack Developer — XCEED, NIT Jalandhar &nbsp;·&nbsp; *Jun 2026 – Present*

`145 PRs` `135 merged` `560 commits` across the institute's AMS platform and its mobile app

#### 🎯 ILEED – Intelligent Learning Engagement and Entity Detection

AI attendance platform for **1,000+ students** across **30+ cameras**

`140 PRs` `131 merged` `269 commits` `Jun – Sep 2026`

`Node.js` `Express` `React` `Python` `MongoDB` `FAISS` `ONNX` `FFmpeg` `FCM` `PM2`

**🧠 Face recognition & ML pipeline**
- Built real-time, institute-wide student identification from uploaded videos and **live RTSP streams** on a **FAISS** vector index, with **RetinaFace (ONNX)** detection and automatic model download
- Automated ERP face-embedding generation, **nightly subject-embedding rebuilds**, and active learning from backup images with low-confidence eviction
- Added unknown-face storage and automated face clustering with confidence scores; integrated **Gemini** as the primary AI generation provider

**📸 Ground truth & attendance workflows**
- ERP photo upload and roster sync from the student database, plus a split-screen ground-truth editor with side-by-side ERP reference photos for double verification
- Ground-truth acquisition limited to college hours, forenoon/afternoon room acquisition, and **slot-wise attendance control**
- Attendance push and in-app notifications, delivered only to enrolled students

**🎥 Streaming & recording**
- Migrated the RTSP recording architecture to the Node.js backend: scheduled recordings, downloads and MP3 audio extraction
- Live-preview auto-retry and stale-frame detection; fixed a use-after-free when an RTSP capture was released before its reader thread stopped

**🛠️ Reliability, DevOps & observability**
- One-click **Pull & Deploy** with a health check and **automatic rollback**; an ML-service deploy button that replaced manual `scp`
- **GPU inventory dashboard** with best-card selection, MIG-slice and per-service VRAM telemetry; fixed an H100 crash-loop
- Health monitoring, recovery/lifecycle email alerts, a twice-daily uptime digest, an SMTP-lockout-safe mail outbox, and a server error console
- Fixed a production memory leak, moved ML/data routes to non-blocking I/O, repaired the client & server test suites, and added one-click MongoDB backups

**🔐 Security**
- Fixed broken access control for the student role, a pre-quiz data leak, unauthenticated exposure of ERP roll numbers, and Host-header trust in OTA download URLs

#### 📱 XCEED Learning App — Android & iOS

The AMS web platform as a native mobile app: kept in sync with the web codebase and updated over the air.

`5 PRs` `4 merged` `291 commits` `Aug – Sep 2026`

`React` `Vite` `Capacitor` `Capgo Updater` `FCM` `TanStack Query` `GitHub Actions`

- **Built the app from the first commit:** PIN + native biometric sign-in, camera capture, multi-account switching, and deep links (Android App Links, iOS universal links)
- **OTA update pipeline:** a secure OTA server with GitHub Action deploys and an admin "Publish OTA" button, then **delta OTA** that downloads only the files a release changed, instead of a ~21.6 MB, 574-file zip every time
- **AMS → app sync pipeline:** 75 automated syncs of the web client through a vendor branch, with custom merge drivers and automatic resolution of additive conflicts. Mobile-only behaviour lives behind override "seams" so the app never edits AMS files, and an `ams-edits` checker enforces it (sped up from 87s to 0.3s)
- **Push notifications** via **Firebase Cloud Messaging**: attendance and quiz alerts, broadcasts to every app user, many-to-many device-token registration
- **Offline-first caching:** TanStack Query persisted to Capacitor Preferences and bounded by build version; a global 401 interceptor that ends zombie sessions
- Native file handling (timetable PDFs, study material and CSV exports saved in-app), leaner OTA and APK bundles, and keeping session tokens out of stream URLs
- Bringing the **iOS platform** into the repo: CocoaPods, a light/dark launch screen and app icon

<sub>🔒 Private organisation repositories — stats are from the PRs and commits I authored.</sub>

---

# 🌍 Open Source & Community Contributions

| Repository | Pull Requests | What I contributed |
|---|---|---|
| [**AarogyaClubNITJ/aarogya**](https://github.com/AarogyaClubNITJ/aarogya/pulls?q=is%3Apr+author%3Aguptakaran20) | **9 merged** · Aug 2026 | [#1](https://github.com/AarogyaClubNITJ/aarogya/pull/1) Real-time orientation quiz module — WebSocket-driven display screen with a QR code that rotates every 2s, token pool, live top-10 leaderboard, anti-cheat tab-switch detection, JWT admin login<br>[#2](https://github.com/AarogyaClubNITJ/aarogya/pull/2) Explicit CORS allowlist for Express + Socket.IO and IP rate limiting behind Render's proxy<br>[#15](https://github.com/AarogyaClubNITJ/aarogya/pull/15) 3-lifeline quiz system, with a submit lock that fixes a double-click race condition<br>#3, #12, #13, #16, #17, #18 — API config, UI & question bank, CORS fix, token TTL, leaderboard sound, phone field |
| [**Abhishek-Verma0/Employee-Leave-Management-System**](https://github.com/Abhishek-Verma0/Employee-Leave-Management-System/pull/65) | **1 merged** · GSSoC'26 `level:advanced` | [#65](https://github.com/Abhishek-Verma0/Employee-Leave-Management-System/pull/65) Hardened auth validation (email normalization), ObjectId guards that return `400` instead of crashing with `500`, reimbursement amount validation, richer dashboard `populate`, and a standard `success` API contract |

---

# 🚀 Featured Projects

## ⚙️ EventFlow

Distributed Workflow Orchestration Engine &nbsp;·&nbsp; `53 commits · Jul 2026` &nbsp;·&nbsp; `MIT`

**Features**

- Graph-based DAG workflow execution with a visual **DAG editor**
- Distributed, auto-scaling workers on **Redis Streams**
- Retry policies, **Dead Letter Queue** and one-click retry of dead-lettered nodes
- Worker heartbeats and stuck-job recovery with `XPENDING` / `XCLAIM`
- **gRPC + Protobuf** internal transport and `Idempotency-Key` support
- Real-time execution updates over **WebSockets**, with paginated observability APIs, metrics and logs
- API-key + **JWT** authentication, rate limiting and security hardening
- CI on GitHub Actions: `ruff` lint, `mypy` type-check, `pytest`
- Dockerized: PostgreSQL + Redis + FastAPI + Next.js

**Tech**

`FastAPI` `Python` `Next.js` `Alembic` `PostgreSQL`
`Redis Streams` `SQLAlchemy` `gRPC` `Docker` `Render`

<p>
<a href="https://goeventflow.vercel.app"><img src="https://img.shields.io/badge/Live-Demo-success?style=flat-square"/></a>
<a href="https://github.com/guptakaran20/EventFlow"><img src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github"/></a>
</p>

---

## ⚔️ CodeArena

Real-Time Competitive Coding Platform &nbsp;·&nbsp; `50 commits · Jun 2026`

**Features**

- Live 1v1 coding battles with **Redis**-backed matchmaking
- **Tournaments** with brackets, live leaderboards and notifications
- **Socket.IO** sync for battle rooms, contest state and player presence
- Multi-language sandboxed code execution with **Piston** (migrated from Judge0)
- AI-assisted features and an **admin portal**
- JWT + **Google OAuth** authentication
- Deployed with Docker on **AWS EC2 + Nginx** through a GitHub Actions deploy pipeline
- **Prometheus + Grafana** monitoring stack

**Tech**

`Next.js` `TypeScript` `Node.js` `Express` `MongoDB` `Redis`
`Socket.IO` `Docker` `AWS EC2` `Nginx` `Prometheus` `Grafana`

<p>
<a href="https://codearenabattle.vercel.app"><img src="https://img.shields.io/badge/Live-Demo-success?style=flat-square"/></a>
<a href="https://github.com/guptakaran20/CodeBattle"><img src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github"/></a>
</p>

---

## 🤖 ImportlyAI

AI-Powered CSV Import Platform &nbsp;·&nbsp; `15 commits · 1 merged PR · Jul 2026`

- Multi-stage **Gemini** extraction pipeline that maps any CSV onto a standard CRM schema
- Automatic schema detection and intelligent field mapping
- Live import progress streamed over **Server-Sent Events**
- Batched inference tuned for large, inconsistent datasets
- **180+** automated benchmark tests
- Monorepo (`apps/` + `packages/`), dark mode, Docker Compose

**Tech**

`Next.js` `TypeScript` `Node.js` `Express` `Gemini API` `PapaParse` `Docker`

<p>
<a href="https://importlyai.vercel.app"><img src="https://img.shields.io/badge/Live-Demo-success?style=flat-square"/></a>
<a href="https://github.com/guptakaran20/ImportlyAI"><img src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github"/></a>
</p>

---

## 💼 SponsorGrid

Full Stack SaaS Sponsorship Platform &nbsp;·&nbsp; `41 commits · 3 merged PRs · Feb – Mar 2026`

- Sponsor, deal and funding-workflow management
- Cookie-based auth (HttpOnly access token) with **CSRF protection**
- **Google OAuth** and a forgot/reset-password flow
- **Zod** request validation and API throttling
- **Cloudinary** image uploads for company profiles
- PostgreSQL + **Prisma ORM**, GitHub Actions CI, Nginx + Docker config

**Tech**

`Next.js` `TypeScript` `PostgreSQL` `Prisma` `Zod` `Cloudinary` `Docker`

<p>
<a href="https://trysponsorgrid.vercel.app"><img src="https://img.shields.io/badge/Live-Demo-success?style=flat-square"/></a>
<a href="https://github.com/guptakaran20/Sponsorship"><img src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github"/></a>
</p>

---

## 🧩 More Projects

| Project | What it is | Stack |
|---|---|---|
| 🛒 [**Arovia Vibes**](https://github.com/guptakaran20/AroviaVibes) · [Live](https://aroviavibes.vercel.app) | Production eCommerce store with an admin panel, analytics and email workflows | `Next.js` `Supabase` `Resend` |
| 🎭 [**SeatSphere**](https://github.com/guptakaran20/SeatSphere) | Auditorium booking & event management: club event requests, admin approvals, seat locking & booking, QR ticket validation, OTP auth, 3D hero UI | `Next.js` `Prisma` `NextAuth` |
| 🌐 [**Portfolio**](https://github.com/guptakaran20/portfolio) · [Live](https://guptakaran0720.vercel.app) | Personal portfolio with SEO optimisation · 54 commits | `Next.js` `TypeScript` |

---

# 🗓️ 2026 Build Log

```text
Jan  ▸ Set up this profile + contribution-snake workflow · Face-Detector
Feb  ▸ StrangerBlogs · started SponsorGrid
Mar  ▸ SponsorGrid: OAuth, throttling, production deploy
Apr  ▸ Shipped Arovia Vibes · launched portfolio · started SeatSphere
May  ▸ GSSoC'26 PR #65 (merged) · SeatSphere auth, roles & dashboards
Jun  ▸ Joined XCEED · ERP auto-embeddings, unknown-face clustering · built CodeArena in 10 days
Jul  ▸ FAISS live-stream identification @ XCEED · ImportlyAI (2 days) · EventFlow (10 days)
Aug  ▸ Launched the XCEED Learning App: OTA updates, biometric sign-in, push · Aarogya quiz: 9 PRs in 6 days
Sep  ▸ Delta OTA, AMS → app sync pipeline, iOS platform · Pull & Deploy with auto-rollback, GPU dashboard
```

---

# 💻 Tech Stack

## 📝 Languages

<img src="https://skillicons.dev/icons?i=cpp,python,ts,js"/>

---

## 🎨 Frontend

<img src="https://skillicons.dev/icons?i=react,nextjs,tailwind,html,css"/>

React Query • Redux Toolkit • Framer Motion

---

## ⚙️ Backend

<img src="https://skillicons.dev/icons?i=fastapi,nodejs,express"/>

REST APIs • WebSockets • Socket.IO • Server-Sent Events • gRPC • JWT • OAuth

---

## 🗄️ Database & Storage

<img src="https://skillicons.dev/icons?i=postgres,mongodb,redis,mysql"/>

SQLAlchemy • Prisma ORM • Supabase • Redis Streams • FAISS

---

## ☁️ DevOps & Cloud

<img src="https://skillicons.dev/icons?i=docker,aws,nginx,git,github,vercel"/>

Docker Compose • GitHub Actions CI/CD • PM2 • Prometheus • Grafana • Linux • Render

---

## 📱 Mobile

<img src="https://skillicons.dev/icons?i=androidstudio,firebase"/>

Capacitor • Firebase Cloud Messaging • Android

---

## 🛠️ Tools & Technologies

ONNX Runtime • FFmpeg • TanStack Query • Alembic • Pydantic • Zod • Gemini API • Piston • Cloudinary • Postman

---

# 🚀 Currently Exploring

- ☸️ Kubernetes
- ⚡ Microservices
- 📡 Cloud Infrastructure
- 🧮 Data Science
- 🤖 AI Agents & LLM Integrations

---

# 📈 GitHub Analytics

<p align="center">
<img height="170" src="https://github-readme-stats.vercel.app/api?username=guptakaran20&show_icons=true&theme=tokyonight&hide_border=true"/>
<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=guptakaran20&layout=compact&theme=tokyonight&hide_border=true"/>
</p>

<p align="center">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=guptakaran20&theme=tokyonight&hide_border=true"/>
</p>

<p align="center">
<img width="95%" src="https://github-readme-activity-graph.vercel.app/graph?username=guptakaran20&theme=tokyo-night&hide_border=true"/>
</p>

---

# 🐍 Contribution Snake

<p align="center">
<img src="https://raw.githubusercontent.com/guptakaran20/guptakaran20/output/github-contribution-grid-snake.svg"/>
</p>

---

# 💭 Philosophy

> Build software that is scalable, reliable, and enjoyable to use.

I enjoy solving backend challenges involving distributed systems, AI integrations, cloud infrastructure, and real-time communication.

<h2 align="center"><strong>Eat Code Sleep Repeat</strong></h2>

---

<div>

## 🤝 Let's Connect

I'm always interested in collaborating on:

**Backend Engineering • AI Applications • Developer Productivity Tools • Cloud & DevOps • Open Source**

⭐ If you like my work, don't forget to star my repositories!

</div>
