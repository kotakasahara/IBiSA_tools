dd <- read.table("histogram.txt.K",header=T)
dd <- as.matrix(dd)
dd.r <- dd/sum(dd)
dd.rl <- log10(dd.r)

colnames(dd.r) <- as.numeric(substring(colnames(dd.r),2))
rownames(dd.r) <- as.numeric(rownames(dd.r))

dd.1dh <- apply(dd, 1, sum)
dd.1dh.r <- dd.1dh / sum(dd.1dh)
dd.1dh.rl <- log10(dd.1dh.r)

png("density_plot_k.png")
plot.new()
par(mfrow=c(2,1))
barplot(dd.1dh)
image(dd.rl)
dev.off()
