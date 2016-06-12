

dd <- read.table("density_distribution.txt.K",header=T)
dd <- as.matrix(dd)
dd.r <- dd.k/sum(dd)

colnames(dd.r) <- as.numeric(substring(colnames(dd.r),2))
rownames(dd.r) <- as.numeric(rownames(dd.r))

dd.1dh <- apply(dd, 1, sum)
dd.1dh.r <- dd.1dh / sum(dd.1dh)
dd.1dh.rl <- log10(dd.1dh.r)

postscript("density_plot_k.eps")
plot.new()
par(mfrow=c(2,1))
barplot(dd.1dh)
image(dd.rl, zlim=(-6.0, 0))
dev.off()
