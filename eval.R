
setwd(".")
df <- read.csv("test/evaluation.csv", sep="\t")
summary(df)

library(ggplot2)

ggplot(df, aes(n, attempts))+
  geom_point()+
  geom_line()
