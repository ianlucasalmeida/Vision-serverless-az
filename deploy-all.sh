#!/bin/bash

# Script para disparar deploys manuais do backend e frontend via GitHub Actions
# Requer: GitHub CLI (gh) instalado e autenticado

echo "🔁 Disparando deploy do BACKEND via GitHub Actions..."
gh workflow run deploy-backend.yml

echo "🔁 Disparando deploy do FRONTEND via GitHub Actions..."
gh workflow run deploy-frontend.yml

echo "✅ Deploys disparados! Acompanhe em https://github.com/ianlucasalmeida/Vision-serverless-az/actions"
