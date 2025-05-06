import os
SPARK_MASTER_HOST=0.0.0.0
SPARK_LOCAL_IP=spark-master
SPARK_PUBLIC_DNS=os.getenv("SPARK_PUBLIC_DNS", "spark-master")
# SPARK_PUBLIC_DNS = <your_local_ip