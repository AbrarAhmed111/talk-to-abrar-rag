# Project: MamtaAI — AI-Powered Baby-Care Platform

## Overview
- **Project Name:** MamtaAI
- **Category:** Artificial Intelligence / Healthcare SaaS
- **Type:** Client Delivery
- **Live URL:** https://mamtaai.vercel.app/
- **GitHub Repository:** https://github.com/AbrarAhmed111/mamtaAi
- **Tech Stack:** Next.js 15, React 19, TypeScript, Python, FastAPI, Supabase (Auth, Database, Storage), Tailwind CSS, Machine Learning

## What is MamtaAI?
MamtaAI is a modern baby care and health tracking platform powered by artificial intelligence. It serves parents, caregivers, and extended family by combining daily activity tracking (feeding, sleeping, milestone logging) with automated baby cry analysis powered by a machine-learning acoustic processing pipeline.

## The Problem It Solves
New parents often struggle to decipher why an infant is crying and frequently experience communication gaps when multiple caregivers (parents, grandparents, babysitters) manage the baby's routine across different disjointed notes or apps. MamtaAI provides a unified, trustworthy digital health hub.

## Architecture & Specialized GitHub Repositories
The MamtaAI system is architected as a decoupled multi-service platform across three specialized repositories:
1. **Core Web App & SaaS (`AbrarAhmed111/mamtaAi`):**
   - **Repository:** https://github.com/AbrarAhmed111/mamtaAi
   - **Tech Stack:** Next.js 15, React 19, TypeScript, Tailwind CSS, Supabase (Auth, DB, Storage), Stripe.
   - **Features:** Caregiver and family collaboration, daily activity logs (feeding, sleeping, milestone tracking), Stripe subscription billing, notifications, and parent community forum.
2. **Audio ML & Cry Classification Backend (`AbrarAhmed111/mamtaai-ml`):**
   - **Repository:** https://github.com/AbrarAhmed111/mamtaai-ml
   - **Tech Stack:** Python 3, FastAPI, Machine Learning, Audio Signal Processing.
   - **Features:** Processes infant cry audio files, extracts acoustic features, and classifies cry states with endpoints for model training, inference, and real-time processing.
3. **Product & Customer Support RAG Assistant (`AbrarAhmed111/mamtaai-rag`):**
   - **Repository:** https://github.com/AbrarAhmed111/mamtaai-rag
   - **Tech Stack:** Python 3, FastAPI, RAG, LLM APIs.
   - **Features:** Fast, grounded, and cost-efficient retrieval-augmented question answering for onboarding, feature explanations, caregiver workflows, and subscription assistance.

## What Abrar Ahmed Personally Built
Abrar owned the full-stack architecture and technical delivery from concept to production:
1. **System Architecture:** Designed a decoupled `nextjs-fastapi` architecture where Next.js 15 handles web presentation, user state, and community interactions, while FastAPI handles heavy acoustic data processing and RAG intelligence.
2. **Audio ML Pipeline:** Engineered the FastAPI service for audio signal processing, acoustic feature extraction, and baby cry classification with real-time prediction and training endpoints.
3. **RAG Knowledge Assistant:** Implemented the specialized RAG assistant (`mamtaai-rag`) for fast user support and product navigation.
4. **Caregiver Collaboration:** Implemented multi-user family invites and role-based access control (RBAC), allowing parents to grant customized permissions to family members and nannies.
5. **Interactive Dashboard & Community:** Built responsive activity logging timelines, health insight popovers, notifications, and a community space with articles, discussion forums, and favorite resources.
6. **Cloud Deployment:** Set up continuous production deployments on Vercel and secure Supabase database environments.

## Results & Impact
- Shipped a fully functioning AI product with active live access at `mamtaai.vercel.app`.
- Provided real acoustic classification replacing guesswork for caregivers.
- Engineered three integrated repositories spanning frontend SaaS, acoustic ML, and RAG intelligence.

