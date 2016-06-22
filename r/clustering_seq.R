align.sim <- read.table("align_sim.txt", header=T)
seq <- read.table("sequences_header.txt")[,-1]
colnames(seq) <- c("seq.id","run.id", "seq", "begin","end","run.title")
align.d <- as.dist(1-align.sim)
align.hc <- hclust(align.d, method="complete")
plot(align.hc)
label.seq <- function(elem){
  elem.id <- as.numeric(attributes(elem)$label)
  attributes(elem)$label <- subset(seq, seq.id == elem.id)[1,]$seq;
  elem
}
dend <- dendrapply(as.dendrogram(align.hc), label.seq)
postscript("dendrogram.eps")
plot(dend)
dev.off()
