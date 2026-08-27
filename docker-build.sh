#!/bin/bash

# Docker build script for Mithi River Eye application

set -e

echo "🐳 Building Mithi River Eye Docker image..."

# Build the production image
docker build -t mithi-river-eye:latest .

echo "✅ Build completed successfully!"
echo ""
echo "To run the application:"
echo "  docker run -p 3000:3000 mithi-river-eye:latest"
echo ""
echo "Or use docker-compose:"
echo "  docker-compose up"
echo ""
echo "For development with hot reload:"
echo "  docker-compose --profile dev up mithi-river-dev"