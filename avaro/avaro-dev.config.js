module.exports = {
  apps : [
    // {
    //   name: "0-REDIS",
    //   script: "./redis/redis-server.exe",
    //   args: "./redis/redis.windows.conf", 
    //   autorestart: true
    // },
    {
      name: "1-DJANGO-DEV",
      script: "../avaroweb/Scripts/python.exe", 
      args: "manage.py runserver 0.0.0.0:8000",
      autorestart: true
    }
    // {
    //   name: "2-CHATERY-WA",
    //   cwd: "./chatery", 
    //   script: "index.js",
    //   interpreter: "node",
    //   autorestart: true
    // },
    // {
    //   name: "3-CELERY-BEAT",
    //   script: "../avaroweb/Scripts/celery.exe",
    //   args: "-A avaro beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler",
    //   autorestart: true
    // },
  ]
}