# Deployment Notes

## Runtime
- Django app entry point: `trucare.wsgi:application`
- Gunicorn binds to `0.0.0.0:8000`
- Systemd service: `trucare-gunicorn.service`
- Nginx on port 80 serves the existing frontend; Django is exposed separately on port 8000

## Production Settings
- `DEBUG = False`
- `ALLOWED_HOSTS = ['146.190.113.182', 'localhost', '127.0.0.1']`
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`
- WhiteNoise is enabled for Django static files

## Deploy Steps
1. Activate the virtualenv.
2. Install requirements.
3. Run migrations:
   - `python manage.py migrate --noinput`
4. Collect static files:
   - `python manage.py collectstatic --noinput`
5. Restart the app service:
   - `systemctl restart trucare-gunicorn.service`
6. Verify the app:
   - `curl -I http://127.0.0.1:8000/`
   - `curl -I http://127.0.0.1:8000/static/admin/css/base.css`

## Logs
- Gunicorn service status:
  - `systemctl status trucare-gunicorn.service`
- Gunicorn logs:
  - `journalctl -u trucare-gunicorn.service -f`
- Nginx logs:
  - `/var/log/nginx/access.log`
  - `/var/log/nginx/error.log`

## Notes
- The backend root URL may return `404` if no `/` route is defined. That does not mean the service is broken.
- Admin CSS should load from Django directly through WhiteNoise.
- If the public site on port 80 is frontend-owned, keep Django on port 8000 and do not reuse port 80 for Gunicorn.
