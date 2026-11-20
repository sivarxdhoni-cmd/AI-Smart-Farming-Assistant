# Smart Farming RAG - Agricultural Source Registry

## Purpose

This registry tracks authoritative agricultural information used by the Smart Farming Assistant.

Demo documents must not be treated as verified agricultural advice.

## Source 1 - Tamil Nadu Agricultural University

- Organization: Tamil Nadu Agricultural University (TNAU)
- Source type: Official agricultural university
- Region: Tamil Nadu, India
- Topic: Rice cultivation and crop production
- URL: https://agritech.tnau.ac.in/agriculture/agri_cropproduction_cereals_rice_season.html
- Status: IDENTIFIED - NOT YET INGESTED
- Review required: Yes

## Source 2 - TNAU Crop Production Guide

- Organization: TNAU and Directorate of Agriculture
- Document: Crop Production Guide - Agriculture 2020
- Region: Tamil Nadu, India
- URL: https://www.agritech.tnau.ac.in/pdf/AGRICULTURE.pdf
- Local file: data/raw_sources/TNAU_Crop_Production_Guide_2020.pdf
- PDF pages: 454
- ChromaDB chunks: 1529
- Status: OFFICIAL TNAU-HOSTED SOURCE - INGESTED
- Publisher verification: Official TNAU-hosted document
- Publication year: 2020
- Review required: Yes - verify recommendation currency and regional applicability.

## Source 3 - Indian Council of Agricultural Research

- Organization: Indian Council of Agricultural Research (ICAR)
- Document: Kharif Agro-Advisories for Farmers 2025
- Region: India (advisories may be state-specific)
- URL: https://icar.gov.in/sites/default/files/Circulars/ICAR%20En-Kharif%20Agro-Advisories%20for%20Farmers%202025.pdf
- Status: IDENTIFIED - NOT YET INGESTED
- Review required: Yes

## Demo Documents - Unverified

### Demo 1

- File: crop_health_and_pest_monitoring.md
- ChromaDB chunks: 3
- Status: DEMO - NOT VERIFIED
- Must not be presented as official agricultural advice.

### Demo 2

- File: soil_and_water_management.md
- ChromaDB chunks: 3
- Status: DEMO - NOT VERIFIED
- Must not be presented as official agricultural advice.

## Source Validation Rules

1. Prefer official agricultural universities and government sources.
2. Record the original source URL.
3. Record publication or revision date whenever available.
4. Check regional applicability before using recommendations.
5. Do not mix recommendations from different regions without review.
6. Do not treat demo content as verified agricultural guidance.
7. Chemical treatments and fertilizer quantities require crop-specific and region-specific authoritative verification.
8. Every ingested document must retain its source information.
9. If information is outdated or uncertain, flag it for review.
10. Preserve PDF page numbers in every relevant retrieved chunk.
11. Never invent source citations, page numbers, or agricultural recommendations.

## Current Status

- RAG foundation: COMPLETED
- Retrieval quality checker: COMPLETED
- Evaluation runner: IMPLEMENTED - GROUND TRUTH PENDING
- ChromaDB ingestion: COMPLETED
- Total ChromaDB records: 1535
- TNAU PDF records: 1529
- Demo document records: 6
- Authoritative source identification: IN PROGRESS
- Source document ingestion: PARTIALLY COMPLETED
- Agricultural content validation: PENDING
- Phase 4 LLM integration: NOT STARTED