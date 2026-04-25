module.exports = {
  apps : [
    {
      name: "0-REDIS",
      script: "./redis/redis-server.exe",
      args: "./redis/redis.windows.conf", 
      autorestart: true
    },
    {
      name: "1-DJANGO-WAITRESS",
      script: "../avaroweb/Scripts/python.exe", 
      args: "run_server.py",
      autorestart: true
    },
    {
      name: "2-CHATERY-WA",
      cwd: "./chatery", 
      script: "index.js", // GANTI dengan file utama Chatery Anda (misal: server.js)
      interpreter: "node",
      autorestart: true
    },
    {
      name: "3-CELERY-BEAT",
      script: "../avaroweb/Scripts/celery.exe",
      args: "-A avaro beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler",
      autorestart: true
    },
    {
      name: "4-WORKER-VERTICA",
      script: "../avaroweb/Scripts/celery.exe",
      args: "-A avaro worker -l info --pool=threads --concurrency=4 -Q queue_vertica",
      autorestart: true
    },
    {
      name: "5-WORKER-FINEREPORT",
      script: "../avaroweb/Scripts/celery.exe",
      args: "-A avaro worker -l info --pool=threads --concurrency=2 -Q queue_finereport,queue_rekapkp",
      autorestart: true
    },
    {
      name: "6-FLOWER",
      script: "../avaroweb/Scripts/celery.exe",
      args: "-A avaro flower",
      autorestart: true
    }
  ]
}