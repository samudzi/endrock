# Load essential libraries
library(tidyverse)
library(cluster)
library(factoextra)
library(purrr)



# OPTION 1 for computing optimal number of clusters: Elbow Method
set.seed(123)

fviz_nbclust(df,kmeans,method="wss")

# OPTION 2 - Silhouette Method

fviz_nbclust(df, kmeans,method="silhouette")

# OPTION 3 - Gap Statistic Method

set.seed(123)
gap_stat <- clusGap(df, FUN = kmeans, nstart = 25,
                    K.max = 10, B = 50)
# Print the result
print(gap_stat, method = "firstmax")

fviz_gap_stat(gap_stat)


# We can create multiple clustered scatterplots

# 4 clusters - per Elbow Method
k4 <- kmeans(df, centers = 4, nstart = 25)
str(k4)

#Scatterplot

fviz_cluster(k4, data = df)

