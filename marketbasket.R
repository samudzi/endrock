library(readr)
t <- read_csv("Downloads/marketbasket.csv")
View(t)

i <- split(t$`Lineitem name`, t$Name)

library("arules")
txn <- as(i, "transactions")

basket_rules <- apriori(txn, parameter = list(sup = 0.005, conf = 0.01, target="rules"))


## Most frequent items ordered
itemFrequencyPlot(txn, topN = 10)

inspect(basket_rules)


basket_rules_broad <- apriori(txn, parameter = list(sup = 0.001, conf = 0.001, target="rules"))

library(arulesViz)
plot(basket_rules_broad,measure=c("support", "lift"), shading = "confidence")

sel <- plot(basket_rules_broad, measure=c("support", "lift"), shading = "confidence", interactive = TRUE)


## Inspect top rules by lift

inspect(head(sort(basket_rules_broad,by="lift"),20))