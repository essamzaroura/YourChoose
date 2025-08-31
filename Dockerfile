<<<<<<< HEAD
FROM node:18

WORKDIR /admin

ENV TZ="UTC"

COPY package.json ./
COPY yarn.lock ./

RUN yarn install --frozen-lockfile --production
COPY . .

RUN npm i -g typescript
RUN yarn build
RUN npx prisma generate

ENV ADMIN_JS_SKIP_BUNDLE="true"

EXPOSE 3000
CMD yarn prisma migrate dev --schema prisma/schema.prisma && yarn start


=======
# Dockerfile
FROM python:3.9-slim as backend

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM node:16 as frontend-build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM backend as final

COPY --from=frontend-build /app/build /app/static

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
>>>>>>> 1d21c3cce1c16d667fdc2bd0238fe8f103b0350e
