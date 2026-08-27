# Multi-stage build for React + Vite application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production --silent

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with Caddy web server
FROM caddy:2.7-alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /srv

# Copy Caddyfile for configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Expose port 3000 (as configured in Caddyfile)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Caddy will automatically use the Caddyfile
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]