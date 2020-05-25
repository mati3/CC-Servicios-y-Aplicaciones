from pyspark import SparkConf
from pyspark import SparkContext
from pyspark import SQLContext

if __name__ == "__main__":
    conf = SparkConf().setAppName("Matilde Cabrera González Practica 4")
    Sp = SparkContext(conf=conf)

    headers = Sp.textFile("/user/datasets/ecbdl14/ECBDL14_IR2.header").collect()
    headers = list(filter(lambda x: "@inputs" in x, headers))[0]
    headers = headers.replace(",", "").strip().split()
    del headers[0]
    headers.append("class")

    sqlc = SQLContext(Sp)
    df = sqlc.read.csv('/user/datasets/ecbdl14/ECBDL14_IR2.data', header=False, inferSchema=True)

    for i, colname in enumerate(df.columns):
        df = df.withColumnRenamed(colname, headers[i])

    df = df.select( "PredRCH_freq_global_3", "PSSM_r2_0_P", "PSSM_r2_-3_K", "PSSM_central_2_L", "PSSM_r2_3_K", "PSSM_r1_-3_V", "class")
    df.write.csv('./filteredC.small.training', header=True)

