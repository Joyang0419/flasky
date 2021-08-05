broker_url = 'redis://192.168.56.103:6379/0'
result_backend = 'redis://192.168.56.103:6379/0'
# 指定任務序列化方式
task_serializer = 'json'
# 指定結果序列化方式
result_serializer = 'json'
# 指定任務接受的序列化類型.
accept_content = ['json', 'application/text']
timezone = 'asia/taipei'
enable_utc = True
# 儲存的結果過期時間,celery任務執行結果的超時時間
result_expires = 60 * 20
# 任務發送完成是否需要確認，這一項對性能有一點影響
task_acks_late = False
# 壓縮方案選擇，可以是zlib, bzip2，默認是發送沒有壓縮的數據
result_compression = 'zlib'
# 規定完成任務的時間
task_time_limit = 300  # 在5s內完成任務，否則執行該任務的worker將被殺死，任務移交給父進程
# celery worker的併發數，默認是服務器的內核數目,也是命令行-c參數指定的數目
worker_concurrency = 4
# celery worker 每次去rabbitmq預取任務的數量
worker_prefetch_multiplier = 4
# 每個worker執行了多少任務就會死掉，默認是無限的
worker_max_tasks_per_child = 40
# 設置默認的隊列名稱，如果一個消息不符合其他的隊列就會放在默認隊列裡面，如果什麼都不設置的話，數據都會發送到默認的隊列中
task_default_queue = 'default'
# List of modules to import when the Celery worker starts.
imports = ("flasky")
