# Multi-stage build for React + Vite application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev dependencies needed for build)
RUN npm install --silent

# Verify vite is available
RUN npx vite --version || echo "Vite not found, checking node_modules..." && ls -la node_modules/.bin/ | grep vite

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with Caddy web server
FROM caddy:2.7-alpine

# Install wget for health checks
RUN apk add --no-cache wget

# Copy built assets from builder stage
COPY --from=builder /app/dist /srv

# Copy Caddyfile for configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Expose the PORT environment variable (Railway assigns this dynamically)
EXPOSE $PORT

# Health check using the dynamic port
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${PORT:-3000}/health || exit 1

# Caddy will automatically use the Caddyfile
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]