# 1단계: 호환성 좋은 Node.js slim 환경에서 앱 빌드하기
FROM node:20-slim AS build
WORKDIR /app

# 클라우드 빌드 중 메모리 부족(OOM) 방지 및 자잘한 경고 무시
ENV NODE_OPTIONS="--max-old-space-size=2048"
ENV CI=false

COPY package*.json ./
# 호환성 문제 방지를 위해 강제로 깔끔하게 설치
RUN npm install

COPY . .
RUN npm run build

# 2단계: Nginx를 이용해 빌드된 정적 파일 배포하기
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]