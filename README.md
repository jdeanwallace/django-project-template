<!-- Source: https://github.com/jdeanwallace/django-project-template -->

<!-- Start -->

# Example Django Project
---

## Getting Started

```bash
python -m venv venv && \
  . venv/bin/activate && \
  pip install pip pip-tools --upgrade && \
  pip-sync requirements/dev.txt && \
  npm install && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py createsuperuser
```

## Run development server

```bash
npm run dev
```

## Deploy

### Launch fly.io app

```bash
fly launch --ha=false --volume-initial-size=1
```

### Set fly.io secrets

```bash
cat .env.prod | xargs fly secrets set
```

### Build bundles

```bash
npm run build
```

### Deploy changes when needed

```bash
fly deploy
```

<!-- End. -->
