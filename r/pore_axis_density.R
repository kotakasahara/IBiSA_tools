
pa <- read.table("pore_axis.txt", na.string="-")
pa.n <- as.numeric(pa[!is.na(pa)])
h <- hist(pa.n, breaks=500)
postscript("density_distribution.eps")
plot(h$mids, h$count/sum(h$count), type="l")
dev.off()
