# cw_drf
Курсовая работа по DRF DJANGO (good habbits)


### работают следующие команды для Windows с celery и celery-beat
`celery -A config worker --loglevel=info -E -P eventlet`

`celery -A config beat -l info -S django`