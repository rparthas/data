from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler, RFormula
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession
from pyspark.ml.feature import OneHotEncoder, StringIndexer
import pyspark.sql.functions as F


def print_coefficient(trainDF):
    vecAssembler = VectorAssembler(inputCols=['bedrooms'], outputCol='features')
    vecTrainDF = vecAssembler.transform(trainDF)
    vecTrainDF.select("bedrooms", "features", "price").show(10)
    lr = LinearRegression(featuresCol="features", labelCol="price")
    lrModel = lr.fit(vecTrainDF)
    m = round(lrModel.coefficients[0], 2)
    b = round(lrModel.intercept, 2)
    print(f"""The formula for the linear regression line is price = {m}*bedrooms + {b}""")


def single_feature():
    vecAssembler = VectorAssembler(inputCols=['bedrooms'], outputCol='features')
    lr = LinearRegression(featuresCol="features", labelCol="price")
    return Pipeline(stages=[vecAssembler, lr])


def multiple_features(trainDF):
    categoricalCols = [field for (field, dataType) in trainDF.dtypes
                       if dataType == "string"]
    indexOutputCols = [x + "Index" for x in categoricalCols]
    oheOutputCols = [x + "OHE" for x in categoricalCols]
    stringIndexer = StringIndexer(inputCols=categoricalCols,
                                  outputCols=indexOutputCols,
                                  handleInvalid='skip')
    oheEncoder = OneHotEncoder(inputCols=indexOutputCols,
                               outputCols=oheOutputCols)
    numericCols = [field for (field, dataType) in trainDF.dtypes
                   if ((dataType == "double") & (field != "price"))]
    assemblerInputs = oheOutputCols + numericCols
    vecAssembler = VectorAssembler(inputCols=assemblerInputs,
                                   outputCol="features")

    lr = LinearRegression(labelCol="price", featuresCol="features")
    return Pipeline(stages=[stringIndexer, oheEncoder, vecAssembler, lr])


def rFormula():
    rFormula = RFormula(formula="price ~ .",
                        featuresCol="features",
                        labelCol="price",
                        handleInvalid="skip")
    lr = LinearRegression(labelCol="price", featuresCol="features")
    return Pipeline(stages=[rFormula, lr])


def score(model, trainDF, testDF):
    pipelineModel = model.fit(trainDF)
    predDF = pipelineModel.transform(testDF)
    predDF.select("features", "price", "prediction").show(10)

    regressionEvaluator = RegressionEvaluator(
        predictionCol="prediction",
        labelCol="price",
        metricName="rmse")
    rmse = regressionEvaluator.evaluate(predDF)
    print(f"RMSE is {rmse:.1f}")

    r2 = regressionEvaluator.setMetricName("r2").evaluate(predDF)
    print(f"R2 is {r2}")


if __name__ == "__main__":
    base_path = "../../data/"
    spark = SparkSession.builder. \
        appName("MlLib").getOrCreate()

    filePath = f"{base_path}sf-airbnb/sf-airbnb-clean.parquet/"
    airbnbDF = spark.read.parquet(filePath)
    airbnbDF.select("neighbourhood_cleansed", "room_type", "bedrooms", "bathrooms",
                    "number_of_reviews", "price").show(10)
    airbnbDF = airbnbDF.withColumn("price", F.log("price"))

    trainDF, testDF = airbnbDF.randomSplit([0.8, 0.2], seed=43)
    print(f"""There are {trainDF.count()} rows in the training set, and {testDF.count()} in the test set""")

    print_coefficient(trainDF)

    score(single_feature(), trainDF, testDF)
    score(multiple_features(trainDF), trainDF, testDF)
    score(rFormula(), trainDF, testDF)
