# =========================
# Étape 1 : Build Angular
# =========================
FROM node:18 AS build

# Répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm ci --legacy-peer-deps

# Copier tout le code source
COPY . .

# Build Angular en production
RUN npm run build -- --configuration=production

# =========================
# Étape 2 : Serveur Nginx
# =========================
FROM nginx:alpine

# Copier le build Angular vers le serveur Nginx
COPY --from=build /app/dist/resume-management /usr/share/nginx/html

# Exposer le port 80
EXPOSE 80

# Lancer Nginx en foreground
CMD ["nginx", "-g", "daemon off;"]