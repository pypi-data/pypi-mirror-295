from skt.vault_utils import get_secrets


def get_hms():
    from hmsclient import hmsclient

    s = get_secrets(path="ye/hivemetastore")
    host = s["ip"]
    port = s["port"]
    client = hmsclient.HMSClient(host=host, port=port)
    client.open()
    return client


def get_hdfs_conn():
    try:
        from pyarrow import hdfs

        conn = hdfs.connect(user="airflow")
    except ImportError:
        import os
        import subprocess

        from pyarrow import fs

        print("Using pyarrow.fs.HadoopFileSystem, Cause pyarrow.hdfs is deprecated.")

        hadoop_bin = os.path.join(os.environ["HADOOP_HOME"], "bin", "hadoop")
        classpath = subprocess.check_output((hadoop_bin, "classpath", "--glob"))

        os.environ["CLASSPATH"] = classpath.decode("utf-8")

        conn = fs.HadoopFileSystem("default", user="airflow")

    return conn


def get_pkl_from_hdfs(pkl_path):
    import pickle

    conn = get_hdfs_conn()
    byte_object = conn.cat(f"{pkl_path}")
    pkl_object = pickle.loads(byte_object)
    return pkl_object


def get_spark(scale=0, queue=None, jars=None):
    import os
    import uuid

    from pyspark import version as spark_version
    from pyspark.sql import SparkSession

    is_spark_3 = spark_version.__version__ >= "3.0.0"

    tmp_uuid = str(uuid.uuid4())
    app_name = f"skt-{os.environ.get('USER', 'default')}-{tmp_uuid}"

    # key = get_secrets("gcp/sktaic-datahub/dataflow")["config"]
    # key_file_name = tempfile.mkstemp()[1]
    # with open(key_file_name, "wb") as key_file:
    #     key_file.write(key.encode())
    #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file.name

    if not queue:
        if "JUPYTERHUB_USER" in os.environ:
            queue = "dmig_eda"
        else:
            queue = "airflow_job"

    bigquery_jars = (
        "hdfs:///jars/spark-bigquery-with-dependencies_2.12-0.24.2.jar"
        if is_spark_3
        else "hdfs:///jars/spark-bigquery-with-dependencies_2.11-0.17.3.jar"
    )

    spark_jars = ",".join([bigquery_jars, jars]) if jars else bigquery_jars

    arrow_enabled = "spark.sql.execution.arrow.pyspark.enabled" if is_spark_3 else "spark.sql.execution.arrow.enabled"

    arrow_pre_ipc_format = "0" if is_spark_3 else "1"
    os.environ["ARROW_PRE_0_15_IPC_FORMAT"] = arrow_pre_ipc_format

    if queue == "nrt":
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", "6g")
            .config("spark.executor.memory", "4g")
            .config("spark.driver.maxResultSize", "6g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.executor.core", "4")
            .config("spark.executor.instances", "32")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
        spark.conf.set(arrow_enabled, "true")
        return spark

    if scale in [1, 2, 3, 4]:
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", f"{scale * 8}g")
            .config("spark.executor.memory", f"{scale * 3}g")
            .config("spark.executor.instances", f"{scale * 8}")
            .config("spark.driver.maxResultSize", f"{scale * 4}g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
    elif scale in [5, 6, 7, 8]:
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", "8g")
            .config("spark.executor.memory", f"{2 ** scale}g")
            .config("spark.executor.instances", "32")
            .config("spark.driver.maxResultSize", "8g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
    else:
        if is_spark_3:
            spark = (
                SparkSession.builder.config("spark.app.name", app_name)
                .config("spark.driver.memory", "8g")
                .config("spark.executor.memory", "8g")
                .config("spark.executor.instances", "8")
                .config("spark.driver.maxResultSize", "6g")
                .config("spark.rpc.message.maxSize", "1024")
                .config("spark.yarn.queue", queue)
                .config("spark.ui.enabled", "false")
                .config("spark.port.maxRetries", "128")
                .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config(
                    "spark.jars",
                    spark_jars,
                )
                .enableHiveSupport()
                .getOrCreate()
            )
        else:
            spark = (
                SparkSession.builder.config("spark.app.name", app_name)
                .config("spark.driver.memory", "6g")
                .config("spark.executor.memory", "8g")
                .config("spark.shuffle.service.enabled", "true")
                .config("spark.dynamicAllocation.enabled", "true")
                .config("spark.dynamicAllocation.maxExecutors", "200")
                .config("spark.driver.maxResultSize", "6g")
                .config("spark.rpc.message.maxSize", "1024")
                .config("spark.yarn.queue", queue)
                .config("spark.ui.enabled", "false")
                .config("spark.port.maxRetries", "128")
                .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config(
                    "spark.jars",
                    spark_jars,
                )
                .enableHiveSupport()
                .getOrCreate()
            )
    spark.conf.set(arrow_enabled, "true")
    return spark


def parquet_to_pandas(hdfs_path):
    import os

    from pyarrow import fs, parquet

    from skt.ye import get_hdfs_conn

    # Load hadoop environment
    get_hdfs_conn().close()

    os.environ["ARROW_LIBHDFS_DIR"] = "/usr/hdp/3.0.1.0-187/usr/lib"
    hdfs = fs.HadoopFileSystem("ye.sktai.io", 8020, user="airflow")
    if hdfs_path.startswith("hdfs://yellowelephant/"):
        hdfs_path = hdfs_path[21:]
    df = parquet.read_table(hdfs_path, filesystem=hdfs).to_pandas()
    df.info()
    return df


def pandas_to_parquet(pandas_df, hdfs_path, spark):
    df = spark.createDataFrame(pandas_df)
    df.write.mode("overwrite").parquet(hdfs_path)


def slack_send(
    text="This is default text",
    username="SKT",
    channel="#leavemealone",
    icon_emoji=":large_blue_circle:",
    blocks=None,
    dataframe=False,
    adot=False,
):
    import requests

    from skt.vault_utils import get_secrets

    if dataframe:
        from tabulate import tabulate

        text = "```" + tabulate(text, tablefmt="simple", headers="keys") + "```"

    token = (
        get_secrets("airflow_k8s/adot_slack/slack_alarmbot_token")["token"]
        if adot
        else get_secrets("slack")["bot_token"]["airflow"]
    )
    proxy = get_secrets("proxy")["proxy"]
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"Bearer {token}",
    }
    json_body = {
        "username": username,
        "channel": channel,
        "text": text,
        "blocks": blocks,
        "icon_emoji": icon_emoji,
    }
    r = requests.post(
        "https://www.slack.com/api/chat.postMessage",
        proxies=proxies,
        headers=headers,
        json=json_body,
    )
    r.raise_for_status()
    if not r.json()["ok"]:
        raise Exception(r.json())


def send_email(subject, text, send_from, send_to, attachment=None):
    """
    :param str attachment: Attachment to send as .txt file with email
    """
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formatdate

    from skt.vault_utils import get_secrets

    c = get_secrets(path="mail")
    host, port = c["smtp_host"], c["smtp_port"]
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = send_to
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    if attachment:
        part = MIMEApplication(attachment, NAME=subject)
        part.add_header("Content-Disposition", f"attachment; filename={subject}.txt")
        msg.attach(part)

    with smtplib.SMTP(host, port) as smtp:
        if "sktelecom.com" in host:
            smtp.starttls()
        return smtp.sendmail(send_from, send_to.split(","), msg.as_string())


def get_github_util():
    from skt.github_utils import GithubUtil

    github_token = get_secrets("github/sktaiflow")["token"]
    proxy = get_secrets("proxy")["proxy"]
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    g = GithubUtil(github_token, proxies)
    return g


def _write_to_parquet_via_spark(pandas_df, hdfs_path):
    spark = get_spark()
    spark_df = spark.createDataFrame(pandas_df)
    spark_df.write.mode("overwrite").parquet(hdfs_path)


def _write_to_parquet(pandas_df, hdfs_path):
    import pyarrow as pa
    import pyarrow.parquet as pq

    # Read Parquet INT64 timestamp issue:
    # https://issues.apache.org/jira/browse/HIVE-21215
    if "datetime64[ns]" in pandas_df.dtypes.tolist():
        _write_to_parquet_via_spark(pandas_df, hdfs_path)
        return

    pa_table = pa.Table.from_pandas(pandas_df)
    hdfs_conn = get_hdfs_conn()
    try:
        pq.write_to_dataset(pa_table, root_path=hdfs_path, filesystem=hdfs_conn)
    finally:
        hdfs_conn.close()
